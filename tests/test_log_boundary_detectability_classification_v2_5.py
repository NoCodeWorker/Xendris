from copy import deepcopy

from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.execution import classify_execution_status, execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.schemas import LogBoundarySweepPoint
from phyng.synthetic_benchmark_design.sweep import classify_parameter_reasonableness, run_log_boundary_sweep


def test_detectability_classification_uses_epsilon():
    sweep = run_log_boundary_sweep(create_log_boundary_candidate_spec())
    sweep.best_point = sweep.best_point.model_copy(update={"max_abs_delta": sweep.epsilon_exp})

    assert classify_execution_status(sweep) == "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA"


def test_undetectable_maps_to_claim_blocked():
    record = normalize_status("LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA", domain="synthetic_benchmark_execution")

    assert record.canonical_permission.value == "CLAIM_BLOCKED"
    assert "UNDETECTABLE_DELTA" in {reason.value for reason in record.blocked_reasons}


def test_detectable_synthetic_does_not_authorize_physical_claim():
    result = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())

    assert result.status == "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"
    assert result.canonical_status.evidence_level.value == "SYNTHETIC_ONLY"
    assert any("physical" in claim.lower() for claim in result.blocked_claims)
    assert "Experimental validation" not in result.allowed_claims


def test_extreme_parameters_block_claim():
    sweep = run_log_boundary_sweep(create_log_boundary_candidate_spec())
    assert sweep.best_point is not None
    extreme_best = sweep.best_point.model_copy(
        update={"parameter_reasonableness": classify_parameter_reasonableness(in_declared_sweep=False, extreme=True)}
    )
    sweep = deepcopy(sweep)
    sweep.best_point = LogBoundarySweepPoint.model_validate(extreme_best)

    assert classify_execution_status(sweep) == "LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS"
