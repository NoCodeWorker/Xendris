"""Accepted residual audit debt register."""

from __future__ import annotations

from phyng.audit_remediation.schemas import (
    AcceptedResidualAuditDebt,
    StatusMappingRemediationRecord,
    TestHardeningPlanItem,
)


def build_residual_debt(
    status_records: list[StatusMappingRemediationRecord],
    test_plan: list[TestHardeningPlanItem],
) -> list[AcceptedResidualAuditDebt]:
    debts: list[AcceptedResidualAuditDebt] = []
    residual_statuses = [record for record in status_records if record.proposed_mapping_action in {"KEEP_UNMAPPED_INFO_ONLY", "DEPRECATE_STATUS"}]
    if residual_statuses:
        debts.append(
            AcceptedResidualAuditDebt(
                debt_id="RESIDUAL-STATUS-MAPPING-v4_4_2",
                source_issue_id="UNMAPPED-STATUS-GROUP",
                category="STATUS_MAPPING",
                severity="MEDIUM",
                reason_accepted="Noncritical statuses were classified and prevented from granting claim permissions.",
                owner="Phygn audit remediation",
                next_review_phase="v4.4.3 remaining status mapping",
                may_continue_pipeline=True,
                blocks_claims=["Physical validation", "PredictiveGain", "Gradient mechanism support"],
                does_not_block=["Remediation reporting", "Non-claim-bearing pipeline preparation"],
                notes=[f"{len(residual_statuses)} noncritical statuses remain as classified residual debt."],
            )
        )
    if test_plan:
        debts.append(
            AcceptedResidualAuditDebt(
                debt_id="RESIDUAL-TEST-HARDENING-v4_4_2",
                source_issue_id="STATUS-ONLY-TEST-GROUP",
                category="TEST_HARDENING",
                severity="MEDIUM",
                reason_accepted="Status-only tests were classified with required negative fixtures and scheduled for hardening.",
                owner="Phygn audit remediation",
                next_review_phase="v4.4.3 test hardening sprint",
                may_continue_pipeline=True,
                blocks_claims=["Scientific validation based only on passing tests"],
                does_not_block=["Continuing acquisition work under existing claim blocks"],
                notes=[f"{len(test_plan)} status-only tests remain scheduled."],
            )
        )
    return debts


def residual_debt_is_bounded(debts: list[AcceptedResidualAuditDebt]) -> bool:
    return all(debt.category and debt.owner and debt.next_review_phase and debt.blocks_claims for debt in debts)
