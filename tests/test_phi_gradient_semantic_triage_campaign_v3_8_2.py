from __future__ import annotations

from pathlib import Path

from phyng.extract_candidate_review.campaign import run_phi_gradient_extract_candidate_review_campaign
from phyng.semantic_triage.campaign import run_phi_gradient_semantic_triage_campaign

from tests.test_extract_candidate_review_loader_v3_8 import raw_candidate as v3_8_raw_candidate
from tests.test_extract_candidate_review_loader_v3_8 import write_minimal_v3_8_inputs
from tests.test_semantic_triage_loader_v3_8_2 import raw_candidate, write_minimal_v3_8_2_inputs


def test_campaign_generates_v3_8_2_outputs(tmp_path: Path) -> None:
    write_minimal_v3_8_2_inputs(
        tmp_path,
        [
            raw_candidate(
                candidate_id="PED-1",
                source_id="SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                sha256="h5",
                extracted_text="A magnetic field gradient changes spin-motion coupling and effective dynamics.",
                normalized_text="a magnetic field gradient changes spin-motion coupling and effective dynamics.",
            )
        ],
    )

    result = run_phi_gradient_semantic_triage_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY"
    assert result.gate_result.priority_packet_count == 1
    assert result.gate_result.pedernales_slot4_count == 1
    for path in result.gate_result.output_paths.values():
        assert (tmp_path / path).exists()
    assert result.gate_result.next_gate_readiness.ready_for_v3_9 is False


def test_existing_v3_8_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v3_8_inputs(tmp_path, candidates=[v3_8_raw_candidate()], blocked_pedernales=False)

    result = run_phi_gradient_extract_candidate_review_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION"
    assert result.gate_result.validation_ready_count == 1
    assert "Validation-ready extract equals source support." in result.gate_result.blocked_claims
