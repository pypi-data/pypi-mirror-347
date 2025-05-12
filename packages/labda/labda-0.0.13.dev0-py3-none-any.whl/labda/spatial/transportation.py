from typing import Any

import pandas as pd
from pyproj import CRS

from .expanders import get_speed

TRANSPORTATION_MODES = pd.CategoricalDtype(
    [
        "walk",
        "run",
        "bicycle",
        "vehicle",
        "unspecified",
    ]
)


TRANSPORTATION_CUT_POINTS: dict[str, Any] = {
    "heidler_activity_2025": {
        "name": "Heidler (Activity, 2025)",
        "reference": None,
        "sampling_frequency": "15s",
        "category": "adult",
        "speed": {
            "units": "kph",
            "cut_points": [
                {"name": "walk", "min": 0, "max": 8},
                {"name": "run", "min": 8, "max": 16},
                {"name": "bicycle", "min": 10, "max": 35},
                {"name": "vehicle", "min": 30, "max": float("inf")},
            ],
            "alpha": 3,
            "boost": None,
        },
        "activity": {
            "map": [
                {"name": "walk", "activities": ["walk", "stairs", "row"]},
                {"name": "run", "activities": ["run"]},
                {"name": "bicycle", "activities": ["bicycle"]},
                {"name": "vehicle", "activities": ["sit", "stand", "lie", "move"]},
            ],
            "boost": 0.25,
        },
        "fuzzy": "max",
    },
    "heidler_intensity_2025": {
        "name": "Heidler (Intensity, 2025)",
        "reference": None,
        "sampling_frequency": "15s",
        "category": "adult",
        "speed": {
            "units": "kph",
            "cut_points": [
                {"name": "walk", "min": 0, "max": 6},
                {"name": "run", "min": 6, "max": 16},
                {"name": "bicycle", "min": 12, "max": 35},
                {"name": "vehicle", "min": 30, "max": float("inf")},
            ],
            "alpha": 3,
            "boost": None,
        },
        "activity_intensity": {
            "map": [
                {"name": "walk", "activity_intensity": ["light"]},
                {
                    "name": "run",
                    "activity_intensity": ["vigorous", "very vigorous"],
                },
                {
                    "name": "bicycle",
                    "activity_intensity": [
                        "light",
                        "moderate",
                        "vigorous",
                    ],
                },
                {"name": "vehicle", "activity_intensity": ["sedentary", "light"]},
            ],
            "boost": None,
        },
        "fuzzy": "mean",
    },
}


def _filter_speed(speed: pd.Series, alpha: float) -> pd.Series:
    q1 = speed.quantile(0.25)
    q3 = speed.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - alpha * iqr
    upper_bound = q3 + alpha * iqr
    speed = speed.loc[(speed >= lower_bound) & (speed <= upper_bound)]

    return speed


def _classify_intervals(series: pd.Series, intervals: dict[str, Any]) -> pd.Series:
    column = series.name  # Name of the column to classify
    values = series.to_frame()

    for interval in intervals:
        name = interval["name"]
        min, max = interval["min"], interval["max"]
        values.loc[values[column].between(min, max, inclusive="both"), name] = True

    values = values.drop(columns=[column]).count(axis=0) / len(values)
    values.name = column

    return values


def _classify_map(series: pd.Series, map: dict[str, list[str]]) -> pd.Series:
    column = series.name  # Name of the column to classify
    values = series.to_frame()

    for activity in map:
        name = activity["name"]  # Transportation mode from the map (algorithm)
        activities = activity[
            column
        ]  # Activities within the specific transportation mode
        values.loc[values[column].isin(activities), name] = True

    values = values.drop(columns=[column]).count(axis=0) / len(values)
    values.name = column

    return values


def get_transport_from_speed(
    df: pd.DataFrame,
    crs: str | CRS,
    algorithm: dict[str, Any],
) -> pd.Series:
    params = algorithm.get("speed")

    if not params:
        return pd.Series(name="speed")

    alpha = params["alpha"]
    cut_points = params["cut_points"]
    boost = params.get("boost")

    speed = get_speed(df, crs, False)
    speed = _filter_speed(speed, alpha)
    transport = _classify_intervals(speed, cut_points)

    if boost:
        transport += boost

    return transport


def get_transport_from_map(
    value: str,
    df: pd.DataFrame,
    algorithm: dict[str, Any],
) -> pd.Series:

    params: dict | None = algorithm.get(value)

    if not params:
        return pd.Series(name=value)

    map = params["map"]
    boost = params.get("boost")

    transport = _classify_map(df[value], map)

    if boost:
        transport += boost

    return transport


def _detect_transport(
    df: pd.DataFrame,
    crs: str | CRS,
    algorithm: dict[str, Any],
) -> pd.Series:
    transports = []

    fuzzy = algorithm.get("fuzzy")
    maps = ["activity", "activity_intensity"]

    for map in maps:
        transport = get_transport_from_map(map, df, algorithm)
        if not transport.empty:
            transports.append(transport)

    speed_transport = get_transport_from_speed(df, crs, algorithm)
    if not speed_transport.empty:
        transports.append(speed_transport)

    if transports:
        transports = pd.concat(transports, axis=1, join="outer")
        transports["mean"] = transports.mean(
            axis=1
        )  # NOTE: This is important because NaN data will be skipped, i.e. missing activity, so only speed will be used as a fall back. Maybe use skipna and have NA values where None?
        transports["max"] = transports.max(axis=1)

        # print(transports, df.index[0])

        if fuzzy:
            transport = transports[fuzzy]
        else:
            transport = transports["max"]

        transport = transport.idxmax()

    else:
        transport = "unspecified"

    df = pd.Series(transport, index=df.index, name="transport")

    return df


def detect_transports(
    df: pd.DataFrame,
    crs: str | CRS,
    algorithm: dict[str, Any],
) -> pd.Series:
    columns = ["trip_id", "trip_status", "latitude", "longitude"]

    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")

    df = df.loc[df["trip_status"] == "transport"]

    transport = (
        df.groupby("trip_id", observed=True)
        .apply(
            lambda x: _detect_transport(x, crs, algorithm),
            include_groups=False,
        )
        .reset_index(level=0, drop=True)
    )
    transport = transport.astype(TRANSPORTATION_MODES)

    return transport
