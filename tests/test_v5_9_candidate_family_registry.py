from phyng.candidates.family_registry import build_candidate_family_registry


def test_log_boundary_not_reactivated():
    families = build_candidate_family_registry()

    assert all(family.candidate_family_id != "LOG_BOUNDARY" for family in families)
    assert len(families) >= 10


def test_candidate_requires_baseline_comparator():
    families = build_candidate_family_registry()
    active = [family for family in families if family.candidate_type == "C_STRUCTURE_CANDIDATE"]

    assert active
    assert all(family.can_compare_to_baseline for family in active)
