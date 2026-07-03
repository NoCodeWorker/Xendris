from __future__ import annotations

from phyng.full_suite_logic_audit.metric_integrity_audit import (
    audit_negative_control_payload,
    audit_predictive_gain_payload,
    audit_ytrue_payload,
)


def test_metric_audit_blocks_benchmark_score_as_predictive_gain() -> None:
    issues = audit_predictive_gain_payload({"benchmark_score": 0.8, "predictive_gain": 0.8})

    assert any(issue.category == "BENCHMARK_SCORE_AS_PREDICTIVE_GAIN" for issue in issues)


def test_ytrue_audit_blocks_value_without_provenance() -> None:
    payload = {"y_true_id": "Y-1", "value": 1.2, "unit": "s"}

    issues = audit_ytrue_payload(payload)

    assert any(issue.category == "YTRUE_WITHOUT_PROVENANCE" for issue in issues)


def test_negative_control_audit_requires_claim_impact() -> None:
    payload = {"control_id": "NEGATIVE-CONTROL-1", "status": "ACTIVE"}

    issues = audit_negative_control_payload(payload)

    assert any(issue.category == "NEGATIVE_CONTROL_WITHOUT_CLAIM_IMPACT" for issue in issues)
