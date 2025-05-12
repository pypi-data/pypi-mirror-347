"""TO-DO..."""

from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from ..subject import Subject

COLUMNS = {
    "latitude": "float64",
    "longitude": "float64",
    "hdop": "float32",
    "vdop": "float32",
    "pdop": "float32",
    "sat_viewed": "uint16",
    "sat_used": "uint16",
    "sat_ratio": "float32",
    "snr_viewed": "uint16",
    "snr_used": "uint16",
    "distance": "float32",
    "speed": "float32",
    "altitude": "float32",
    "indoor": "float32",
}
VENDOR = "Qstarz"
DEFAULT_CRS = "EPSG:4326"
DEFAULT_TIMEZONE = "UTC"


def _remove_empty_column(df: pd.DataFrame) -> None:
    column = ""
    if column in df.columns:
        df.drop(columns=column, inplace=True)


def _remove_headers(df: pd.DataFrame) -> None:
    header = df.columns
    indexes = df[df.eq(header).all(axis=1)].index
    df.drop(indexes, inplace=True)


def _remove_invalid_rows(df: pd.DataFrame) -> None:
    invalid = ["no fix", "estimated (dead reckoning)", "unknown mode"]

    if "valid" in df.columns:
        df["valid"] = df["valid"].str.lower()
        indexes = df[(df["valid"].isin(invalid))].index
        df.drop(indexes, inplace=True)
        df.drop(columns="valid", inplace=True)


def _parse_coordinates(df: pd.DataFrame) -> None:
    columns = ["latitude", "longitude", "n/s", "e/w"]
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}.")

    df[["latitude", "longitude"]] = df[["latitude", "longitude"]].apply(pd.to_numeric)

    df["latitude"] = np.where(df["n/s"] == "S", -df["latitude"], df["latitude"])
    df["longitude"] = np.where(df["e/w"] == "W", -df["longitude"], df["longitude"])

    df.drop(columns=["n/s", "e/w"], inplace=True)


def _parse_datetimes(
    df: pd.DataFrame,
    datetime_format: str | None,
) -> None:
    date, time, utc = None, None, False

    if "utc" in df.columns:
        utc = True
        df.rename(columns={"utc": "datetime"}, inplace=True)
    else:
        if "date" in df.columns and "time" in df.columns:
            date, time = "date", "time"
        elif "utc date" in df.columns and "utc time" in df.columns:
            date, time = "utc date", "utc time"
            utc = True
        else:
            raise ValueError("No date/time columns found.")

        df[[date, time]] = df[[date, time]].astype("string")
        df["datetime"] = df[date] + " " + df[time]
        df.drop(columns=[date, time], inplace=True)

    df["datetime"] = pd.to_datetime(
        df["datetime"], format=datetime_format, errors="coerce", utc=utc
    )

    if df["datetime"].isna().all():
        raise ValueError("Problem with datetime parsing. Check the datetime format.")

    df.dropna(subset=["datetime"], inplace=True)
    df.drop_duplicates(subset=["datetime"], inplace=True)

    df.set_index("datetime", inplace=True, drop=True)
    df.sort_index(inplace=True)


def _parse_distance(df: pd.DataFrame) -> None:
    columns = ["distance(m)", "distance"]

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("M")

            df[column] = pd.to_numeric(df[column])
            df.rename(columns={column: "distance"}, inplace=True)

            break


def _parse_speed(df: pd.DataFrame) -> None:
    columns = ["speed", "speed(km/h)", "speed_kmh"]

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("km/h")

            df[column] = pd.to_numeric(df[column])
            df[column] = (df[column] / 3.6).round(3)
            df.rename(columns={column: "speed"}, inplace=True)

            break


def _parse_altitude(df: pd.DataFrame) -> None:
    columns = ["height", "height(m)", "height_m"]

    for column in columns:
        if column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].str.strip("M")
            df[column] = pd.to_numeric(df[column])
            df.rename(columns={column: "altitude"}, inplace=True)

            break


def _parse_satellites(df: pd.DataFrame) -> None:
    if "nsat" in df.columns:
        df["nsat"] = df["nsat"].astype("string")
        df.rename(columns={"nsat": "sat_used"}, inplace=True)
        df["sat_used"] = pd.to_numeric(df["sat_used"])
    else:
        column = next(
            (column for column in df.columns if "nsat" in column), None
        )  # "NSAT (USED/VIEW)", "NSAT(USED/VIEW)", "NSAT(USED/VIEWED)"
        if column:
            try:
                df[column] = df[column].astype("string")

                if df[column].str.contains("/").any():
                    df[column] = df[column].str.split("/")
                elif df[column].str.contains(r"\(").any():
                    df[column] = df[column].str.replace(")", "").str.split("(")

                df["sat_used"] = pd.to_numeric(df[column].str[0])
                df["sat_viewed"] = pd.to_numeric(df[column].str[1])
                df.drop(columns=[column], inplace=True)
            except Exception:
                print("Could not parse satellites.")


