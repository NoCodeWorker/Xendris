from phyng.campaigns.phi_gradient_real_literature_ingestion import (
    run_phi_gradient_real_literature_ingestion_campaign,
)
from phyng.campaigns.phi_gradient_real_source_acquisition import (
    run_phi_gradient_real_source_acquisition_campaign,
)


def test_campaign_generates_reports(tmp_path):
    result = run_phi_gradient_real_source_acquisition_campaign(tmp_path)

    assert result.campaign_id == "PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0"
    assert result.status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING"
    assert len(result.report_paths) == 9
    assert all((tmp_path / path).exists() for path in result.report_paths.values())


def test_existing_v2_9_behavior_preserved(tmp_path):
    result = run_phi_gradient_real_literature_ingestion_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    assert result.gate_result.actual_real_sources_ingested is False
