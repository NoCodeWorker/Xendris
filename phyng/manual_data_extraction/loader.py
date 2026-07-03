"""Load v4.4 manual extraction inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.manual_data_extraction.schemas import ManualExtractionInputs


INPUT_PATHS = {
    "manual_queue": Path("data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json"),
    "source_coverage_audit": Path("data/y_true/phi_gradient_source_coverage_audit_v4_3.json"),
    "ytrue_candidates": Path("data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json"),
    "previous_dataset": Path("data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json"),
    "blocked_targets": Path("data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json"),
    "previous_quality_report": Path("data/y_true/phi_gradient_dataset_quality_report_v4_3.json"),
    "previous_next_inputs": Path("data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json"),
    "normalized_targets": Path("data/observables/phi_gradient_normalized_observable_targets_v4_2.json"),
    "qc_rules": Path("data/observables/phi_gradient_quality_control_rules_v4_2.json"),
    "model_predictions": Path("data/model_comparison/phi_gradient_model_predictions_v4_1.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
    "slot4_debt": Path("data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json"),
}


def load_manual_extraction_inputs(root: str | Path = ".") -> ManualExtractionInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return ManualExtractionInputs(blocked_reason="PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE")
    queue_payload = _load_json(repo_root / INPUT_PATHS["manual_queue"])
    return ManualExtractionInputs(
        manual_queue=queue_payload.get("manual_table_extraction_queue", []),
        source_coverage_audit=_load_json(repo_root / INPUT_PATHS["source_coverage_audit"]),
        ytrue_candidates=_load_json(repo_root / INPUT_PATHS["ytrue_candidates"]),
        previous_dataset=_load_json(repo_root / INPUT_PATHS["previous_dataset"]),
        blocked_targets=_load_json(repo_root / INPUT_PATHS["blocked_targets"]),
        previous_quality_report=_load_json(repo_root / INPUT_PATHS["previous_quality_report"]),
        previous_next_inputs=_load_json(repo_root / INPUT_PATHS["previous_next_inputs"]),
        normalized_targets=_load_json(repo_root / INPUT_PATHS["normalized_targets"]),
        qc_rules=_load_json(repo_root / INPUT_PATHS["qc_rules"]),
        model_predictions=_load_json(repo_root / INPUT_PATHS["model_predictions"]),
        source_hashes=_load_json(repo_root / INPUT_PATHS["source_hashes"]),
        slot4_debt=_load_json(repo_root / INPUT_PATHS["slot4_debt"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
