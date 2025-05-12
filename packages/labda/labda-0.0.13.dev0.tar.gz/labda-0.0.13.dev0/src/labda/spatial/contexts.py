import pandas as pd
from pyproj import CRS
from shapely import Polygon

from .utils import df_to_gdf


def detect_spatial_context(
    df: pd.DataFrame,
    crs: str | CRS,
    geometry: Polygon,
) -> pd.Series:
    df = df[df["latitude"].notna() & df["longitude"].notna()]
    df = df_to_gdf(df, crs=crs)
    context = df.within(geometry)

    return context
