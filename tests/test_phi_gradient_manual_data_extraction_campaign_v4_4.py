from __future__ import annotations

from pathlib import Path

from phyng.manual_data_extraction.campaign import run_phi_gradient_manual_data_extraction_campaign
from phyng.ytrue_extraction.campaign import run_phi_gradient_real_ytrue_extraction_campaign

from tests.test_manual_data_extraction_loader_v4_4 import queue_item, write_minimal_v4_4_inputs
from tests.test_ytrue_extraction_loader_v4_3 import write_minimal_v4_3_inputs


def test_slot4_debt_remains_open_blocking(tmp_path: Path) -> None:
    write_minimal_v4_4_inputs(tmp_path, [queue_item()])

    result = run_phi_gradient_manual_data_extraction_campaign(tmp_path)

    assert result.gate_result.slot4_debt_status == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_minimal_v4_4_inputs(tmp_path, [queue_item()])

    result = run_phi_gradient_manual_data_extraction_campaign(tmp_path)

    assert "PHI_GRADIENT is predictively validated." in result.gate_result.blocked_claims
    assert result.gate_result.physical_claim_permission == "BLOCKED"


def test_campaign_generates_v4_4_outputs(tmp_path: Path) -> None:
    write_minimal_v4_4_inputs(tmp_path, [queue_item()])

    result = run_phi_gradient_manual_data_extraction_campaign(tmp_path)

    assert result.gate_result.reviewed_count == 1
    assert result.gate_result.accepted_y_true_count == 1
    assert "campaign" in result.report_paths
    for path in result.gate_result.output_paths.values():
        assert (tmp_path / path).exists()


def test_existing_v4_3_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v4_3_inputs(tmp_path)

    result = run_phi_gradient_real_ytrue_extraction_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL"
