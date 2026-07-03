from phyng.campaigns.phi_gradient_real_literature_ingestion import run_phi_gradient_real_literature_ingestion_campaign
from phyng.campaigns.phi_gradient_source_benchmark_pressure import run_phi_gradient_source_benchmark_pressure_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_phi_gradient_real_literature_ingestion_campaign(tmp_path)

    assert result.campaign_id == "PHI-GRADIENT-REAL-LITERATURE-INGESTION-v2_9"
    assert result.status == "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    assert set(result.report_paths) == {"manifest", "extract_validation", "source_gate", "benchmark_records", "loop_feedback", "campaign"}


def test_existing_v2_8_behavior_preserved(tmp_path):
    result = run_phi_gradient_source_benchmark_pressure_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_BENCHMARK_DATA_FOUND"
    assert result.source_result.status == "PHI_GRADIENT_SOURCE_BACKED_LIMITED"
