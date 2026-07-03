"""Load v4.1 model comparison inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.model_comparison.schemas import ModelComparisonInputs

INPUT_PATHS = {
    "benchmark_manifest": Path("data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json"),
    "observable_alignment": Path("data/benchmarks/phi_gradient_observable_alignment_v4_0.json"),
    "benchmark_rows": Path("data/benchmarks/phi_gradient_benchmark_rows_v4_0.json"),
    "negative_control_plan": Path("data/benchmarks/phi_gradient_negative_control_plan_v4_0.json"),
    "debt_object": Path("data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json"),
    "slot4_resolution_plan": Path("data/debts/slot4_resolution_plan_v4_0.json"),
    "next_gate_inputs": Path("data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json"),
}


def load_model_comparison_inputs(root: str | Path = ".") -> ModelComparisonInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return ModelComparisonInputs(
            blocked_reason="PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK"
        )
    return ModelComparisonInputs(
        benchmark_manifest=_load_json(repo_root / INPUT_PATHS["benchmark_manifest"]),
        observable_alignment=_load_json(repo_root / INPUT_PATHS["observable_alignment"]),
        benchmark_rows=_load_json(repo_root / INPUT_PATHS["benchmark_rows"]),
        negative_control_plan=_load_json(repo_root / INPUT_PATHS["negative_control_plan"]),
        debt_object=_load_json(repo_root / INPUT_PATHS["debt_object"]),
        slot4_resolution_plan=_load_json(repo_root / INPUT_PATHS["slot4_resolution_plan"]),
        next_gate_inputs=_load_json(repo_root / INPUT_PATHS["next_gate_inputs"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
