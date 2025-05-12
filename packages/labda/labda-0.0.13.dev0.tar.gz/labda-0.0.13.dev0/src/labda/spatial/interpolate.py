from datetime import timedelta
from functools import partial
from typing import Literal

import pandas as pd
from pyproj import CRS

from ..core.expanders import get_timedelta
from ..core.utils import gap_splitter, get_rle
from .expanders import get_distance, get_speed
from .fuzzy_features import get_fuzzy_features
from .utils import df_to_gdf, gdf_to_df, valid_coordinates

InterpolationMethod = Literal["linear", "meseck", "hwang"]


def _get_intervals_for_interpolation(
    df: pd.DataFrame, limit: str | timedelta
) -> pd.DataFrame:
    df = df[~df.isna().all(axis=1)]
    timedelta = get_timedelta(df).to_frame()
    interval = gap_splitter(timedelta, limit)
    interval.name = "interval"

    return interval


def _linear_interpolation(df: pd.DataFrame) -> pd.DataFrame:
    coordinates = df[["latitude", "longitude"]].copy()
    existing_coordinates = valid_coordinates(coordinates).index
    coordinates["impute"] = True
    coordinates.loc[existing_coordinates, "impute"] = False
    coordinates[["latitude", "longitude"]] = coordinates[
        ["latitude", "longitude"]
    ].interpolate(method="linear")

    return coordinates


def _meseck_interpolation(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    crs: str | CRS,
    window: timedelta,
) -> pd.DataFrame:
    df["gap"] = df.isna().all(axis=1)
    df["interval"] = get_rle(df["gap"])
    df = df_to_gdf(df, crs=crs)
    gaps = df[df["gap"]].groupby("interval")

    valid = df[~df["gap"]]
    df.loc[valid.index, "impute"] = False

    for interval, data in gaps:
        start = data.index[0] - window
        end = data.index[0] - sampling_frequency
        gap_indexes = data.index

        preceding = valid[start:end]
        preceding_centroid = preceding.geometry.union_all().centroid
        df.loc[gap_indexes, "geometry"] = preceding_centroid
        df.loc[gap_indexes, "impute"] = True

    df = gdf_to_df(df)

    return df[["latitude", "longitude", "impute"]]


def _hwang_interpolation(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    crs: str | CRS,
    window: timedelta,
) -> pd.DataFrame:
    velocity = 1  # m/s
    distance = 100  # metres

    df["gap"] = df.isna().all(axis=1)
    df["interval"] = get_rle(df["gap"])
    gaps = df[df["gap"]].groupby("interval")  # Finding the gaps.

    # This calculates the distance and speed of the valid data even if there are gaps.
    # Therefore will get the speed and distance of gaps based on the last valid fix and the first valid fix.
    valid = df[~df["gap"]]
    valid["timedelta"] = get_timedelta(valid)
    valid["distance"] = get_distance(valid, crs)
    valid["speed"] = get_speed(valid, crs)

    df.loc[valid.index, "impute"] = False

    for interval, data in gaps:
        start_index = data.index[0]  # Start of the gap
        end_index = data.index[-1]  # End of the gap
        gap_indexes = data.index  # The indexes of the gap

        fix_before_index = (
            start_index - sampling_frequency
        )  # Last valid fix before the gap
        fix_after_index = (
            end_index + sampling_frequency
        )  # First valid fix after the gap

        data_before = valid[
            fix_before_index - window : fix_before_index
        ]  # Data before the gap
        fix_before = data_before.iloc[-1]  # Data of the last valid fix before the gap

        data_after = valid[fix_after_index : end_index + window]  # Data after the gap
        fix_after = data_after.iloc[0]  # Data of the first valid fix after the gap

        gap_distance = fix_after["distance"]
        gap_speed = fix_after["speed"] / 3.6  # Convert to m/s

        # STOP
        if gap_distance <= distance and gap_speed < velocity:
            df.loc[gap_indexes, ["latitude", "longitude"]] = fix_before[
                ["latitude", "longitude"]
            ].values
            df.loc[gap_indexes, "impute"] = "stop"

        # MOVE
        elif gap_distance > distance and gap_speed >= velocity:
            df.loc[gap_indexes, "impute"] = "move"

        # STOP-AND-MOVE (SAM) or STOP-OR-MOVE (SOM)
        else:
            fuzzy_before = (
                get_fuzzy_features(data_before, crs) if len(data_before) > 1 else {}
            )
            fuzzy_after = (
                get_fuzzy_features(data_after, crs) if len(data_after) > 1 else {}
            )

            state_before = fuzzy_before.get("state")
            state_after = fuzzy_after.get("state")

            # STOP-AND-MOVE (SAM)
            if gap_distance > distance and gap_speed < velocity:
                if state_after == "move":
                    move_duration = pd.Timedelta(
                        seconds=gap_distance / fuzzy_after.get("speed")
                    )
                    stop_end = end_index - move_duration
                    df.loc[start_index:stop_end, ["latitude", "longitude"]] = (
                        fix_before[["latitude", "longitude"]].values
                    )
                    df.loc[gap_indexes, "impute"] = "stop-and-move"

            # STOP-OR-MOVE (SOM)
            elif gap_distance <= distance and gap_speed >= velocity:
                if state_before == "stop" and state_after == "stop":
                    df.loc[gap_indexes, ["latitude", "longitude"]] = fix_before[
                        ["latitude", "longitude"]
                    ].values
                    df.loc[gap_indexes, "impute"] = "stop-or-move"

        df.loc[gap_indexes, ["latitude", "longitude"]] = df.loc[
            fix_before_index:fix_after_index, ["latitude", "longitude"]
        ].interpolate(method="linear")
        df.loc[df.index.isin(gap_indexes) & df["impute"].isna(), "impute"] = (
            "interpolate"
        )

    return df[["latitude", "longitude", "impute"]]


def interpolate(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    crs: str | CRS,
    method: InterpolationMethod,
    limit: str | timedelta,
    window: str | timedelta | None = None,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    limit = pd.Timedelta(limit)
    window = pd.Timedelta(window)

    df = df[["latitude", "longitude"]].copy()
    intervals = _get_intervals_for_interpolation(
        df, limit
    )  # Based on the max limit of what can be interpolated, data is split into intervals.

    if method == "linear":
        interpolation_func = _linear_interpolation

    elif method == "meseck" or method == "hwang":
        if window is None:
            raise ValueError(f"Window must be provided for {method} interpolation.")

        interpolation_func = (
            _hwang_interpolation if method == "hwang" else _meseck_interpolation
        )

        interpolation_func = partial(
            interpolation_func,
            sampling_frequency=sampling_frequency,
            crs=crs,
            window=window,
        )

    else:
        raise ValueError(f"Interpolation method {method} not supported.")

    coordinates = df.groupby(intervals, group_keys=False)[
        ["latitude", "longitude"]
    ].apply(lambda x: interpolation_func(x.resample(sampling_frequency).asfreq()))

    return coordinates
