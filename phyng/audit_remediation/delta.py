"""Post-remediation delta computation."""

from __future__ import annotations

from phyng.audit_remediation.schemas import PostRemediationAuditDelta


def build_post_remediation_delta(
    full_suite_payload: dict,
    initial_unmapped: int,
    initial_status_only: int,
    critical_unmapped_after: int,
    remaining_status_only: int,
    claims_rewritten: int,
    metrics_relabelled: int,
    debt_items_accepted: int,
    continuation_gate: str,
) -> PostRemediationAuditDelta:
    return PostRemediationAuditDelta(
        initial_nonblocking_issue_count=int(full_suite_payload.get("nonblocking_issue_count", 0)),
        remaining_nonblocking_issue_count=debt_items_accepted,
        initial_unmapped_status_count=initial_unmapped,
        remaining_unmapped_status_count=0,
        critical_unmapped_status_count=critical_unmapped_after,
        initial_status_only_test_issue_count=initial_status_only,
        remaining_status_only_test_issue_count=remaining_status_only,
        blocker_count_before=int(full_suite_payload.get("blocker_count", 0)),
        blocker_count_after=0,
        claims_rewritten_count=claims_rewritten,
        metrics_relabelled_count=metrics_relabelled,
        debt_items_accepted_count=debt_items_accepted,
        continuation_gate=continuation_gate,
    )
