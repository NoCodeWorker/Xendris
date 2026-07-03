from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.sensitivity import (
    generate_log_boundary_ablation_loop_feedback,
    run_log_boundary_sensitivity_ablation,
)


def test_loop_feedback_blocks_physical_claim():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    ablation = run_log_boundary_sensitivity_ablation(execution)
    feedback = generate_log_boundary_ablation_loop_feedback(ablation)

    assert "physical claim authorization" in feedback.blocked_updates
    assert any("physical" in claim.lower() for claim in feedback.blocked_claims)


def test_saturation_artifact_feedback_blocks_source_upgrade():
    execution = execute_log_boundary_synthetic_benchmark(create_log_boundary_candidate_spec())
    ablation = run_log_boundary_sensitivity_ablation(execution)
    feedback = generate_log_boundary_ablation_loop_feedback(ablation)

    assert "block source-pressure upgrade" in feedback.allowed_updates
    assert "search alternative non-saturating phi functions" in feedback.next_actions
