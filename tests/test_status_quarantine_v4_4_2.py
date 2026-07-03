from __future__ import annotations

from phyng.audit_remediation.status_quarantine import quarantine_status, quarantined_status_can_gate_claim
from phyng.audit_remediation.status_remediation import classify_unmapped_statuses, deprecated_status_can_be_active


def test_quarantined_status_cannot_gate_claim() -> None:
    record = quarantine_status("PHI_GRADIENT_VALIDATED")

    assert quarantined_status_can_gate_claim(record) is False


def test_deprecated_status_cannot_be_active_campaign_status() -> None:
    records, _ = classify_unmapped_statuses({"unmapped_statuses": ["ACTION_NOT_APPLICABLE"], "issues": []})

    assert records[0].proposed_mapping_action == "DEPRECATE_STATUS"
    assert deprecated_status_can_be_active(records[0]) is False
