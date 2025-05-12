from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from pandas import factorize


def gap_splitter(
    df: pd.DataFrame,
    duration: str | timedelta,
) -> pd.Series:
    duration = pd.Timedelta(duration)

    if "timedelta" not in df.columns:
        raise ValueError("DataFrame must contain column 'timedelta'.")

    diff = df["timedelta"] > duration
    gaps = diff.cumsum()
    gaps.name = "gaps"

    return gaps


def get_rle(df: pd.DataFrame | pd.Series) -> pd.Series:
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    if df.empty:
        raise ValueError("DataFrame is empty.")

    df = df.apply(
        lambda x: factorize(x)[0] + 1
    )  # TODO: This should be fixed, whenever there is only one group, it crashes.
    df = df.astype(str)
    series = df.apply(lambda x: "_".join(x), axis=1)
    series = pd.Series(
        series.factorize()[0] + 1, index=df.index
    )  # TODO: Same most probably applies here.
    series = (series != series.shift()).cumsum()
    series.name = "rle"

    return series.astype("UInt16")


def timedelta_to_hertz(x: timedelta) -> float:
    return 1 / x.total_seconds()


def hertz_to_timedelta(frequency: float) -> timedelta:
    return timedelta(seconds=1 / frequency)


def get_sampling_frequency(
    df: pd.DataFrame,
    samples: int = 1_000,
) -> str:
    df = get_consecutive_samples(df, samples)
    timedeltas = pd.Series(df.index.diff())  # type: ignore
    most_frequent_timedelta = timedeltas.mode()

    if len(most_frequent_timedelta) > 1:
        raise ValueError(
            f"Multiple most frequent timedeltas found (seconds): {most_frequent_timedelta.to_list()}."
        )

    detected_sf = most_frequent_timedelta[0].total_seconds()
    detected_sf = f"{detected_sf}s"

    return detected_sf


def get_consecutive_samples(
    df: pd.DataFrame,
    samples: int,
) -> pd.DataFrame:
    if samples < len(df):
        start_row = np.random.randint(len(df))
        df = df.iloc[start_row : start_row + samples]

    return df


def change_timezone(
    df: pd.DataFrame,
    source: str | ZoneInfo | None,
    target: str | ZoneInfo,
) -> pd.DataFrame:
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex.")

    if df.index.tz:
        if str(df.index.tz) == str(source):
            df.index = df.index.tz_convert(target)
        else:
            raise ValueError(
                f"Timezone of the DataFrame {str(df.index.tz)} does not match the source timezone {source}."
            )

    else:
        df.index = df.index.tz_localize(target)

    return df


def change_timeframe(
    df,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
) -> pd.DataFrame:
    timezone = df.index.tz if df.index.tz else None

    start = pd.Timestamp(start, tz=timezone) if start else None
    end = pd.Timestamp(end, tz=timezone) if end else None

    if not start and not end:
        raise ValueError("Start or end time must be provided.")

    if start and end and not start < end:
        raise ValueError("Start time must be before end time.")

    rule_start = df.index >= start if start else True
    rule_end = df.index <= end if end else True
    rules = rule_start & rule_end
    df = df[rules]

    if df.empty:
        raise ValueError("No data available for the specified timeframe.")

    return df


def get_missing_records(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
) -> pd.DataFrame:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    df = df.resample(sampling_frequency).asfreq()
    missing_records = df[df.isna().all(axis=1)]

    if not missing_records.empty:
        print(f"Missing records: {len(missing_records)}.")
    else:
        print("No missing records found.")

    return missing_records


def filter_by_temporal_intervals(
    df: pd.DataFrame,
    start: datetime | time,
    end: datetime | time,
) -> pd.DataFrame:
    if isinstance(start, time) and isinstance(end, time):
        temporal = df.between_time(start, end, inclusive="left")
    elif isinstance(start, time) or isinstance(end, time):
        raise ValueError("If one of the start or end is a time, both must be.")
    elif isinstance(start, datetime) and isinstance(end, datetime):
        temporal = df.loc[(df.index >= start) & (df.index < end)]

    return temporal
