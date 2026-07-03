"""Status quarantine policy."""

from __future__ import annotations

from phyng.audit_remediation.schemas import StatusQuarantineRecord


CRITICAL_MARKERS = (
    "VALIDATED",
    "PREDICTIVE_GAIN",
    "YTRUE_AVAILABLE",
    "SOURCE_BACKED",
    "PHYSICAL_CLAIM",
    "GRADIENT_MECHANISM",
    "SLOT4_RESOLVED",
    "CLAIM_ALLOWED",
    "BENCHMARK_SUPPORTED",
    "SUPPORTS_CANDIDATE",
    "SUPPORTS_COMPONENT",
)


def is_critical_status(status: str) -> bool:
    upper = status.upper()
    return any(marker in upper for marker in CRITICAL_MARKERS)


def quarantine_status(status: str) -> StatusQuarantineRecord:
    return StatusQuarantineRecord(
        status=status,
        reason="Critical unmapped permission-bearing status cannot safely govern claims.",
        severity="HIGH",
        may_appear_in_reports=True,
        may_gate_claims=False,
        may_unlock_next_phase=False,
        replacement_status=None,
        required_remediation="Map to a conservative canonical status or deprecate before active campaign use.",
    )


def quarantined_status_can_gate_claim(record: StatusQuarantineRecord) -> bool:
    return record.may_gate_claims or record.may_unlock_next_phase
