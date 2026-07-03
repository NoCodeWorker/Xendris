"""Core compatibility grammar for Phygn status interpretation."""

from phyng.core.permissions import CanonicalPermission
from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.evidence_levels import CanonicalEvidenceLevel
from phyng.core.support_levels import CanonicalSupportLevel
from phyng.core.risk_levels import CanonicalRiskLevel
from phyng.core.status_mapping import (
    CanonicalAuditEventType,
    CanonicalStatusRecord,
    STATUS_COMPATIBILITY_MAP,
)
from phyng.core.compatibility import (
    get_blocked_reasons,
    get_canonical_permission,
    is_blocked,
    normalize_status,
    requires_human_review,
)
from phyng.core.report_contract import (
    CanonicalReportContract,
    append_canonical_status_section,
    build_report_contract,
    render_canonical_report_section,
)

__all__ = [
    "CanonicalPermission",
    "CanonicalBlockedReason",
    "CanonicalEvidenceLevel",
    "CanonicalSupportLevel",
    "CanonicalRiskLevel",
    "CanonicalAuditEventType",
    "CanonicalStatusRecord",
    "CanonicalReportContract",
    "STATUS_COMPATIBILITY_MAP",
    "normalize_status",
    "get_canonical_permission",
    "get_blocked_reasons",
    "is_blocked",
    "requires_human_review",
    "build_report_contract",
    "render_canonical_report_section",
    "append_canonical_status_section",
]
