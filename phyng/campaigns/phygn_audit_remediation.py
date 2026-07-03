"""Campaign wrapper for PHYGN audit remediation v4.4.2."""

from __future__ import annotations

from pathlib import Path

from phyng.audit_remediation.campaign import run_phygn_audit_remediation_campaign


def run(root: str | Path = "."):
    return run_phygn_audit_remediation_campaign(root)


if __name__ == "__main__":
    result = run_phygn_audit_remediation_campaign(root=".")
    gate = result.continuation_gate
    print(
        {
            "status": result.status,
            "inputs_loaded": result.inputs_loaded,
            "status_mapping_records": len(result.status_mapping_records),
            "quarantine_records": len(result.quarantine_records),
            "residual_debt_count": len(result.residual_debt),
            "continuation_gate": gate.gate_status if gate else None,
            "can_continue_pipeline": gate.can_continue_pipeline if gate else False,
        }
    )
