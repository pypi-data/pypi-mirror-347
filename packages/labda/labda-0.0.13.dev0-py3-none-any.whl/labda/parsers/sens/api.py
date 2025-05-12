import json
import time
from datetime import datetime
from typing import Any, Self
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests
from pydantic import (
    AliasPath,
    BaseModel,
    Field,
    HttpUrl,
    SecretStr,
    TypeAdapter,
    field_validator,
    model_validator,
)
from tqdm.auto import tqdm

from .file import _read

UTC = ZoneInfo("UTC")
SERVER_URL = "https://app.sens.dk"  # "https://api-0005.sens.dk"
API_VERSION = 1.0

ENDPOINT_AUTH = "auth/login"
ENDPOINT_ACC_DATA = "export/sensor/raw"
ENDPOINT_SCOPES = "access_scopes/list"
ENDPOINT_PROJECTS = "projects"
ENDPOINT_PATIENTS = "patients"
ENDPOINT_SENSORS = "sensors"
ENDPOINT_SENSOR_DETAILS = "sensor/details"
ENDPOINT_DOWNLOAD_TOKEN = "auth/get_download_token"
ENDPOINT_ACTIVITY_DATA = "export/sensor/derived"


class Sensor(BaseModel):
    id: str
    mac: str
    name: str = Field(validation_alias="short_name")
    firmware: str = Field(validation_alias="firmware_version")
    last_seen: datetime = Field(validation_alias="last_seen")
    last_sync: datetime | None = Field(validation_alias="last_synced_timestamp")
    battery: str = Field(validation_alias=AliasPath("battery", "status"))
    scope_id: str
    project_id: str

    @field_validator("battery")
    @classmethod
    def convert_battery_status(cls, v: str) -> str:
        return v.split("/")[1]


class Project(BaseModel):
    name: str
    id: str
    active: bool
    active_patients: int = Field(
        validation_alias=AliasPath("statistics", "num_active_patients")
    )
    sensors: list[Sensor] | None = Field(default=None, repr=False)


class Scope(BaseModel):
    name: str
    id: str
    projects: list[Project] | None = None


