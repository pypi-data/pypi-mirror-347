from datetime import timedelta
from typing import Any

import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype

from labda.core.utils import get_rle

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


WEAR_CATEGORIES = CategoricalDtype(
    categories=["wear", "non-wear", "missing"],
)

WEAR_CATEGORIES_COLORS = {
    "wear": "#8BC34A",
    "non-wear": "#F44336",
    "missing": "#9E9E9E",
}


def _pre_wear(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    wear_limit: float = 0.5,
) -> pd.DataFrame:
    df = df["wear"].copy().resample(sampling_frequency).asfreq().to_frame()
    df["limit"] = df["wear"] >= wear_limit

    df["plot"] = "non-wear"
    df.loc[df["limit"], "plot"] = "wear"
    df.loc[df["wear"].isna(), "plot"] = "missing"
    df = df[["plot"]].astype(WEAR_CATEGORIES)
    df["id"] = get_rle(df["plot"])
    df["start"] = df.index
    df["end"] = df.index.shift(1)
    intervals = df.groupby("id").apply(
        lambda x: pd.Series(
            {
                "start": x["start"].iloc[0],
                "end": x["end"].iloc[-1],
                "wear": x["plot"].iloc[0],
            }
        ),
        include_groups=False,
    )
    intervals.loc[intervals.index[-1], "end"] = df.index[-1]

    return intervals


def plot_timeline(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    name: str,
    type: str,
) -> Any:
    if type not in df.columns:
        raise ValueError(f"The dataframe must contain the '{type}' column.")

    title = f"Subject: {name}"
    hover_text = "Status"
    legend_title = None
    df = df[[type]].copy()

    if type == "wear":
        df = _pre_wear(df, sampling_frequency)
        color_discrete_map = WEAR_CATEGORIES_COLORS
        category_orders = {"wear": ["wear", "non-wear", "missing"]}
    else:
        raise NotImplementedError(f"Type '{type}' is not implemented.")

    df["x_end"] = df[
        "end"
    ]  # Fix for plotly bug where "end" is automatically converted to integer, then when hover over the timeline, it shows the wrong date.
    df["placeholder"] = 0

    fig = px.timeline(
        df,
        x_start="start",
        x_end="x_end",
        y="placeholder",
        color=type,
        height=200,
        custom_data=[type, "start", "end"],
        template="plotly_white",
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
    )

    fig.update_layout(
        margin=dict(l=60, r=60, t=50, b=40),
        bargap=0,
        font_family="Verdana",
        title=title,
        title_y=0.90,
        legend=dict(
            title=legend_title,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate=hover_text
        + ": %{customdata[0]}<br>Start: %{customdata[1]}<br>End: %{customdata[2]}<extra></extra>",
    )
    fig.update_xaxes(
        visible=True,
        title=None,
        range=[df.iloc[0]["start"], df.iloc[-1]["end"]],
        linewidth=1.5,
        linecolor="black",
        mirror=True,
        tickfont=dict(size=13),
        tickformat=DATETIME_FORMAT,
    )
    fig.update_yaxes(
        visible=True,
        title=None,
        showticklabels=False,
        linewidth=1.5,
        linecolor="black",
        mirror=True,
    )

    return fig
