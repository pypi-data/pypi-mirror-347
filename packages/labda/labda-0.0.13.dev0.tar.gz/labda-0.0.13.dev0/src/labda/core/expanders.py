import numpy as np
import pandas as pd


def get_timedelta(
    df: pd.DataFrame,
) -> pd.Series:
    deltas = pd.Series(
        df.index.diff(),  # type: ignore
        index=df.index,
        name="timedelta",
    )

    return deltas


def get_vector_magnitude(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in DataFrame.")

    vm = np.linalg.norm(
        df[columns].astype(float),
        axis=1,
    )
    vm = pd.Series(vm, index=df.index, name="vector_magnitude")

    return vm
