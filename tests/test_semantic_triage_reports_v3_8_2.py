from __future__ import annotations

from pathlib import Path

from phyng.semantic_triage.campaign import run_phi_gradient_semantic_triage_campaign

from tests.test_semantic_triage_loader_v3_8_2 import raw_candidate, write_minimal_v3_8_2_inputs


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    write_minimal_v3_8_2_inputs(tmp_path, [raw_candidate()])

    result = run_phi_gradient_semantic_triage_campaign(tmp_path)
    report = Path(result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in report
    assert "v3.8.2 chooses what deserves attention" in report


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_minimal_v3_8_2_inputs(tmp_path, [raw_candidate()])

    result = run_phi_gradient_semantic_triage_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "Frontera C is validated." in result.gate_result.blocked_claims
