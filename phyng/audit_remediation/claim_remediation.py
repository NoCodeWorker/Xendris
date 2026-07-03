"""Claim leakage remediation records."""

from __future__ import annotations

from phyng.audit_remediation.schemas import ClaimLeakageRemediationRecord


def build_claim_remediation_records(claim_payload: dict) -> list[ClaimLeakageRemediationRecord]:
    records: list[ClaimLeakageRemediationRecord] = []
    for issue in claim_payload.get("issues", []):
        records.append(
            ClaimLeakageRemediationRecord(
                leakage_id=issue.get("issue_id", "UNKNOWN-LEAKAGE"),
                artifact_path=issue.get("path", ""),
                claim_text=issue.get("evidence") or issue.get("message", ""),
                leakage_status="NO_OPEN_BLOCKER_IN_V4_4_1" if issue.get("severity") != "BLOCKER" else "OPEN_BLOCKER",
                severity=issue.get("severity", "UNKNOWN"),
                remediation_action="ACCEPT_AS_NONBLOCKING_WITH_NOTE" if issue.get("severity") != "BLOCKER" else "MOVE_TO_BLOCKED_CLAIMS",
                rewritten_claim=None,
                final_status="ACCEPTED_RESIDUAL" if issue.get("severity") != "BLOCKER" else "BLOCKS_NEXT_GATE",
                blocks_next_gate=issue.get("severity") == "BLOCKER",
            )
        )
    return records
