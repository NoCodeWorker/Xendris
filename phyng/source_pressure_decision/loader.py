"""Load v3.9 source pressure decision inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_pressure_decision.schemas import SourcePressureInputs


INPUT_PATHS = {
    "validation_ready_pack": Path("data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json"),
    "review_decisions": Path("data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json"),
    "analogy_only_items": Path("data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json"),
    "manual_review_queue": Path("data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json"),
    "next_source_pressure_inputs": Path("data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
}


def load_source_pressure_inputs(root: str | Path = ".") -> SourcePressureInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return SourcePressureInputs(blocked_reason="PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK")
    return SourcePressureInputs(
        validation_ready_pack=_load_json(repo_root / INPUT_PATHS["validation_ready_pack"]),
        review_decisions=_load_json(repo_root / INPUT_PATHS["review_decisions"]),
        analogy_only_items=_load_json(repo_root / INPUT_PATHS["analogy_only_items"]),
        manual_review_queue=_load_json(repo_root / INPUT_PATHS["manual_review_queue"]),
        next_source_pressure_inputs=_load_json(repo_root / INPUT_PATHS["next_source_pressure_inputs"]),
        source_hashes=_load_json(repo_root / INPUT_PATHS["source_hashes"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
