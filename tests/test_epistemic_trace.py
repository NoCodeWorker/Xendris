"""
Tests for epistemic trace τ_O(H).
"""

import numpy as np
import pytest

from phyng.epistemic_trace import (
    jensen_shannon_divergence,
    kl_divergence,
    normalize_distribution,
    epistemic_trace,
)


def test_normalize_distribution():
    p = np.array([2.0, 3.0, 5.0])
    result = normalize_distribution(p)
    assert np.isclose(result.sum(), 1.0)


def test_normalize_rejects_negative():
    with pytest.raises(ValueError):
        normalize_distribution(np.array([1.0, -1.0]))


def test_normalize_rejects_zero_sum():
    with pytest.raises(ValueError):
        normalize_distribution(np.array([0.0, 0.0]))


def test_js_zero_for_equal_distributions():
    p = np.array([0.5, 0.5])
    q = np.array([0.5, 0.5])
    jsd = jensen_shannon_divergence(p, q)
    assert np.isclose(jsd, 0.0, atol=1e-10)


def test_js_positive_for_different_distributions():
    p = np.array([0.9, 0.1])
    q = np.array([0.1, 0.9])
    jsd = jensen_shannon_divergence(p, q)
    assert jsd > 0


def test_js_bounded():
    """JSD is bounded by ln(2) ≈ 0.693."""
    p = np.array([1.0, 0.0])
    q = np.array([0.0, 1.0])
    jsd = jensen_shannon_divergence(p, q)
    assert jsd <= np.log(2) + 1e-10


def test_epistemic_trace_null():
    p = np.array([0.5, 0.5])
    result = epistemic_trace(p, p)
    assert result["trace_type"] == "NULL_TRACE"
    assert result["operational_status"] == "EMPTY"


def test_epistemic_trace_detectable():
    p_h = np.array([0.9, 0.1])
    p_not_h = np.array([0.1, 0.9])
    result = epistemic_trace(p_h, p_not_h, epsilon_exp=1e-6)
    assert result["trace_type"] == "DETECTABLE_TRACE"
    assert result["tau"] > 1e-6
