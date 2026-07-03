from __future__ import annotations

from phyng.audit_remediation.test_hardening import build_test_hardening_plan, status_only_tests_are_classified


def test_status_only_tests_are_classified() -> None:
    payload = {
        "issues": [
            {
                "path": "tests/test_model_comparison.py",
                "message": "Test `test_status_only` appears to assert status.",
                "category": "STATUS_ONLY_TEST",
            }
        ]
    }

    plan = build_test_hardening_plan(payload)

    assert status_only_tests_are_classified(plan)
    assert plan[0].required_negative_fixture == "predictive_gain_without_ytrue_fixture"
