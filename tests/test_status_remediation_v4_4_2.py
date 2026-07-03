from __future__ import annotations

from phyng.audit_remediation.status_remediation import classify_unmapped_statuses, critical_unmapped_after_remediation


def test_critical_unmapped_status_cannot_unlock_claim() -> None:
    payload = {"unmapped_statuses": ["PHI_GRADIENT_VALIDATED"], "issues": []}

    records, quarantine = classify_unmapped_statuses(payload)

    assert records[0].proposed_mapping_action == "QUARANTINE_STATUS"
    assert records[0].canonical_permission == "CLAIM_BLOCKED"
    assert quarantine[0].may_gate_claims is False


def test_status_hardening_reduces_or_classifies_unmapped_statuses() -> None:
    payload = {"unmapped_statuses": ["BENCHMARK_RANGE_CONTROL", "PHI_GRADIENT_VALIDATED"], "issues": []}

    records, _ = classify_unmapped_statuses(payload)

    assert critical_unmapped_after_remediation(records) == 0
    assert all(record.remediation_status.startswith("CLASSIFIED_") for record in records)
