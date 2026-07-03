import numpy as np

from phyng.benchmarking.metrics import mae, max_abs_error, predictive_gain, rmse, safe_mape


def test_benchmarking_stack_metrics_are_consistent():
    y_true = np.array([1.0, 0.0])
    y_pred = np.array([0.5, 0.25])

    assert mae(y_true, y_pred) == 0.375
    assert round(rmse(y_true, y_pred), 6) == 0.395285
    assert safe_mape(y_true, y_pred) == 0.5
    assert max_abs_error(y_true, y_pred) == 0.5
    assert predictive_gain(2.0, 1.0) == 0.5
