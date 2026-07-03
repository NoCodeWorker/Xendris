"""Campaign wrapper for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

from pathlib import Path

from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def run(root: str | Path = "."):
    return run_frontera_c_targeted_ytrue_extraction_campaign(root)


if __name__ == "__main__":
    result = run_frontera_c_targeted_ytrue_extraction_campaign(root=".")
    print(
        {
            "status": result.status,
            "candidate_count": len(result.candidates),
            "new_accepted_ytrue_count": len(result.accepted),
            "rejected_ytrue_count": len(result.rejected),
            "total_accepted_ytrue_count": result.next_gate_decision.get("total_accepted_ytrue_count"),
            "independent_source_count": result.next_gate_decision.get("independent_source_count"),
            "allowed_next_phase": result.next_gate_decision.get("allowed_next_phase"),
        }
    )
