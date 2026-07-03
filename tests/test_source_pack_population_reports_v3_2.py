from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_phi_gradient_source_pack_population_campaign(tmp_path)
    campaign_report = (tmp_path / result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in campaign_report
    assert "PHI_GRADIENT_SOURCE_PACK_POPULATED" in campaign_report
    assert "organized pressure waiting to happen" in campaign_report


def test_campaign_generates_reports(tmp_path):
    result = run_phi_gradient_source_pack_population_campaign(tmp_path)

    assert len(result.report_paths) == 6
    assert all((tmp_path / path).exists() for path in result.report_paths.values())
