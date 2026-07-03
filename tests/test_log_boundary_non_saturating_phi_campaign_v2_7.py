from phyng.campaigns.log_boundary_non_saturating_phi_search import run_log_boundary_non_saturating_phi_search_campaign
from phyng.campaigns.log_boundary_sensitivity_ablation import run_log_boundary_sensitivity_ablation_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_log_boundary_non_saturating_phi_search_campaign(tmp_path)

    assert result.campaign_id == "LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7"
    assert result.status == "PHI_CANDIDATE_SURVIVES_CONTROLS"
    assert set(result.report_paths) == {"families", "control_resistance", "ranking", "loop_feedback", "campaign"}


def test_existing_v2_6_behavior_preserved(tmp_path):
    result = run_log_boundary_sensitivity_ablation_campaign(tmp_path)

    assert result.status == "LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT"
    assert result.ablation_result.metrics.candidate_delta == 0.7152665915101674
    assert result.ablation_result.metrics.control_gain == 0.0
