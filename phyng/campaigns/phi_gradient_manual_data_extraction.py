"""Campaign wrapper for PHI_GRADIENT manual data extraction v4.4."""

from __future__ import annotations

from pathlib import Path

from phyng.manual_data_extraction.campaign import run_phi_gradient_manual_data_extraction_campaign


def run(root: str | Path = "."):
    return run_phi_gradient_manual_data_extraction_campaign(root)


if __name__ == "__main__":
    result = run_phi_gradient_manual_data_extraction_campaign(root=".")
    gate = result.gate_result
    print(
        {
            "status": result.status,
            "manual_queue_count": gate.manual_queue_count,
            "reviewed_count": gate.reviewed_count,
            "accepted_y_true_count": gate.accepted_y_true_count,
            "rejected_count": gate.rejected_count,
            "rerouted_count": gate.rerouted_count,
            "matched_prediction_count": gate.matched_prediction_count,
            "ready_for_predictive_gain": gate.ready_for_predictive_gain,
            "predictive_gain_status": gate.predictive_gain_status,
            "slot4_debt_status": gate.slot4_debt_status,
        }
    )
