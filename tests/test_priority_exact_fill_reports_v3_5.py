from pathlib import Path

from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_priority_exact_fill import run_phi_gradient_priority_exact_fill_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_reports_include_canonical_section(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "## Blocked Claims" in text or "### Blocked Uses" in text


def test_physical_claims_remain_blocked(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "Availability of a source URL counts as exact source text." in result.gate_result.blocked_claims
