from typing import Any

import pandas as pd
import plotly.express as px
import pydeck as pdk
from PIL import ImageColor
from pyproj import CRS
from shapely.geometry import Point

from .utils import DEFAULT_CRS, df_to_gdf


def _get_color(color: str) -> tuple[int]:
    return ImageColor.getcolor(color, "RGB")  # type: ignore


def get_colors(
    series: pd.Series, pallete: list[str] = px.colors.qualitative.Plotly
) -> dict[str, Any]:
    values = series.unique().tolist()
    colors = [_get_color(color) for color in pallete]
    colors = dict(zip(values, colors))

    return colors


def get_center(df: pd.DataFrame, crs) -> Point:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(DEFAULT_CRS, inplace=True)
    center = gdf["geometry"].union_all().centroid  # type: ignore

    return center


def _get_context_tooltip(df: pd.DataFrame) -> pd.Series:
    tooltip = "Context: <strong>{context} ({priority:.0f})</strong>"
    return df.apply(
        lambda x: tooltip.format(context=x["context"], priority=x["priority"]), axis=1
    )


def get_context_layer(
    df: pd.DataFrame,
    crs: str | CRS,
    colormap: dict[str, Any] | None = None,
) -> pdk.Layer:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(DEFAULT_CRS, inplace=True)

    if not colormap:
        colormap = get_colors(gdf["context"])  # type: ignore

    gdf["color"] = gdf["context"].map(colormap)  # type: ignore
    gdf["tooltip"] = _get_context_tooltip(gdf)

    layer = pdk.Layer(
        "GeoJsonLayer",
        gdf[["geometry", "color", "tooltip"]],
        stroked=True,
        filled=False,
        get_position="geometry.coordinates",
        get_fill_color="color",
        get_line_width=5,
        get_line_color="color",
        pickable=True,
        auto_highlight=True,
        highlight_color=ImageColor.getcolor("black", "RGB"),
        opacity=1,
    )

    return layer


def _get_gps_tooltip(df: pd.DataFrame, color: str | None = None) -> pd.Series:
    df["datetime"] = df.index.strftime("%Y-%m-%d %H:%M:%S")  # type: ignore

    if color:
        tooltip = """
        <strong>{datetime}</strong><br>
        Coordinates: {latitude:.7f}, {longitude:7f}<br>
        Color: {color}
        """
        series = df.apply(
            lambda x: tooltip.format(
                datetime=x["datetime"],
                latitude=x.geometry.x,
                longitude=x.geometry.y,
                color=x[color],
            ),
            axis=1,
        )
    else:
        tooltip = """
            <strong>{datetime}</strong><br>
            {latitude}, {longitude}<br>
            """
        series = df.apply(
            lambda x: tooltip.format(
                datetime=x["datetime"],
                latitude=x.geometry.x,
                longitude=x.geometry.y,
            ),
            axis=1,
        )

    return series


def get_gps_layer(
    df: pd.DataFrame,
    crs: str | CRS,
    color: str | None = None,
    colormap: dict[str, Any] | None = None,
) -> pdk.Layer:
    gdf = df_to_gdf(df, crs)
    gdf.to_crs(DEFAULT_CRS, inplace=True)

    columns = ["geometry", "tooltip", "color"]
    default_color = "white"

    if color:
        gdf["color"] = gdf[color].astype(str)

        if not colormap:
            colormap = get_colors(gdf["color"])  # type: ignore

        gdf["color"] = gdf["color"].map(colormap)  # type: ignore
    else:
        gdf["color"] = default_color
        gdf["color"] = gdf["color"].apply(lambda x: _get_color(x))  # type: ignore

    gdf["tooltip"] = _get_gps_tooltip(gdf, color)

    layer = pdk.Layer(
        "GeoJsonLayer",
        gdf[columns],
        stroked=True,
        filled=True,
        get_position="geometry.coordinates",
        get_fill_color="color",
        get_line_width=5,
        get_radius=10,
        get_line_color="color",
        pickable=True,
        auto_highlight=True,
        highlight_color=ImageColor.getcolor("red", "RGB"),
        opacity=1,
    )

    return layer


def get_map(center: Point, layers: list[pdk.Layer]) -> Any:
    view_state = pdk.ViewState(longitude=center.x, latitude=center.y, zoom=10)

    map = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"html": "{tooltip}"},  # type: ignore
        # map_style=pdk.map_styles.CARTO_LIGHT,
    )

    return map
