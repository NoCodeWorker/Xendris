"""Continuation gate for v4.4.2 remediation."""

from __future__ import annotations

from phyng.audit_remediation.schemas import AcceptedResidualAuditDebt, ContinuationGate


def compute_continuation_gate(
    blocker_count: int,
    critical_unmapped_status_count: int,
    open_claim_leakage_blocker_count: int,
    residual_debt: list[AcceptedResidualAuditDebt],
) -> ContinuationGate:
    if blocker_count:
        status = "RESUME_BLOCKED_PENDING_CLAIM_LEAKAGE_FIX"
        can_continue = False
        required = ["Resolve blocker audit findings."]
        next_phase = "v4.4.3 — Blocking Logic Remediation Sprint"
    elif critical_unmapped_status_count:
        status = "RESUME_BLOCKED_PENDING_STATUS_MAPPING"
        can_continue = False
        required = ["Map, quarantine, or deprecate every critical unmapped status."]
        next_phase = "v4.4.3 — Remaining Status Mapping & Test Hardening"
    elif open_claim_leakage_blocker_count:
        status = "RESUME_BLOCKED_PENDING_CLAIM_LEAKAGE_FIX"
        can_continue = False
        required = ["Rewrite or move claim leakage blockers into blocked-claims sections."]
        next_phase = "v4.4.3 — Blocking Logic Remediation Sprint"
    elif residual_debt:
        status = "RESUME_ALLOWED_WITH_RESIDUAL_DEBT"
        can_continue = True
        required = ["Review accepted residual audit debt before v4.5 claim interpretation."]
        next_phase = "v4.5 — Public Dataset Acquisition & Table/Figure Review Continuation"
    else:
        status = "RESUME_ALLOWED"
        can_continue = True
        required = []
        next_phase = "v4.5 — Public Dataset Acquisition & Table/Figure Review Continuation"
    return ContinuationGate(
        gate_status=status,
        can_continue_pipeline=can_continue,
        recommended_next_phase=next_phase,
        required_before_v4_5=required,
        accepted_residual_debt_ref="data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json",
        allowed_claims=["Audit remediation was performed.", "Pipeline continuation was computed by gate."],
        blocked_claims=[
            "Remediation validates PHI_GRADIENT.",
            "Remediation creates y_true.",
            "Remediation creates PredictiveGain.",
            "Remediation closes SLOT_4 debt.",
        ],
        notes=["Continuation permission is operational only; scientific claims remain blocked by existing gates."],
    )