class SensConnector(BaseModel):
    server: HttpUrl
    api_version: float
    token: SecretStr = Field(exclude=True, repr=False)
    scopes: list[Scope] | None = None

    class Config:
        arbitrary_types_allowed = True

    @model_validator(mode="after")
    def _initialize(self) -> Self:
        self._get_scopes()
        self._get_projects()
        self._get_sensors()

        return self

    def reinitialize(self) -> None:
        self._initialize()

    @property
    def sensors(self) -> pd.DataFrame:
        df = []
        for scope in self.scopes:
            scope_name = scope.name

            for project in scope.projects:
                project_name = project.name

                for sensor in project.sensors:
                    sensor = sensor.model_dump(exclude={})
                    sensor["scope"] = scope_name
                    sensor["project"] = project_name
                    df.append(sensor)

        df = pd.DataFrame(df)
        df.set_index("name", inplace=True)
        # df = df[["scope", "project", "firmware_version", "last_seen", "battery"]]

        return df

    @classmethod
    def from_auth(
        cls,
        email: str,
        password: str,
        server: str = SERVER_URL,
        api_version: float = API_VERSION,
    ) -> Self:
        token = cls._get_token_from_auth(email, password, server, api_version)
        return cls(server=server, api_version=api_version, token=token)

    @classmethod
    def from_token(
        cls,
        token: str,
        server: str = SERVER_URL,
        api_version: float = API_VERSION,
    ) -> Self:
        return cls(server=server, api_version=api_version, token=token)

    @staticmethod
    def _get_token_from_auth(
        email: str,
        password: str,
        server: str,
        version: float,
    ) -> str:
        url = urljoin(server, f"/api/{version}/{ENDPOINT_AUTH}")

        params = {
            "user_email": email,
            "password": password,
        }

        response = requests.post(
            url,
            json=params,
        )

        response.raise_for_status()
        response = json.loads(response.content)

        return response["value"]["auth_token"]

    def _get_endpoint_url(self, endpoint: str) -> str:
        return urljoin(
            self.server.unicode_string(),
            f"api/{self.api_version}/" + endpoint,
        )

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        url = self._get_endpoint_url(endpoint)

        response = requests.get(
            url,
            params=params,
            headers={
                "Auth-Token": self.token.get_secret_value(),
                "Accept": "application/json",
            },
        )

        response.raise_for_status()

        return response

    def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        url = self._get_endpoint_url(endpoint)

        response = requests.post(
            url,
            json=params,
            headers={
                "Auth-Token": self.token.get_secret_value(),
                "Accept": "application/json",
            },
        )

        response.raise_for_status()

        return response

    def _get_scopes(
        self,
    ) -> None:
        response = self.get(ENDPOINT_SCOPES).json()
        response = response.get("value").get("scopes")

        if response:
            self.scopes = TypeAdapter(list[Scope]).validate_python(response)
        else:
            raise ValueError("No scopes found.")

    def _get_projects(
        self,
    ) -> None:
        for scope in self.scopes:
            params = {"scope_id": scope.id}
            response = self.get(ENDPOINT_PROJECTS, params).json()
            response = response.get("value")[0].get("projects")

            if response:
                projects = []

                for project in response:
                    project["scope_id"] = scope.id
                    projects.append(Project(**project))

                scope.projects = projects

    def _get_sensors(self) -> None:
        for scope in self.scopes:
            for project in scope.projects:
                params = {
                    "org_id": scope.id,
                    "project_id": project.id,
                }
                response = self.get(ENDPOINT_SENSORS, params).json()
                response = response.get("value").get("sensors")

                if response:
                    sensors = []

                    for sensor in response:
                        sensor["scope_id"] = scope.id
                        sensor["project_id"] = project.id
                        sensors.append(Sensor(**sensor))

                    project.sensors = sensors

    def get_scope(self, name: str) -> Scope:
        for scope in self.scopes:
            if scope.name == name:
                return scope

        raise ValueError(f"Scope with name '{name}' not found.")

    def get_project(self, name: str) -> Project:
        for scope in self.scopes:
            for project in scope.projects:
                if project.name == name:
                    return project

        raise ValueError(f"Project with name '{name}' not found.")

    def get_sensor(self, name: str) -> Sensor:
        for scope in self.scopes:
            for project in scope.projects:
                for sensor in project.sensors:
                    if sensor.name == name:
                        return sensor

        raise ValueError(f"Sensor with name '{name}' not found.")

    def get_raw_data(
        self,
        sensor: str,
        start: datetime | str,
        end: datetime | str,
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        stream_name = "acc/3ax/4g"
        file_format = "bin"

        if not sensor:
            raise ValueError("No sensor provided.")

        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        elif start is None:
            raise ValueError("No start date provided.")

        if isinstance(end, str):
            end = datetime.fromisoformat(end)
        elif end is None:
            raise ValueError("No end date provided.")

        start_datetime = start.astimezone(UTC).isoformat()
        end_datetime = end.astimezone(UTC).isoformat()

        sensor = self.get_sensor(sensor)

        params = {
            "scope_id": sensor.scope_id,
            "project_id": sensor.project_id,
            "sensor_id": sensor.id,
            "start_time": start_datetime,
            "end_time": end_datetime,
            "stream_name": stream_name,
            "file_format": file_format,
        }

        buffer = self._poll_and_download(ENDPOINT_ACC_DATA, params)
        df, metadata = _read(buffer, np.frombuffer, normalize=True)

        metadata["id"] = sensor.name
        metadata["firmware"] = sensor.firmware

        return df, metadata

    def _poll_and_download(
        self,
        endpoint: str,
        params: dict[str, Any],
        poll_interval: int = 2,
    ) -> bytes | None:
        print(
            f"Polling and downloading '{params['stream_name']}' data for sensor '{params['sensor_id']}' started."
        )
        status = ""
        export_bar = tqdm(total=100, desc="Queuing")

        while status != "export_status/completed":
            response = self.post(endpoint, params).json()
            status = response["value"]["queue_entry"]["status"]
            export_bar.update(1)
            time.sleep(poll_interval)

        export_bar.update(export_bar.total - export_bar.n)
        export_bar.close()

        url = response["value"]["queue_entry"]["url"]
        file = requests.get(url, stream=True)
        file.raise_for_status()

        download_bar = tqdm(
            desc="Downloading",
            total=int(file.headers.get("content-length", 0)),
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        buffer = bytearray()
        for data in file.iter_content(chunk_size=1024):
            buffer.extend(data)
            download_bar.update(len(data))

        download_bar.close()

        return buffer
