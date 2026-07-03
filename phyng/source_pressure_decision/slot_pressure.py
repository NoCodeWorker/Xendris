"""Compute slot-level pressure summaries for v3.9."""

from __future__ import annotations

from phyng.source_pressure_decision.schemas import (
    ExtractPressureRecord,
    SlotPressureSummary,
    SLOTS,
)


def compute_slot_pressure(records: list[ExtractPressureRecord]) -> list[SlotPressureSummary]:
    """Aggregate extract pressure records into per-slot summaries."""
    slot_groups: dict[str, list[ExtractPressureRecord]] = {slot: [] for slot in SLOTS}
    for record in records:
        if record.assigned_slot in slot_groups:
            slot_groups[record.assigned_slot].append(record)

    summaries: list[SlotPressureSummary] = []
    for slot_id in SLOTS:
        group = slot_groups[slot_id]
        summary = _summarize_slot(slot_id, group)
        summaries.append(summary)
    return summaries


def _summarize_slot(slot_id: str, records: list[ExtractPressureRecord]) -> SlotPressureSummary:
    if not records:
        return SlotPressureSummary(
            slot_id=slot_id,
            pressure_status="SLOT_NO_VALID_EXTRACTS",
            summary=f"No validation-ready extracts in {slot_id}.",
        )

    support = sum(1 for r in records if r.pressure_class.startswith("SUPPORTS_"))
    benchmark = sum(1 for r in records if r.pressure_class == "SUPPORTS_BENCHMARK_ALIGNMENT")
    contradiction = sum(1 for r in records if r.pressure_class == "CONTRADICTS_COMPONENT")
    limitation = sum(1 for r in records if r.pressure_class == "LIMITS_COMPONENT")
    analogy = sum(1 for r in records if r.pressure_class == "ANALOGY_ONLY")
    inconclusive = sum(1 for r in records if r.pressure_class == "INCONCLUSIVE")

    total_score = sum(r.pressure_score for r in records)
    status = _slot_status(support, benchmark, contradiction, limitation, analogy, inconclusive, total_score)

    return SlotPressureSummary(
        slot_id=slot_id,
        extract_count=len(records),
        support_count=support,
        benchmark_count=benchmark,
        contradiction_count=contradiction,
        limitation_count=limitation,
        analogy_only_count=analogy,
        inconclusive_count=inconclusive,
        pressure_status=status,
        pressure_score=round(total_score, 4),
        summary=f"{slot_id}: {len(records)} extracts, status={status}.",
    )


def _slot_status(
    support: int,
    benchmark: int,
    contradiction: int,
    limitation: int,
    analogy: int,
    inconclusive: int,
    total_score: float,
) -> str:
    """Determine slot-level pressure status. Contradictions dominate per rule 6."""
    if contradiction > 0 and total_score < 0:
        return "SLOT_CONTRADICTED"
    if limitation > 0 and support == 0:
        return "SLOT_LIMITED"
    if support > 0 and benchmark > 0:
        return "SLOT_BENCHMARK_RELEVANT"
    if support > 0:
        return "SLOT_SOURCE_BACKED_LIMITED"
    if analogy > 0 and support == 0 and contradiction == 0:
        return "SLOT_ANALOGY_ONLY"
    if inconclusive > 0:
        return "SLOT_INCONCLUSIVE"
    return "SLOT_NO_VALID_EXTRACTS"
