from datetime import timedelta
from typing import Any

import pandas as pd


def sum(x: pd.Series):
    return x.sum(min_count=1)


def mode(x: pd.Series):
    # FIXME: This is real problem, because mode is not always the best solution. Should be discussed.
    m = x.mode()
    m = None if m.empty else m[0]

    return m


UNIFORM: dict[str, Any] = {
    # --- Base ---
    "subject": "first",
    "timedelta": sum,
    "wear": "mean",
    # --- Counts ---
    "counts_x": sum,
    "counts_y": sum,
    "counts_z": sum,
    "vm_counts": "mean",
    # --- Taxonomy ---
    # Column.MOVEMENT: mode,
    # Column.ACTION: mode,
    "activity": mode,
    # # --- Other ---
    # Column.ACTIVITY_INTENSITY: mode,
    # Column.ACTIVITY_VALUE: "mean",
    "steps": sum,
    # Column.HEART_RATE: "mean",
    # Column.TEMPERATURE: "mean",
    # Column.LUX: "mean",
    # --- Spatial ---
    "altitude": "first",
    "latitude": "first",
    "longitude": "first",
    "gnss_accuracy": "mean",
    "sat_viewed": "mean",
    "sat_used": "mean",
    "sat_ratio": "mean",
    "snr_viewed": "mean",
    "snr_used": "mean",
    "pdop": "mean",
    "hdop": "mean",
    "vdop": "mean",
    "distance": sum,
    "speed": "mean",
    "acceleration": "mean",
    "bearing": "first",
    "indoor": "mean",
}

DOWNSAMPLE: dict[str, Any] = {
    # --- Base ---
    "subject": "first",
    "timedelta": sum,
    "wear": "mean",
    # --- Counts ---
    "counts_x": sum,
    "counts_y": sum,
    "counts_z": sum,
    "vm_counts": "mean",
    # # --- Taxonomy ---
    # Column.MOVEMENT: mode,
    # Column.ACTION: mode,
    "activity": mode,
    # # --- Other ---
    # Column.ACTIVITY_INTENSITY: mode,
    # Column.ACTIVITY_VALUE: "mean",
    "steps": sum,
    # Column.HEART_RATE: "mean",
    # Column.TEMPERATURE: "mean",
    # Column.LUX: "mean",
    # --- Spatial ---
    "altitude": "first",
    "latitude": "first",
    "longitude": "first",
    "gnss_accuracy": "mean",
    "sat_viewed": "mean",
    "sat_used": "mean",
    "sat_ratio": "mean",
    "snr_viewed": "mean",
    "snr_used": "mean",
    "pdop": "mean",
    "hdop": "mean",
    "vdop": "mean",
    "distance": sum,
    "speed": "mean",
    "acceleration": "mean",
    "bearing": "first",
    "indoor": "mean",
}


def _validate_columns(
    df: pd.DataFrame,
    mapper: dict[str, Any],
    drop_extra: bool,
) -> dict[str, Any]:
    columns = list(mapper.keys())

    dropped = [col for col in df.columns if col not in columns]

    if dropped and not drop_extra:
        raise ValueError(f"Columns are missing in mapper ({', '.join(dropped)}).")

    mapper = {col: method for col, method in mapper.items() if col in df.columns}

    return mapper


def resample(
    df: pd.DataFrame,
    source: str | timedelta,
    target: str | timedelta,
    mapper: dict[str, Any] | None = None,
    drop_extra: bool = False,
) -> pd.DataFrame:
    source = pd.Timedelta(source)
    target = pd.Timedelta(target)

    if not mapper:
        if source < target:
            mapper = DOWNSAMPLE
        elif source > target:
            if not mapper:
                raise ValueError(f"Upsampling is not supported ({source} < {target}).")
        else:
            mapper = UNIFORM

    mapper = _validate_columns(df, mapper, drop_extra)

    df = df.resample(target).agg(mapper)  # type: ignore
    df.dropna(inplace=True, how="all")

    return df
