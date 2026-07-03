import pytest

from phyng.model_comparison.metrics import (
    compute_predictive_gain,
    mae,
    mse,
    rmse,
)


def test_mse():
    assert mse([1.0, 2.0, 3.0], [1.0, 1.0, 5.0]) == pytest.approx(5.0 / 3.0)


def test_mae():
    assert mae([1.0, 2.0, 3.0], [1.0, 1.0, 5.0]) == pytest.approx(1.0)


def test_rmse():
    assert rmse([1.0, 2.0, 3.0], [1.0, 1.0, 5.0]) == pytest.approx((5.0 / 3.0) ** 0.5)


def test_gain_positive_when_candidate_better():
    assert compute_predictive_gain(4.0, 1.0) == pytest.approx(0.75)
