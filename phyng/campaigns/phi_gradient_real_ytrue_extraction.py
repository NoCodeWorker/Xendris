"""Campaign wrapper for PHI_GRADIENT v4.3 Real y_true Extraction & Assembly."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from phyng.ytrue_extraction import campaign as ye_campaign


def run_phi_gradient_real_ytrue_extraction_campaign(
    root: str | Path = ".",
) -> dict[str, Any]:
    repo_root = Path(root)

    # Run campaign
    campaign_result = ye_campaign.run_phi_gradient_real_ytrue_extraction_campaign(repo_root)

    return {
        "campaign_id": "PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3",
        "status": campaign_result.status,
        "ytrue_extraction": campaign_result.model_dump(mode="json"),
        "report_paths": campaign_result.report_paths,
    }


if __name__ == "__main__":
    res = run_phi_gradient_real_ytrue_extraction_campaign(root=".")
    print(
        {
            "status": res["status"],
            "accepted_records": res["ytrue_extraction"]["gate_result"]["assembled_y_true_dataset"]["y_true_record_count"],
            "blocked_targets": len(res["ytrue_extraction"]["gate_result"]["blocked_y_true_targets"]),
            "ready_for_predictive_gain": res["ytrue_extraction"]["gate_result"]["assembled_y_true_dataset"]["ready_for_predictive_gain"],
        }
    )
