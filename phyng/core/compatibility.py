"""Compatibility helpers for domain status normalization."""

from __future__ import annotations

from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.evidence_levels import CanonicalEvidenceLevel
from phyng.core.permissions import CanonicalPermission
from phyng.core.status_mapping import (
    CanonicalAuditEventType,
    CanonicalStatusRecord,
    STATUS_COMPATIBILITY_MAP,
)
from phyng.core.support_levels import CanonicalSupportLevel


def normalize_status(domain_status: str, domain: str | None = None) -> CanonicalStatusRecord:
    record = STATUS_COMPATIBILITY_MAP.get(domain_status)
    if record is not None:
        if domain is None or record.domain == domain:
            return record.model_copy(deep=True)
        return record.model_copy(update={"domain": domain}, deep=True)

    return CanonicalStatusRecord(
        domain_status=domain_status,
        domain=domain or "unknown",
        canonical_permission=CanonicalPermission.REVIEW_REQUIRED,
        blocked_reasons=[CanonicalBlockedReason.HUMAN_REVIEW_REQUIRED],
        evidence_level=CanonicalEvidenceLevel.NO_EVIDENCE,
        support_level=CanonicalSupportLevel.UNSUPPORTED,
        blocked_uses=["Treating unknown status as permission"],
        next_actions=["Add the domain status to STATUS_COMPATIBILITY_MAP after review."],
        audit_event_type=CanonicalAuditEventType.UNKNOWN_STATUS_REVIEW_REQUIRED,
        notes="Unknown status fallback is intentionally conservative.",
    )


def get_canonical_permission(domain_status: str, domain: str | None = None) -> CanonicalPermission:
    return normalize_status(domain_status, domain).canonical_permission


def get_blocked_reasons(domain_status: str, domain: str | None = None) -> list[CanonicalBlockedReason]:
    return list(normalize_status(domain_status, domain).blocked_reasons)


def is_blocked(domain_status: str, domain: str | None = None) -> bool:
    permission = get_canonical_permission(domain_status, domain)
    return permission in {
        CanonicalPermission.CLAIM_BLOCKED,
        CanonicalPermission.ACTION_BLOCKED,
        CanonicalPermission.EXECUTION_BLOCKED,
        CanonicalPermission.SCALE_BLOCKED,
        CanonicalPermission.REVIEW_REQUIRED,
    }


def requires_human_review(domain_status: str, domain: str | None = None) -> bool:
    record = normalize_status(domain_status, domain)
    return (
        record.canonical_permission == CanonicalPermission.REVIEW_REQUIRED
        or CanonicalBlockedReason.HUMAN_REVIEW_REQUIRED in record.blocked_reasons
    )
