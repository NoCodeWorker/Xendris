"""Campaign wrapper for v5.7.1 targeted literature acquisition."""

from __future__ import annotations

from pathlib import Path

from phyng.source_acquisition.campaign import run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign


def run(root: str | Path = "."):
    return run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(root)


if __name__ == "__main__":
    result = run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(root=".")
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "resolved_candidate_source_count": result.next_gate_decision.get("resolved_candidate_source_count"),
            "download_required_count": result.next_gate_decision.get("download_required_count"),
            "allowed_next_phase": result.next_gate_decision.get("allowed_next_phase"),
        }
    )
