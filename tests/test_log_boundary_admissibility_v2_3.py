from phyng.synthetic_benchmark_design.admissibility import check_log_boundary_admissibility
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec


def test_missing_observable_blocks_admissibility():
    spec = create_log_boundary_candidate_spec(observable="")
    result = check_log_boundary_admissibility(spec)

    assert result.is_admissible is False
    assert "FAIL_NO_OBSERVABLE" in result.blocked_reasons


def test_missing_failure_condition_blocks_admissibility():
    spec = create_log_boundary_candidate_spec()
    spec.failure_conditions.clear()
    result = check_log_boundary_admissibility(spec)

    assert result.is_admissible is False
    assert "FAIL_NO_FAILURE_CONDITION" in result.blocked_reasons


def test_ad_hoc_scale_blocks_admissibility():
    spec = create_log_boundary_candidate_spec()
    spec.scale_L_post_hoc = True
    result = check_log_boundary_admissibility(spec)

    assert result.is_admissible is False
    assert "FAIL_AD_HOC_SCALE" in result.blocked_reasons
