from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.sensitivity import run_log_boundary_sensitivity_ablation


def _ablation():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    return run_log_boundary_sensitivity_ablation(execution)


def test_phi_saturation_warning_detected():
    result = _ablation()

    assert "WARN_PHI_SATURATION" in result.metrics.warnings


def test_control_gain_computed():
    result = _ablation()

    assert result.metrics.control_gain == 0.0


def test_coordinate_contribution_score_computed():
    result = _ablation()

    assert result.metrics.coordinate_contribution_score >= 0.0
