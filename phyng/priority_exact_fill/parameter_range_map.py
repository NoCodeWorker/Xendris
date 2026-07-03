"""Parameter and benchmark range map for priority exact fills."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.priority_exact_fill.schemas import (
    PriorityExactFillRecord,
    PriorityParameterRangeMap,
    PriorityParameterRangeMapEntry,
)

PARAMETER_RANGE_MAP_PATH = Path("data/real_sources/extracts/phi_gradient_priority_parameter_range_map_v3_5.json")


def build_priority_parameter_range_map(records: list[PriorityExactFillRecord]) -> PriorityParameterRangeMap:
    entries: list[PriorityParameterRangeMapEntry] = []
    for record in records:
        if not record.validation_ready:
            continue
        if not (record.parameter_range_text or record.benchmark_range_text or record.negative_constraint_text):
            continue
        entries.append(
            PriorityParameterRangeMapEntry(
                priority_source_id=record.priority_source_id,
                source_id=record.source_id,
                parameter_range_text=record.parameter_range_text,
                benchmark_range_text=record.benchmark_range_text,
                negative_constraint_text=record.negative_constraint_text,
                comparability_status="PRIORITY_RANGE_READY_FOR_REVIEW",
                missing_requirements=[],
            )
        )
    return PriorityParameterRangeMap(entries=entries)


def write_priority_parameter_range_map(root: str | Path, parameter_map: PriorityParameterRangeMap) -> str:
    path = Path(root) / PARAMETER_RANGE_MAP_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(parameter_map.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
