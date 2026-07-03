from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.compatibility import get_canonical_permission, normalize_status
from phyng.core.permissions import CanonicalPermission
from phyng.core.status_mapping import STATUS_COMPATIBILITY_MAP


def test_known_business_status_maps_to_scale_blocked():
    record = normalize_status("BUSINESS_BLOCKED_NO_WTP")

    assert record.domain_status == "BUSINESS_BLOCKED_NO_WTP"
    assert record.canonical_permission == CanonicalPermission.SCALE_BLOCKED
    assert CanonicalBlockedReason.NO_PAYMENT_SIGNAL in record.blocked_reasons


def test_outside_claim_boundary_maps_to_claim_blocked():
    assert get_canonical_permission("OUTSIDE_CLAIM_BOUNDARY") == CanonicalPermission.CLAIM_BLOCKED


def test_falsehood_boundary_maps_to_claim_blocked_with_contradiction():
    record = normalize_status("CROSSED_FALSEHOOD_BOUNDARY")

    assert record.canonical_permission == CanonicalPermission.CLAIM_BLOCKED
    assert CanonicalBlockedReason.CONTRADICTION in record.blocked_reasons


def test_undetectable_delta_maps_to_claim_blocked():
    record = normalize_status("UNDETECTABLE_SYNTHETIC_DELTA")

    assert record.canonical_permission == CanonicalPermission.CLAIM_BLOCKED
    assert CanonicalBlockedReason.UNDETECTABLE_DELTA in record.blocked_reasons


def test_validated_limited_maps_to_limited_allowed():
    record = normalize_status("BUSINESS_VALIDATED_LIMITED")

    assert record.canonical_permission == CanonicalPermission.SCALE_ALLOWED
    assert CanonicalBlockedReason.NO_BLOCK in record.blocked_reasons


def test_required_prompt_statuses_are_mapped():
    required = {
        "BUSINESS_BLOCKED_NO_WTP",
        "BUSINESS_BLOCKED_NO_CUSTOMER",
        "BUSINESS_VALIDATED_LIMITED",
        "UNIT_ECONOMICS_NEGATIVE",
        "WTP_7_PAID_PILOT",
        "OUTSIDE_CLAIM_BOUNDARY",
        "CROSSED_OVERCLAIM_BOUNDARY",
        "CROSSED_FALSEHOOD_BOUNDARY",
        "ACTION_BLOCKED",
        "AUTOMATED_EXECUTION_ALLOWED",
        "UNDETECTABLE_SYNTHETIC_DELTA",
        "DETECTABLE_SYNTHETIC_DELTA",
        "FAIL_NO_SOURCE_SUPPORT",
        "FAIL_NO_BENCHMARK",
        "SURVIVES_AS_TOY_NEGATIVE_CONTROL",
        "SOURCE_BACKED_LIMITED",
        "BENCHMARK_SUPPORTED",
        "FILTER_NOT_PREDICTIVELY_USEFUL_YET",
        "COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE",
    }

    assert required.issubset(STATUS_COMPATIBILITY_MAP)
