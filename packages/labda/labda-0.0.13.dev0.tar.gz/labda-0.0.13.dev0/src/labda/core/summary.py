from datetime import timedelta
from typing import Literal

import pandas as pd


def _get_summary(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
    variables: list[str],
    freq: str,
) -> pd.DataFrame:
    variables = [pd.Grouper(freq=freq, sort=True)] + variables  # type: ignore

    summary = (
        df.groupby(variables, observed=False).size() * sampling_frequency
    )  # To drop NaN values: dropna=True add to groupby
    summary.name = "duration"
    summary = summary.reset_index()

    return summary


def get_summary(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    variables: (
        Literal[
            "activity_intensity",
            "trip_status",
            "trip_transport",
            "context",
        ]
        | list[str]
    ),
    freq: str = "D",
    context: bool = False,
) -> pd.DataFrame:
    sampling_frequency = pd.to_timedelta(sampling_frequency)

    if isinstance(variables, str):
        variables = [variables]

    for var in variables:
        if var not in df.columns:
            raise ValueError(f"DataFrame must contain column '{var}'.")

    if context:
        if context and "context" in variables:
            raise ValueError(
                "Cannot use 'context' variables with 'context' set to True."
            )

        contexts = df.columns[df.columns.str.contains("context_")].to_list()

        if not contexts:
            raise ValueError("DataFrame must contain context columns.")

        summaries = []

        for name in contexts:
            x = df[df[name].notna() & df[name]]
            summary = _get_summary(x, sampling_frequency, variables, freq)
            summary.insert(1, "context", name.removeprefix("context_"))
            summaries.append(summary)

        summary = pd.concat(summaries)

    else:
        summary = _get_summary(df, sampling_frequency, variables, freq)

    return summary
