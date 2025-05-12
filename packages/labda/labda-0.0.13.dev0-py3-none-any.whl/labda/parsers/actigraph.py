import io
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
from dateutil.parser import parse as parse_dt

from ..subject import Subject

VENDOR = "ActiGraph"
COLUMNS = {
    "counts_y": "uint32",
    "counts_x": "uint32",
    "counts_z": "uint32",
    "counts_vm": "float32",
    "steps": "uint32",
    "lux": "float32",
    "wear": "float32",
}


def _parse_metadata(
    header: list[str],
    datetime_format: str | None,
) -> dict[str, Any]:
    model = header[0].split("ActiGraph")[-1].split()[0].strip()
    firmware = header[0].split("Firmware")[-1].split()[0].strip()
    serial_number = header[1].split()[-1].strip()
    start_time = header[2].split()[-1].strip()
    start_date = header[3].split()[-1].strip()
    dt = start_date + " " + start_time
    if datetime_format:
        start_datetime = datetime.strptime(dt, datetime_format)
    else:
        start_datetime = parse_dt(start_date + " " + start_time)

    sampling_frequency = pd.to_timedelta(header[4].split()[-1].strip()).total_seconds()
    sampling_frequency = f"{sampling_frequency}s"

    return {
        "model": model,
        "firmware": firmware,
        "serial_number": serial_number,
        "start_datetime": start_datetime,
        "sampling_frequency": sampling_frequency,
    }


def _parse_df_with_header(data: list[str]) -> pd.DataFrame:
    df_header = data[0].split(",")
    df = data[1:]
    df = pd.DataFrame(df)
    df = df[0].str.split(",", expand=True)
    df.columns = df_header
    df.columns = df.columns.str.lower().str.strip()

    column_mapping = {
        "epoch": "time",
        "axis1": "counts_y",
        "axis2": "counts_x",
        "axis3": "counts_z",
        "activity": "counts_y",
        "activity (horizontal)": "counts_x",
        "3rd axis": "counts_z",
        "vector magnitude": "counts_vm",
        "vm": "counts_vm",
        "steps": "steps",
        "lux": "counts_lux",
        "inclinometer off": "non_wear",
        "inclinometer standing": "standing",
        "inclinometer sitting": "sitting",
        "inclinometer lying": "lying",
    }

    for old_column, new_column in column_mapping.items():
        if old_column in df.columns:
            df.rename(columns={old_column: new_column}, inplace=True)

    if "vm_counts" in df.columns and df["vm_counts"].dtype == object:
        df["vm_counts"] = df["vm_counts"].str.replace('"', "")

    return df


def _parse_inclinometer(df: pd.DataFrame) -> pd.DataFrame:
    columns = ["non_wear", "standing", "sitting", "lying"]
    exists_columns = []

    for column in columns:
        if column in df.columns:
            exists_columns.append(column)

    if exists_columns:
        df["inclinometer"] = df[exists_columns].idxmax(axis=1)
        df["inclinometer"] = pd.Categorical(df["inclinometer"], categories=columns)

        # if "non_wear" in exists_columns:
        #     df["wear"] = True
        #     df.loc[df["inclinometer"] == "non_wear", "wear"] = False
        #     # df.loc[~df["wear"], "inclinometer"] = pd.NA
        #     df["wear"] = df["wear"].astype("Float32")

        # exists_columns.append("inclinometer")
        df.drop(columns=exists_columns, inplace=True)

    return df


