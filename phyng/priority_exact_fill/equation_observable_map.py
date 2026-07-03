"""Equation and observable map for priority exact fills."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.priority_exact_fill.schemas import (
    PriorityEquationObservableMap,
    PriorityEquationObservableMapEntry,
    PriorityExactFillRecord,
)

EQUATION_OBSERVABLE_MAP_PATH = Path("data/real_sources/extracts/phi_gradient_priority_equation_observable_map_v3_5.json")


def build_priority_equation_observable_map(records: list[PriorityExactFillRecord]) -> PriorityEquationObservableMap:
    entries = [
        PriorityEquationObservableMapEntry(
            priority_source_id=record.priority_source_id,
            source_id=record.source_id,
            equation_text=record.equation_text,
            observable_text=record.observable_text,
            slot_id=record.slot_id,
            candidate_relevance="PRIORITY_EXACT_FILL_READY_FOR_MAPPING",
            limitations=["Mapping is limited to exact reviewed local content."],
        )
        for record in records
        if record.validation_ready and (record.equation_text or record.observable_text)
    ]
    return PriorityEquationObservableMap(entries=entries)


def write_priority_equation_observable_map(
    root: str | Path,
    equation_map: PriorityEquationObservableMap,
) -> str:
    path = Path(root) / EQUATION_OBSERVABLE_MAP_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(equation_map.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
