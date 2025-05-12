from datetime import time, timedelta
from typing import Literal

import pandas as pd


def parse_time(time: str | time) -> time:
    if isinstance(time, str):
        return pd.to_datetime(time).time()
    return time


def _get_stats(
    df: pd.DataFrame,
    sampling_frequency: timedelta,
) -> pd.Series:
    gnss, acc, total = 0, 0, 0

    if ("latitude" in df.columns) and ("longitude" in df.columns):
        gnss = len(df.loc[df["latitude"].notna() & df["longitude"].notna()])

    if "wear" in df.columns:
        acc = len(df.loc[df["wear"] == 1])

    if (
        ("latitude" in df.columns)
        and ("longitude" in df.columns)
        and ("wear" in df.columns)
    ):
        total = len(
            df.loc[df["latitude"].notna() & df["longitude"].notna() & (df["wear"] == 1)]
        )

    stats = pd.Series(
        {
            "acc": acc,
            "gnss": gnss,
            "acc+gnss": total,
        },
        name="wear_times",
    )
    stats = stats * sampling_frequency

    return stats


def _get_times(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    start: str | time | None = None,
    end: str | time | None = None,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)

    if start:
        start = parse_time(start)
        df = df.loc[df.index.time >= start]  # type: ignore

    if end:
        end = parse_time(end)
        df = df.loc[df.index.time < end]  # type: ignore

    stats = df.groupby(pd.Grouper(freq="D", sort=True)).apply(
        lambda x: _get_stats(x, sampling_frequency)
    )

    return stats


def _get_days(
    wear_times: pd.DataFrame,
    duration: str | timedelta,
    drop: str | None = None,
) -> tuple[pd.DataFrame, pd.DatetimeIndex]:
    valid_days = None
    duration = pd.Timedelta(duration)
    days = wear_times >= duration

    weekdays = days[days.index.weekday < 5].sum().to_frame(name="weekday").T  # type: ignore
    weekends = days[days.index.weekday >= 5].sum().to_frame(name="weekend").T  # type: ignore
    total = days.sum().to_frame(name="day").T

    summary = pd.concat([weekdays, weekends, total])

    if drop:
        if drop not in wear_times.columns:
            raise ValueError(f"Sensor data do not exist in the dataframe: {drop}.")

        valid_days = days[days[drop]]
        n_days, n_valid_days = len(days.index), len(valid_days.index)
        print(f"Dropped {n_days - n_valid_days} days of data.")
    else:
        valid_days = days

    # valid_days = valid_days.index.normalize()  # type: ignore

    return summary, valid_days


def _filter_days(df: pd.DataFrame, valid_days: pd.DatetimeIndex) -> pd.DataFrame:
    if valid_days.empty:
        raise ValueError("No valid days found.")

    return df.loc[df.index.normalize().isin(valid_days.index)].copy()  # type: ignore


def get_wear_times(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    start: str | time | None = None,
    end: str | time | None = None,
    duration: str | timedelta | None = None,
    drop: Literal["acc", "gnss", "acc+gnss"] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if drop and not duration:
        raise ValueError("Duration must be provided to drop invalid data.")

    duration = "0s" if duration is None else duration

    days = pd.DataFrame()
    wear_times = _get_times(df, sampling_frequency, start, end)
    days, valid_days = _get_days(wear_times, duration, drop)

    if drop:
        df = _filter_days(df, valid_days)

    wear_times.insert(0, "day", wear_times.index.weekday)  # type: ignore

    if ("latitude" not in df.columns) and ("longitude" not in df.columns):
        wear_times.drop(columns=["gnss", "acc+gnss"], inplace=True)
        days.drop(columns=["gnss", "acc+gnss"], inplace=True)

    if "wear" not in df.columns:
        wear_times.drop(columns=["acc", "acc+gnss"], inplace=True)
        days.drop(columns=["acc", "acc+gnss"], inplace=True)

    return wear_times, days, df
