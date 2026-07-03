from __future__ import annotations

from pathlib import Path

from phyng.pdf_text_extraction.campaign import run_phi_gradient_pdf_text_extraction_campaign

from tests.test_pdf_text_extraction_registry_boundary_v3_7 import _write_registry


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    _write_registry(tmp_path, sha256=None, exists=True)

    result = run_phi_gradient_pdf_text_extraction_campaign(tmp_path)

    assert result.report_paths
    campaign_report = Path(result.report_paths["campaign"])
    text = campaign_report.read_text(encoding="utf-8")
    assert "## Canonical Status" in text
    assert "Extraction is contact, not belief." in text


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    _write_registry(tmp_path, sha256=None, exists=True)

    result = run_phi_gradient_pdf_text_extraction_campaign(tmp_path)

    blocked_claims = result.extraction_result.blocked_claims
    assert "PHI_GRADIENT is physically validated." in blocked_claims
    assert "Extracted quote candidate is source support." in blocked_claims
