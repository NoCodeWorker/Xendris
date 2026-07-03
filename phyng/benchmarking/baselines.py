"""Simple baseline models with optional scikit-learn support."""

from __future__ import annotations

import numpy as np


def sklearn_available() -> bool:
    try:
        import sklearn  # noqa: F401

        return True
    except ModuleNotFoundError:
        return False


def mean_baseline(y_true) -> dict:
    y = np.asarray(y_true, dtype=float)
    value = float(np.mean(y)) if len(y) else 0.0
    return {
        "model_id": "MEAN_BASELINE",
        "model_family": "constant",
        "parameter_count": 1,
        "fitted_or_not": "FITTED_BASELINE",
        "leakage_risk": "MEDIUM",
        "prediction": [value for _ in y],
        "sklearn_available": sklearn_available(),
    }


def linear_regression_baseline(x, y) -> dict:
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if sklearn_available():
        from sklearn.linear_model import LinearRegression

        model = LinearRegression().fit(x_arr.reshape(-1, 1), y_arr)
        pred = model.predict(x_arr.reshape(-1, 1))
        params = {"intercept": float(model.intercept_), "coef": float(model.coef_[0])}
    else:
        coef, intercept = np.polyfit(x_arr, y_arr, 1)
        pred = intercept + coef * x_arr
        params = {"intercept": float(intercept), "coef": float(coef), "fallback": "numpy_polyfit"}
    return {
        "model_id": "LINEAR_REGRESSION_BASELINE",
        "model_family": "linear",
        "parameter_count": 2,
        "fitted_or_not": "FITTED_BASELINE",
        "leakage_risk": "MEDIUM",
        "parameters": params,
        "prediction": [float(v) for v in pred],
        "sklearn_available": sklearn_available(),
    }