def _sat_info(signals: list[str]) -> dict[str, int]:
    sat_used = 0
    sat_viewed = len(signals)

    snr_used = 0
    snr_viewed = 0

    for signal in signals:
        id, snr = signal.split("-")
        snr = int(snr)

        if "#" in id:
            snr_used += snr
            sat_used += 1
        else:
            snr_viewed += snr

    snr_viewed += snr_used

    return {
        "sat_viewed": sat_viewed,
        "sat_used": sat_used,
        "snr_viewed": snr_viewed,
        "snr_used": snr_used,
    }


def _parse_sat_info(df: pd.DataFrame) -> None:
    columns = ["sat info (sid-ele-azi-snr)", "sat info (sid-snr)", "snr", "sat info"]

    def parse_no_symbol_snr(df: pd.DataFrame, column: str) -> pd.DataFrame:
        # Not nice but works.
        # Parsing without "#" in form "sat info (sid-ele-azi-snr)"
        df = df.copy()
        symbol = df[column].str.contains("#").any()
        df[column] = df[column].str.split(";")
        size = len(df[column].iloc[0][0].split("-"))

        def _parse(row: pd.Series, column: str):
            output = {}
            signals = row[column]
            used = row.get("sat_used")
            snr = [int(signal.split("-")[-1]) for signal in signals]

            if used:
                output["snr_used"] = sum(snr[:used])
                output["snr_viewed"] = sum(snr[used:]) + output["snr_used"]
            else:
                output["snr_viewed"] = sum(snr)

            return pd.Series(output)

        if not symbol and size == 4:
            snr = df.apply(lambda row: _parse(row, column), axis=1)
        else:
            snr = pd.DataFrame()

        return snr

    for column in columns:
        if column in df.columns:
            try:
                snr = parse_no_symbol_snr(df, column)

                if not snr.empty:
                    df[snr.columns] = snr
                else:
                    df[column] = df[column].astype("string")
                    df[column] = df[column].str.split(";")

                    sat_info = df[column].apply(lambda row: _sat_info(row))
                    sat_info = pd.json_normalize(sat_info)  # type: ignore
                    sat_info.index = df.index
                    df[sat_info.columns] = sat_info

                    df.drop(columns=[column], inplace=True)
            except Exception:
                print("Could not parse satellites info.")

            break


def _validate_columns(df: pd.DataFrame, columns: dict[str, str]) -> None:
    for column, dtype in columns.items():
        if column in df.columns:
            df[column] = df[column].astype(dtype)  # type: ignore


def from_csv(
    path: Path | str,
    *,
    datetime_format: str | None = None,
    timezone: str | ZoneInfo | None = None,
) -> Subject:
    """Parses a QStarz file in CSV format into a LABDA's data object.

    Warning:
        Due to the potentially inconsistent structure of legacy CSV files, achieving fully automated and accurate parsing with this parser is challenging. Consequently, errors might occur during the parsing process. Therefore, it is currently considered experimental.

    Args:
        path (Path | str): The path to the Qstarz file.
        datetime_format (str | None, optional): The strftime to parse time, e.g. "%d/%m/%Y". See  [strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) for more info.
        timezone (str | ZoneInfo | None, optional): The timezone which the data comes from. If not provided, time will be timezone-naive.

    Returns:
        Subject: The LABDA's data object.

    Example:
        ```python

        from labda.parsers import Qstarz

        sbj = Qstarz.from_csv(
            "joel_miller.csv",
            datetime_format="%d/%m/%Y %H:%M:%S",
            timezone="America/Chicago",
        )
        ```
    """
    if isinstance(path, str):
        path = Path(path)

    df = pd.read_csv(path, engine="pyarrow")

    _remove_empty_column(df)
    _remove_headers(df)
    df.columns = df.columns.str.lower().str.strip()  # Normalize column names
    _remove_invalid_rows(df)
    _parse_coordinates(df)

    _parse_datetimes(df, datetime_format)
    _parse_distance(df)
    _parse_speed(df)
    _parse_altitude(df)
    _parse_satellites(df)
    _parse_sat_info(df)

    metadata = {
        "vendor": VENDOR,
        "id": path.stem,
        "crs": DEFAULT_CRS,
    }

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex.")

    if timezone:
        if df.index.tz:
            df.index = df.index.tz_convert(timezone)
        else:
            df.index = df.index.tz_localize(timezone, ambiguous=False)

        metadata["timezone"] = str(timezone)
    elif str(df.index.tz) == DEFAULT_TIMEZONE:
        metadata["timezone"] = DEFAULT_TIMEZONE

    _validate_columns(df, COLUMNS)
    cols = [col for col in COLUMNS.keys() if col in df.columns]

    df = df[cols]

    return Subject.from_parser(df, metadata)
