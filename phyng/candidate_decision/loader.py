"""Loader module for v4.6 candidate freeze review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

class MissingFreezeDecisionError(FileNotFoundError):
    """Raised when the v4.5 freeze decision file is missing."""
    pass

def load_candidate_decision_inputs(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root)

    # Required files
    files_to_load = {
        "freeze_decision_v4_5": "data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json",
        "next_predictive_gain_inputs_v4_5": "data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json",
        "assembled_dataset_v4_5": "data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json",
        "table_review_results_v4_5": "data/external_evidence/phi_gradient_table_review_results_v4_5.json",
        "supplementary_search_results_v4_5": "data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json",
        "public_dataset_search_results_v4_5": "data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json",
        "external_y_true_accepted_v4_5": "data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json",
        "external_y_true_rejected_v4_5": "data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json",
        "external_evidence_audit_trail_v4_5": "data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json",
        "benchmark_comparison_scores_v4_1": "data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json",
        "debt_slot4": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        "continuation_gate": "data/audits/remediation/phygn_v4_4_2_continuation_gate.json",
    }

    loaded_data = {}
    
    # Check freeze decision first to raise specific error
    freeze_decision_path = root_path / files_to_load["freeze_decision_v4_5"]
    if not freeze_decision_path.exists():
        raise MissingFreezeDecisionError(f"Missing freeze decision file: {files_to_load['freeze_decision_v4_5']}")

    for key, rel_path in files_to_load.items():
        abs_path = root_path / rel_path
        if not abs_path.exists():
            raise FileNotFoundError(f"Missing required input file: {rel_path}")
        with open(abs_path, "r", encoding="utf-8") as f:
            loaded_data[key] = json.load(f)

    # Optional historical directories presence
    loaded_data["closed_loop_dir_exists"] = (root_path / "data/closed_loop").is_dir()
    loaded_data["synthetic_benchmark_dir_exists"] = (root_path / "data/synthetic_benchmark_design").is_dir()
    loaded_data["source_pressure_dir_exists"] = (root_path / "data/source_pressure").is_dir()
    loaded_data["benchmarks_dir_exists"] = (root_path / "data/benchmarks").is_dir()

    return loaded_data
