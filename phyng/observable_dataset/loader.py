"""Load v4.2 observable dataset and y_true plan inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.observable_dataset.schemas import ObservableYTrueInputs

INPUT_PATHS = {
    "model_registry": Path("data/model_comparison/phi_gradient_model_registry_v4_1.json"),
    "model_predictions": Path("data/model_comparison/phi_gradient_model_predictions_v4_1.json"),
    "benchmark_scores": Path("data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json"),
    "negative_control_results": Path("data/model_comparison/phi_gradient_negative_control_results_v4_1.json"),
    "claim_permission_update": Path("data/model_comparison/phi_gradient_claim_permission_update_v4_1.json"),
    "next_gate_inputs": Path("data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json"),
    "benchmark_rows": Path("data/benchmarks/phi_gradient_benchmark_rows_v4_0.json"),
    "observable_alignment": Path("data/benchmarks/phi_gradient_observable_alignment_v4_0.json"),
    "debt_object": Path("data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json"),
}


def load_observable_ytrue_inputs(root: str | Path = ".") -> ObservableYTrueInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return ObservableYTrueInputs(
            blocked_reason="PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON"
        )
    return ObservableYTrueInputs(
        model_registry=_load_json(repo_root / INPUT_PATHS["model_registry"]),
        model_predictions=_load_json(repo_root / INPUT_PATHS["model_predictions"]),
        benchmark_scores=_load_json(repo_root / INPUT_PATHS["benchmark_scores"]),
        negative_control_results=_load_json(repo_root / INPUT_PATHS["negative_control_results"]),
        claim_permission_update=_load_json(repo_root / INPUT_PATHS["claim_permission_update"]),
        next_gate_inputs=_load_json(repo_root / INPUT_PATHS["next_gate_inputs"]),
        benchmark_rows=_load_json(repo_root / INPUT_PATHS["benchmark_rows"]),
        observable_alignment=_load_json(repo_root / INPUT_PATHS["observable_alignment"]),
        debt_object=_load_json(repo_root / INPUT_PATHS["debt_object"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
