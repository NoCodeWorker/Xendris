"""Campaign wrapper for PHI_GRADIENT v4.2 Observable Dataset Normalization & y_true Plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.observable_dataset import campaign as od_campaign


def run_phi_gradient_observable_ytrue_plan_campaign(
    root: str | Path = ".",
) -> dict[str, Any]:
    repo_root = Path(root)

    # Run campaign
    campaign_result = od_campaign.run_phi_gradient_observable_ytrue_plan_campaign(repo_root)

    # Write next gate inputs JSON if successful
    if campaign_result.status != "PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON":
        next_gate_inputs_file = repo_root / "data" / "observables" / "phi_gradient_v4_2_next_gate_inputs.json"
        next_gate_inputs_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "schema_path": "data/observables/phi_gradient_observable_schema_v4_2.json",
            "normalized_targets_path": "data/observables/phi_gradient_normalized_observable_targets_v4_2.json",
            "y_true_acquisition_plan_path": "data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json",
            "dataset_source_registry_path": "data/observables/phi_gradient_dataset_source_registry_v4_2.json",
            "measurement_readiness_matrix_path": "data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json",
            "quality_control_rules_path": "data/observables/phi_gradient_quality_control_rules_v4_2.json",
            "status": campaign_result.status,
            "ready_for_next_phase": campaign_result.status == "PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY",
            "recommended_next_phase": "v4.3 — Real y_true Extraction & Dataset Assembly",
            "notes": [
                "Observable targets normalized.",
                "y_true acquisition plan ready.",
                "PredictiveGain remains undefined.",
                "SLOT_4 debt remains open blocking.",
            ],
        }

        _write_json(next_gate_inputs_file, payload)

    return {
        "campaign_id": "PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2",
        "status": campaign_result.status,
        "observable_dataset": campaign_result.model_dump(mode="json"),
        "report_paths": campaign_result.report_paths,
        "next_gate_inputs_path": "data/observables/phi_gradient_v4_2_next_gate_inputs.json"
        if campaign_result.status != "PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON"
        else None,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    res = run_phi_gradient_observable_ytrue_plan_campaign(root=".")
    print(
        {
            "status": res["status"],
            "next_gate_inputs_path": res["next_gate_inputs_path"],
            "target_count": len(res["observable_dataset"]["gate_result"]["normalized_targets"]),
            "readiness_rows": len(res["observable_dataset"]["gate_result"]["readiness_matrix"]),
        }
    )
