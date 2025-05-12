from datetime import timedelta

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def _get_valid_indexes(
    series: pd.Series,
    treshold: float,
    seed: int,
    points: int,
) -> list:
    valid_positive_pts = series[(series.notna()) & (series >= treshold)]
    valid_negative_pts = series[(series.notna()) & (series <= -treshold)]

    valid = len(valid_positive_pts) > 1 and len(valid_negative_pts) > 1

    if not valid:
        raise ValueError("No valid data for calibration")

    random_positive_pts = valid_positive_pts.sample(frac=1, random_state=seed).head(
        points
    )
    random_negative_pts = valid_negative_pts.sample(frac=1, random_state=seed).head(
        points
    )

    return random_positive_pts.index.to_list() + random_negative_pts.index.to_list()


def _get_calibration_points(
    df: pd.DataFrame,
    window: int,
    step: int,
    seed: int,
) -> pd.DataFrame:
    n_points = 500
    moving_sd_threshold = 0.013
    valid_pts_threshold = 0.3

    moving_mean = df.rolling(window, 1, True).mean()
    moving_sd = df.rolling(window, 1, True).std()

    moving_mean_nth = moving_mean.iloc[::step]
    moving_sd_nth = moving_sd.iloc[::step]

    valid_df = moving_mean_nth[(moving_sd_nth <= moving_sd_threshold).all(axis=1)]

    valid_indexes = []
    for axis in valid_df.columns:
        series = valid_df[axis]
        indexes = _get_valid_indexes(series, valid_pts_threshold, seed, n_points)
        valid_indexes.extend(indexes)

    valid_indexes = pd.to_datetime(valid_indexes).unique()
    valid_df = valid_df.loc[valid_indexes].sort_index()

    return valid_df


def _get_regression_results(df_X, df_y, weights) -> pd.DataFrame:
    results = []
    for axis in df_X.columns:
        regression = LinearRegression().fit(
            df_X[[axis]],
            df_y[[axis]],
            sample_weight=weights,
        )

        scale = regression.coef_[0]
        offset = regression.intercept_

        results.append(
            {
                "axis": axis,
                "scale": scale[0],
                "offset": offset[0],  # type: ignore
            }
        )

    return pd.DataFrame.from_records(results, index="axis")


def auto_calibration(
    df: pd.DataFrame,
    window: timedelta | str,
    overlap: timedelta | str,
    sampling_frequency: timedelta,
    seed: int = 281_597,
) -> pd.DataFrame:
    max_iter = 1_000
    convergence_treshold = 1e-9
    errors_threshold = 0.02

    window = int(
        pd.Timedelta(window).total_seconds() / sampling_frequency.total_seconds()
    )
    step = int(
        pd.Timedelta(overlap).total_seconds() / sampling_frequency.total_seconds()
    )

    try:
        temp = df[["acc_x", "acc_y", "acc_z"]].copy()
        calibration_pts = _get_calibration_points(temp, window, step, seed)

        calibration_df = calibration_pts.copy()
        calibration_df["weights"] = 1
        variables = pd.DataFrame(
            {"scale": [1, 1, 1], "offset": [0, 0, 0]}, index=["acc_x", "acc_y", "acc_z"]
        )

        for iter in range(max_iter):
            calibration_df[["acc_x", "acc_y", "acc_z"]] = (
                calibration_pts[["acc_x", "acc_y", "acc_z"]]
                .multiply(variables["scale"], axis=1)
                .add(variables["offset"])
            )

            calibration_df["vm"] = np.linalg.norm(
                calibration_df[["acc_x", "acc_y", "acc_z"]],
                axis=1,
            )
            calibration_df["errors"] = np.abs(calibration_df["vm"] - 1)

            target_df = calibration_df[["acc_x", "acc_y", "acc_z"]].div(
                calibration_df["vm"], axis=0
            )

            regression = _get_regression_results(
                calibration_df[["acc_x", "acc_y", "acc_z"]],
                target_df,
                calibration_df["weights"],
            )

            variables["scale_before"] = variables["scale"].copy()
            variables["scale"] = variables["scale"].multiply(regression["scale"])
            variables["offset"] = variables["offset"].add(regression["offset"])

            calibration_df["weights"] = (1 / calibration_df["errors"]).clip(upper=100)

            convergence_error = sum(abs(variables["scale"] - variables["scale_before"]))

            if convergence_error < convergence_treshold:
                print(f"Convergence achieved after {iter} iterations")
                break

        errors_mean = calibration_df["errors"].mean()

        if errors_mean > errors_threshold:
            print("Calibration not successful.")

        else:
            if iter == max_iter - 1:
                print("No convergence but calibration successful")

            temp = (
                temp[["acc_x", "acc_y", "acc_z"]]
                .multiply(variables["scale"], axis=1)
                .add(variables["offset"], axis=1)
            )

    except ValueError as e:
        print(e)

    return temp.astype(np.float32)
