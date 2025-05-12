from datetime import datetime
from typing import Any, Self
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import pandas as pd
import requests
from pydantic import (
    AliasPath,
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    SecretStr,
    TypeAdapter,
    field_validator,
)

UTC = ZoneInfo("UTC")
VENDOR = "Traccar"
CRS = "EPSG:4326"

ENDPOINT_SERVER = "server"
ENDPOINT_SESSION = "session"
ENDPOINT_DEVICES = "devices"
ENDPOINT_DATA = "reports/route"

COLUMNS = {
    "latitude": "float64",
    "longitude": "float64",
    "altitude": "float32",
    "speed": "float32",
    "bearing": "float32",
    "gnss_accuracy": "float32",
    "distance": "float32",
}


class Record(BaseModel):
    id: int
    user_id: int = Field(validation_alias="deviceId")
    datetime_: datetime = Field(
        alias="datetime",
        validation_alias="fixTime",
    )
    latitude: float
    longitude: float
    altitude: float
    speed: float
    bearing: float = Field(validation_alias="course")
    gnss_accuracy: float = Field(validation_alias="accuracy")
    distance: float = Field(validation_alias=AliasPath("attributes", "distance"))

    class Config:
        populate_by_name = True

    @field_validator("distance")
    @classmethod
    def convert_knots_to_kph(cls, v: float) -> float:
        return v * 1.852


class Subject(BaseModel):
    id: int = Field(validation_alias="id")
    subject_id: str = Field(validation_alias="uniqueId")
    name: str
    status: str
    updated: datetime | None = Field(validation_alias="lastUpdate")
    records: list[Record] | None = Field(default=None, repr=False)

    def to_dict(self) -> dict:
        records = self.model_dump(
            exclude={
                "records": {"__all__": {"id", "user_id"}},
            },
            by_alias=True,
        )

        return records

    def to_df(self) -> pd.DataFrame:
        if not self.records:
            raise ValueError("No records found.")

        records = self.to_dict()["records"]
        df = pd.DataFrame.from_records(records)

        df.set_index("datetime", inplace=True)

        df = df.astype(COLUMNS)

        return df


class TraccarConnector(BaseModel):
    server: HttpUrl
    email: EmailStr = Field(exclude=True, repr=False)
    password: SecretStr = Field(exclude=True, repr=False)
    session: requests.Session | None = None
    firmware: float | None = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_auth(
        cls,
        server: str,
        email: str,
        password: str,
    ) -> Self:
        connection = cls(server=server, email=email, password=password)  # type: ignore
        connection.session = connection.get_session()
        connection.firmware = connection.get_server_info()["version"]

        return connection

    def get_session(self) -> requests.Session:
        url = self._get_endpoint_url(ENDPOINT_SESSION)
        data = {
            "email": self.email,
            "password": self.password.get_secret_value(),
        }

        session = requests.Session()

        response = session.post(
            url,
            data=data,
        )

        response.raise_for_status()

        return session

    def _get_endpoint_url(self, endpoint: str) -> str:
        return urljoin(self.server.unicode_string(), "api/" + endpoint)

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        url = self._get_endpoint_url(endpoint)

        if not self.session:
            raise ValueError(
                "Session not initialized. Please call get_session() first."
            )

        response = self.session.get(
            url,
            params=params,
            headers={
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        # response = response.json()

        return response

    def get_server_info(self) -> dict[str, Any]:
        response = self.get(ENDPOINT_SERVER)
        version = float(response.json()["version"])

        return {"version": version}

    def get_subjects(
        self,
        subjects: str | list[str] | None = None,
        mode: str | None = "pandas",
    ) -> list[Subject] | pd.DataFrame:
        if subjects:
            params = {"uniqueId": subjects}
        else:
            params = {"all": True}

        response = self.get(ENDPOINT_DEVICES, params)
        objs = TypeAdapter(list[Subject]).validate_json(response.content)

        if not objs:
            raise ValueError("No devices found.")

        match mode:
            case "object":
                data = objs
            case "pandas":
                infos = []

                for sbj in objs:
                    obj = sbj.to_dict()
                    del obj["records"]

                    infos.append(obj)

                data = pd.DataFrame.from_records(infos, index="id")

            case _:
                raise ValueError(f"Mode '{mode}' not supported.")

        return data

    def get_data(
        self,
        subject: str | Subject,
        start: datetime | str | None = None,
        end: datetime | str | None = None,
        mode: str | None = "pandas",
    ) -> Subject | tuple[pd.DataFrame, dict[str, Any]]:
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        elif start is None:
            start = datetime.fromtimestamp(0)

        if isinstance(end, str):
            end = datetime.fromisoformat(end)
        elif end is None:
            end = datetime.now()

        start_datetime = start.astimezone(UTC).isoformat()
        end_datetime = end.astimezone(UTC).isoformat()

        if not subject:
            raise ValueError("No subject provided.")

        if isinstance(subject, str):
            sbj = self.get_subjects(subject, mode="object")[0]

        params = {
            "deviceId": sbj.id,
            "from": start_datetime,
            "to": end_datetime,
        }
        response = self.get(ENDPOINT_DATA, params)
        sbj.records = TypeAdapter(list[Record]).validate_json(response.content)

        match mode:
            case "object":
                return sbj  # type: ignore

            case "pandas":
                df = sbj.to_df()
                metadata = {
                    "id": sbj.subject_id,
                    "name": sbj.name,
                    "vendor": VENDOR,
                    "firmware": self.firmware,
                    "timezone": str(UTC),
                    "crs": CRS,
                }
                metadata  # type: ignore

                return df, metadata

            case _:
                raise ValueError(f"Mode '{mode}' not supported.")
