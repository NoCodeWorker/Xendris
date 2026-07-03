"""Campaign wrapper for PHYGN full-suite logic audit v4.4.1."""

from __future__ import annotations

from pathlib import Path

from phyng.full_suite_logic_audit.campaign import run_phygn_full_suite_logic_audit_campaign


def run(root: str | Path = "."):
    return run_phygn_full_suite_logic_audit_campaign(root)


if __name__ == "__main__":
    result = run_phygn_full_suite_logic_audit_campaign(root=".")
    print(
        {
            "status": result.status,
            "blocker_count": result.blocker_count,
            "nonblocking_issue_count": result.nonblocking_issue_count,
            "can_continue_pipeline": result.remediation_plan.can_continue_pipeline,
            "gate_status": result.remediation_plan.gate_status,
        }
    )
