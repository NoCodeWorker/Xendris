from phyng.campaigns.phi_gradient_reviewed_local_manifest import run_phi_gradient_reviewed_local_manifest_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_phi_gradient_reviewed_local_manifest_campaign(tmp_path)
    campaign_report = (tmp_path / result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in campaign_report
    assert "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED" in campaign_report
    assert "Only validated extracts can walk through it." in campaign_report


def test_campaign_generates_reports(tmp_path):
    result = run_phi_gradient_reviewed_local_manifest_campaign(tmp_path)

    assert result.campaign_id == "PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1"
    assert len(result.report_paths) == 10
    assert all((tmp_path / path).exists() for path in result.report_paths.values())
