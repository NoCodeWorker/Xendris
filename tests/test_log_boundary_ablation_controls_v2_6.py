from phyng.synthetic_benchmark_design.ablation import (
    run_alpha_sensitivity,
    run_constant_phi_one_control,
    run_no_log_coordinates_control,
    run_remove_u_control,
    run_remove_w_control,
)
from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec


def _execution():
    return execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())


def test_constant_phi_one_control_exists():
    control = run_constant_phi_one_control(_execution())

    assert control.control_id == "CONTROL_CONSTANT_PHI_ONE"
    assert control.max_abs_delta >= 0.0


def test_alpha_one_sensitivity_runs():
    control = run_alpha_sensitivity(_execution())

    assert control.control_id == "CONTROL_ALPHA_ONE"
    assert control.max_abs_delta >= 0.0


def test_remove_u_control_runs():
    control = run_remove_u_control(_execution())

    assert control.control_id == "CONTROL_REMOVE_U"
    assert 0.0 <= control.phi_value <= 1.0


def test_remove_w_control_runs():
    control = run_remove_w_control(_execution())

    assert control.control_id == "CONTROL_REMOVE_W"
    assert 0.0 <= control.phi_value <= 1.0


def test_no_log_coordinates_control_runs():
    control = run_no_log_coordinates_control(_execution())

    assert control.control_id == "CONTROL_NO_LOG_COORDINATES"
    assert control.phi_value == 0.5
