from pathlib import Path
from typing import Any, Literal
from zoneinfo import ZoneInfo

import pandas as pd
from pandas.api.types import CategoricalDtype

from ..core.utils import get_rle

COLUMNS = {
    "latitude": "float64",
    "longitude": "float64",
    "indoor": "float32",
    "y_counts": "uint32",
    "x_counts": "uint32",
    "z_counts": "uint32",
    "vm_counts": "float32",
    "wear": "float32",
    "trip_status": "category",
    "trip_id": "uint32",
    "stationary_id": "uint32",
    "trip_mode": "category",
    "activity_intensity": "category",
}

VENDOR = "PALMS"
DEFAULT_CRS = "EPSG:4326"
DEFAULT_TIMEZONE = None

GNSS_STATUS = {
    # -1: None,
    0: "invalid",
    1: "valid",
    2: "first-fix",
    3: "last-fix",
    4: "last-valid-fix",
    5: "lone-fix",
    6: "inserted-fix",
}

ENVIRONMENT = {
    # -1: None,
    0: "outdoor",
    1: "indoor",
    2: "vehicle",
}

TRIP_STATUS = {
    0: "stationary",
    1: "start-point",
    2: "mid-point",
    3: "pause",
    4: "end-point",
}

TRIP_MODE = {
    # -1: None,
    0: "stationary",
    1: "walk/run",
    2: "bicycle",
    3: "vehicle",
}

ACTIVITY_INTENSITY = {
    -2: "non-wear",
    # -1: None,
    0: "sedentary",
    1: "light",
    2: "moderate",
    3: "vigorous",
    4: "very-vigorous",
}


def _validate_columns(df: pd.DataFrame, columns: dict[str, str]) -> None:
    for column, dtype in columns.items():
        if column in df.columns:
            df[column] = df[column].astype(dtype)  # type: ignore


def _get_category_dtype(series: pd.Series, map: dict[int, Any]) -> pd.Series:
    # dtype = [x for x in map.values() if x is not None]
    dtype = map.values()
    series = series.map(map).astype(CategoricalDtype(categories=dtype))  # type: ignore

    return series


def parse_gnss_status(df: pd.DataFrame) -> None:
    df["gnss_status"] = _get_category_dtype(
        df["gnss_status"], GNSS_STATUS
    )  # Map GPS status. None means no GPS fix (only accelerometer data).
    df.loc[
        df["gnss_status"].isna(),
        ["latitude", "longitude", "environment", "trip_id", "trip_status", "trip_mode"],
    ] = None  # Set non-GPS records to None.


def parse_environment(df: pd.DataFrame) -> None:
    df["environment"] = _get_category_dtype(
        df["environment"], ENVIRONMENT
    )  # Map environment.
    df["indoor"] = None  # Set indoor to 0 for GPS records.
    df.loc[
        (df["environment"] == "outdoor") | (df["environment"] == "vehicle"), "indoor"
    ] = 0  # Set indoor to 0 for outdoor and vehicle GPS records.
    df.loc[df["environment"] == "indoor", "indoor"] = (
        1  # Set indoor to 1 for indoor GPS records.
    )


