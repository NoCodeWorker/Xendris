"""Numerical benchmark metrics."""

from __future__ import annotations

import numpy as np


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float))))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    diff = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)
    return float(np.sqrt(np.mean(diff * diff)))


def safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float | None:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if not np.any(mask):
        return None
    return float(np.mean(np.abs((y_pred[mask] - y_true[mask]) / y_true[mask])))


def max_abs_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float))))


def predictive_gain(error_base: float, error_candidate: float) -> float | None:
    if error_base == 0:
        return None
    return float((error_base - error_candidate) / error_base)


def residual_table(y_true: np.ndarray, y_pred: np.ndarray) -> list[dict]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return [
        {"index": int(i), "y_true": float(t), "y_pred": float(p), "residual": float(p - t)}
        for i, (t, p) in enumerate(zip(y_true, y_pred))
    ]
