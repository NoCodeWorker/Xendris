from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.loop_feedback import generate_log_boundary_loop_feedback


def test_loop_feedback_blocks_physical_claim():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    feedback = generate_log_boundary_loop_feedback(execution)

    assert "claim gate relaxation" in feedback.blocked_updates
    assert any("physical" in claim.lower() for claim in feedback.blocked_claims)


def test_loop_feedback_generates_next_actions():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    feedback = generate_log_boundary_loop_feedback(execution)

    assert feedback.update_proposals
    assert feedback.next_actions
    assert any("source" in action.lower() for action in feedback.next_actions)
