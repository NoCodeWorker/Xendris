from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.sensitivity import run_log_boundary_sensitivity_ablation


def test_saturation_artifact_blocks_source_pressure_upgrade():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    result = run_log_boundary_sensitivity_ablation(execution)

    assert result.classification.status == "LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT"
    assert result.classification.canonical_status.canonical_permission.value == "CLAIM_BLOCKED"


def test_survives_ablation_keeps_physical_claim_blocked():
    record = normalize_status("LOG_BOUNDARY_SURVIVES_ABLATION", domain="synthetic_benchmark_ablation")

    assert record.canonical_permission.value == "CLAIM_LIMITED_ALLOWED"
    assert record.evidence_level.value == "SYNTHETIC_ONLY"
    assert "Physical prediction" in record.blocked_uses
