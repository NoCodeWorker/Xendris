"""Campaign wrapper for v5.7 visibility/decoherence dataset expansion."""

from __future__ import annotations

from pathlib import Path

from phyng.dataset_expansion.campaign import run_frontera_c_visibility_decoherence_dataset_expansion_campaign


def run(root: str | Path = "."):
    return run_frontera_c_visibility_decoherence_dataset_expansion_campaign(root)


if __name__ == "__main__":
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(root=".")
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "accepted_ytrue_count_total": len(result.accepted_ytrue),
            "independent_source_count": result.dataset.source_count if result.dataset else 0,
            "allowed_next_phase": result.next_gate_decision.get("allowed_next_phase"),
        }
    )
