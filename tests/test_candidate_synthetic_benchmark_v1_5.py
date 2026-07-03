"""
Tests v1.5 — Candidate Synthetic Benchmark Core

Tests:
    test_v_base_and_candidate_shapes_match
    test_alpha_zero_or_tiny_produces_near_zero_delta
    test_default_b_suppressed_candidate_undetectable
    test_no_y_true_blocks_predictive_gain
    test_benchmark_result_has_required_fields
"""

import math
import pytest

from phyng.candidates.synthetic_benchmark import (
    CandidateSyntheticBenchmarkInput,
    run_synthetic_benchmark,
    compute_v_base,
    compute_v_candidate,
    compute_delta,
    compute_max_abs_delta,
)


# Default toy parameters from spec
B = 7.426160269118667e-38
GAMMA_ENV = 0.05
T_GRID = [i * 10.0 / 100 for i in range(101)]  # linspace(0, 10, 101)
EPSILON_EXP = 1e-6


def make_input(alpha: float = 1.0, y_true=None) -> CandidateSyntheticBenchmarkInput:
    return CandidateSyntheticBenchmarkInput(
        benchmark_id="BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001",
        candidate_id="CAND-FC-B-NEGCTRL-001",
        system_id="CAMPAIGN-002-MESOSCOPIC",
        m_kg=1e-17,
        L_value_m=1e-7,
        B=B,
        QB=2.612280302374279e-56,
        gamma_env=GAMMA_ENV,
        alpha=alpha,
        t_grid=T_GRID,
        epsilon_exp=EPSILON_EXP,
        y_true=y_true,
        error_metric="MAE",
        benchmark_provenance="SYNTHETIC",
    )


def test_v_base_and_candidate_shapes_match():
    """V_base and V_candidate must have the same length as t_grid."""
    v_base = compute_v_base(GAMMA_ENV, T_GRID)
    v_cand = compute_v_candidate(GAMMA_ENV, 0.0, T_GRID)
    assert len(v_base) == len(T_GRID)
    assert len(v_cand) == len(T_GRID)


def test_alpha_zero_or_tiny_produces_near_zero_delta():
    """With alpha ~ 0, delta(t) ≈ 0 everywhere."""
    v_base = compute_v_base(GAMMA_ENV, T_GRID)
    delta_gamma_c = 0.0 * B
    v_cand = compute_v_candidate(GAMMA_ENV, delta_gamma_c, T_GRID)
    delta = compute_delta(v_cand, v_base)
    max_d = compute_max_abs_delta(delta)
    assert max_d < 1e-15


def test_default_b_suppressed_candidate_undetectable():
    """With default alpha=1 and B~7e-38, the candidate is undetectable."""
    inp = make_input(alpha=1.0)
    result = run_synthetic_benchmark(inp)
    assert result.detectability_status == "UNDETECTABLE_SYNTHETIC_DELTA"
    assert result.max_abs_delta < EPSILON_EXP


def test_no_y_true_blocks_predictive_gain():
    """Without y_true, synthetic_gain_status must be NOT_COMPUTABLE_WITHOUT_Y_TRUE."""
    inp = make_input(alpha=1.0, y_true=None)
    result = run_synthetic_benchmark(inp)
    assert result.synthetic_gain_status == "NOT_COMPUTABLE_WITHOUT_Y_TRUE"


def test_no_sources_blocks_physical_interpretation():
    """FAIL_NO_SOURCE_SUPPORT must appear in triggered failures (always for SYNTHETIC benchmark)."""
    inp = make_input(alpha=1.0)
    result = run_synthetic_benchmark(inp)
    assert "FAIL_NO_SOURCE_SUPPORT" in result.triggered_failure_conditions


def test_benchmark_result_has_required_fields():
    """All required output fields must be present and non-None."""
    inp = make_input(alpha=1.0)
    result = run_synthetic_benchmark(inp)
    assert result.benchmark_id == "BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001"
    assert result.candidate_id == "CAND-FC-B-NEGCTRL-001"
    assert isinstance(result.v_base, list)
    assert isinstance(result.v_candidate, list)
    assert isinstance(result.delta, list)
    assert isinstance(result.max_abs_delta, float)
    assert isinstance(result.detectability_status, str)
    assert isinstance(result.synthetic_gain_status, str)
    assert isinstance(result.triggered_failure_conditions, list)
    assert isinstance(result.allowed_claims, list)
    assert isinstance(result.blocked_claims, list)


def test_v_base_starts_at_one():
    """V_base(0) = exp(0) = 1.0."""
    v_base = compute_v_base(GAMMA_ENV, T_GRID)
    assert abs(v_base[0] - 1.0) < 1e-14


def test_v_base_decays_monotonically():
    """V_base(t) must be monotonically decreasing for gamma_env > 0."""
    v_base = compute_v_base(GAMMA_ENV, T_GRID)
    for i in range(1, len(v_base)):
        assert v_base[i] <= v_base[i - 1]
