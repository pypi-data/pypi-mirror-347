from datetime import datetime, time, timedelta
from typing import Any

import geopandas as gpd
import pandas as pd
from pandera import Column, DataFrameSchema
from pyproj import CRS
from shapely import Polygon

from .core.bouts import get_bouts
from .core.contexts import detect_temporal_context
from .object import BaseObject
from .spatial.contexts import detect_spatial_context
from .spatial.utils import df_to_gdf

GEO_CONTEXTS_SCHEMA = DataFrameSchema(
    {
        "context": Column(str, unique=True),
        "start": Column(datetime, required=False, nullable=True),
        "end": Column(datetime, required=False, nullable=True),
        "priority": Column(int, required=False, nullable=False, unique=True),
        "geometry": Column(gpd.array.GeometryDtype, required=False, nullable=True),  # type: ignore
    },
    coerce=True,
)


class Contexts(BaseObject):

    def validate(self, schema: DataFrameSchema = GEO_CONTEXTS_SCHEMA) -> None:
        super().validate(schema)

    def get_context(self, context: str) -> dict[str, Any] | None:
        context = self.df[self.df["context"] == context].to_dict(orient="records")
        return context[0] if context else None

    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return df_to_gdf(
            self.df,
            crs=self.metadata.crs,
            geometry="geometry",
        )


def detect_context(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta | None = None,
    crs: str | CRS | None = None,
    geometry: Polygon | None = None,
    start: datetime | time | None = None,
    end: datetime | time | None = None,
    bout_duration: str | timedelta | None = None,
    artefact_duration: str | timedelta | None = None,
) -> pd.Series:
    context = pd.DataFrame(index=df.index)

    if geometry:
        if crs is None:
            raise ValueError("CRS must be provided for spatial context.")

        context["spatial"] = detect_spatial_context(df, crs, geometry)

    if start and end:
        context["temporal"] = detect_temporal_context(df, start, end)

    if "spatial" in context and "temporal" in context.columns:
        context["context"] = context["spatial"] & context["temporal"]
    elif "spatial" in context.columns:
        context["context"] = context["spatial"]
    elif "temporal" in context.columns:
        context["context"] = context["temporal"]

    if bout_duration:
        if sampling_frequency is None:
            raise ValueError("Sampling frequency must be provided for bouts.")
        context["context"] = context["context"].astype(
            "Int8"
        )  # From True/False to boolean, so that the function get_bouts can be used, i.e. point in polygon = 1 (true).
        context["context"] = get_bouts(
            context["context"],
            sampling_frequency=sampling_frequency,
            bout_min_value=1,
            bout_min_duration=bout_duration,  # Finding bouts of 1, i.e. point in polygon.
            artefact_max_duration=artefact_duration,
            artefact_max_value=0,  # Finding artefacts of 0, i.e. point not in polygon.
        )

    return context["context"]


def detect_contexts(
    df: pd.DataFrame,
    contexts: pd.DataFrame,
    sampling_frequency: str | timedelta | None = None,
    crs: str | CRS | None = None,
    bout_duration: str | timedelta | None = None,
    artefact_duration: str | timedelta | None = None,
) -> pd.DataFrame:
    priority = True if "priority" in contexts.columns else False
    detected_contexts = pd.DataFrame(index=df.index)

    if priority:
        contexts = contexts.sort_values("priority", ascending=False)
        detected_contexts["context"] = pd.NA

    for context in contexts.to_dict(orient="records"):
        name = context.get("context")
        column_name = f"context_{name}"
        detected_contexts[column_name] = detect_context(
            df,
            sampling_frequency=sampling_frequency,
            crs=crs,
            geometry=context.get("geometry"),
            start=context.get("start"),
            end=context.get("end"),
            bout_duration=bout_duration,
            artefact_duration=artefact_duration,
        )

        if priority:
            detected_contexts.loc[detected_contexts[column_name], "context"] = name

    return detected_contexts
