from datetime import timedelta
from typing import Any

import numpy as np
import pandas as pd
from pyproj import CRS

from labda.core.utils import get_rle
from labda.spatial.utils import df_to_gdf, valid_coordinates


def get_gaps(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    gap_duration: timedelta,
) -> pd.Series:
    # Impute missing values, find gaps, and assign them indices

    sampling_frequency = pd.Timedelta(sampling_frequency)
    gap_duration = pd.Timedelta(gap_duration)

    df = df.copy()
    df["gap"] = df.isna().all(axis=1)
    df["rle"] = get_rle(df["gap"])

    # Find the short segments of missing data and make them as not missing
    short_missing_bouts = (
        df[df["gap"]].groupby("rle").size() * sampling_frequency
    ).sort_values(ascending=False)
    short_missing_bouts = short_missing_bouts[short_missing_bouts <= gap_duration]
    df.loc[df["rle"].isin(short_missing_bouts.index), "gap"] = False

    return df["gap"]


def get_consecutive_intervals(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    continous_duration: timedelta,
) -> pd.Series:
    # Find the longest continuous segments of data and filter out short segments

    sampling_frequency = pd.Timedelta(sampling_frequency)
    continous_duration = pd.Timedelta(continous_duration)

    df = df.copy()
    df["rle"] = get_rle(df["gap"])

    complete_bouts = (
        df[~df["gap"]].groupby("rle").size() * sampling_frequency
    ).sort_values(ascending=False)
    complete_bouts = complete_bouts[complete_bouts >= continous_duration]
    df = df[df["rle"].isin(complete_bouts.index)]
    df["interval"] = get_rle(df["rle"])

    return df["interval"]


def _sample_to_remove(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    max_removable_duration: timedelta,
) -> dict[str, Any]:
    max_removable_duration = pd.Timedelta(max_removable_duration)
    sampling_frequency = pd.Timedelta(sampling_frequency)

    df = df.iloc[1:-1]  # Remove first and last rows to avoid edge cases

    max_removable_samples = (
        max_removable_duration.total_seconds() / sampling_frequency.total_seconds()
    )
    remove_samples = np.random.randint(1, max_removable_samples)

    if max_removable_samples >= len(df):
        raise ValueError(
            f"Max removable samples ({max_removable_samples}) is greater than the length of the dataframe ({len(df)})."
        )

    start_row = np.random.randint(len(df))
    end_row = start_row + remove_samples

    df = df.iloc[start_row:end_row]

    return {
        "start": df.index[0],
        "end": df.index[-1],
        "duration": df.index[-1] - df.index[0],
    }


def get_samples_to_remove(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    samples: tuple[int, int],
    max_duration: timedelta,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    max_duration = pd.Timedelta(max_duration)

    to_remove = []
    for i in range(np.random.randint(samples[0], samples[1] + 1)):
        sample = _sample_to_remove(df, sampling_frequency, max_duration)
        to_remove.append(sample)

    to_remove = sorted(to_remove, key=lambda item: item["end"])
    prev_end = to_remove[0]["end"]

    for sample in to_remove[1:]:
        if sample["start"] < prev_end:
            to_remove.remove(sample)
        else:
            prev_end = sample["end"]

    return pd.DataFrame(to_remove)


def randomly_remove_data(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    max_missing_bout: str | timedelta,
    min_continous_bout: str | timedelta,
    max_duration: str | timedelta,
    samples: tuple[int, int],
) -> pd.DataFrame:
    max_missing_bout = pd.Timedelta(max_missing_bout)
    min_continous_bout = pd.Timedelta(min_continous_bout)
    sampling_frequency = pd.Timedelta(sampling_frequency)
    max_duration = pd.Timedelta(max_duration)

    df = df.copy()
    df = df[["latitude", "longitude", "true_trip", "true_transport"]]
    df = df.resample(sampling_frequency).asfreq()

    df["gap"] = get_gaps(df, sampling_frequency, max_missing_bout)
    df["interval"] = get_consecutive_intervals(
        df, sampling_frequency, min_continous_bout
    )

    to_remove = df.groupby("interval").apply(
        lambda x: get_samples_to_remove(x, sampling_frequency, samples, max_duration),
        include_groups=False,
    )

    df = df[df["interval"].notna()]
    df["remove"] = False

    for remove in to_remove.itertuples():
        df.loc[remove.start : remove.end, "remove"] = True

    return df


def get_origin_geodataframe(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    crs: str | CRS,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    df = valid_coordinates(df)
    df = df.copy()

    df = df.resample(sampling_frequency).asfreq()

    df["gap"] = df.isna().all(axis=1)
    df["rle"] = get_rle(df["gap"])
    df = df[~df["gap"]]
    df = df_to_gdf(df, crs).to_crs("EPSG:4326")
    df["datetime"] = df.index
    df.index = df.index.astype(np.int64) // 10**9

    return df


def get_interpolate_geodataframe(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    crs: str | CRS,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    df = df.copy()
    df = df.resample(sampling_frequency).asfreq()

    df["gap"] = df.isna().all(axis=1)
    df["rle"] = get_rle(df[["gap", "impute"]])
    df = df[~df["gap"]]
    df = df[df["impute"] != False]
    df = df_to_gdf(df, crs).to_crs("EPSG:4326")
    df["datetime"] = df.index
    df.index = df.index.astype(np.int64) // 10**9

    return df


import geopandas as gpd


def get_location_deviation(
    origin: gpd.GeoDataFrame,
    imputed: gpd.GeoDataFrame,
    crs: str | CRS,
) -> gpd.GeoDataFrame:
    loc_dev = pd.concat(
        [
            origin[["geometry"]].to_crs(crs),
            imputed[["geometry", "impute"]].to_crs(crs).add_prefix("impute_"),
        ],
        axis=1,
    )
    loc_dev = loc_dev[loc_dev["impute_impute"].notna() & loc_dev["geometry"].notna()]
    loc_dev["distance"] = loc_dev["geometry"].distance(loc_dev["impute_geometry"])

    return loc_dev["distance"]
