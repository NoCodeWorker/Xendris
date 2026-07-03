from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.phi_candidates import generate_phi_candidate_families
from phyng.synthetic_benchmark_design.phi_evaluation import classify_phi_candidate, evaluate_phi_candidate
from phyng.synthetic_benchmark_design.schemas import PhiControlResistanceMetrics


def test_saturating_candidate_is_rejected():
    metrics = PhiControlResistanceMetrics(
        candidate_delta=1.0,
        constant_phi_delta=1.0,
        mean_phi_delta=1.0,
        remove_u_delta=1.0,
        remove_w_delta=1.0,
        no_log_delta=1.0,
        alpha_1_delta=0.1,
        saturation_ratio=1.0,
        control_gain=0.0,
        coordinate_contribution_score=0.0,
        threshold_robustness_score=1.0,
        alpha_sensitivity_score=1.0,
        non_saturation_score=0.0,
        numerical_stability_score=1.0,
        control_resistance_score=0.0,
    )

    assert classify_phi_candidate(metrics) == "PHI_CANDIDATE_SATURATES"


def test_constant_control_match_blocks_candidate():
    metrics = PhiControlResistanceMetrics(
        candidate_delta=1.0,
        constant_phi_delta=1.0,
        mean_phi_delta=1.0,
        remove_u_delta=1.0,
        remove_w_delta=1.0,
        no_log_delta=1.0,
        alpha_1_delta=0.1,
        saturation_ratio=0.5,
        control_gain=0.0,
        coordinate_contribution_score=0.0,
        threshold_robustness_score=1.0,
        alpha_sensitivity_score=1.0,
        non_saturation_score=0.5,
        numerical_stability_score=1.0,
        control_resistance_score=0.0,
    )

    assert classify_phi_candidate(metrics) == "PHI_CANDIDATE_FAILS_CONSTANT_CONTROL"


def test_coordinate_contribution_required():
    candidate = next(item for item in generate_phi_candidate_families() if item.family == "PHI_COORDINATE_CONTRAST")
    result = evaluate_phi_candidate(create_log_boundary_candidate_spec(), candidate)

    assert result.classification == "PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION"