def _fix_adjacent_pauses_to_stationaries(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["pause_id"] = get_rle(
        df["pause"]
    )  # Get the pause id for each pause segment even if it is not a pause point.
    df["pause_temp"] = (
        df["stationary"].shift(-1) | df["stationary"].shift(1)
    )  # Check if stationary intervals are adjacent to pause intervals by shifting the stationary column by one row back and forth and checking if it is True.
    adjacent_pauses = (
        df[df["pause"] & ~df["stationary"]]
        .groupby("pause_id", group_keys=False)[["pause_temp"]]
        .apply(
            lambda x: x if x["pause_temp"].any() else None,  # type: ignore
            include_groups=False,
        )
        .index
    )  # Get the indexes of the pause segments that are adjacent to stationary segments.
    df.loc[adjacent_pauses, "stationary"] = (
        True  # Set the adjacent pause segments as stationary.
    )
    df.loc[adjacent_pauses, "pause"] = (
        False  # Set the adjacent pause segments as non-pause.
    )

    return df[["stationary", "pause"]]


def parse_trip_status(df: pd.DataFrame) -> pd.DataFrame:
    df["trip_status"] = _get_category_dtype(
        df["trip_status"], TRIP_STATUS
    )  # Map trip status.
    df["trip_status"] = df["trip_status"].cat.add_categories(["transport"])
    df = df.loc[df["gnss_status"].notna(), ["trip_id", "trip_status"]].copy()

    if df.empty:
        raise ValueError("No GPS records found.")

    df[["trip", "stationary", "pause"]] = False
    df.loc[
        (df["trip_id"] != 0) | (df["trip_status"] == "pause"),
        "trip",
    ] = True
    df.loc[df["trip_id"] == 0, "stationary"] = True
    df.loc[
        df["trip_status"] == "pause",
        "stationary",
    ] = False
    df.loc[df["trip_status"] == "pause", "pause"] = True
    df[["stationary", "pause"]] = _fix_adjacent_pauses_to_stationaries(
        df[["stationary", "pause"]]
    )
    df.loc[df["trip"] | df["pause"], "trip_status"] = "transport"
    df.loc[df["stationary"], "trip_status"] = "stationary"

    df["trip_id"] = get_rle(df["trip_status"])
    df.loc[df["trip_status"] == "transport", "trip_id"] = (
        pd.factorize(df.loc[df["trip_status"] == "transport", "trip_id"])[0] + 1
    )
    df.loc[df["trip_status"] != "transport", "trip_id"] = None

    df.loc[df["pause"], "trip_status"] = "pause"
    df["trip_status"] = df["trip_status"].cat.remove_categories(
        ["start-point", "mid-point", "end-point"]
    )

    df["unique_id"] = get_rle(df["trip_status"])
    df["stationary_id"] = get_rle(df.loc[df["stationary"] | df["pause"], "unique_id"])

    return df[["trip_status", "trip_id", "stationary_id"]]


def parse_transportation_mode(df: pd.DataFrame) -> None:
    df["trip_mode"] = _get_category_dtype(df["trip_mode"], TRIP_MODE)  # Map trip mode.
    df.loc[df["trip_mode"] == "stationary", "trip_mode"] = (
        None  # Set trip mode to None if it is stationary.
    )
    df["trip_mode"] = df["trip_mode"].cat.remove_categories(["stationary"])


def parse_accelerometer(df: pd.DataFrame, counts: str) -> None:
    df["activity_intensity"] = _get_category_dtype(
        df["activity_intensity"], ACTIVITY_INTENSITY
    )  # Map activity intensity.
    acc_records = df["activity_intensity"].notna()  # Filter accelerometer records.

    df.loc[acc_records, "wear"] = 1  # Set wear to 1 for accelerometer records.
    df.loc[df["activity_intensity"] == "non-wear", "wear"] = (
        0  # Set wear to 0 for non-wear accelerometer records.
    )

    df.loc[df["activity_intensity"] == "non-wear", "activity_intensity"] = (
        None  # Set activity intensity to None for non-wear accelerometer records.
    )
    df["activity_intensity"] = df["activity_intensity"].cat.remove_categories(
        ["non-wear"]
    )

    df.loc[df[counts] == -2, counts] = (
        0  # Set activity counts to 0 if it is -2 (non-wear).
    )
    df.loc[df["activity_intensity"].isna(), counts] = None


def _parse_subject(
    df: pd.DataFrame,
    subject: str,
    counts: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    df = df.loc[df["subject"] == subject].copy()

    if df.empty:
        raise ValueError(f"No records found for subject: {subject}.")

    df.set_index("datetime", inplace=True)

    parse_gnss_status(df)
    parse_environment(df)

    try:
        df[["trip_status", "trip_id", "stationary_id"]] = parse_trip_status(df)
        parse_transportation_mode(df)
    except ValueError as e:
        print(
            f"Subject {subject}. An error occurred while parsing trip and transportation mode: {e}"
        )

    parse_accelerometer(df, counts)

    _validate_columns(df, COLUMNS)
    cols = [col for col in COLUMNS.keys() if col in df.columns]
    df = df[["gnss_status"] + cols]

    metadata = {
        "vendor": VENDOR,
        "id": subject,
        "crs": DEFAULT_CRS,
    }

    return df, metadata


def from_csv(
    path: Path | str,
    *,
    timezone: str | ZoneInfo | None = None,
    counts: Literal["x_counts", "y_counts", "z_counts", "vm_counts"] = "x_counts",
    subjects: list[str] | None = None,
) -> list[tuple[pd.DataFrame, dict[str, Any]]]:
    if isinstance(path, str):
        path = Path(path)

    # Check if coutns parameter is valid.
    counts_columns = ["x_counts", "y_counts", "z_counts", "vm_counts"]
    if counts not in counts_columns:
        raise ValueError(f"Counts column must be set to: {', '.join(counts_columns)}")

    df = pd.read_csv(path, engine="pyarrow")

    df.rename(
        columns={
            "dateTime": "datetime",
            "identifier": "subject",
            "lat": "latitude",
            "lon": "longitude",
            "fixTypeCode": "gnss_status",
            "iov": "environment",
            "tripNumber": "trip_id",
            "tripType": "trip_status",
            "tripMOT": "trip_mode",
            "activity": counts,
            "activityIntensity": "activity_intensity",
            # "ele": "elevation",
            # "distance": "distance",
            # "duration": "timedelta",
            # "heartrate": "heart_rate",
        },
        inplace=True,
    )

    if timezone:
        df["datetime"] = df["datetime"].tz_localize(timezone)

    if not subjects:
        subjects = df["subject"].unique().tolist()  # type: ignore

    parsed = []

    if subjects:
        for sbj in subjects:
            parsed.append(_parse_subject(df, sbj, counts))
    else:
        raise ValueError("No subjects found in the dataframe.")

    return parsed
