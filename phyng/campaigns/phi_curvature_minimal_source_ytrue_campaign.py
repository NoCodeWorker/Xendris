"""Campaign wrapper for PHI_CURVATURE minimal source/y_true v4.8."""

from __future__ import annotations

from pathlib import Path

from phyng.phi_curvature_minimal_campaign.campaign import run_phi_curvature_minimal_source_ytrue_campaign


def run(root: str | Path = "."):
    return run_phi_curvature_minimal_source_ytrue_campaign(root)


if __name__ == "__main__":
    result = run_phi_curvature_minimal_source_ytrue_campaign(root=".")
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "source_resolution_count": len(result.source_resolution),
            "accepted_ytrue_count": len(result.accepted_ytrue),
            "rejected_ytrue_count": len(result.rejected_ytrue),
            "threshold_reached": result.dataset.threshold_reached,
            "allowed_next_phase": result.next_gate.allowed_next_phase,
        }
    )
