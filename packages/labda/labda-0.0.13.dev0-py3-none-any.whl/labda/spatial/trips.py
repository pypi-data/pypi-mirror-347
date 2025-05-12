from datetime import timedelta

import pandas as pd
from pandas.api.types import CategoricalDtype
from pyproj import CRS

from ..core.utils import get_rle
from ..spatial.expanders import get_distance, get_turn_angle
from ..spatial.utils import get_stops

TRIP_CATEGORIES = CategoricalDtype(categories=["stationary", "transport", "pause"])


def _invalid_turn_angle(
    x: pd.DataFrame,
    crs: str | CRS,
    turn_angle: float,
) -> pd.DataFrame | None:
    turn_angles = get_turn_angle(x, crs)

    if turn_angles.any():
        if turn_angles.mean() < turn_angle:
            return x

    return None


def detect_trips(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    crs: str | CRS,
    stop_radius: float,
    stop_duration: str | timedelta,
    pause_radius: float | None = None,
    pause_duration: str | timedelta | None = None,
    min_length: float | None = None,
    min_duration: str | timedelta | None = None,
    indoor_limit: float | None = None,
    turn_angle: float | None = None,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    stop_duration = pd.Timedelta(stop_duration)
    pause_duration = pd.Timedelta(pause_duration) if pause_duration else None
    min_duration = pd.Timedelta(min_duration) if min_duration else None

    columns = ["latitude", "longitude"]

    if stop_duration <= sampling_frequency:
        raise ValueError("Stop duration must be greater than the sampling rate.")

    if min_duration and min_duration <= sampling_frequency:
        raise ValueError("Min duration must be greater than the sampling rate.")

    if pause_duration and stop_duration <= pause_duration:
        raise ValueError("Stop duration must be greater than pause duration.")

    if pause_radius and stop_radius <= pause_radius:
        raise ValueError("Stop radius must be greater than pause radius.")

    if indoor_limit:
        if "indoor" not in df.columns:
            raise ValueError(
                "Indoor limit is provided but the indoor column is missing."
            )
        else:
            columns.append("indoor")

    df = df[columns].copy()  # Select only the columns that are needed.
    df = df.loc[
        df[["latitude", "longitude"]].notna().all(axis=1)
    ]  # Drop the rows with missing latitude or longitude.

    df["transport"] = True  # Mark the valid points as potentional transport.

    ###########################################################################
    # STATIONARY POINTS
    ###########################################################################
    df["stationary"] = get_stops(
        df, crs, stop_radius, stop_duration
    )  # Get the stationary points. Only the valid points are considered.

    # Fix statuses.
    df.loc[df["stationary"], "transport"] = False

    ###########################################################################
    # PAUSE POINTS
    ###########################################################################
    if pause_radius and pause_duration:
        df["pause"] = get_stops(
            df[df["transport"]], crs, pause_radius, pause_duration
        )  # Get the pause points. Only the transport points.

        df["id"] = get_rle(df["pause"])

        # Fix statuses.
        df.loc[df["pause"], "transport"] = False

        ###########################################################################
        # ADJACENT PAUSE AND STATIONARY POINTS: FIXING THE PAUSE POINTS
        ###########################################################################
        df["temp"] = df["stationary"].shift(-1) | df["stationary"].shift(
            1
        )  # Check if stationary intervals are adjacent to pause intervals by shifting the stationary column by one row back and forth and checking if it is True.

        adjacent_pauses = (
            df[df["pause"]]
            .groupby("id", group_keys=False)[["temp"]]
            .apply(
                lambda x: x if x["temp"].any() else None,  # type: ignore
                include_groups=False,
            )
            .index
        )  # Get the indexes of the pause segments that are adjacent to stationary segments.

        # Fix statuses.
        df.loc[adjacent_pauses, "pause"] = False
        df.loc[adjacent_pauses, "transport"] = False
        df.loc[adjacent_pauses, "stationary"] = True

        del adjacent_pauses

    ###########################################################################
    # SHORT LENGTH TRIPS
    ###########################################################################
    if min_length:
        df["temp"] = df["transport"] | df["pause"]
        df["id"] = get_rle(df["temp"])

        short_length_trips = (
            df[df["temp"]]
            .groupby("id", group_keys=False)[["latitude", "longitude"]]
            .apply(
                lambda x: x if get_distance(x, crs).sum() < min_length else None,  # type: ignore
                include_groups=False,
            )
            .index
        )

        # Fix statuses.
        df.loc[short_length_trips, "stationary"] = True
        df.loc[short_length_trips, "pause"] = False
        df.loc[short_length_trips, "transport"] = False

        del short_length_trips

    ###########################################################################
    # SHORT DURATION TRIPS
    ###########################################################################
    if min_duration:
        df["temp"] = df["transport"] | df["pause"]
        df["id"] = get_rle(df["temp"])

        short_duration_trips = (
            df[df["temp"]]
            .groupby("id", group_keys=False)[["latitude", "longitude"]]
            .apply(
                lambda x: x if x.index.max() - x.index.min() < min_duration else None,  # type: ignore
                include_groups=False,
            )
        ).index

        # Fix statuses.
        df.loc[short_duration_trips, "stationary"] = True
        df.loc[short_duration_trips, "pause"] = False
        df.loc[short_duration_trips, "transport"] = False

        del short_duration_trips

    ###########################################################################
    # REMOVE INDOOR TRIPS
    ###########################################################################
    if indoor_limit:
        df["temp"] = df["transport"] | df["pause"]
        df["id"] = get_rle(df["temp"])

        indoor_trips = (
            df[df["temp"]]
            .groupby("id", group_keys=False)[["indoor"]]
            .apply(
                lambda x: x if x["indoor"].mean() > indoor_limit else None,  # type: ignore
                include_groups=False,
            )
        ).index

        # Fix statuses.
        df.loc[indoor_trips, "stationary"] = True
        df.loc[indoor_trips, "pause"] = False
        df.loc[indoor_trips, "transport"] = False

        del indoor_trips

    ###########################################################################
    # REMOVE INVALID TURN ANGLE TRIPS
    ###########################################################################

    if turn_angle:
        df["temp"] = df["transport"] | df["pause"]
        df["id"] = get_rle(df["temp"])

        invalid_turn_angle_trips = (
            df[df["temp"]]
            .groupby("id", group_keys=False)[["latitude", "longitude"]]
            .apply(
                lambda x: _invalid_turn_angle(x, crs, turn_angle),  # type: ignore
                include_groups=False,
            )
        ).index

        # Fix statuses.
        df.loc[invalid_turn_angle_trips, "stationary"] = True
        df.loc[invalid_turn_angle_trips, "pause"] = False
        df.loc[invalid_turn_angle_trips, "transport"] = False

        del invalid_turn_angle_trips

    ###########################################################################
    # TRIP STATUS
    ###########################################################################
    df["status"] = pd.NA
    df["status"] = df["status"].astype(TRIP_CATEGORIES)

    df.loc[df["stationary"], "status"] = "stationary"
    df.loc[df["transport"] | df["pause"], "status"] = (
        "transport"  # The pause points are also considered as transport points at this stage to get the ID for whole transport segments (including pause points).
    )

    df["id"] = get_rle(
        df["status"]
    )  # Get id for each consecutive segment of the same status (stationary, "transport", "pause").
    df.loc[df["pause"], "status"] = "pause"  # Fix the status of the pause points.
    df.loc[df["status"] == pd.NA, "id"] = pd.NA  # Fix the status of the NA points.

    df.dropna(subset=["status"], inplace=True)  # Drop the rows with NA status.

    return df[["status", "id"]]
