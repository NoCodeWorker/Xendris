from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.phi_search import generate_phi_search_loop_feedback, run_phi_candidate_search
from phyng.synthetic_benchmark_design.schemas import PhiCandidateRankingResult


def test_loop_feedback_blocks_physical_claim():
    _, ranking = run_phi_candidate_search(create_log_boundary_candidate_spec())
    feedback = generate_phi_search_loop_feedback(ranking)

    assert "physical claim authorization" in feedback.blocked_updates
    assert any("physical" in claim.lower() for claim in feedback.blocked_claims)


def test_no_survivor_downranks_log_boundary():
    ranking = PhiCandidateRankingResult(
        status="PHI_SEARCH_NO_SURVIVOR",
        canonical_status=normalize_status("PHI_SEARCH_NO_SURVIVOR", domain="phi_search"),
        ranked_candidates=[],
        survivor_count=0,
        best_candidate_family=None,
    )
    feedback = generate_phi_search_loop_feedback(ranking)

    assert "down-rank LOG_BOUNDARY family" in feedback.next_actions
    assert "reject/down-rank saturating or constant-control formulations" in feedback.allowed_updates
