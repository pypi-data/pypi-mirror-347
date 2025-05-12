from datetime import timedelta

import pandas as pd

from .utils import get_rle


def _get_bouts(bouts: pd.DataFrame, duration: timedelta) -> bool:
    if (bouts.index[-1] - bouts.index[0]) >= duration:
        return True

    return False


def _get_artefacts(
    artefacts: pd.DataFrame,
    duration: timedelta,
    bouts: timedelta | None,
    df: pd.DataFrame,
) -> bool:
    first = artefacts.index[0]
    last = artefacts.index[-1]

    if (last - first) <= duration:
        if bouts:
            before = df["bout"].loc[first - bouts : first].iloc[:-1]
            before = before.all()

            if before:
                after = df["bout"].loc[last : last + bouts].iloc[1:]
                after = after.all()

                if after:
                    return True
        else:
            return True

    return False


def get_bouts(
    series: pd.Series,
    sampling_frequency: str | timedelta,
    bout_min_duration: str | timedelta,
    bout_min_value: float | None = None,
    bout_max_value: float | None = None,
    artefact_max_duration: str | timedelta | None = None,
    artefact_between_duration: str | timedelta | None = None,
    artefact_min_value: float | None = None,
    artefact_max_value: float | None = None,
):
    column = series.name
    df = series.resample(sampling_frequency).asfreq().to_frame()
    del series

    if bout_min_value is None and bout_max_value is None:
        raise ValueError("At least one of bout_min_value or bout_max_value is required")

    df["bout_min_value"] = (
        True if bout_min_value is None else df[column] >= bout_min_value
    )
    df["bout_max_value"] = (
        True if bout_max_value is None else df[column] <= bout_max_value
    )
    df["bout"] = (df["bout_min_value"]) & (df["bout_max_value"])
    df["bout_id"] = get_rle(df["bout"])

    if artefact_max_duration:
        if artefact_min_value is None and artefact_max_value is None:
            raise ValueError(
                "At least one of artefact_min_value or artefact_max_value is required"
            )

        df["artefact_min_value"] = (
            True if artefact_min_value is None else df[column] >= artefact_min_value
        )
        df["artefact_max_value"] = (
            True if artefact_max_value is None else df[column] <= artefact_max_value
        )
        df["artefact"] = (df["artefact_min_value"]) & (df["artefact_max_value"])
        df["artefact_id"] = get_rle(df["artefact"])

        artefact_max_duration = pd.to_timedelta(artefact_max_duration)
        artefact_between_duration = (
            pd.to_timedelta(artefact_between_duration)
            if artefact_between_duration
            else None
        )

        artefacts = (
            df[df["artefact"]]
            .groupby("artefact_id")
            .apply(
                lambda x: _get_artefacts(
                    x, artefact_max_duration, artefact_between_duration, df
                ),
                include_groups=False,
            )
        )
        artefacts = artefacts[artefacts].index
        df["artefact"] = False
        df.loc[df["artefact_id"].isin(artefacts), "artefact"] = True

    df.loc[df["artefact"], "bout"] = True
    df["bout_id"] = get_rle(df["bout"])

    bout_min_duration = pd.to_timedelta(bout_min_duration)
    bouts = (
        df[df["bout"]]
        .groupby("bout_id")
        .apply(lambda x: _get_bouts(x, bout_min_duration), include_groups=False)
    )
    bouts = bouts[bouts].index
    df["bout"] = False
    df.loc[df["bout_id"].isin(bouts), "bout"] = True

    return df["bout"]
