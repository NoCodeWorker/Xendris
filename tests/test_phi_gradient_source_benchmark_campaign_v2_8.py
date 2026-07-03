from phyng.campaigns.log_boundary_non_saturating_phi_search import run_log_boundary_non_saturating_phi_search_campaign
from phyng.campaigns.phi_gradient_source_benchmark_pressure import run_phi_gradient_source_benchmark_pressure_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_phi_gradient_source_benchmark_pressure_campaign(tmp_path)

    assert result.campaign_id == "PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8"
    assert result.status == "PHI_GRADIENT_BENCHMARK_DATA_FOUND"
    assert set(result.report_paths) == {"slots", "source_gate", "benchmark", "negative_sources", "loop_feedback", "campaign"}


def test_existing_v2_7_behavior_preserved(tmp_path):
    result = run_log_boundary_non_saturating_phi_search_campaign(tmp_path)

    assert result.status == "PHI_CANDIDATE_SURVIVES_CONTROLS"
    assert result.ranking.best_candidate_family == "PHI_GRADIENT"
