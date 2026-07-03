from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec


def test_log_boundary_candidate_has_explicit_equation():
    spec = create_log_boundary_candidate_spec()

    assert spec.candidate_id == "HEUR-PHY-003"
    assert spec.candidate_family == "LOG_BOUNDARY"
    assert "V_base" in spec.baseline_equation
    assert "V_log" in spec.candidate_equation
    assert "DeltaGamma_log" in spec.delta_gamma_equation
    assert "phi_log" in spec.phi_function


def test_log_boundary_uses_dimensionless_variables():
    spec = create_log_boundary_candidate_spec()

    for variable in ("q", "b", "u", "w", "alpha", "k", "k2", "u0", "w0"):
        assert variable in spec.dimensionless_variables


def test_delta_gamma_log_has_rate_units_by_construction():
    spec = create_log_boundary_candidate_spec()

    assert "Gamma_env" in spec.delta_gamma_equation
    assert "alpha" in spec.delta_gamma_equation
    assert "phi_log" in spec.delta_gamma_equation
