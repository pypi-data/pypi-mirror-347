from typing import Any

import numpy as np
import pandas as pd
from pyproj import CRS

from labda.spatial.expanders import (
    get_distance,
    get_speed,
    get_timedelta,
    get_turn_angle,
)
from labda.spatial.utils import df_to_gdf

WEIGHTS = {
    "speed": 0.2,
    "turn_angle": 0.4,
    "circuity": 0.4,
}


def membership_speed_stop(speed: float) -> float:
    # NOTE: The speed is in m/s
    return 1 / (1 + np.exp(2 * (speed - 1.2)))


def membership_speed_move(speed: float) -> float:
    # NOTE: The speed is in m/s
    return 1 / (1 + np.exp(-3 * (speed - 0.8)))


def membership_turn_angle_stop(angle: float) -> float:
    return 1 / (1 + np.exp(0.125 * (angle - 95)))


def membership_turn_angle_move(angle: float) -> float:
    return 1 / (1 + np.exp(-0.125 * (angle - 105)))


def membership_circuity_stop(circuity: float) -> float:
    return 1 / (1 + np.exp(-2 * (circuity - 4)))


def membership_circuity_move(circuity: float) -> float:
    return 1 / (1 + np.exp(3 * (circuity - 2)))


def _calculate_circuity_ratio(df: pd.DataFrame, crs: str | CRS) -> float:
    distance = df["distance"].sum()
    df = df_to_gdf(df.iloc[[0, -1]], crs)
    circuity = df["geometry"].iat[0].distance(df["geometry"].iat[-1])
    circuity = 1 if circuity == 0 and distance == 0 else circuity / distance

    return circuity


def get_fuzzy_features(
    df: pd.DataFrame,
    crs: str | CRS,
    weights: dict[str, float] = WEIGHTS,
) -> dict[str, Any]:
    df = df[["latitude", "longitude"]].copy()

    if df.empty or len(df) <= 2:
        print(
            "DataFrame is empty or has only two rows. Future features cannot be calculated."
        )
        return {
            "start": df.index[0],
            "end": df.index[-1],
            "records": len(df),
        }

    weight_speed = weights["speed"]
    weight_turn_angle = weights["turn_angle"]
    weight_circuity = weights["circuity"]
    weight_sum = weight_speed + weight_turn_angle + weight_circuity

    df["timedelta"] = get_timedelta(df)
    df["distance"] = get_distance(df, crs)
    df["speed"] = get_speed(df, crs)
    df["turn_angle"] = get_turn_angle(df, crs)

    speed = df["speed"].mean() / 3.6
    turn_angle = df["turn_angle"].mean()
    circuity = _calculate_circuity_ratio(df, crs)

    speed_stop, speed_move = membership_speed_stop(speed), membership_speed_move(speed)
    turn_angle_stop, turn_angle_move = membership_turn_angle_stop(
        turn_angle
    ), membership_turn_angle_move(turn_angle)
    circuity_stop, circuity_move = membership_circuity_stop(
        circuity
    ), membership_circuity_move(circuity)

    # Calculate stop probability
    stop = (
        weight_speed * speed_stop
        + weight_turn_angle * turn_angle_stop
        + weight_circuity * circuity_stop
    ) / weight_sum

    # Calculate move probability
    move = (
        weight_speed * speed_move
        + weight_turn_angle * turn_angle_move
        + weight_circuity * circuity_move
    ) / weight_sum

    state = "stop" if stop > move else "move"

    return {
        "start": df.index[0],
        "end": df.index[-1],
        "records": len(df),
        "speed": speed,
        "turn_angle": turn_angle,
        "circuity": circuity,
        "state": state,
        "probabilities": {
            "stop": {
                "value": stop,
                "membership": {
                    "speed": speed_stop,
                    "turn_angle": turn_angle_stop,
                    "circuity": circuity_stop,
                },
            },
            "move": {
                "value": move,
                "membership": {
                    "speed": speed_move,
                    "turn_angle": turn_angle_move,
                    "circuity": circuity_move,
                },
            },
        },
    }
