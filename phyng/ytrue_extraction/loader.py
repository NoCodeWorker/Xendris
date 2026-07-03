"""Load v4.3 y_true extraction campaign inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.ytrue_extraction.schemas import ExtractionInputs

INPUT_PATHS = {
    "observable_schema": Path("data/observables/phi_gradient_observable_schema_v4_2.json"),
    "normalized_targets": Path("data/observables/phi_gradient_normalized_observable_targets_v4_2.json"),
    "y_true_acquisition_plan": Path("data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json"),
    "dataset_source_registry": Path("data/observables/phi_gradient_dataset_source_registry_v4_2.json"),
    "measurement_readiness_matrix": Path("data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json"),
    "quality_control_rules": Path("data/observables/phi_gradient_quality_control_rules_v4_2.json"),
    "v4_2_next_gate_inputs": Path("data/observables/phi_gradient_v4_2_next_gate_inputs.json"),
    "benchmark_rows": Path("data/benchmarks/phi_gradient_benchmark_rows_v4_0.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
    "debt_object": Path("data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json"),
    "model_predictions": Path("data/model_comparison/phi_gradient_model_predictions_v4_1.json"),
}


def load_extraction_inputs(root: str | Path = ".") -> ExtractionInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return ExtractionInputs(
            blocked_reason="PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN"
        )
    return ExtractionInputs(
        observable_schema=_load_json(repo_root / INPUT_PATHS["observable_schema"]),
        normalized_targets=_load_json(repo_root / INPUT_PATHS["normalized_targets"]),
        y_true_acquisition_plan=_load_json(repo_root / INPUT_PATHS["y_true_acquisition_plan"]),
        dataset_source_registry=_load_json(repo_root / INPUT_PATHS["dataset_source_registry"]),
        measurement_readiness_matrix=_load_json(repo_root / INPUT_PATHS["measurement_readiness_matrix"]),
        quality_control_rules=_load_json(repo_root / INPUT_PATHS["quality_control_rules"]),
        v4_2_next_gate_inputs=_load_json(repo_root / INPUT_PATHS["v4_2_next_gate_inputs"]),
        benchmark_rows=_load_json(repo_root / INPUT_PATHS["benchmark_rows"]),
        source_hashes=_load_json(repo_root / INPUT_PATHS["source_hashes"]),
        debt_object=_load_json(repo_root / INPUT_PATHS["debt_object"]),
        model_predictions=_load_json(repo_root / INPUT_PATHS["model_predictions"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
