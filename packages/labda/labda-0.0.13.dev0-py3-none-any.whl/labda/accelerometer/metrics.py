from datetime import timedelta

import numpy as np
import pandas as pd

from ..core.expanders import get_vector_magnitude


def get_enmo(
    df: pd.DataFrame,
    sampling_frequency: timedelta | str,
    epoch: timedelta | str,
    absolute: bool = False,
    trim: bool = True,
) -> pd.Series:
    sampling_frequency = pd.Timedelta(sampling_frequency)
    epoch = pd.Timedelta(epoch)
    samples = epoch // sampling_frequency

    vm = get_vector_magnitude(df, ["acc_x", "acc_y", "acc_z"]) - 1

    if absolute:
        vm = vm.abs()
        name = "enmoa"
    else:
        name = "enmo"

    vm.loc[vm < 0] = 0
    vm = vm.resample(epoch).agg(["mean", "count"])

    if trim:
        vm = vm[vm["count"] >= samples]

    vm = vm["mean"]
    vm.name = name

    return vm.astype(np.float32)
