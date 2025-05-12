import numpy as np
import pandas as pd
from pyproj import CRS

from ..core.expanders import get_timedelta
from .utils import DEFAULT_CRS, change_crs, check_crs_unit, df_to_gdf


def get_distance(
    df: pd.DataFrame,
    crs: str | CRS,
) -> pd.Series:
    if (
        not isinstance(df.index, pd.DatetimeIndex)
        or "latitude" not in df.columns
        or "longitude" not in df.columns
    ):
        raise ValueError(
            "DataFrame must contain columns 'latitude', and 'longitude' and have a DatetimeIndex."
        )

    check_crs_unit(crs, "metre")

    gdf = df_to_gdf(df, crs)

    distance = gdf.distance(gdf.shift(1))  # type: ignore
    distance.name = "distance"
    # distance.iloc[0] = 0 # It is better to use iat or at. Much faster than iloc.

    return distance.astype("Float32")


def get_speed(
    df: pd.DataFrame,
    crs: str | CRS,
    precomputed: bool = True,
) -> pd.Series:
    if not precomputed:
        df = df[["latitude", "longitude"]].copy()
        df["distance"] = get_distance(df, crs)
        df["timedelta"] = get_timedelta(df)

    if "distance" not in df.columns or "timedelta" not in df.columns:
        raise ValueError("DataFrame must contain columns 'distance' and 'timedelta'.")

    speed = df["distance"] / df["timedelta"].dt.total_seconds()
    speed = speed * 3.6  # Convert to km/h
    speed.name = "speed"
    # speed.iloc[0] = 0 # It is better to use iat or at. Much faster than iloc.

    return speed.astype("Float32")


def get_acceleration(
    df: pd.DataFrame,
    crs: str | CRS,
    precomputed: bool = True,
) -> pd.Series:
    if not precomputed:
        df = df[["latitude", "longitude"]].copy()
        df["speed"] = get_speed(df, crs)
        df["timedelta"] = get_timedelta(df)

    if "speed" not in df.columns or "timedelta" not in df.columns:
        raise ValueError("DataFrame must contain columns 'speed' and 'timedelta'.")

    acceleration = df["speed"].diff(1) / df["timedelta"].dt.total_seconds()
    acceleration.name = "acceleration"
    # acceleration.iloc[0] = 0 # It is better to use iat or at. Much faster than iloc.

    return acceleration.astype("Float32")


def get_bearing(
    df: pd.DataFrame,
    crs: str | CRS,
    shift: int = 1,
) -> pd.Series:
    df = change_crs(df, crs, DEFAULT_CRS)
    df[["latitude", "longitude"]] = df[["latitude", "longitude"]].apply(np.radians)
    df[["latitude_shift", "longitude_shift"]] = df[["latitude", "longitude"]].shift(
        shift
    )
    df["delta_longitude"] = df["longitude_shift"] - df["longitude"]
    df["x"] = np.cos(df["latitude_shift"]) * np.sin(df["delta_longitude"])
    df["y"] = np.cos(df["latitude"]) * np.sin(df["latitude_shift"]) - np.sin(
        df["latitude"]
    ) * np.cos(df["latitude_shift"]) * np.cos(df["delta_longitude"])
    df["bearing"] = np.atan2(df["y"], df["x"])
    df["bearing"] = np.degrees(df["bearing"])
    df["bearing"] = (df["bearing"] + 360) % 360

    return df["bearing"].astype("Float32")


def get_turn_angle(df: pd.DataFrame, crs: str | CRS) -> pd.Series:
    df = change_crs(df[["latitude", "longitude"]].copy(), crs, "EPSG:4326")
    df[["latitude", "longitude"]] = np.radians(df[["latitude", "longitude"]])
    df[["a_lat", "a_lon"]] = df[["latitude", "longitude"]].shift(1)
    df[["c_lat", "c_lon"]] = df[["latitude", "longitude"]].shift(-1)
    df["angle"] = np.arctan2(
        df["c_lat"] - df["latitude"], df["c_lon"] - df["longitude"]
    ) - np.arctan2(df["a_lat"] - df["latitude"], df["a_lon"] - df["longitude"])
    df["angle"] = (np.degrees(df["angle"]) + 360) % 360
    df.loc[df["angle"] > 180, "angle"] = 360 - df["angle"]

    return df["angle"].astype("Float32")
