from __future__ import annotations

from phyng.audit_remediation.residual_debt import build_residual_debt, residual_debt_is_bounded
from phyng.audit_remediation.status_remediation import classify_unmapped_statuses


def test_accepted_residual_debt_requires_next_review() -> None:
    records, _ = classify_unmapped_statuses({"unmapped_statuses": ["BENCHMARK_RANGE_CONTROL"], "issues": []})

    debt = build_residual_debt(records, [])

    assert debt[0].next_review_phase
    assert residual_debt_is_bounded(debt)
