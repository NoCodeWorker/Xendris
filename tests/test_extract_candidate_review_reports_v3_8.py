from __future__ import annotations

from pathlib import Path

from phyng.extract_candidate_review.campaign import run_phi_gradient_extract_candidate_review_campaign

from tests.test_extract_candidate_review_loader_v3_8 import raw_candidate, write_minimal_v3_8_inputs


def test_pedernales_blocked_creates_high_priority_manual_review_item(tmp_path: Path) -> None:
    write_minimal_v3_8_inputs(tmp_path, candidates=[], blocked_pedernales=True)

    result = run_phi_gradient_extract_candidate_review_campaign(tmp_path)

    items = result.gate_result.manual_review_queue
    pedernales = [item for item in items if item.source_id == "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING"]
    assert pedernales
    assert pedernales[0].priority == "HIGH"
    assert "SLOT_4" in pedernales[0].reason


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    write_minimal_v3_8_inputs(tmp_path, candidates=[raw_candidate()], blocked_pedernales=False)

    result = run_phi_gradient_extract_candidate_review_campaign(tmp_path)
    report = Path(result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in report
    assert "A validation-ready extract is not support" in report


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_minimal_v3_8_inputs(tmp_path, candidates=[raw_candidate()], blocked_pedernales=False)

    result = run_phi_gradient_extract_candidate_review_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "Validation-ready extract equals source support." in result.gate_result.blocked_claims
