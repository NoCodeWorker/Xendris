"""Expand v3.8.3 review targets with all relevant Pedernales SLOT_4 records."""

from __future__ import annotations

from phyng.priority_packet_review.schemas import ReviewTarget
from phyng.semantic_triage.schemas import PriorityReviewItem, SemanticTriageRecord

PEDERNALES_ID = "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING"
SLOT_4 = "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"


def build_review_targets(packet: list[PriorityReviewItem], triage_records: list[SemanticTriageRecord]) -> tuple[list[ReviewTarget], int]:
    records_by_id = {record.candidate_id: record for record in triage_records}
    targets = [_target_from_packet(item, records_by_id.get(item.candidate_id)) for item in packet]
    seen = {_dedupe_key(target) for target in targets}
    expanded = 0
    for record in triage_records:
        if record.source_id != PEDERNALES_ID or record.assigned_slot != SLOT_4:
            continue
        if not record.include_in_priority_packet and record.priority not in {"CRITICAL", "HIGH", "MEDIUM"}:
            continue
        target = _target_from_record(record)
        key = _dedupe_key(target)
        if key in seen:
            continue
        targets.append(target)
        seen.add(key)
        expanded += 1
    return targets, expanded


def _target_from_packet(item: PriorityReviewItem, record: SemanticTriageRecord | None) -> ReviewTarget:
    return ReviewTarget(
        review_item_id=item.review_item_id,
        candidate_id=item.candidate_id,
        source_id=item.source_id,
        page_number=item.page_number,
        assigned_slot=item.assigned_slot,
        priority=item.priority,
        exact_text_or_preview=item.exact_text_or_preview,
        review_question=item.review_question,
        decision_needed=item.decision_needed,
        triage_record=record,
    )


def _target_from_record(record: SemanticTriageRecord) -> ReviewTarget:
    return ReviewTarget(
        review_item_id=f"PEDERNALES-EXPANDED-{record.candidate_id}",
        candidate_id=record.candidate_id,
        source_id=record.source_id,
        page_number=record.page_number,
        assigned_slot=record.assigned_slot,
        priority=record.priority,
        exact_text_or_preview=record.extracted_text,
        review_question=record.review_question,
        decision_needed=record.decision_needed,
        triage_record=record,
    )


def _dedupe_key(target: ReviewTarget) -> tuple[str, str, int | None, str]:
    normalized = target.triage_record.normalized_text if target.triage_record else target.exact_text_or_preview.lower()
    return (target.candidate_id, target.source_id, target.page_number, normalized or "")
