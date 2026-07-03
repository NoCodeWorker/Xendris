from phyng.campaigns.phi_gradient_real_source_acquisition import run_phi_gradient_real_source_acquisition_campaign


def test_reports_include_backend_status(tmp_path):
    result = run_phi_gradient_real_source_acquisition_campaign(tmp_path)
    gate_report = (tmp_path / result.report_paths["real_source_gate"]).read_text(encoding="utf-8")

    assert "backend_status" in gate_report
    assert "NOOP_SOURCE_ACQUISITION_BACKEND" in gate_report
    assert "actual_real_sources_acquired" in gate_report


def test_reports_include_canonical_section(tmp_path):
    result = run_phi_gradient_real_source_acquisition_campaign(tmp_path)
    campaign_report = (tmp_path / result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in campaign_report
    assert "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING" in campaign_report
    assert "A query plan is a map." in campaign_report


def test_physical_claims_remain_blocked(tmp_path):
    result = run_phi_gradient_real_source_acquisition_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.acquisition_result.blocked_claims
    assert "PHI_GRADIENT validates Frontera C." in result.acquisition_result.blocked_claims
