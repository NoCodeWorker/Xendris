"""Build v3.8.2 priority review packet and outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.semantic_triage.schemas import (
    LowValueTriageExclusion,
    NextGateReadiness,
    PriorityReviewItem,
    SemanticTriageRecord,
    SlotReviewQueue,
)
from phyng.semantic_triage.slot_rules import ALL_SLOTS


OUTPUT_PATHS = {
    "semantic_triage_map": Path("data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json"),
    "priority_review_packet": Path("data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json"),
    "slot_review_queues": Path("data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json"),
    "low_value_exclusions": Path("data/real_sources/extracts/phi_gradient_triage_rejected_low_value_v3_8_2.json"),
    "next_gate_readiness": Path("data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json"),
}


def build_priority_packet(records: list[SemanticTriageRecord], limit: int = 60) -> list[PriorityReviewItem]:
    included = [record for record in records if record.include_in_priority_packet]
    included.sort(key=lambda item: (_priority_rank(item.priority), item.triage_score, item.source_priority_score), reverse=True)
    selected = _ensure_slot_coverage(included[:limit], included, limit)
    return [_packet_item(index, record) for index, record in enumerate(selected[:limit], start=1)]


def build_slot_review_queues(packet: list[PriorityReviewItem]) -> list[SlotReviewQueue]:
    queues: list[SlotReviewQueue] = []
    for slot in ALL_SLOTS:
        items = [item for item in packet if item.assigned_slot == slot]
        source_coverage: dict[str, int] = {}
        for item in items:
            source_coverage[item.source_id] = source_coverage.get(item.source_id, 0) + 1
        queues.append(
            SlotReviewQueue(
                slot_id=slot,
                items=items,
                critical_count=sum(1 for item in items if item.priority == "CRITICAL"),
                high_count=sum(1 for item in items if item.priority == "HIGH"),
                medium_count=sum(1 for item in items if item.priority == "MEDIUM"),
                low_count=sum(1 for item in items if item.priority == "LOW"),
                source_coverage=source_coverage,
            )
        )
    return queues


def build_low_value_exclusions(records: list[SemanticTriageRecord]) -> list[LowValueTriageExclusion]:
    excluded = [record for record in records if not record.include_in_priority_packet]
    return [
        LowValueTriageExclusion(
            candidate_id=record.candidate_id,
            source_id=record.source_id,
            reason="priority below packet threshold or low semantic value",
            triage_score=record.triage_score,
            text_preview=_preview(record.extracted_text, 180),
        )
        for record in excluded
    ]


def build_next_gate_readiness(
    status: str,
    packet: list[PriorityReviewItem],
    validation_ready_count: int,
    blocked_claims: list[str],
) -> NextGateReadiness:
    critical_count = sum(1 for item in packet if item.priority == "CRITICAL")
    high_count = sum(1 for item in packet if item.priority == "HIGH")
    ready = validation_ready_count > 0
    reason = "v3.8.2 generated a review packet but did not create validation-ready extracts."
    if ready:
        reason = "Validation-ready extracts already exist from a previous gate; v3.8.2 did not create them."
    return NextGateReadiness(
        status=status,
        priority_packet_count=len(packet),
        critical_count=critical_count,
        high_count=high_count,
        manual_review_required=True,
        ready_for_v3_9=ready,
        reason=reason,
        recommended_next_action="Run v3.8.3 priority packet review before any positive v3.9 pressure decision.",
        blocked_claims=blocked_claims,
    )


def write_v3_8_2_outputs(
    root: str | Path,
    records: list[SemanticTriageRecord],
    packet: list[PriorityReviewItem],
    queues: list[SlotReviewQueue],
    exclusions: list[LowValueTriageExclusion],
    readiness: NextGateReadiness,
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {key: repo_root / path for key, path in OUTPUT_PATHS.items()}
    paths["semantic_triage_map"].parent.mkdir(parents=True, exist_ok=True)
    _write_json(paths["semantic_triage_map"], {"triage_records": [item.model_dump(mode="json") for item in records], "triage_count": len(records)})
    _write_json(paths["priority_review_packet"], {"priority_review_packet": [item.model_dump(mode="json") for item in packet], "packet_count": len(packet)})
    _write_json(paths["slot_review_queues"], {"slot_review_queues": [item.model_dump(mode="json") for item in queues]})
    _write_json(paths["low_value_exclusions"], {"low_value_exclusions": [item.model_dump(mode="json") for item in exclusions], "low_value_count": len(exclusions)})
    _write_json(paths["next_gate_readiness"], readiness.model_dump(mode="json"))
    return {key: str(path.relative_to(repo_root)) for key, path in paths.items()}


def _ensure_slot_coverage(selected: list[SemanticTriageRecord], included: list[SemanticTriageRecord], limit: int) -> list[SemanticTriageRecord]:
    selected_ids = {item.candidate_id for item in selected}
    selected_slots = {item.assigned_slot for item in selected}
    for slot in ALL_SLOTS:
        if slot in selected_slots:
            continue
        candidate = next((item for item in included if item.assigned_slot == slot and item.candidate_id not in selected_ids), None)
        if candidate is None:
            continue
        if len(selected) >= limit:
            selected[-1] = candidate
        else:
            selected.append(candidate)
        selected_ids.add(candidate.candidate_id)
        selected_slots.add(slot)
    selected.sort(key=lambda item: (_priority_rank(item.priority), item.triage_score, item.source_priority_score), reverse=True)
    return selected


def _packet_item(index: int, record: SemanticTriageRecord) -> PriorityReviewItem:
    return PriorityReviewItem(
        review_item_id=f"TRIAGE-v3_8_2-{index:03d}",
        candidate_id=record.candidate_id,
        source_id=record.source_id,
        page_number=record.page_number,
        assigned_slot=record.assigned_slot,
        priority=record.priority,
        exact_text_or_preview=_preview(record.extracted_text, 700),
        why_relevant=f"{record.assigned_slot} candidate with triage_score={record.triage_score:.4f}.",
        review_question=record.review_question,
        decision_needed=record.decision_needed,
        possible_outcomes=_possible_outcomes(record.assigned_slot),
        next_gate_impact="v3.8.3 must review this item before any validation-ready promotion or v3.9 pressure decision.",
    )


def _possible_outcomes(slot: str) -> list[str]:
    outcomes = ["VALIDATION_READY_EXTRACT", "MANUAL_REVIEW_REQUIRED", "REJECT_AS_GARBAGE", "ANALOGY_ONLY"]
    if "SLOT_1" in slot:
        outcomes.append("BASELINE_RELEVANT")
    if "SLOT_3" in slot:
        outcomes.append("BENCHMARK_RELEVANT")
    if "SLOT_4" in slot:
        outcomes.append("GRADIENT_COMPONENT_RELEVANT")
    if "SLOT_5" in slot:
        outcomes.append("PARAMETER_CONSTRAINT_RELEVANT")
    if "SLOT_6" in slot:
        outcomes.append("NEGATIVE_CONSTRAINT")
    return outcomes


def _priority_rank(priority: str) -> int:
    return {"EXCLUDE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}.get(priority, 0)


def _preview(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
