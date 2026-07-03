"""
Tests v1.5 — Failure Report and Candidate Survival

Tests:
    test_fail_undetectable_delta_triggered
    test_fail_no_benchmark_when_y_true_none
    test_fail_no_source_support_always_present_in_synthetic
    test_requires_unphysical_alpha_when_alpha_min_extreme
    test_survival_as_toy_negative_control
    test_survival_fails_parameter_reasonableness
"""

import pytest

from phyng.candidates.failure_report_v1_5 import (
    evaluate_v1_5_failure_conditions,
    classify_candidate_survival,
)


def test_fail_undetectable_delta_triggered():
    """FAIL_UNDETECTABLE_DELTA must be in failures when delta is undetectable."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-50,
        epsilon_exp=1e-6,
        y_true=None,
        alpha_min=1e38,
        detectability_status="UNDETECTABLE_SYNTHETIC_DELTA",
    )
    assert "FAIL_UNDETECTABLE_DELTA" in failures


def test_fail_no_benchmark_when_y_true_none():
    """FAIL_NO_BENCHMARK must be triggered when y_true is None."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-50,
        epsilon_exp=1e-6,
        y_true=None,
        alpha_min=None,
        detectability_status="UNDETECTABLE_SYNTHETIC_DELTA",
    )
    assert "FAIL_NO_BENCHMARK" in failures


def test_fail_no_benchmark_absent_when_y_true_present():
    """FAIL_NO_BENCHMARK must NOT be triggered when y_true is provided."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-50,
        epsilon_exp=1e-6,
        y_true=[0.5, 0.4, 0.3],
        alpha_min=None,
        detectability_status="UNDETECTABLE_SYNTHETIC_DELTA",
    )
    assert "FAIL_NO_BENCHMARK" not in failures


def test_fail_no_source_support_always_present_in_synthetic():
    """FAIL_NO_SOURCE_SUPPORT is always triggered in the synthetic benchmark context."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-3,
        epsilon_exp=1e-6,
        y_true=[0.5, 0.4],
        alpha_min=1.0,
        detectability_status="DETECTABLE_SYNTHETIC_DELTA",
    )
    assert "FAIL_NO_SOURCE_SUPPORT" in failures


def test_requires_unphysical_alpha_when_alpha_min_extreme():
    """REQUIRES_UNPHYSICAL_ALPHA triggered when alpha_min > 1e35."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-50,
        epsilon_exp=1e-6,
        y_true=None,
        alpha_min=1e36,
        detectability_status="UNDETECTABLE_SYNTHETIC_DELTA",
    )
    assert "REQUIRES_UNPHYSICAL_ALPHA" in failures


def test_requires_unphysical_alpha_absent_when_alpha_min_reasonable():
    """REQUIRES_UNPHYSICAL_ALPHA must NOT be triggered for small alpha_min."""
    failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=1e-50,
        epsilon_exp=1e-6,
        y_true=None,
        alpha_min=1e5,
        detectability_status="UNDETECTABLE_SYNTHETIC_DELTA",
    )
    assert "REQUIRES_UNPHYSICAL_ALPHA" not in failures


def test_survival_as_toy_negative_control():
    """B-suppressed undetectable candidate with no sources → SURVIVES_AS_TOY_NEGATIVE_CONTROL."""
    failures = ["FAIL_UNDETECTABLE_DELTA", "FAIL_NO_BENCHMARK", "FAIL_NO_SOURCE_SUPPORT"]
    status = classify_candidate_survival(failures)
    assert status == "SURVIVES_AS_TOY_NEGATIVE_CONTROL"


def test_survival_fails_parameter_reasonableness():
    """Unphysical alpha requirement → FAILS_PARAMETER_REASONABLENESS."""
    failures = ["REQUIRES_UNPHYSICAL_ALPHA", "FAIL_NO_SOURCE_SUPPORT"]
    status = classify_candidate_survival(failures)
    assert status == "FAILS_PARAMETER_REASONABLENESS"


def test_survival_blocked_physical_interpretation():
    """Source failure alone → BLOCKED_PHYSICAL_INTERPRETATION."""
    failures = ["FAIL_NO_SOURCE_SUPPORT"]
    status = classify_candidate_survival(failures)
    assert status == "BLOCKED_PHYSICAL_INTERPRETATION"
