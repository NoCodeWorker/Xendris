from phyng.core.evidence_levels import CanonicalEvidenceLevel
from phyng.heuristic_discovery.generator import generate_heuristic_candidates
from phyng.heuristic_discovery.prioritizer import rank_heuristic_candidates


def test_b_suppressed_downranked_after_negative_control():
    candidates = generate_heuristic_candidates("Mesoscopic visibility decay", "physical_candidate")
    ranking = rank_heuristic_candidates(candidates)
    ranked_families = [candidate.candidate_family for candidate in ranking.candidates]

    assert ranked_families.index("B_SUPPRESSED") > ranked_families.index("LOG_BOUNDARY")


def test_priority_score_is_not_evidence():
    candidates = generate_heuristic_candidates("Mesoscopic visibility decay", "physical_candidate")
    ranking = rank_heuristic_candidates(candidates)

    assert ranking.canonical_status.evidence_level == CanonicalEvidenceLevel.HEURISTIC_ONLY
    assert "not evidence" in ranking.warnings[0]
    assert all("priority_score" in candidate.heuristic_scores for candidate in ranking.candidates)
