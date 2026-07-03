from phyng.core.permissions import CanonicalPermission
from phyng.synthetic_benchmark_design.log_boundary import (
    create_log_boundary_candidate_spec,
    design_synthetic_benchmark,
)


def test_synthetic_benchmark_design_has_delta_metric():
    result = design_synthetic_benchmark(create_log_boundary_candidate_spec())

    assert result.benchmark_design is not None
    assert "max_abs_delta" in result.benchmark_design.delta_metric


def test_synthetic_benchmark_design_permission_is_test_design_allowed():
    result = design_synthetic_benchmark(create_log_boundary_candidate_spec())

    assert result.status == "SYNTHETIC_BENCHMARK_DESIGNED"
    assert result.canonical_status.canonical_permission == CanonicalPermission.TEST_DESIGN_ALLOWED


def test_synthetic_benchmark_does_not_authorize_physical_claim():
    result = design_synthetic_benchmark(create_log_boundary_candidate_spec())

    blocked = " ".join(result.blocked_claims)
    assert "Physical prediction" in blocked
    assert "Experimental validation" in blocked
    assert "Source-backed claim" in blocked
