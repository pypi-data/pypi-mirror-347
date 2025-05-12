from typing import Literal

import pandas as pd


def _calculate_sat_ratio(df: pd.DataFrame) -> pd.Series:
    if "sat_viewed" not in df.columns and "sat_used" not in df.columns:
        raise ValueError(
            "Columns 'sat_viewed' and 'sat_used' are required to calculate 'sat_ratio'."
        )

    df = df.loc[df["sat_used"].notna() & df["sat_viewed"].notna()]
    sat_ratio = df["sat_used"] / df["sat_viewed"]

    return sat_ratio


def detect_indoor(
    df: pd.DataFrame,
    method: Literal[
        "sat_viewed", "sat_used", "sat_ratio", "snr_viewed", "snr_used", "gnss_accuracy"
    ],
    limit: float,
) -> pd.Series:
    methods = [
        "sat_viewed",  # 9 (F1: 42,93)
        "sat_used",  # 7 (F1: 48,86)
        "sat_ratio",  # 0.7 (F1: 46,40)
        "snr_viewed",  # 260 (F1: 71,18)
        "snr_used",  # 225 (F1: 46,80)
        "gnss_accuracy",
    ]
    if method not in methods:
        raise ValueError(
            f"Invalid method '{method}'. Choose from: {', '.join(methods)}."
        )

    if method not in df.columns:
        if method == "sat_ratio":
            print("Sat ratio not found. Calculating sat ratio.")
            indoor = _calculate_sat_ratio(df)

        raise ValueError(f"Column '{method}' does not exist in dataframe.")

    else:
        indoor = df[method].dropna()

    if method == "gnss_accuracy":
        indoor = (indoor >= limit).astype(int)
    else:
        indoor = (indoor <= limit).astype(int)
    indoor = pd.Series(indoor, index=df.index, name="indoor")

    return indoor
