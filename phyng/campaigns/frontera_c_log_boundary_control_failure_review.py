"""Campaign wrapper for v5.6 LOG_BOUNDARY control failure review."""

from __future__ import annotations

from pathlib import Path

from phyng.frontera_c_disposition.campaign import run_frontera_c_log_boundary_control_failure_review_campaign


def run(root: str | Path = "."):
    return run_frontera_c_log_boundary_control_failure_review_campaign(root)


if __name__ == "__main__":
    result = run_frontera_c_log_boundary_control_failure_review_campaign(root=".")
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "primary_disposition": result.disposition.primary_disposition if result.disposition else None,
            "allowed_next_phase": result.next_direction.allowed_next_phase if result.next_direction else None,
        }
    )
