from phyng.campaigns.closed_loop_meta_improvement import run_closed_loop_meta_improvement_campaign
from phyng.campaigns.log_boundary_synthetic_execution import run_log_boundary_synthetic_execution_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_log_boundary_synthetic_execution_campaign(tmp_path)

    assert result.campaign_id == "LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5"
    assert result.status == "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"
    assert result.execution_result.sweep_result.sweep_count == 1728
    assert set(result.report_paths) == {"sweep", "detectability", "failure_conditions", "loop_feedback", "campaign"}


def test_existing_v2_4_behavior_preserved(tmp_path):
    result = run_closed_loop_meta_improvement_campaign(tmp_path)

    assert result.status == "META_CHANGE_APPROVED_LOW_RISK"
    assert result.candidate_loop_result.new_status == "LOOP_UPDATE_PROPOSED"
