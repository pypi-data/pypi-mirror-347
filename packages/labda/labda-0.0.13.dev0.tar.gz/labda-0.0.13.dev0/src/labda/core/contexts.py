from datetime import datetime, time

import pandas as pd

from .utils import filter_by_temporal_intervals


def detect_temporal_context(
    df: pd.DataFrame,
    start: datetime | time,
    end: datetime | time,
) -> pd.Series:
    if start.tzinfo is None:
        start = start.replace(tzinfo=df.index.tz)
        print("Timezone from DataFrame is used for start.")

    if end.tzinfo is None:
        end = end.replace(tzinfo=df.index.tz)
        print("Timezone from DataFrame is used for end.")

    temporal = filter_by_temporal_intervals(
        df,
        start=start,
        end=end,
    )

    context = pd.Series(False, index=df.index)
    context[temporal.index] = True

    return context
