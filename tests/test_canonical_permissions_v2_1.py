from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.evidence_levels import CanonicalEvidenceLevel
from phyng.core.permissions import CanonicalPermission
from phyng.core.risk_levels import CanonicalRiskLevel
from phyng.core.support_levels import CanonicalSupportLevel


def test_canonical_permission_enum_contains_core_permissions():
    assert CanonicalPermission.CLAIM_BLOCKED.value == "CLAIM_BLOCKED"
    assert CanonicalPermission.SCALE_BLOCKED.value == "SCALE_BLOCKED"
    assert CanonicalPermission.REVIEW_REQUIRED.value == "REVIEW_REQUIRED"
    assert CanonicalBlockedReason.HUMAN_REVIEW_REQUIRED.value == "HUMAN_REVIEW_REQUIRED"
    assert CanonicalEvidenceLevel.NO_EVIDENCE.value == "NO_EVIDENCE"
    assert CanonicalSupportLevel.UNSUPPORTED.value == "UNSUPPORTED"
    assert CanonicalRiskLevel.BUSINESS_RISK.value == "BUSINESS_RISK"
