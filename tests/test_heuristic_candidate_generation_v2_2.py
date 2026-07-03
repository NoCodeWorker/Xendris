from phyng.heuristic_discovery.generator import generate_heuristic_candidates


def test_physical_generator_includes_log_boundary_candidate():
    candidates = generate_heuristic_candidates("Boundary behavior", "physical_candidate")
    families = {candidate.candidate_family for candidate in candidates}

    assert "LOG_BOUNDARY" in families
    assert "B_SUPPRESSED" in families
    assert all(candidate.canonical_status.domain_status == "HEURISTIC_SEED" for candidate in candidates)


def test_business_generator_includes_wtp_candidate():
    candidates = generate_heuristic_candidates("Deeptech diligence product", "business_hypothesis")
    families = {candidate.candidate_family for candidate in candidates}

    assert "WTP_HYPOTHESIS" in families
