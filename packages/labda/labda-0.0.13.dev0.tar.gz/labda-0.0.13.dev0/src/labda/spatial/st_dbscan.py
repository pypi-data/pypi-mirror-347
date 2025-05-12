from datetime import timedelta
from typing import Any, Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, PositiveFloat, PositiveInt, field_validator
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import DBSCAN

# DOI: 10.1145/3486637.3489487


class ST_DBSCAN(BaseModel):
    distance: PositiveFloat
    time: timedelta | str
    samples: PositiveInt

    class Config:
        validate_assignment = True
        extra = "ignore"

    @field_validator("time", mode="before")
    @classmethod
    def parse_sampling_frequency(cls, value: Any) -> timedelta | Any:
        return pd.Timedelta(value).to_pytimedelta()

    def fit(
        self, df: pd.DataFrame, metric: Literal["euclidean"] = "euclidean"
    ) -> pd.Series:
        df = df[["latitude", "longitude"]].copy()

        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("DataFrame must have a DatetimeIndex.")

        if df.index.tz:
            df.index = df.index.tz_convert("UTC")

        coordinates = df[["latitude", "longitude"]].astype("float64").to_numpy()
        timestamps = (df.index.astype("int64") // 10**9).to_numpy()
        indexes = df.index
        del df

        n_rows = len(timestamps)

        # Precompute the pairwise time and euclidean distances
        time_dist = pdist(
            timestamps.reshape(n_rows, 1), metric=metric
        )  # Pairwise time differences
        euc_dist = pdist(coordinates, metric=metric)  # Pairwise euclidean distances
        del coordinates, timestamps

        dist = np.where(
            time_dist <= self.time.total_seconds(),  # type: ignore
            euc_dist,
            2 * self.distance,
        )
        dist = squareform(dist)
        del time_dist, euc_dist

        db = DBSCAN(eps=self.distance, min_samples=self.samples, metric="precomputed")
        db.fit(dist)
        labels = pd.Series(db.labels_, index=indexes, name="cluster")
        labels = labels.replace(-1, np.nan)

        return labels
