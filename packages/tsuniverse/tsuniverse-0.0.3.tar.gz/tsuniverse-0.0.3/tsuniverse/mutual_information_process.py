"""The mutual information process function."""

# pylint: disable=duplicate-code,too-many-locals
from typing import Any, Iterator

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression  # type: ignore

from .feature import Feature
from .transform import Transform
from .transforms import TRANSFORMS

_MUTUAL_INFORMATION_CACHE: dict[str, Feature] = {}


def mutual_information_positive_lags(
    target: pd.Series,
    predictor: pd.Series,
    max_window: int,
    x_transform: Transform,
    y_transform: Transform,
) -> Feature:
    """Calculate the best pearson correlation for the 2 series within a lag window"""
    target = TRANSFORMS[x_transform](target).dropna()
    predictor = TRANSFORMS[y_transform](predictor).dropna()

    mi_vals = []
    lags = range(1, max_window + 1)

    for lag in lags:
        shifted = predictor.shift(lag)
        aligned = pd.concat([target, shifted], axis=1, join="inner").dropna()

        if aligned.shape[0] < 5 or aligned.iloc[:, 1].nunique() < 2:
            # Too few samples or no variation in predictor → MI is zero
            mi_vals.append(0.0)
            continue

        x = aligned.iloc[:, 1].values.reshape(-1, 1)  # type: ignore
        y = aligned.iloc[:, 0].values  # target

        try:
            mi = mutual_info_regression(x, y, n_neighbors=3, random_state=42)[0]
        except ValueError:
            mi = 0.0

        mi_vals.append(mi)

    best_idx = np.argmax(mi_vals)
    best_lag = lags[best_idx]
    best_mi = mi_vals[best_idx]

    return {
        "predictor": str(predictor.name),
        "predictor_transform": y_transform,
        "predictand": str(target.name),
        "predictand_transform": x_transform,
        "lag": float(best_lag),
        "correlation": float(abs(best_mi)),
        "notes": "mutual_information",
    }


def mutual_information_process(
    df: pd.DataFrame,
    predictand: str,
    max_window: int,
    pool: Any,
    predictand_transform: str,
) -> Iterator[Feature]:
    """Process the dataframe for tsuniverse features."""
    predictors = df.columns.values.tolist()
    cached_predictors = []
    for predictor in predictors:
        for transform in TRANSFORMS:
            key = "_".join(
                sorted([predictor, transform, predictand, predictand_transform])
            )
            feature = _MUTUAL_INFORMATION_CACHE.get(key)
            if feature is not None:
                yield feature
                cached_predictors.append(predictor)
    for transform in TRANSFORMS:
        for feature in pool.starmap(
            mutual_information_positive_lags,
            [
                (df[x], df[predictand], max_window, transform, predictand_transform)
                for x in df.columns.values.tolist()
                if x != predictand and x not in cached_predictors
            ],
        ):
            if feature is None:
                continue
            key = "_".join(
                sorted(
                    [
                        feature["predictor"],
                        transform,
                        feature["predictand"],
                        predictand_transform,
                    ]
                )
            )
            _MUTUAL_INFORMATION_CACHE[key] = feature
            yield feature
