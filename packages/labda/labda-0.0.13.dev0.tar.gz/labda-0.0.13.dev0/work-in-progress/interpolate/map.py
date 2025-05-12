from typing import Any

import pandas as pd
import pydeck as pdk
from pyproj import CRS

from labda.spatial.utils import df_to_gdf


def plot_map(df: pd.DataFrame, crs: str | CRS) -> Any:
    df = df[df["latitude"].notna() & df["longitude"].notna()]
    gdf = df_to_gdf(df, crs)
    gdf.to_crs("EPSG:4326", inplace=True)

    layer = pdk.Layer(
        "GeoJsonLayer",
        gdf,
        filled=True,
        get_fill_color="color",
        get_radius=10,
        pickable=True,
    )
    layers = [layer]

    center = gdf["geometry"].union_all().centroid
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=15)

    map = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"html": "{tooltip}"},  # type: ignore
        # map_style=pdk.map_styles.CARTO_LIGHT,
    )

    return map
