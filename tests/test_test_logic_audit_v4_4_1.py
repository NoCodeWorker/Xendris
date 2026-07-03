from __future__ import annotations

from phyng.full_suite_logic_audit.test_logic_audit import audit_test_file


def test_test_logic_audit_flags_status_only_test() -> None:
    source = """
def test_status_only():
    result = run()
    assert result.status == "DONE"
"""

    issues = audit_test_file(source)

    assert any(issue.category == "STATUS_ONLY_TEST" for issue in issues)


def test_test_logic_audit_allows_behavior_assertion() -> None:
    source = """
def test_status_with_gate():
    result = run()
    assert result.status == "DONE"
    assert "PHI_GRADIENT is validated." in result.blocked_claims
"""

    issues = audit_test_file(source)

    assert issues == []
