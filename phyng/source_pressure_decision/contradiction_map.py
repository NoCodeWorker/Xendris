"""Build contradiction and limitation map for v3.9."""

from __future__ import annotations

from phyng.source_pressure_decision.schemas import (
    ContradictionLimitationMap,
    ExtractPressureRecord,
)


def build_contradiction_map(records: list[ExtractPressureRecord]) -> ContradictionLimitationMap:
    """Collect all contradiction and limitation extracts into a structured map."""
    contradictions: list[dict] = []
    limitations: list[dict] = []
    source_ids: set[str] = set()
    affected_slots: set[str] = set()

    for record in records:
        if record.pressure_class == "CONTRADICTS_COMPONENT":
            contradictions.append({
                "extract_id": record.extract_id,
                "source_id": record.source_id,
                "slot": record.assigned_slot,
                "text_preview": _preview(record.exact_text),
                "reasoning": record.reasoning,
                "pressure_score": record.pressure_score,
            })
            source_ids.add(record.source_id)
            affected_slots.add(record.assigned_slot)
        elif record.pressure_class == "LIMITS_COMPONENT":
            limitations.append({
                "extract_id": record.extract_id,
                "source_id": record.source_id,
                "slot": record.assigned_slot,
                "text_preview": _preview(record.exact_text),
                "reasoning": record.reasoning,
                "pressure_score": record.pressure_score,
            })
            source_ids.add(record.source_id)
            affected_slots.add(record.assigned_slot)

    dominant_risks = _dominant_risks(contradictions, limitations)
    required_changes = _required_changes(contradictions, limitations)

    return ContradictionLimitationMap(
        contradictions=contradictions,
        limitations=limitations,
        dominant_risks=dominant_risks,
        source_ids=sorted(source_ids),
        affected_slots=sorted(affected_slots),
        required_model_changes=required_changes,
    )


def _dominant_risks(contradictions: list[dict], limitations: list[dict]) -> list[str]:
    risks: list[str] = []
    if contradictions:
        risks.append("Direct contradiction from reviewed source extracts.")
    if limitations:
        risks.append("Source-backed limitations constrain candidate viability.")
    if not contradictions and not limitations:
        risks.append("No contradiction or limitation detected in current extract pack.")
    return risks


def _required_changes(contradictions: list[dict], limitations: list[dict]) -> list[str]:
    changes: list[str] = []
    if contradictions:
        changes.append("Review contradicted components before any model update.")
        changes.append("Consider candidate revision or kill/pivot gate.")
    if limitations:
        changes.append("Assess whether limitations narrow the candidate to a viable regime.")
    return changes


def _preview(text: str, limit: int = 180) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."
