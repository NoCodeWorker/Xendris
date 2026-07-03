"""Loader module for v4.7 PHI_CURVATURE accessibility screen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

class MissingPivotDecisionError(FileNotFoundError):
    """Raised when the v4.6 pivot decision file is missing."""
    pass

def load_screening_inputs(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root)

    # Required files
    files_to_load = {
        "selection_matrix_v4_6": "data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json",
        "pivot_decision_v4_6": "data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json",
        "method_only_redefinition_v4_6": "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json",
        "final_claim_permissions_v4_6": "data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json",
        "experiment_requirement_v4_6": "data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json",
        "debt_slot4": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
    }

    loaded_data = {}
    
    # Check pivot decision first to raise specific error
    pivot_decision_path = root_path / files_to_load["pivot_decision_v4_6"]
    if not pivot_decision_path.exists():
        raise MissingPivotDecisionError(f"Missing pivot decision file: {files_to_load['pivot_decision_v4_6']}")

    for key, rel_path in files_to_load.items():
        abs_path = root_path / rel_path
        if not abs_path.exists():
            raise FileNotFoundError(f"Missing required input file: {rel_path}")
        with open(abs_path, "r", encoding="utf-8") as f:
            loaded_data[key] = json.load(f)

    # Optional historical directories presence
    loaded_data["synthetic_benchmark_dir_exists"] = (root_path / "data/synthetic_benchmark_design").is_dir()
    loaded_data["closed_loop_dir_exists"] = (root_path / "data/closed_loop").is_dir()
    loaded_data["source_pressure_dir_exists"] = (root_path / "data/source_pressure").is_dir()
    loaded_data["benchmarks_dir_exists"] = (root_path / "data/benchmarks").is_dir()

    return loaded_data
