"""
Tests v1.5 — Detectability Classifier

Tests:
    test_detectability_no_threshold
    test_detectable_when_delta_exceeds_epsilon
    test_undetectable_when_delta_below_epsilon
    test_alpha_reasonableness_classification
    test_alpha_min_estimate_positive
    test_alpha_min_none_when_no_epsilon
"""

import math
import pytest

from phyng.candidates.detectability import (
    classify_detectability,
    classify_alpha_reasonableness,
    estimate_alpha_min_for_detectability,
)

B = 7.426160269118667e-38
GAMMA_ENV = 0.05
T_GRID = [i * 10.0 / 100 for i in range(101)]
EPSILON_EXP = 1e-6


def test_detectability_no_threshold():
    """When epsilon_exp is None, status must be NO_THRESHOLD_DECLARED."""
    status = classify_detectability(1.0, None)
    assert status == "NO_THRESHOLD_DECLARED"


def test_detectable_when_delta_exceeds_epsilon():
    """When max_abs_delta > epsilon_exp, must be DETECTABLE_SYNTHETIC_DELTA."""
    status = classify_detectability(1e-3, 1e-6)
    assert status == "DETECTABLE_SYNTHETIC_DELTA"


def test_undetectable_when_delta_below_epsilon():
    """When max_abs_delta <= epsilon_exp, must be UNDETECTABLE_SYNTHETIC_DELTA."""
    status = classify_detectability(1e-10, 1e-6)
    assert status == "UNDETECTABLE_SYNTHETIC_DELTA"


def test_undetectable_when_delta_equals_epsilon():
    """When max_abs_delta == epsilon_exp, must be UNDETECTABLE (boundary)."""
    status = classify_detectability(1e-6, 1e-6)
    assert status == "UNDETECTABLE_SYNTHETIC_DELTA"


def test_alpha_reasonableness_toy():
    assert classify_alpha_reasonableness(1.0) == "ALPHA_REASONABLE_TOY"
    assert classify_alpha_reasonableness(1e6) == "ALPHA_REASONABLE_TOY"


def test_alpha_reasonableness_large():
    assert classify_alpha_reasonableness(1e10) == "ALPHA_LARGE"
    assert classify_alpha_reasonableness(1e20) == "ALPHA_LARGE"


def test_alpha_reasonableness_extreme():
    assert classify_alpha_reasonableness(1e25) == "ALPHA_EXTREME"
    assert classify_alpha_reasonableness(1e35) == "ALPHA_EXTREME"


def test_alpha_reasonableness_unphysical():
    assert classify_alpha_reasonableness(1e36) == "ALPHA_UNPHYSICAL_OR_UNCONSTRAINED"
    assert classify_alpha_reasonableness(1e40) == "ALPHA_UNPHYSICAL_OR_UNCONSTRAINED"


def test_alpha_min_estimate_positive():
    """alpha_min estimate should be a positive finite number."""
    alpha_min = estimate_alpha_min_for_detectability(B, GAMMA_ENV, T_GRID, EPSILON_EXP)
    assert alpha_min is not None
    assert alpha_min > 0
    assert math.isfinite(alpha_min)


def test_alpha_min_none_when_no_epsilon():
    """When epsilon_exp is None, alpha_min must be None."""
    alpha_min = estimate_alpha_min_for_detectability(B, GAMMA_ENV, T_GRID, None)
    assert alpha_min is None


def test_alpha_min_none_when_b_is_zero():
    """When B = 0, denominator is zero, so alpha_min must be None."""
    alpha_min = estimate_alpha_min_for_detectability(0.0, GAMMA_ENV, T_GRID, EPSILON_EXP)
    assert alpha_min is None
