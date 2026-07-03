from __future__ import annotations

from pathlib import Path

from phyng.priority_packet_review.campaign import run_phi_gradient_priority_packet_review_campaign

from tests.test_priority_packet_review_loader_v3_8_3 import triage_record, write_minimal_v3_8_3_inputs


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    write_minimal_v3_8_3_inputs(tmp_path, [triage_record()])

    result = run_phi_gradient_priority_packet_review_campaign(tmp_path)
    report = Path(result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in report
    assert "Promotion means ready to be judged" in report


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_minimal_v3_8_3_inputs(tmp_path, [triage_record()])

    result = run_phi_gradient_priority_packet_review_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "Frontera C is validated." in result.gate_result.blocked_claims
