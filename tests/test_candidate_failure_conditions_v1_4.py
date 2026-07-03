"""
Tests for phyng.candidates.failure_conditions
"""

from phyng.candidates.schemas import CandidatePredictionSpec
from phyng.candidates.failure_conditions import evaluate_candidate_failure_conditions

def test_candidate_without_benchmark_has_fail_no_benchmark():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="PRE_REGISTERED",
        source_ids=["SRC-001"],
        benchmark_ids=[],  # no benchmark
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B"
    )
    failures = evaluate_candidate_failure_conditions(spec)
    assert "FAIL_NO_BENCHMARK" in failures

def test_candidate_without_sources_has_fail_no_source_support():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="PRE_REGISTERED",
        source_ids=[],  # no sources
        benchmark_ids=["BENCH-001"],
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B"
    )
    failures = evaluate_candidate_failure_conditions(spec)
    assert "FAIL_NO_SOURCE_SUPPORT" in failures

def test_all_failures_triggered():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="FREE_UNCONSTRAINED",  # triggers FAIL_PARAMETER_UNDERIDENTIFIED
        source_ids=[],                          # triggers FAIL_NO_SOURCE_SUPPORT
        benchmark_ids=[],                        # triggers FAIL_NO_BENCHMARK
        term_units=None,                        # triggers FAIL_DIMENSIONAL_INVALID
        alpha_units=None,
        dimensionless_core=None,
        detectability_threshold=0.05
    )
    failures = evaluate_candidate_failure_conditions(
        spec, gain=-0.1, max_abs_delta=0.01
    )
    assert "FAIL_GAIN_NONPOSITIVE" in failures
    assert "FAIL_UNDETECTABLE_DELTA" in failures
    assert "FAIL_PARAMETER_UNDERIDENTIFIED" in failures
    assert "FAIL_DIMENSIONAL_INVALID" in failures
    assert "FAIL_NO_SOURCE_SUPPORT" in failures
    assert "FAIL_NO_BENCHMARK" in failures
