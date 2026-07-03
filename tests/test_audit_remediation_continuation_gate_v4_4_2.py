from __future__ import annotations

from phyng.audit_remediation.continuation_gate import compute_continuation_gate
from phyng.audit_remediation.schemas import AcceptedResidualAuditDebt


def test_continuation_gate_blocks_critical_unmapped_statuses() -> None:
    gate = compute_continuation_gate(blocker_count=0, critical_unmapped_status_count=1, open_claim_leakage_blocker_count=0, residual_debt=[])

    assert gate.gate_status == "RESUME_BLOCKED_PENDING_STATUS_MAPPING"
    assert gate.can_continue_pipeline is False


def test_continuation_gate_allows_residual_debt_when_bounded() -> None:
    debt = AcceptedResidualAuditDebt(
        debt_id="D",
        source_issue_id="I",
        category="STATUS_MAPPING",
        severity="MEDIUM",
        reason_accepted="bounded",
        owner="audit",
        next_review_phase="v4.4.3",
        may_continue_pipeline=True,
        blocks_claims=["Physical validation"],
        does_not_block=["Preparation"],
    )

    gate = compute_continuation_gate(blocker_count=0, critical_unmapped_status_count=0, open_claim_leakage_blocker_count=0, residual_debt=[debt])

    assert gate.gate_status == "RESUME_ALLOWED_WITH_RESIDUAL_DEBT"
    assert gate.can_continue_pipeline is True
