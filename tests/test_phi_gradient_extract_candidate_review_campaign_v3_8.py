from __future__ import annotations

from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.extract_candidate_review.campaign import run_phi_gradient_extract_candidate_review_campaign

from tests.test_extract_candidate_review_loader_v3_8 import raw_candidate, write_minimal_v3_8_inputs


def test_campaign_generates_v3_8_outputs(tmp_path: Path) -> None:
    write_minimal_v3_8_inputs(tmp_path, candidates=[raw_candidate()], blocked_pedernales=True)

    result = run_phi_gradient_extract_candidate_review_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL"
    assert result.gate_result.input_candidate_count == 1
    assert result.gate_result.validation_ready_count == 1
    assert result.gate_result.manual_review_count == 1
    for path in result.gate_result.output_paths.values():
        assert (tmp_path / path).exists()


def test_existing_v3_7_behavior_preserved() -> None:
    record = normalize_status("PHI_GRADIENT_PDF_EXTRACTION_PARTIAL", domain="pdf_text_extraction")

    assert record.domain_status == "PHI_GRADIENT_PDF_EXTRACTION_PARTIAL"
    assert record.canonical_permission.value == "REVIEW_REQUIRED"
    assert "Physical prediction" in record.blocked_uses
