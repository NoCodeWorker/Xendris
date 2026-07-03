from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.campaigns.phi_gradient_source_pack_validation import run_phi_gradient_source_pack_validation_campaign


def test_reports_include_canonical_section(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_source_pack_validation_campaign(tmp_path)
    campaign_report = (tmp_path / result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in campaign_report
    assert "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED" in campaign_report
    assert "candidate source becomes evidence pressure only when its extract survives" in campaign_report


def test_campaign_generates_reports(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_source_pack_validation_campaign(tmp_path)

    assert len(result.report_paths) == 8
    assert all((tmp_path / path).exists() for path in result.report_paths.values())
