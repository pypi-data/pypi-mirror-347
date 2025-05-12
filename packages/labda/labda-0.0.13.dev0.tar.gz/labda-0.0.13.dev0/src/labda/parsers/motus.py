from pathlib import Path
from typing import Any

import pandas as pd

VENDOR = "Motus"
TIMEZONE = "UTC"
COLUMNS = {
    "activity": "category",
    "steps": "float32",
    "wear": "float32",
}


def from_dataframe(
    df: pd.DataFrame, id: str = "unknown"
) -> tuple[pd.DataFrame, dict[str, Any]]:
    # FIXME: Automatic timezone and not hard-coded.

    df = df[["activity", "steps"]]

    df["wear"] = 1
    df["activity"] = df["activity"].cat.rename_categories(
        {
            "non_wear": "non-wear",
        }
    )
    df.loc[df["activity"] == "non-wear", "wear"] = 0

    metadata = {
        "id": id,
        "vendor": VENDOR,
        "timezone": TIMEZONE,
    }

    df = df.astype(COLUMNS)

    return df, metadata


def from_file(
    path: Path | str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    if isinstance(path, str):
        path = Path(path)

    df = pd.read_parquet(path)
    df, metadata = from_dataframe(df, path.stem)

    return df, metadata
