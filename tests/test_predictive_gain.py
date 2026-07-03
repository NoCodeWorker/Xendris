"""
Tests for predictive gain.
"""

import pytest

from phyng.predictive_gain import predictive_gain


def test_predictive_gain_positive():
    result = predictive_gain(error_base=10.0, error_model=7.5)
    assert result["gain"] == 0.25
    assert result["status"] == "POSITIVE_GAIN"


def test_predictive_gain_zero():
    result = predictive_gain(error_base=10.0, error_model=10.0)
    assert result["gain"] == 0.0
    assert result["status"] == "ZERO_GAIN"


def test_predictive_gain_negative():
    result = predictive_gain(error_base=10.0, error_model=12.0)
    assert result["gain"] < 0
    assert result["status"] == "NEGATIVE_GAIN"


def test_predictive_gain_perfect():
    result = predictive_gain(error_base=10.0, error_model=0.0)
    assert result["gain"] == 1.0
    assert result["status"] == "POSITIVE_GAIN"


def test_predictive_gain_rejects_zero_base():
    with pytest.raises(ValueError):
        predictive_gain(error_base=0.0, error_model=5.0)


def test_predictive_gain_rejects_negative_model():
    with pytest.raises(ValueError):
        predictive_gain(error_base=10.0, error_model=-1.0)
