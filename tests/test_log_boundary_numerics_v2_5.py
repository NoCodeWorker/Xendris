import math

from phyng.synthetic_benchmark_design.numerics import (
    compute_boundary_coordinates,
    compute_max_abs_delta,
    compute_phi_log,
    compute_visibility_curves,
)


def test_boundary_coordinates_are_finite():
    coordinates = compute_boundary_coordinates(m_kg=1e-17, L_m=1e-7)

    for value in coordinates.model_dump().values():
        assert math.isfinite(value)


def test_phi_log_is_bounded():
    phi = compute_phi_log(u=-64.0, w=-21.0, k=5.0, k2=5.0, u0=-70.0, w0=-20.0)

    assert 0.0 <= phi <= 1.0


def test_visibility_curves_have_matching_lengths():
    t_grid = [i * 0.1 for i in range(101)]
    curves = compute_visibility_curves(t_grid, Gamma_env=0.1, alpha=1.0, phi_log=0.5)

    assert len(curves.t_grid) == len(curves.V_base) == len(curves.V_log) == len(curves.delta)
    assert all(0.0 <= value <= 1.0 for value in curves.V_base)
    assert all(0.0 <= value <= 1.0 for value in curves.V_log)


def test_max_abs_delta_non_negative():
    value = compute_max_abs_delta([1.0, 0.9, 0.8], [1.0, 0.85, 0.7])

    assert value >= 0.0
