from copy import deepcopy
from datetime import timedelta
from typing import Any

import pandas as pd

ACTIVITY_INTENSITIES = pd.CategoricalDtype(
    [
        "sedentary",
        "light",
        "moderate",
        "vigorous",
        "very vigorous",
    ]
)

COUNTS_CUT_POINTS: dict[str, Any] = {
    "freedson_adults_1998": {
        "name": "Freedson Adult (1998)",
        "reference": "https://journals.lww.com/acsm-msse/fulltext/1998/05000/calibration_of_the_computer_science_and.21.aspx",
        "sampling_frequency": "60s",
        "category": "adult",
        "placement": "hip",
        "required_data": "counts_y",
        "cut_points": [
            {"name": "sedentary", "max": 99},
            {"name": "light", "max": 1951},
            {"name": "moderate", "max": 5724},
            {"name": "vigorous", "max": 9498},
            {"name": "very vigorous", "max": float("inf")},
        ],
    },
    "freedson_adults_vm3_2011": {
        "name": "Freedson Adult VM3 (2011)",
        "reference": "https://doi.org/10.1016/j.jsams.2011.04.003",
        "sampling_frequency": "60s",
        "category": "adult",
        "placement": "hip",
        "required_data": "counts_vm",
        "cut_points": [
            # {
            #     "name": "sedentary",
            #     "max": 100,
            # },  # NOTE: That is not original, original has no sedentary. This helps transportation mode detection a lot, because if it is sedentary, it counts towards vehicle only.
            {"name": "light", "max": 2689},
            {"name": "moderate", "max": 6166},
            {"name": "vigorous", "max": 9642},
            {"name": "very vigorous", "max": float("inf")},
        ],
    },
    "evenson_children_2018": {
        "name": "Evenson Children (2008)",
        "reference": "https://doi.org/10.1080/02640410802334196",
        "sampling_frequency": "15s",
        "category": "children",
        "placement": "hip",
        "required_data": "counts_vm",
        "cut_points": [
            {"name": "sedentary", "max": 25},
            {"name": "light", "max": 573},
            {"name": "moderate", "max": 1002},
            {"name": "vigorous", "max": float("inf")},
        ],
    },
    "troiano_adults_2008": {
        "name": "Troiano Adults (2008)",
        "reference": "https://doi.org/10.1249/mss.0b013e31815a51b3",
        "sampling_frequency": "60s",
        "category": "adults",
        "placement": "hip",
        "required_data": "counts_vm",
        "cut_points": [
            {"name": "sedentary", "max": 99},
            {"name": "light", "max": 2019},
            {"name": "moderate", "max": 5998},
            {"name": "vigorous", "max": float("inf")},
        ],
    },
}


def _scale_cut_points(
    cut_points: list[dict[str, Any]],
    sampling_frequency: timedelta,
    algorithm_sampling_frequency: timedelta,
) -> list[dict[str, Any]]:
    cut_points = deepcopy(cut_points)

    if sampling_frequency != algorithm_sampling_frequency:
        coeff = algorithm_sampling_frequency / sampling_frequency

        for cp in cut_points:
            cp["max"] = cp["max"] / coeff

        print(
            f"Cut points scaled from {algorithm_sampling_frequency} to {sampling_frequency}."
        )

    return cut_points


def _apply_cut_points(
    series: pd.Series,
    cut_points: list[dict[str, Any]],
) -> pd.Series:
    # Extract min and max values from cut_points
    bins = [-float("inf")]
    bins += [cp["max"] for cp in cut_points]

    # Extract names from cut_points
    labels = [cp["name"] for cp in cut_points]

    # Apply cut points
    return pd.cut(series, bins=bins, labels=labels)


def detect_activity_intensity_from_counts(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    algorithm: dict[str, Any],
    non_wear: float | None = 0.8,
) -> pd.Series:
    required_data = algorithm["required_data"]

    if required_data not in df.columns:
        raise ValueError(f"Required data '{required_data}' not found in the dataframe.")

    if "wear" in df.columns and non_wear is not None:
        df = df[df["wear"] >= non_wear]

    sampling_frequency = pd.to_timedelta(sampling_frequency)
    algorithm_sampling_frequency = pd.to_timedelta(algorithm["sampling_frequency"])
    cut_points = _scale_cut_points(
        algorithm["cut_points"], sampling_frequency, algorithm_sampling_frequency
    )
    activity_intensity = _apply_cut_points(df[required_data], cut_points)
    activity_intensity.name = "activity_intensity"
    activity_intensity = activity_intensity.astype(ACTIVITY_INTENSITIES)

    return activity_intensity
