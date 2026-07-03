"""Load v4.0 benchmark construction inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.benchmark_construction.schemas import BenchmarkConstructionInputs

INPUT_PATHS = {
    "source_pressure_decision": Path("data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json"),
    "extract_pressure_map": Path("data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json"),
    "slot_pressure_summary": Path("data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json"),
    "benchmark_alignment": Path("data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json"),
    "contradiction_map": Path("data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json"),
    "next_model_update_recommendations": Path("data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json"),
    "validation_ready_pack": Path("data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
}


def load_benchmark_construction_inputs(root: str | Path = ".") -> BenchmarkConstructionInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return BenchmarkConstructionInputs(
            blocked_reason="PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE"
        )
    return BenchmarkConstructionInputs(
        source_pressure_decision=_load_json(repo_root / INPUT_PATHS["source_pressure_decision"]),
        extract_pressure_map=_load_json(repo_root / INPUT_PATHS["extract_pressure_map"]),
        slot_pressure_summary=_load_json(repo_root / INPUT_PATHS["slot_pressure_summary"]),
        benchmark_alignment=_load_json(repo_root / INPUT_PATHS["benchmark_alignment"]),
        contradiction_map=_load_json(repo_root / INPUT_PATHS["contradiction_map"]),
        next_model_update_recommendations=_load_json(repo_root / INPUT_PATHS["next_model_update_recommendations"]),
        validation_ready_pack=_load_json(repo_root / INPUT_PATHS["validation_ready_pack"]),
        source_hashes=_load_json(repo_root / INPUT_PATHS["source_hashes"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
