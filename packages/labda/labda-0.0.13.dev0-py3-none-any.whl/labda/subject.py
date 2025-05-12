from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, Literal, Self
from zoneinfo import ZoneInfo

import pandas as pd
from pyproj import CRS

from .accelerometer import (
    auto_calibration,
    detect_activity_intensity_from_counts,
    detect_wear,
)
from .accelerometer.metrics import get_enmo
from .contexts import Contexts, detect_contexts
from .core import merge, resample
from .core.expanders import get_timedelta, get_vector_magnitude
from .core.summary import get_summary
from .core.utils import change_timeframe, change_timezone, get_sampling_frequency
from .core.wear_times import get_wear_times
from .metadata import Metadata
from .object import BaseObject
from .spatial.charts import (
    get_center,
    get_gps_layer,
    get_map,
)
from .spatial.event import get_timeline
from .spatial.expanders import get_acceleration, get_distance, get_speed
from .spatial.indoor import detect_indoor
from .spatial.transportation import detect_transports
from .spatial.trips import detect_trips
from .spatial.utils import change_crs, get_crs_info, get_timezone


class Subject(BaseObject):
    """
    LABDA's data object.
    """

    @classmethod
    def from_parser(
        cls,
        df: pd.DataFrame,
        metadata: dict[str, Any],
    ) -> Self:
        if not metadata.get("sampling_frequency"):
            metadata["sampling_frequency"] = get_sampling_frequency(df, 10_000)

        id = metadata.get("id")

        if not id:
            raise ValueError("id is required.")

        duplicates = df.index.duplicated(keep="first")
        df = df.loc[~duplicates]

        n_duplicates = duplicates.sum()
        if n_duplicates > 0:
            print(f"Duplicates removed: {n_duplicates}")

        metadata_obj = Metadata(**metadata)

        return cls(id=id, df=df, metadata=metadata_obj)

    def infer_crs(self) -> tuple[str, str]:
        if self.metadata.crs == CRS.from_epsg(4326):
            return get_crs_info(self.df, crs=self.metadata.crs)  # type: ignore
        else:
            raise ValueError("CRS needs to be EPSG:4326 to infer.")

    def set_crs(self, crs: str | CRS = "infer") -> None:
        self.metadata.check_crs()
        source_crs = self.metadata.crs

        if crs == "infer":
            crs, unit = self.infer_crs()

        self.df = change_crs(self.df, source_crs, crs)
        self.metadata.crs = crs
        print(f"CRS changed from {source_crs} to {self.metadata.crs}.")

    def infer_timezone(self) -> str:
        self.metadata.check_crs()

        return get_timezone(self.df, self.metadata.crs, 20)

    def set_timezone(self, timezone: str | ZoneInfo = "infer") -> None:
        source_timezone = self.metadata.timezone

        if timezone == "infer":
            timezone = self.infer_timezone()

        self.df = change_timezone(self.df, source_timezone, timezone)
        self.metadata.timezone = timezone
        print(f"Timezone changed from {source_timezone} to {self.metadata.timezone}.")

    def set_timeframe(
        self,
        start: str | datetime | None = None,
        end: str | datetime | None = None,
    ) -> None:
        self.df = change_timeframe(self.df, start, end)
        print(f"Timeframe set from {self.df.index.min()} to {self.df.index.max()}.")

    def resample(
        self,
        sampling_frequency: str | timedelta = "uniform",
        mapper: dict[str, Any] | None = None,
        drop: bool = False,
    ) -> None:
        source_sampling_frequency = self.metadata.sampling_frequency

        if sampling_frequency == "uniform":
            sampling_frequency = source_sampling_frequency

        self.df = resample(
            self.df,
            source_sampling_frequency,
            sampling_frequency,
            mapper,
            drop,
        )
        self.metadata.sampling_frequency = sampling_frequency  # type: ignore
        print(
            f"Sampling frequency changed from {source_sampling_frequency} to {self.metadata.sampling_frequency}."
        )

    def merge(
        self,
        other: Self,
        how: Literal["outer", "inner"] = "outer",
        inplace: bool = False,
    ) -> Self | None:
        df, metadata = merge(self, other, how)

        if not inplace:
            return Subject(id=self.id, df=df, metadata=metadata)

        self.df = df
        self.metadata = metadata

    def add_vector_magnitude(
        self,
        columns: list[str] | Literal["counts"],
        name: str | None = None,
        overwrite: bool = False,
    ) -> None:
        if not name and columns != "counts":
            raise ValueError("Name is required if columns is not 'counts'.")

        if not overwrite and name in self.df.columns:
            raise ValueError(
                f"Column '{name}' already exists. Set overwrite to True to overwrite."
            )

        if isinstance(columns, str) and columns == "counts":
            columns = ["counts_x", "counts_y", "counts_z"]

            if not name:
                name = "counts_vm"

        self.df[name] = get_vector_magnitude(self.df, columns)

    def get_enmo(
        self,
        epoch: timedelta | str = "1s",
        absolute: bool = False,
        trim: bool = True,
    ) -> pd.Series:
        columns = ["acc_x", "acc_y", "acc_z"]

        if not all(col in self.df.columns for col in columns):
            raise ValueError("Accelerometer columns are missing.")

        enmo = get_enmo(
            self.df, self.metadata.sampling_frequency, epoch, absolute, trim
        )

        return enmo

    def calibrate(
        self,
        window: timedelta | str = "10s",
        overlap: timedelta | str = "10s",
    ) -> None:
        columns = ["acc_x", "acc_y", "acc_z"]

        if not all(col in self.df.columns for col in columns):
            raise ValueError("Accelerometer columns are missing.")

        self.df[["acc_x", "acc_y", "acc_z"]] = auto_calibration(
            self.df,
            window,
            overlap,
            self.metadata.sampling_frequency,
        )

    def detect_wear(
        self,
        algorithm: dict[str, Any],
        overwrite: bool = False,
    ) -> None:
        if not overwrite and "wear" in self.df.columns:
            raise ValueError(
                "Wear column already exists. Set overwrite to True to overwrite."
            )

        self.df["wear"] = detect_wear(
            self.df, self.metadata.sampling_frequency, algorithm
        )

    def detect_indoor(
        self,
        method: Literal[
            "sat_viewed",
            "sat_used",
            "sat_ratio",
            "snr_viewed",
            "snr_used",
            "gnss_accuracy",
        ] = "snr_viewed",
        limit: float = 215,
        overwrite: bool = False,
    ) -> None:
        if not overwrite and "indoor" in self.df.columns:
            raise ValueError(
                "Indoor column already exists. Set overwrite to True to overwrite."
            )

        self.df["indoor"] = detect_indoor(self.df, method, limit)

    def detect_trips(
        self,
        stop_radius: float = 30,
        stop_duration: str | timedelta = "5min",
        pause_radius: float | None = 15,
        pause_duration: str | timedelta | None = "2.5min",
        min_length: float | None = None,
        min_duration: str | timedelta | None = "1min",
        indoor_limit: float | None = 0.7,  # Ideal from validation is 0.7
        turn_angle: float | None = None,
        overwrite: bool = False,
    ) -> None:
        self.metadata.check_crs()

        columns = ["trip_status", "trip_id"]

        if not overwrite and any(col in self.df.columns for col in columns):
            raise ValueError(
                "Trip columns already exist. Set overwrite to True to overwrite."
            )

        self.df[["trip_status", "trip_id"]] = detect_trips(
            self.df,
            self.metadata.sampling_frequency,
            self.metadata.crs,
            stop_radius,
            stop_duration,
            pause_radius,
            pause_duration,
            min_length,
            min_duration,
            indoor_limit,
            turn_angle,
        )

    def detect_transportation(
        self,
        algorithm: dict[str, Any],
        overwrite: bool = False,
    ) -> None:
        self.metadata.check_crs()

        if not overwrite and "trip_transport" in self.df.columns:
            raise ValueError(
                "Trip transportation column already exists. Set overwrite to True to overwrite."
            )

        self.df["trip_transport"] = detect_transports(
            self.df, self.metadata.crs, algorithm
        )

    # def detect_locations(
    #     self,
    #     features: Features,
    #     buffer: float = 5,
    #     limit: float | None = None,
    #     overwrite: bool = False,
    # ) -> None:
    #     # FIXME: Problem with detection locations is that it tries to detect location for dropped trips but those dropped trips, are for example 2-3 short trips, merged into one stationary interval (id).
    #     # So it should have different trip_id or maybe another column or status, that it was drop, it is not stationary. It is dropped trip.
    #     if not overwrite and "osm_location" in self.df.columns:
    #         raise ValueError(
    #             "Location column already exists. Set overwrite to True to overwrite."
    #         )

    #     self.df["osm_location"] = detect_locations(
    #         self.df, features.df, self.metadata.crs, buffer, limit
    #     )

    def detect_activity_intensity(
        self,
        algorithm: dict[str, Any],
        non_wear: float | None = 0.8,
        overwrite: bool = False,
    ) -> None:
        if not overwrite and "activity_intensity" in self.df.columns:
            raise ValueError(
                "Activity intensity column already exists. Set overwrite to True to overwrite."
            )

        self.df["activity_intensity"] = detect_activity_intensity_from_counts(
            self.df, self.metadata.sampling_frequency, algorithm, non_wear=non_wear
        )

    def add_distance(
        self,
        overwrite: bool = False,
    ) -> None:
        self.metadata.check_crs()
        name = "distance"

        if not overwrite and name in self.df.columns:
            raise ValueError(
                f"Column '{name}' already exists. Set overwrite to True to overwrite."
            )

        self.df[name] = get_distance(self.df, self.metadata.crs)

    def add_timedelta(
        self,
        overwrite: bool = False,
    ) -> None:
        name = "timedelta"

        if not overwrite and name in self.df.columns:
            raise ValueError(
                f"Column '{name}' already exists. Set overwrite to True to overwrite."
            )

        self.df[name] = get_timedelta(self.df)

    def add_speed(self, overwrite: bool = False, precomputed: bool = False) -> None:
        self.metadata.check_crs()
        name = "speed"

        if not overwrite and name in self.df.columns:
            raise ValueError(
                f"Column '{name}' already exists. Set overwrite to True to overwrite."
            )

        self.df[name] = get_speed(self.df, self.metadata.crs, precomputed)

    def add_acceleration(
        self, overwrite: bool = False, precomputed: bool = False
    ) -> None:
        self.metadata.check_crs()
        name = "acceleration"

        if not overwrite and name in self.df.columns:
            raise ValueError(
                f"Column '{name}' already exists. Set overwrite to True to overwrite."
            )

        self.df[name] = get_acceleration(self.df, self.metadata.crs, precomputed)

    def detect_contexts(
        self,
        contexts: Contexts,
        bout_duration: str | timedelta | None = None,
        artefact_duration: str | timedelta | None = None,
    ) -> None:
        self.metadata.check_crs()
        contexts.metadata.check_crs()

        if self.metadata.crs != contexts.metadata.crs:
            raise ValueError("CRS of subject and contexts do not match.")

        if not contexts.df.empty:
            detected_contexts = detect_contexts(
                self.df,
                contexts.df,
                self.metadata.sampling_frequency,
                self.metadata.crs,
                bout_duration,
                artefact_duration,
            )  # type: ignore

            self.df = pd.concat([self.df, detected_contexts], axis=1)
        else:
            raise ValueError("No contexts to detect.")

    def get_wear_times(
        self,
        start: str | time | None = None,
        end: str | time | None = None,
        duration: str | timedelta | None = None,
        drop: Literal["acc", "gnss", "acc+gnss"] | None = None,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        wear_times, days, self.df = get_wear_times(
            self.df, self.metadata.sampling_frequency, start, end, duration, drop
        )

        return wear_times, days

    def get_summary(
        self,
        variables: (
            Literal[
                "activity_intensity",
                "trip_status",
                "trip_transport",
                "context",
            ]
            | list[str]
        ),
        freq: str = "D",
        context: bool = False,
    ) -> pd.DataFrame:
        return get_summary(
            self.df,
            self.metadata.sampling_frequency,
            variables,
            freq,
            context,
        )

    def plot(
        self,
        how: Literal["map"],
        # context: Contexts | None = None,
        color: str | None = None,
        start: str | datetime | None = None,
        end: str | datetime | None = None,
        export: str | Path | None = None,
    ) -> Any:
        df = self.df
        df = df.loc[df["latitude"].notna() & df["longitude"].notna()]

        if start or end:
            df = change_timeframe(df, start, end)

        if color:
            df = df[df[color].notna()]

        match how:
            case "map":
                crs = self.metadata.crs
                colormap = None

                if not crs:
                    raise ValueError("CRS is missing. Please set the CRS first.")

                # if color == "context" and context:
                #     colormap = get_colors(context.df["context"])

                layers = []
                center = get_center(df, crs)

                gps_layer = get_gps_layer(df, crs, color, colormap)
                layers.append(gps_layer)

                # if context and context.crs:
                #     context_layer = get_context_layer(context.df, context.crs, colormap)
                #     layers.append(context_layer)

                map = get_map(center, layers)
            case _:
                raise ValueError(f"Plot '{how}' is not implemented.")

        return map.to_html(filename=export)

    def get_timeline(
        self,
        type: Literal["transport"],
        format: Literal["json", "dataframe"] = "dataframe",
        expand: bool = True,
    ) -> Any:
        match type:
            case "transport":
                timeline = get_timeline(self.df, format, expand)
            case _:
                raise ValueError(f"Timeline '{type}' is not implemented.")

        return timeline
