"""Build and write v3.8.3 validation-ready output artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.priority_packet_review.schemas import (
    AnalogyOnlyItem,
    ManualReviewItemV383,
    PriorityPacketReviewDecision,
    RejectedPriorityItem,
    ValidationReadyExtractPackV383,
    ValidationReadyExtractV383,
)


OUTPUT_PATHS = {
    "validation_ready_pack": Path("data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json"),
    "review_decisions": Path("data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json"),
    "rejected_items": Path("data/real_sources/extracts/phi_gradient_rejected_priority_items_v3_8_3.json"),
    "analogy_only_items": Path("data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json"),
    "manual_review_queue": Path("data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json"),
    "next_source_pressure_inputs": Path("data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json"),
}


def build_validation_ready_pack(
    extracts: list[ValidationReadyExtractV383],
    manual_review: list[ManualReviewItemV383],
    rejected: list[RejectedPriorityItem],
    analogy: list[AnalogyOnlyItem],
    status: str,
    blocked_claims: list[str],
) -> ValidationReadyExtractPackV383:
    source_coverage = _coverage(extracts, "source_id")
    slot_coverage = _coverage(extracts, "assigned_slot")
    ready = len(extracts) > 0
    return ValidationReadyExtractPackV383(
        extracts=extracts,
        validation_ready_count=len(extracts),
        source_coverage=source_coverage,
        slot_coverage=slot_coverage,
        manual_review_count=len(manual_review),
        rejected_count=len(rejected),
        analogy_only_count=len(analogy),
        status=status,
        ready_for_v3_9=ready,
        blocked_claims=blocked_claims,
        notes=[
            "Validation-ready extracts are ready for v3.9 judgment, not source support.",
            "v3.8.3 grants no benchmark support and no physical validation.",
        ],
    )


def write_v3_8_3_outputs(
    root: str | Path,
    pack: ValidationReadyExtractPackV383,
    decisions: list[PriorityPacketReviewDecision],
    rejected: list[RejectedPriorityItem],
    analogy: list[AnalogyOnlyItem],
    manual_review: list[ManualReviewItemV383],
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {key: repo_root / value for key, value in OUTPUT_PATHS.items()}
    paths["validation_ready_pack"].parent.mkdir(parents=True, exist_ok=True)
    _write_json(paths["validation_ready_pack"], pack.model_dump(mode="json"))
    _write_json(paths["review_decisions"], {"review_decisions": [item.model_dump(mode="json") for item in decisions], "decision_count": len(decisions)})
    _write_json(paths["rejected_items"], {"rejected_priority_items": [item.model_dump(mode="json") for item in rejected], "rejected_count": len(rejected)})
    _write_json(paths["analogy_only_items"], {"analogy_only_items": [item.model_dump(mode="json") for item in analogy], "analogy_only_count": len(analogy)})
    _write_json(paths["manual_review_queue"], {"manual_review_queue": [item.model_dump(mode="json") for item in manual_review], "manual_review_count": len(manual_review)})
    _write_json(
        paths["next_source_pressure_inputs"],
        {
            "ready_for_v3_9": pack.ready_for_v3_9,
            "validation_ready_pack_path": str(OUTPUT_PATHS["validation_ready_pack"]),
            "validation_ready_count": pack.validation_ready_count,
            "source_coverage": pack.source_coverage,
            "slot_coverage": pack.slot_coverage,
            "recommended_next_phase": "v3.9 - Source Pressure Decision Gate",
            "blocked_claims": pack.blocked_claims,
            "notes": pack.notes,
        },
    )
    return {key: str(path.relative_to(repo_root)) for key, path in paths.items()}


def _coverage(items: list[ValidationReadyExtractV383], field: str) -> dict[str, int]:
    coverage: dict[str, int] = {}
    for item in items:
        key = getattr(item, field)
        coverage[key] = coverage.get(key, 0) + 1
    return coverage


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
