from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_reports_include_canonical_section(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_exact_extract_review_campaign(tmp_path)
    campaign_report = (tmp_path / result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in campaign_report
    assert "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW" in campaign_report
    assert "Exactness is the price" in campaign_report


def test_campaign_generates_reports(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_exact_extract_review_campaign(tmp_path)

    assert len(result.report_paths) == 7
    assert all((tmp_path / path).exists() for path in result.report_paths.values())
