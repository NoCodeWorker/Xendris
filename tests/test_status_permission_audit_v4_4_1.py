from __future__ import annotations

from phyng.core.status_mapping import STATUS_COMPATIBILITY_MAP
from phyng.full_suite_logic_audit.status_permission_audit import audit_status_permission_matrix


def test_status_permission_matrix_has_no_unmapped_statuses() -> None:
    observed = set(STATUS_COMPATIBILITY_MAP)

    result = audit_status_permission_matrix(observed)

    assert result.unmapped_statuses == []


def test_status_permission_matrix_flags_unknown_status() -> None:
    result = audit_status_permission_matrix({"PHYGN_UNKNOWN_STATUS_FOR_TEST"})

    assert result.unmapped_statuses == ["PHYGN_UNKNOWN_STATUS_FOR_TEST"]
    assert result.issues[0].category == "UNMAPPED_STATUS"
