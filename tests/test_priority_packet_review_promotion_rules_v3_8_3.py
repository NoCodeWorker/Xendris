from __future__ import annotations

from phyng.priority_packet_review.pedernales_expander import build_review_targets
from phyng.priority_packet_review.promotion_rules import evaluate_promotion
from phyng.semantic_triage.schemas import PriorityReviewItem, SemanticTriageRecord

from tests.test_priority_packet_review_loader_v3_8_3 import triage_record


def test_promotion_requires_source_hash() -> None:
    target = _target(triage_record(sha256="bad"))

    decision, reason, _, _ = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "REJECT_UNSUPPORTED_ROLE"
    assert "hash" in reason


def test_promotion_requires_page_or_location() -> None:
    target = _target(triage_record(page_number=None))

    decision, reason, _, _ = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "SEND_TO_MANUAL_REVIEW"
    assert "page" in reason


def test_promotion_requires_clear_slot_role() -> None:
    target = _target(triage_record(assigned_slot="SLOT_8_ANALOGY_ONLY_OR_BACKGROUND"))

    decision, _, role, _ = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "CLASSIFY_ANALOGY_ONLY"
    assert role == "ANALOGY_ONLY"


def test_ambiguous_item_goes_to_manual_review() -> None:
    target = _target(triage_record(extracted_text="λCSL = m2", assigned_slot="SLOT_5_PARAMETER_CONSTRAINTS"))

    decision, _, _, _ = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "SEND_TO_MANUAL_REVIEW"


def test_negative_or_limitation_item_can_be_promoted() -> None:
    target = _target(
        triage_record(
            assigned_slot="SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
            extracted_text="The dominant background noise creates a limitation that can falsify the claimed coherence-loss mechanism.",
            normalized_text="the dominant background noise creates a limitation that can falsify the claimed coherence-loss mechanism.",
        )
    )

    decision, _, role, _ = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "PROMOTE_VALIDATION_READY"
    assert role == "NEGATIVE_CONSTRAINT_LIMITATION"


def test_validation_ready_extract_is_not_support() -> None:
    target = _target(triage_record())

    decision, _, _, limitations = evaluate_promotion(target, {"SRC-TEST": "abc123"})

    assert decision == "PROMOTE_VALIDATION_READY"
    assert any("does not grant source support" in item for item in limitations)


def _target(record_payload: dict):
    record = SemanticTriageRecord(**record_payload)
    item = PriorityReviewItem(
        review_item_id="ITEM-1",
        candidate_id=record.candidate_id,
        source_id=record.source_id,
        page_number=record.page_number,
        assigned_slot=record.assigned_slot,
        priority=record.priority,
        exact_text_or_preview=record.extracted_text,
        why_relevant="test",
        review_question=record.review_question,
        decision_needed=record.decision_needed,
        possible_outcomes=[],
        next_gate_impact="test",
    )
    return build_review_targets([item], [record])[0][0]
