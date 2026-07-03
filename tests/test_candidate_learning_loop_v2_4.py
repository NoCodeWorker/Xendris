from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput


def _input():
    return CandidateLoopInput(
        loop_id="LOOP-TEST-001",
        input_type="SYNTHETIC_BENCHMARK_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="LOG_BOUNDARY",
        previous_status="HEURISTIC_TEST_DESIGN_READY",
        result_status="SYNTHETIC_BENCHMARK_DESIGNED",
    )


def test_candidate_loop_accepts_synthetic_benchmark_designed():
    result = run_candidate_learning_loop(_input())

    assert result.candidate_id == "HEUR-PHY-003"
    assert result.new_status == "LOOP_UPDATE_PROPOSED"
    assert result.update_proposals


def test_candidate_loop_never_authorizes_physical_claim():
    result = run_candidate_learning_loop(_input())

    assert "authorize physical claim" in result.blocked_claims
    assert all("authorize physical claim" in proposal.forbidden_actions for proposal in result.update_proposals)


def test_candidate_loop_proposes_next_actions():
    result = run_candidate_learning_loop(_input())

    assert "execute synthetic benchmark" in result.next_actions
    assert "source search pressure" in result.next_actions
    assert result.audit_event_id
