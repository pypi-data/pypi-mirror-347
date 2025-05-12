from copy import deepcopy
from typing import TYPE_CHECKING, Literal

import pandas as pd

if TYPE_CHECKING:
    from ..metadata import Metadata
    from ..subject import Subject


def merge(
    left: "Subject",
    right: "Subject",
    how: Literal["inner", "outer"] = "outer",
) -> tuple[pd.DataFrame, "Metadata"]:
    if left.id != right.id:
        raise ValueError(f"IDs do not match: '{left.id}' != '{right.id}'.")

    if left.metadata.sampling_frequency != right.metadata.sampling_frequency:
        raise ValueError(
            f"Sampling frequencies do not match: '{left.metadata.sampling_frequency}' != '{right.metadata.sampling_frequency}'."
        )

    if left.metadata.timezone != right.metadata.timezone:
        raise ValueError(
            f"Timezones do not match: '{left.metadata.timezone}' != '{right.metadata.timezone}'."
        )

    if left.metadata.crs != right.metadata.crs:
        raise ValueError(
            f"CRS do not match: '{left.metadata.crs}' != '{right.metadata.crs}'."
        )

    if set(left.df.columns) & set(right.df.columns):
        raise ValueError(
            "DataFrames have overlapping columns. Please rename/remove them."
        )

    df = left.df.merge(
        right.df,
        how=how,
        left_index=True,
        right_index=True,
        suffixes=(None, None),  # Error if columns overlap.
        validate="one_to_one",
    ).tz_convert(left.metadata.timezone)

    metadata = deepcopy(left.metadata)

    return df, metadata
