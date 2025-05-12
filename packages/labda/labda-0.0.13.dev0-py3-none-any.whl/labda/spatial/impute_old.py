from datetime import timedelta
from typing import Any

import geopandas as gpd
import pandas as pd

from labda.core.expanders import get_timedelta

from ..core.utils import get_rle
from .expanders import get_distance, get_speed, get_turn_angle
from .fuzzy import fuzzy_dataframe


def impute_gap(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    start: timedelta,
    end: timedelta,
    max_gap_duration: timedelta | None,
    fuzzy_duration: timedelta,
    velocity: float,
    distance: float,
) -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame]:
    velocity = velocity / 3.6  # Km/h to m/s
    last_valid_index = start - sampling_frequency  # Before gap
    first_valid_index = end + sampling_frequency  # After gap

    last_valid_fix = df.loc[last_valid_index]
    first_valid_fix = df.loc[first_valid_index]

    gap_distance = first_valid_fix["distance"]  # Metres
    gap_speed = first_valid_fix["speed"] / 3.6  # Km/h
    gap_duration = first_valid_fix["timedelta"]  # Timedelta

    gap = df[start:end].index
    impute = pd.DataFrame(index=gap)
    fuzzy = pd.DataFrame()

    gap_info = {
        "start": start,
        "end": end,
        "duration": gap_duration,
        "distance": gap_distance,
        "speed": gap_speed,
    }

    if max_gap_duration is not None and gap_duration > max_gap_duration:
        return impute, gap_info, fuzzy

    if gap_distance <= distance and gap_speed <= velocity:
        impute.loc[gap, ["latitude", "longitude"]] = last_valid_fix.loc[
            ["latitude", "longitude"]
        ].values
        state = "stop"

    elif gap_distance > distance and gap_speed >= velocity:
        impute.loc[gap, ["latitude", "longitude"]] = df[
            ["latitude", "longitude"]
        ].interpolate(method="linear")
        state = "move"
    else:
        before_start = start - fuzzy_duration
        before_end = last_valid_index

        after_start = first_valid_index
        after_end = end + fuzzy_duration

        fuzzy_before = fuzzy_dataframe(df[before_start:before_end])
        fuzzy_before["segment"] = "before"
        state_before = fuzzy_before["state"]

        fuzzy_after = fuzzy_dataframe(df[after_start:after_end])
        fuzzy_after["segment"] = "after"
        state_after = fuzzy_after["state"]

        if gap_distance > distance and gap_speed < velocity:
            state = "stop-and-move"  # SAM

            speed_before = fuzzy_before["speed"]
            speed_after = fuzzy_after["speed"]
            mean_speed = (speed_before + speed_after) / 2

            if state_after == "move":
                move_duration = timedelta(
                    seconds=(gap_distance / speed_after).astype(float)
                )
                move_end = start + move_duration
                impute.loc[start:move_end, ["latitude", "longitude"]] = (
                    last_valid_fix.loc[["latitude", "longitude"]].values
                )
                impute.loc[move_end:end, ["latitude", "longitude"]] = df[
                    ["latitude", "longitude"]
                ].interpolate(method="linear")
            else:
                move_duration = timedelta(
                    seconds=(gap_distance / mean_speed).astype(float)
                )
                move_end = start + move_duration
                impute.loc[start:move_end, ["latitude", "longitude"]] = (
                    last_valid_fix.loc[["latitude", "longitude"]].values
                )
                impute.loc[move_end:end, ["latitude", "longitude"]] = df[
                    ["latitude", "longitude"]
                ].interpolate(method="linear")
                pass

        elif gap_distance <= distance and gap_speed >= velocity:
            state = "stop-or-move"  # SOM

            if state_before == "stop" and state_after == "stop":
                impute.loc[gap, ["latitude", "longitude"]] = last_valid_fix.loc[
                    ["latitude", "longitude"]
                ].values

            else:
                impute.loc[gap, ["latitude", "longitude"]] = df[
                    ["latitude", "longitude"]
                ].interpolate(method="linear")

        fuzzy = pd.DataFrame([fuzzy_before, fuzzy_after])

    impute["state"] = state

    return impute, gap_info, fuzzy


def impute_gaps(
    df: pd.DataFrame,
    crs: str,
    sampling_frequency: str | timedelta,
    max_gap_duration: str | timedelta | None,
    fuzzy_duration: str | timedelta,
    velocity: float,
    distance: float,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sampling_frequency = pd.to_timedelta(sampling_frequency)
    fuzzy_duration = pd.to_timedelta(fuzzy_duration)

    if max_gap_duration is not None:
        max_gap_duration = pd.to_timedelta(max_gap_duration)

    df = df[["latitude", "longitude"]].copy()

    df["timedelta"] = get_timedelta(df)
    df["distance"] = get_distance(df, crs)
    df["speed"] = get_speed(df, crs)
    df["turn_angle"] = get_turn_angle(df, crs)
    df["geometry"] = gpd.points_from_xy(df["longitude"], df["latitude"], crs=crs)

    df = df.resample(sampling_frequency).asfreq()
    df["gap"] = df.isna().all(axis=1)
    df.loc[~df["gap"], "impute"] = "not-impute"
    df["segment_id"] = get_rle(df["gap"])

    valid_gaps = df[df["gap"]].groupby("segment_id", group_keys=False)
    impute = []
    fuzzy = []
    gaps = []

    for id, gap in valid_gaps:
        result = impute_gap(
            df,
            sampling_frequency,
            gap.index[0],
            gap.index[-1],
            max_gap_duration,
            fuzzy_duration,
            velocity,
            distance,
        )
        result[1]["gap_id"] = id
        result[2]["gap_id"] = id

        impute.append(result[0])
        gaps.append(result[1])
        fuzzy.append(result[2])

    impute = pd.concat(impute)
    impute.rename(columns={"state": "impute"}, inplace=True)
    gaps = pd.DataFrame(gaps).set_index("gap_id")
    fuzzy = pd.concat(fuzzy).set_index(["gap_id", "segment"])
    df.update(impute)

    return df, gaps, fuzzy