def _parse_df_without_header(data: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(
        data,
    )
    df = df[0].str.split(",", expand=True)
    df = df.iloc[:, :3]
    df.columns = ["y_counts", "x_counts", "z_counts"]

    return df


def _load_data(
    path: Path,
    line: int,
    header: bool,
    columns: dict[int, str] | None,
    datetime_format: str | None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    metadata = {}

    with path.open("r") as f:
        file = f.read()

    lines = file.splitlines()
    data = lines[line:]

    if isinstance(header, bool):
        metadata = _parse_metadata(lines[0:line], datetime_format)

    if any(char.isalpha() for char in data[0]) and columns is None:
        df = _parse_df_with_header(data)
    elif columns:
        data = io.StringIO("\n".join(data))
        df = pd.read_csv(data, header=None)
        df = df[columns.keys()]
        df.rename(columns=columns, inplace=True)
    else:
        raise ValueError(
            "Invalid data format. Please check the file. Try to provide the columns parameter."
        )

    _parse_inclinometer(df)

    return df, metadata


def _parse_datetime(
    df: pd.DataFrame,
    metadata: dict[str, Any] | None,
    dt_format: str | None = None,
) -> None:
    if "date" in df.columns and "time" in df.columns:
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format=dt_format)
        df.drop(columns=["date", "time"], inplace=True)
    elif "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], format=dt_format)
    elif metadata:
        start_datetime = metadata["start_datetime"]
        sample_rate = metadata["sampling_frequency"]
        df["datetime"] = pd.date_range(
            start_datetime, periods=len(df), freq=sample_rate
        )

    df.dropna(subset=["datetime"], inplace=True)
    df.set_index("datetime", inplace=True)
    df.sort_index(inplace=True)


def _validate_columns(df: pd.DataFrame, columns: dict[str, str]) -> None:
    for column, dtype in columns.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)  # type: ignore
            except ValueError:
                raise ValueError(
                    f"Invalid data type for column '{column}'. Expected {dtype}."
                )


def from_csv(
    path: Path | str,
    header: bool = True,
    lines: int = 10,
    columns: dict[int, str] | None = None,
    *,
    datetime_format: str | None = None,
    timezone: str | ZoneInfo | None = None,
) -> Subject:
    """Parses a Actigraph file in CSV format into a LABDA's data object.

    Warning:
        Due to the potentially inconsistent structure of legacy CSV files, achieving fully automated and accurate parsing with this parser is challenging.
        Consequently, errors might occur during the parsing process. Therefore, it is currently considered experimental.

    Args:
        path (Path | str): The path to the Actigraph file.
        header (bool, optional): Parsing Actigraph metadata (~10 lines).
        lines (int, optional): The number of lines before the data starts. Usually length of the Actigraph's metadata is 10 lines, therefore those lines are skipped.
        columns (dict[int, str] | None, optional): When the file does not have a column header, the columns can be provided as a dictionary.For example: {0: "y_counts", 1: "x_counts", 2: "z_counts"}, where the keys are the column indices and the values are the column names. If columns header exists and set to None, the columns will be parsed automatically. See [mode documentation](https://actigraphcorp.my.site.com/support/s/article/What-do-the-different-Mode-numbers-mean-in-a-CSV-or-DAT-file) for more info about exported columns
        datetime_format (str | None, optional): The strftime to parse time, e.g. "%d/%m/%Y". See  [strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) for more info.
        timezone (str | ZoneInfo | None, optional): The timezone which the data comes from. If not provided, time will be timezone-naive.

    Returns:
        Subject: The LABDA's data object.

    Example:
        ```python

        from labda.parsers import Actigraph

        sbj = Actigraph.from_csv(
            "ellie_williams.csv",
            header=False,
            lines=0,
            columns={0: "datetime", 1: "counts_y", 2: "counts_x", 3: "counts_z"},
            datetime_format="%d/%m/%Y %H:%M:%S",
            timezone="America/New_York",
        )
        ```
    """
    if isinstance(path, str):
        path = Path(path)

    df, metadata = _load_data(path, lines, header, columns, datetime_format)

    if df.empty:
        raise ValueError("No data found in the file.")

    _parse_datetime(df, metadata, datetime_format)

    if timezone:
        df.index = df.index.tz_localize(timezone, ambiguous=False)  # type: ignore
        metadata["timezone"] = str(timezone)

    _validate_columns(df, COLUMNS)

    del metadata["start_datetime"]
    metadata["vendor"] = VENDOR
    metadata["id"] = path.stem

    return Subject.from_parser(df, metadata)
