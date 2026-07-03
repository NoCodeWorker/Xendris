from __future__ import annotations

from phyng.priority_packet_review.pedernales_expander import build_review_targets
from phyng.semantic_triage.schemas import PriorityReviewItem, SemanticTriageRecord

from tests.test_priority_packet_review_loader_v3_8_3 import triage_record


def test_pedernales_slot4_records_are_expanded_beyond_capped_packet() -> None:
    normal = SemanticTriageRecord(**triage_record())
    ped = SemanticTriageRecord(
        **triage_record(
            candidate_id="PED-1",
            source_id="SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
            sha256="ped123",
            assigned_slot="SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
            extracted_text="The magnetic field gradient couples spin-motion dynamics to the motional state.",
            normalized_text="the magnetic field gradient couples spin-motion dynamics to the motional state.",
            priority="HIGH",
            include_in_priority_packet=True,
        )
    )
    packet = [
        PriorityReviewItem(
            review_item_id="ITEM-1",
            candidate_id=normal.candidate_id,
            source_id=normal.source_id,
            page_number=normal.page_number,
            assigned_slot=normal.assigned_slot,
            priority=normal.priority,
            exact_text_or_preview=normal.extracted_text,
            why_relevant="test",
            review_question=normal.review_question,
            decision_needed=normal.decision_needed,
            possible_outcomes=[],
            next_gate_impact="test",
        )
    ]

    targets, expanded = build_review_targets(packet, [normal, ped])

    assert expanded == 1
    assert any(target.candidate_id == "PED-1" for target in targets)
