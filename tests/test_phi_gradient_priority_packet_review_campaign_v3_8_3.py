from __future__ import annotations

from pathlib import Path

from phyng.priority_packet_review.campaign import run_phi_gradient_priority_packet_review_campaign
from phyng.semantic_triage.campaign import run_phi_gradient_semantic_triage_campaign

from tests.test_priority_packet_review_loader_v3_8_3 import triage_record, write_minimal_v3_8_3_inputs
from tests.test_semantic_triage_loader_v3_8_2 import raw_candidate, write_minimal_v3_8_2_inputs


def test_campaign_generates_v3_8_3_outputs(tmp_path: Path) -> None:
    write_minimal_v3_8_3_inputs(tmp_path, [triage_record()])

    result = run_phi_gradient_priority_packet_review_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE"
    assert result.gate_result.validation_ready_count == 1
    assert result.gate_result.ready_for_v3_9 is True
    for path in result.gate_result.output_paths.values():
        assert (tmp_path / path).exists()


def test_existing_v3_8_2_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v3_8_2_inputs(tmp_path, [raw_candidate()])

    result = run_phi_gradient_semantic_triage_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY"
    assert result.gate_result.next_gate_readiness.ready_for_v3_9 is False
