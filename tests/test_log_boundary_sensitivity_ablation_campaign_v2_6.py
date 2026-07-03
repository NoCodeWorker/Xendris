from phyng.campaigns.log_boundary_sensitivity_ablation import run_log_boundary_sensitivity_ablation_campaign
from phyng.campaigns.log_boundary_synthetic_execution import run_log_boundary_synthetic_execution_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_log_boundary_sensitivity_ablation_campaign(tmp_path)

    assert result.campaign_id == "LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6"
    assert result.status == "LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT"
    assert set(result.report_paths) == {"controls", "metrics", "classification", "loop_feedback", "campaign"}


def test_existing_v2_5_behavior_preserved(tmp_path):
    result = run_log_boundary_synthetic_execution_campaign(tmp_path)

    assert result.status == "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"
    assert result.execution_result.sweep_result.sweep_count == 1728
    assert result.execution_result.sweep_result.best_point.max_abs_delta == 0.7152665915101674
