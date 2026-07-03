from pathlib import Path

from phyng.campaigns.phi_gradient_source_benchmark_pressure import run_phi_gradient_source_benchmark_pressure_campaign


def test_phi_gradient_physical_claims_remain_blocked(tmp_path):
    result = run_phi_gradient_source_benchmark_pressure_campaign(tmp_path)

    assert any("physically validated" in claim for claim in result.source_result.blocked_claims)
    assert result.source_result.canonical_status.canonical_permission.value == "CLAIM_LIMITED_ALLOWED"


def test_reports_include_canonical_section(tmp_path):
    result = run_phi_gradient_source_benchmark_pressure_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "analogy is not support" in text
