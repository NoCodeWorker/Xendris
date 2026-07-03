"""
Tests v1.5 — Alpha Sweep

Tests:
    test_alpha_sweep_contains_expected_values
    test_unphysical_alpha_classification
    test_alpha_sweep_length_matches_input
    test_default_b_suppressed_all_undetectable_in_low_alpha
    test_find_first_detectable_alpha_returns_none_when_all_undetectable
"""

import pytest

from phyng.candidates.alpha_sweep import (
    run_alpha_sweep,
    find_first_detectable_alpha,
    DEFAULT_ALPHA_VALUES,
)

B = 7.426160269118667e-38
GAMMA_ENV = 0.05
T_GRID = [i * 10.0 / 100 for i in range(101)]
EPSILON_EXP = 1e-6


def test_alpha_sweep_contains_expected_values():
    """Alpha sweep must include all DEFAULT_ALPHA_VALUES entries."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP)
    alphas = [row.alpha for row in rows]
    for expected_alpha in DEFAULT_ALPHA_VALUES:
        assert expected_alpha in alphas


def test_alpha_sweep_length_matches_input():
    """Sweep must return one row per alpha value."""
    custom_alphas = [1.0, 1e10, 1e20]
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP, alpha_values=custom_alphas)
    assert len(rows) == 3


def test_unphysical_alpha_classification():
    """Alpha > 1e35 must be classified as ALPHA_UNPHYSICAL_OR_UNCONSTRAINED."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP, alpha_values=[1e38, 1e40])
    for row in rows:
        assert row.alpha_reasonableness_status == "ALPHA_UNPHYSICAL_OR_UNCONSTRAINED"


def test_requires_unphysical_alpha_in_failures():
    """REQUIRES_UNPHYSICAL_ALPHA must be triggered for alpha > 1e35."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP, alpha_values=[1e40])
    row = rows[0]
    assert "REQUIRES_UNPHYSICAL_ALPHA" in row.triggered_failures


def test_alpha_sweep_no_threshold_returns_no_threshold_declared():
    """When epsilon_exp is None, all rows must have NO_THRESHOLD_DECLARED."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, epsilon_exp=None)
    for row in rows:
        assert row.detectability_status == "NO_THRESHOLD_DECLARED"


def test_alpha_row_has_delta_gamma_c():
    """Each row must have delta_gamma_c = alpha * B."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP, alpha_values=[1.0, 1e10])
    assert abs(rows[0].delta_gamma_c - 1.0 * B) < 1e-50
    assert abs(rows[1].delta_gamma_c - 1e10 * B) < 1e-25


def test_find_first_detectable_alpha_returns_none_when_all_undetectable():
    """For tiny alpha values that are all undetectable, must return None."""
    rows = run_alpha_sweep(B, GAMMA_ENV, T_GRID, EPSILON_EXP, alpha_values=[1.0, 1e5])
    result = find_first_detectable_alpha(rows)
    assert result is None
