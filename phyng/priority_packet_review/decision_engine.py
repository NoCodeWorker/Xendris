"""Decision engine for v3.8.3 priority packet review."""

from __future__ import annotations

from pathlib import Path

from phyng.priority_packet_review.promotion_rules import evaluate_promotion, exact_text, pressure_direction
from phyng.priority_packet_review.schemas import (
    AnalogyOnlyItem,
    ManualReviewItemV383,
    PriorityPacketReviewDecision,
    RejectedPriorityItem,
    ReviewTarget,
    ValidationReadyExtractV383,
)


def review_targets(targets: list[ReviewTarget], source_hashes: dict) -> tuple[
    list[ValidationReadyExtractV383],
    list[PriorityPacketReviewDecision],
    list[RejectedPriorityItem],
    list[AnalogyOnlyItem],
    list[ManualReviewItemV383],
]:
    valid_hashes = {item["source_id"]: item["sha256"] for item in source_hashes.get("hashes", [])}
    filenames = {item["source_id"]: Path(item["local_path"]).name for item in source_hashes.get("hashes", [])}
    extracts: list[ValidationReadyExtractV383] = []
    decisions: list[PriorityPacketReviewDecision] = []
    rejected: list[RejectedPriorityItem] = []
    analogy: list[AnalogyOnlyItem] = []
    manual: list[ManualReviewItemV383] = []
    seen_promoted_keys: set[tuple[str, int | None, str]] = set()
    for target in targets:
        decision, reason, role, limitations = evaluate_promotion(target, valid_hashes)
        output_extract_id = None
        text = exact_text(target)
        if decision == "PROMOTE_VALIDATION_READY" and target.triage_record is not None and role is not None:
            key = (target.source_id, target.page_number, " ".join(text.lower().split()))
            if key in seen_promoted_keys:
                decision = "REJECT_DUPLICATE"
                reason = "duplicate promoted text by source, page and normalized text"
            else:
                output_extract_id = f"VRX-v3_8_3-{len(extracts) + 1:03d}"
                extracts.append(
                    ValidationReadyExtractV383(
                        extract_id=output_extract_id,
                        source_id=target.source_id,
                        sha256=target.triage_record.sha256 or "",
                        source_filename=filenames.get(target.source_id),
                        page_number=target.page_number,
                        location_type="PAGE_TEXT",
                        location_value=f"page={target.page_number}; candidate_id={target.candidate_id}",
                        exact_text=text,
                        source_candidate_id=target.candidate_id,
                        assigned_slot=target.assigned_slot,
                        component_role=role,
                        promotion_decision=decision,
                        why_promoted=reason,
                        limitations=limitations,
                        possible_pressure_direction=pressure_direction(target.assigned_slot),
                        validation_questions=[
                            "Does this extract accurately represent the source page?",
                            "Does this extract support, constrain, contradict, or merely contextualize PHI_GRADIENT?",
                        ],
                    )
                )
                seen_promoted_keys.add(key)
        if decision == "CLASSIFY_ANALOGY_ONLY":
            analogy.append(
                AnalogyOnlyItem(
                    review_item_id=target.review_item_id,
                    candidate_id=target.candidate_id,
                    source_id=target.source_id,
                    assigned_slot=target.assigned_slot,
                    why_analogy_only=reason,
                    text_preview=_preview(text),
                )
            )
        elif decision == "SEND_TO_MANUAL_REVIEW":
            manual.append(
                ManualReviewItemV383(
                    review_item_id=target.review_item_id,
                    candidate_id=target.candidate_id,
                    source_id=target.source_id,
                    page_number=target.page_number,
                    assigned_slot=target.assigned_slot,
                    priority=target.priority,
                    reason=reason,
                    suggested_action="Review the source PDF page and nearby context before promotion.",
                    text_preview=_preview(text),
                )
            )
        elif decision.startswith("REJECT"):
            rejected.append(
                RejectedPriorityItem(
                    review_item_id=target.review_item_id,
                    candidate_id=target.candidate_id,
                    source_id=target.source_id,
                    reason=reason,
                    text_preview=_preview(text),
                    decision=decision,
                )
            )
        decisions.append(
            PriorityPacketReviewDecision(
                review_item_id=target.review_item_id,
                candidate_id=target.candidate_id,
                source_id=target.source_id,
                assigned_slot=target.assigned_slot,
                priority=target.priority,
                decision=decision,
                reason=reason,
                output_extract_id=output_extract_id,
                notes=["Validation-ready promotion is not source support."] if output_extract_id else [],
            )
        )
    return extracts, decisions, rejected, analogy, manual


def _preview(text: str, limit: int = 220) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."
