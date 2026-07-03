"""Campaign wrapper for v4.9 source identity preflight."""

from __future__ import annotations

from pathlib import Path

from phyng.source_identity_preflight.campaign import run_phygn_source_identity_preflight_campaign


def run(root: str | Path = "."):
    return run_phygn_source_identity_preflight_campaign(root)


if __name__ == "__main__":
    result = run_phygn_source_identity_preflight_campaign(root=".")
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "candidate_count": result.gate.candidate_count,
            "passed_candidate_count": result.gate.passed_candidate_count,
            "partial_candidate_count": result.gate.partial_candidate_count,
            "failed_candidate_count": result.gate.failed_candidate_count,
            "selected_candidate_family": result.gate.selected_candidate_family,
            "allowed_next_phase": result.gate.allowed_next_phase,
        }
    )
