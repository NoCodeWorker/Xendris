from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.phi_search import run_phi_candidate_search


def test_surviving_candidate_keeps_physical_claim_blocked():
    record = normalize_status("PHI_CANDIDATE_SURVIVES_CONTROLS", domain="phi_search")

    assert record.canonical_permission.value == "CLAIM_LIMITED_ALLOWED"
    assert record.evidence_level.value == "SYNTHETIC_ONLY"
    assert "Physical prediction" in record.blocked_uses


def test_ranking_is_not_evidence():
    _, ranking = run_phi_candidate_search(create_log_boundary_candidate_spec())

    assert "not evidence" in ranking.ranking_note
    assert ranking.survivor_count >= 1
    assert ranking.best_candidate_family in {
        result.candidate.family for result in ranking.ranked_candidates if result.classification == "PHI_CANDIDATE_SURVIVES_CONTROLS"
    }
