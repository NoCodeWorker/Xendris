from phyng.synthetic_benchmark_design.phi_candidates import generate_phi_candidate_families


def test_phi_candidate_families_exist():
    families = {candidate.family for candidate in generate_phi_candidate_families()}

    assert families == {
        "PHI_CENTERED",
        "PHI_GRADIENT",
        "PHI_BANDPASS",
        "PHI_CURVATURE",
        "PHI_RELATIVE_BOUNDARY",
        "PHI_NON_SATURATING_RATIO",
        "PHI_COORDINATE_CONTRAST",
        "PHI_LOCALIZED_WINDOW",
    }


def test_phi_candidates_are_bounded_or_flagged():
    for candidate in generate_phi_candidate_families():
        assert candidate.boundedness_claim
        assert "bounded" in candidate.boundedness_claim.lower()


def test_phi_candidates_use_dimensionless_inputs():
    for candidate in generate_phi_candidate_families():
        assert candidate.dimensionless_inputs
        assert set(candidate.dimensionless_inputs).issubset({"q", "b", "u", "w", "u0", "w0"})
