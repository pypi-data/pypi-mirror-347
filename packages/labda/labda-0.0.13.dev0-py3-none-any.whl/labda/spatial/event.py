from typing import Annotated, Any, Literal, Self

import pandas as pd
from pydantic import BaseModel, BeforeValidator

from labda.core.event import Event
from labda.core.utils import get_rle

TransportMode = Annotated[
    Literal["multimode", "walk", "run", "bicycle", "vehicle", "unspecified", "pause"]
    | None,
    BeforeValidator(lambda x: "pause" if isinstance(x, float) else x),
]


class Partial(Event):
    type: Literal["transport"] = "transport"
    mode: TransportMode
    distance: float

    @classmethod
    def from_dataframe(cls, id: Any, df: pd.DataFrame) -> Self:
        start = df.index[0]
        end = df.index[-1]
        distance = df["distance"].sum()

        mode = Transport.extract_mode(df)

        return cls(
            id=id,
            start=start,
            end=end,
            mode=mode,
            distance=distance,
        )


class Transport(Event):
    type: Literal["transport"] = "transport"
    mode: TransportMode
    distance: float
    partials: list[Partial] | None

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> Self:
        id = df["trip_id"].iloc[0]
        mode = cls.extract_mode(df)
        distance = df["distance"].sum()

        if mode == "multimode":
            partials = []
            rle = get_rle(df["trip_transport"])
            for partial in df.groupby(rle):
                partial = Partial.from_dataframe(*partial)
                partials.append(partial)
        else:
            partials = None

        return cls(
            id=id,
            start=df.index[0],
            end=df.index[-1],
            mode=mode,
            distance=distance,
            partials=partials,
        )

    @staticmethod
    def extract_mode(df: pd.DataFrame) -> str:
        if "trip_transport" not in df.columns:
            return None

        modes = df["trip_transport"].unique()

        if len(modes) == 1:
            return modes[0]
        else:
            return "multimode"

    def to_dataframe(self, expand: bool = True) -> pd.DataFrame:
        if self.mode == "multimode" and expand:
            df = pd.DataFrame([partial.model_dump() for partial in self.partials])
            df["partial.id"] = df["id"]
            df["id"] = self.id
        else:
            df = pd.DataFrame([self.model_dump()])

        return df


class Location(BaseModel):
    id: int
    source: Literal["OSM"]


class Stationary(Event):
    type: Literal["stationary"] = "stationary"
    location: Location | None

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> Self:
        id = df["trip_id"].iloc[0]

        return cls(
            id=id,
            start=df.index[0],
            end=df.index[-1],
            location=cls.extract_location(df),
        )

    @staticmethod
    def extract_location(df: pd.DataFrame) -> str:
        if "osm_location" not in df.columns:
            return None
        else:
            id = df["osm_location"].iloc[0]
            if pd.isna(id):
                return None

            return Location(id=id, source="OSM")

    def to_dataframe(self, expand: bool = True) -> pd.DataFrame:
        df = self.model_dump()

        if expand:
            df = pd.json_normalize(df)
        else:
            df = pd.DataFrame([df])

        return df


def get_events(df: pd.DataFrame) -> list[Event]:
    events = []

    for id, group in df.groupby("trip_id"):
        status = group["trip_status"].iloc[0]

        match status:
            case "transport":
                event = Transport.from_dataframe(group)
            case "stationary":
                event = Stationary.from_dataframe(group)
            case _:
                raise ValueError(f"Unknown trip status: {status}")

        events.append(event)

    return events


def get_timeline(
    df: pd.DataFrame,
    type: Literal["json", "dataframe"],
    expand: bool = True,
) -> pd.DataFrame:

    events = get_events(df)

    match type:
        case "json":
            timeline = [event.model_dump() for event in events]
        case "dataframe":
            timeline = [event.to_dataframe(expand=expand) for event in events]
            timeline = pd.concat(timeline, axis=0).reset_index(drop=True)
        case _:
            raise ValueError(f"Unknown type: {type}")

    return timeline
