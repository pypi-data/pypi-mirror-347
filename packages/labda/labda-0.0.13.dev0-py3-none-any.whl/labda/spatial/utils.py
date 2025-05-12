import warnings
from collections import deque
from datetime import timedelta

import geopandas as gpd
import pandas as pd
from pyproj import CRS
from timezonefinder import TimezoneFinder

warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)

DEFAULT_CRS = "EPSG:4326"


def df_to_gdf(
    df: pd.DataFrame,
    crs: str | CRS,
    latitude: str | None = "latitude",
    longitude: str | None = "longitude",
    geometry: str | None = None,
) -> gpd.GeoDataFrame:

    if geometry:
        if geometry not in df.columns:
            raise ValueError(f"DataFrame must contain column '{geometry}'.")

        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    else:

        if longitude not in df.columns or latitude not in df.columns:
            raise ValueError(
                f"DataFrame must contain columns '{longitude}', and '{latitude}'."
            )

        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df[longitude], df[latitude]), crs=crs
        )  # type: ignore
        gdf.drop(columns=[latitude, longitude], inplace=True)

    if gdf.is_empty.all() or gdf["geometry"].isna().all():
        raise ValueError("DataFrame must contain valid geometry data.")

    return gdf


def gdf_to_df(
    gdf: gpd.GeoDataFrame,
    crs: str | CRS | None = None,  # TODO: This is most probably not needed, but check.
) -> pd.DataFrame:
    if "geometry" not in gdf.columns:
        raise ValueError("DataFrame must contain column 'geometry'.")

    df = gdf.copy()

    if crs:
        df.to_crs(crs, inplace=True)  # type: ignore

    if all(df.loc[df["geometry"].notna()].geom_type == "Point"):
        df["latitude"] = df.geometry.y
        df["longitude"] = df.geometry.x
        df[["latitude", "longitude"]] = df[["latitude", "longitude"]].astype("Float64")
        df.drop(columns=["geometry"], inplace=True)

    return pd.DataFrame(df)


def change_crs(
    df: pd.DataFrame,
    source: str | CRS,
    target: str | CRS,
) -> pd.DataFrame:
    gdf = df_to_gdf(df, source)
    gdf.to_crs(target, inplace=True)
    df = gdf_to_df(gdf)

    return df


def get_crs_info(
    df: pd.DataFrame,
    crs: str | CRS,
) -> tuple[str, str]:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(DEFAULT_CRS, inplace=True)

    estimated_crs = gdf.estimate_utm_crs()
    unit = estimated_crs.axis_info[0].unit_name

    return estimated_crs.to_string(), unit


def get_timezone(
    df: pd.DataFrame,
    crs: str | CRS,
    sample: int = 10,
    limit: float = 0.8,
) -> str:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(DEFAULT_CRS, inplace=True)
    gdf = gdf.sample(sample)

    tz_finder = TimezoneFinder()
    gdf["timezone"] = gdf.apply(
        lambda row: tz_finder.timezone_at(lat=row.geometry.y, lng=row.geometry.x),  # type: ignore
        axis=1,
    )

    timezones = gdf["timezone"].value_counts()
    timezone = timezones.idxmax()

    n = len(gdf)
    count = timezones.loc[timezone]
    percentage = (count / n) * 100

    if percentage < limit:
        raise ValueError(
            f"Timezone could not be determined with sufficient confidence. Most common timezone is less than {limit * 100:.2f}% ({percentage * 100:.2f}%)."
        )

    return timezone  # type: ignore


def check_crs_unit(
    crs: str | CRS,
    unit: str,
) -> None:
    if isinstance(crs, str):
        crs = CRS.from_user_input(crs)

    detected = crs.axis_info[0].unit_name

    if detected != unit:
        raise ValueError(f"CRS must have unit '{unit}', not '{detected}'.")


def get_stops(
    df: pd.DataFrame,
    crs: str | CRS,
    max_radius: float,
    min_duration: str | timedelta,
) -> pd.Series:
    check_crs_unit(crs, "metre")
    gdf = df_to_gdf(df[["latitude", "longitude"]], crs)
    gdf = gdf[~gdf.is_empty]  # Select only non-empty geometries.
    min_duration = pd.Timedelta(min_duration)

    stops = pd.Series(False, index=gdf.index, name="stops", dtype="boolean")
    buffer = deque()

    for dt in gdf.index:
        buffer.append(dt)

        if dt - buffer[0] >= min_duration:
            selected_rows = gdf[buffer[0] : dt]
            centroid = selected_rows.geometry.union_all().centroid

            for row in selected_rows.geometry:
                distance = centroid.distance(row)
                if distance > max_radius:
                    break
            else:
                stops.loc[selected_rows.index] = (
                    True  # Set all rows in the selected range to True.
                )

            buffer.popleft()

    # stops = stops.reindex(
    #     df.index
    # )  # Reindex to original DataFrame, so that empty geometries are also included (NaN).

    return stops


def _convert_distance_parameter(
    param: float,
    sampling_frequency: str | timedelta,
) -> float:
    sampling_frequency = pd.to_timedelta(sampling_frequency)
    meters = param / (60 / sampling_frequency.total_seconds())

    return meters


def min_distance_filter(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    crs: str | CRS,
    min_distance: float,
) -> pd.Series:
    check_crs_unit(crs, "metre")
    gdf = df_to_gdf(df[["latitude", "longitude"]], crs=crs)
    min_distance = _convert_distance_parameter(min_distance, sampling_frequency)

    keep_pts = [gdf.index[0]]  # Keep first point, always.
    prev_pt = gdf.geometry.iloc[0]

    for idx, pt in gdf.geometry.items():
        distance = pt.distance(prev_pt)
        if distance >= min_distance:
            keep_pts.append(idx)
            prev_pt = pt

    keep_pts.append(gdf.index[-1])  # Keep last point, always.

    valid = pd.Series(False, index=df.index, name="valid")
    valid[keep_pts] = True

    return valid


def valid_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    if "latitude" not in df.columns or "longitude" not in df.columns:
        raise ValueError("DataFrame must contain columns 'latitude' and 'longitude'")

    return df[df[["latitude", "longitude"]].notnull().all(axis=1)]
