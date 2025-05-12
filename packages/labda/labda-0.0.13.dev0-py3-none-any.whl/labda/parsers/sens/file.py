from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

BYTES_PER_SAMPLE = 12
SENS_NORMALIZATION_FACTOR = -4 / 512
DTYPE = np.dtype([("timestamp", "6uint8"), ("x", ">i2"), ("y", ">i2"), ("z", ">i2")])
VENDOR = "SENS"
TIMEZONE = "UTC"


def _read(
    obj: Path | bytes, func: Callable, normalize: bool
) -> tuple[pd.DataFrame, dict[str, Any]]:
    # Read the binary file into a structured numpy array
    data = func(obj, dtype=DTYPE, count=-1, offset=0)

    # Calculate timestamps from the datetime field
    timestamps = np.dot(
        data["timestamp"], [1 << 40, 1 << 32, 1 << 24, 1 << 16, 1 << 8, 1]
    )

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(timestamps, unit="ms", utc=True),
            "acc_x": data["x"].astype(np.int16),
            "acc_y": data["y"].astype(np.int16),
            "acc_z": data["z"].astype(np.int16),
        }
    )

    df.set_index("datetime", inplace=True)

    if normalize:
        df = df * SENS_NORMALIZATION_FACTOR

    metadata = {
        "vendor": VENDOR,
        "timezone": TIMEZONE,
    }

    return df.astype(np.float32), metadata  # COMMENT: Should we enforce float32?


def from_file(
    path: Path | str,
    normalize: bool = True,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    if isinstance(path, str):
        path = Path(path)

    if path.suffix != ".bin":
        raise ValueError(
            "File must be a binary file with .bin extension. Other formats are not supported."
        )

    df, metadata = _read(path, np.fromfile, normalize)
    metadata["id"] = path.stem

    return df, metadata
