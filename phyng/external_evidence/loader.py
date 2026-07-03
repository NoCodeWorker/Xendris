"""Loader module for v4.5 external evidence sprint."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_evidence_sprint_inputs(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root)

    # Required files
    files_to_load = {
        "next_predictive_gain_inputs": "data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json",
        "assembled_dataset_v4_4": "data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json",
        "dataset_quality_report_v4_4": "data/y_true/phi_gradient_dataset_quality_report_v4_4.json",
        "manual_extraction_rejected_v4_4": "data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json",
        "manual_extraction_review_records_v4_4": "data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json",
        "public_dataset_lookup_queue_v4_3": "data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json",
        "supplementary_lookup_queue_v4_3": "data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json",
        "normalized_targets_v4_2": "data/observables/phi_gradient_normalized_observable_targets_v4_2.json",
        "model_predictions_v4_1": "data/model_comparison/phi_gradient_model_predictions_v4_1.json",
        "source_hashes_v3_6": "data/real_sources/source_hashes_v3_6.json",
        "debt_slot4": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        "continuation_gate": "data/audits/remediation/phygn_v4_4_2_continuation_gate.json",
        "accepted_residual_debt_v4_4_2": "data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json",
    }

    loaded_data = {}
    for key, rel_path in files_to_load.items():
        abs_path = root_path / rel_path
        if not abs_path.exists():
            # Trigger block if critical files are missing
            raise FileNotFoundError(f"Missing prior artifact: {rel_path}")
        with open(abs_path, "r", encoding="utf-8") as f:
            loaded_data[key] = json.load(f)

    # Directories to inspect
    loaded_data["pdfs_dir_exists"] = (root_path / "data/real_sources/pdfs").is_dir()
    loaded_data["supplementary_dir_exists"] = (root_path / "data/real_sources/supplementary").is_dir()
    loaded_data["external_datasets_dir_exists"] = (root_path / "data/external_datasets").is_dir()

    return loaded_data
