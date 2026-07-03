from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.sweep import run_log_boundary_sweep


def test_default_sweep_has_expected_count():
    sweep = run_log_boundary_sweep(create_log_boundary_candidate_spec())

    assert sweep.sweep_count == 1728
    assert len(sweep.points) == 1728


def test_sweep_finds_best_point():
    sweep = run_log_boundary_sweep(create_log_boundary_candidate_spec())

    assert sweep.best_point is not None
    assert sweep.best_point.max_abs_delta == max(point.max_abs_delta for point in sweep.points)
    assert sweep.best_point.parameter_reasonableness.classification == "PARAMETERS_DECLARED_TOY_RANGE"
