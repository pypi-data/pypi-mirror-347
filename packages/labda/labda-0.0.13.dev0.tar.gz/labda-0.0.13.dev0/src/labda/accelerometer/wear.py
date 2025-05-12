from copy import deepcopy
from datetime import timedelta
from typing import Any

import pandas as pd

from ..core.bouts import get_bouts

WEAR_ALGORITHMS: dict[str, Any] = {
    "troiano_2007": {
        "name": "Troiano (2007)",
        "reference": " https://doi.org/10.1249/mss.0b013e31815a51b3",
        "sampling_frequency": "60s",
        "category": ["children", "adolescents", "adults"],
        "placement": "hip",
        "required_data": "counts_vm",  # Originally developed for a uniaxial accelerometer but can be extended to work on triaxial accelerometers by calculating the VM.
        "params": {
            "bout_min_duration": "60m",
            "bout_max_value": 0,
            "artefact_max_duration": "2m",
            "artefact_max_value": 100,
        },
    },
    "choi_2011": {
        "name": "Choi (2011)",
        "reference": "https://doi.org/10.1249/MSS.0b013e318258cb36",
        "sampling_frequency": "60s",
        "category": ["children", "adolescents", "adults"],
        "placement": "hip",
        "required_data": "counts_vm",  # Originally developed for a uniaxial accelerometer but can be extended to work on triaxial accelerometers by calculating the VM.
        "params": {
            "bout_min_duration": "90m",
            "bout_max_value": 0,
            "artefact_max_duration": "2m",
            "artefact_between_duration": "30m",
            "artefact_max_value": 0,
        },
    },
}


def _scale_params(
    params: dict[str, Any],
    sampling_frequency: timedelta,
    algorithm_sampling_frequency: timedelta,
) -> dict[str, Any]:
    params = deepcopy(params)

    if sampling_frequency != algorithm_sampling_frequency:
        coeff = algorithm_sampling_frequency / sampling_frequency

        for key, value in params.items():
            if "value" in key:
                params[key] = value / coeff

        print(
            f"Cut points scaled from {algorithm_sampling_frequency} to {sampling_frequency}."
        )

    return params


def detect_wear(
    df: pd.DataFrame,
    sampling_frequency: str | timedelta,
    algorithm: dict[str, Any],
) -> pd.Series:
    required_data = algorithm["required_data"]

    if required_data not in df.columns:
        raise ValueError(f"Required data '{required_data}' not found in the dataframe.")

    sampling_frequency = pd.to_timedelta(sampling_frequency)
    algorithm_sampling_frequency = pd.to_timedelta(algorithm["sampling_frequency"])
    params = _scale_params(
        algorithm["params"], sampling_frequency, algorithm_sampling_frequency
    )

    wear = get_bouts(df[required_data], sampling_frequency, **params)
    wear = ~wear
    wear.name = "wear"

    return wear.astype(int)
