"""Campaign wrapper for PHI_GRADIENT v4.1 Debt-Bounded Model Comparison."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.model_comparison import campaign as mc_campaign


def run_phi_gradient_debt_bounded_model_comparison_campaign(
    root: str | Path = ".",
) -> dict[str, Any]:
    repo_root = Path(root)

    # Run campaign
    campaign_result = mc_campaign.run_phi_gradient_debt_bounded_model_comparison_campaign(repo_root)


    # Write next gate inputs JSON if successful
    if campaign_result.status != "PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK":
        next_gate_inputs_file = repo_root / "data" / "model_comparison" / "phi_gradient_v4_1_next_gate_inputs.json"
        next_gate_inputs_file.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "registry_path": "data/model_comparison/phi_gradient_model_registry_v4_1.json",
            "predictions_path": "data/model_comparison/phi_gradient_model_predictions_v4_1.json",
            "comparison_scores_path": "data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json",
            "negative_control_results_path": "data/model_comparison/phi_gradient_negative_control_results_v4_1.json",
            "claim_permission_update_path": "data/model_comparison/phi_gradient_claim_permission_update_v4_1.json",
            "status": campaign_result.status,
            "ready_for_next_phase": campaign_result.status == "PHI_GRADIENT_MODEL_COMPARISON_COMPLETED",
            "recommended_next_phase": "v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan",
            "notes": [
                "Model comparison v4.1 is completed.",
                "Real observed data y_true remains missing.",
                "Physical and gradient claims remain blocked.",
            ],
        }

        _write_json(next_gate_inputs_file, payload)

    return {
        "campaign_id": "PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1",
        "status": campaign_result.status,
        "model_comparison": campaign_result.model_dump(mode="json"),
        "report_paths": campaign_result.report_paths,
        "next_gate_inputs_path": "data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json"
        if campaign_result.status != "PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK"
        else None,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    res = run_phi_gradient_debt_bounded_model_comparison_campaign(root=".")
    print(
        {
            "status": res["status"],
            "next_gate_inputs_path": res["next_gate_inputs_path"],
            "model_count": len(res["model_comparison"]["gate_result"]["models"]),
            "prediction_count": len(res["model_comparison"]["gate_result"]["predictions"]),
        }
    )
