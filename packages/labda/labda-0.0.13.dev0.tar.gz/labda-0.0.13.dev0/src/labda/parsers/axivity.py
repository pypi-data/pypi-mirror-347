from datetime import timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from openmovement.load import CwaData

from ..subject import Subject

VENDOR = "Axivity"
COLUMNS = {
    "acc_y": "float64",
    "acc_x": "float64",
    "acc_z": "float64",
    "gyro_x": "float64",
    "gyro_y": "float64",
    "gyro_z": "float64",
    "lux": "float32",
    "temperature": "float32",
}


def _validate_columns(df: pd.DataFrame, columns: dict[str, str]) -> None:
    for column, dtype in columns.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)  # type: ignore
            except ValueError:
                raise ValueError(
                    f"Invalid data type for column '{column}'. Expected {dtype}."
                )


def from_cwa(
    path: Path | str,
    timezone: str | ZoneInfo | None = None,
) -> Subject:
    if isinstance(path, str):
        path = Path(path)

    with CwaData(
        path,
        include_time=True,
        include_accel=True,
        include_gyro=True,
        include_light=True,
        include_temperature=True,
    ) as cwa_data:
        df = cwa_data.get_samples()
        sampling_frequency = 1 / cwa_data.get_sample_rate()

    if df.empty:
        raise ValueError("No data found in the file.")

    df.rename(
        columns={
            "time": "datetime",
            "accel_x": "acc_x",
            "accel_y": "acc_y",
            "accel_z": "acc_z",
            "light": "lux",
        },
        inplace=True,
    )

    df.set_index("datetime", inplace=True)

    metadata = {
        "id": path.stem,
        "vendor": VENDOR,
        "sampling_frequency": timedelta(seconds=sampling_frequency),
    }

    if timezone:
        df.index = df.index.tz_localize(timezone, ambiguous=False)  # type: ignore
        metadata["timezone"] = str(timezone)

    _validate_columns(df, COLUMNS)
    sbj = Subject.from_parser(df, metadata)

    return sbj
