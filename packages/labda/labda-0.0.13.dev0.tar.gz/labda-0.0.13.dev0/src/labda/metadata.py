import json
from datetime import timedelta
from pathlib import Path
from typing import Any, Self
from zoneinfo import ZoneInfo

import pandas as pd
import pyarrow.parquet as pq
from pydantic import BaseModel, ConfigDict, field_serializer, field_validator
from pyproj import CRS


class Metadata(BaseModel):
    sampling_frequency: timedelta | str | None = None
    timezone: ZoneInfo | str | None = None
    crs: CRS | str | None = None
    extra: dict[str, Any] | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="ignore",
    )

    def __repr__(self):
        fields = []
        if self.sampling_frequency is not None:
            fields.append(f"sampling_frequency={self.sampling_frequency}")
        if self.timezone is not None:
            fields.append(f"timezone={self.timezone}")
        if self.crs is not None:
            fields.append(f"crs={self.crs}")
        if self.extra is not None:
            fields.append(f"extra={self.extra}")
        return f"Metadata({', '.join(fields)})"

    def __str__(self):
        return self.__repr__()

    @field_serializer("timezone", "crs", "sampling_frequency")
    def serialize_timezone(self, value: Any) -> str | None:
        return str(value) if value else None

    @field_validator("crs", mode="before")
    @classmethod
    def parse_crs(cls, value: Any) -> CRS | Any:
        if value:
            return CRS.from_user_input(value)
        else:
            return value

    @field_validator("timezone", mode="before")
    @classmethod
    def parse_timezone(cls, value: Any) -> ZoneInfo | Any:
        if isinstance(value, str):
            return ZoneInfo(value)
        else:
            return value

    @field_validator("sampling_frequency", mode="before")
    @classmethod
    def parse_sampling_frequency(cls, value: Any) -> timedelta | Any:
        return pd.Timedelta(value).to_pytimedelta()

    @classmethod
    def from_parquet(
        cls,
        path: Path | str,
    ) -> Self:
        if isinstance(path, str):
            path = Path(path)

        metadata = pq.read_metadata(path).metadata.get("PANDAS_ATTRS".encode())
        metadata = json.loads(metadata)
        metadata = Metadata(**metadata)

        return metadata

    def check_crs(self) -> None:
        if not self.crs:
            raise ValueError("CRS is missing. Please set the CRS first.")
