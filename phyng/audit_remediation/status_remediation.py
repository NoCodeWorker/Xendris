"""Status remediation classifier."""

from __future__ import annotations

from collections import Counter

from phyng.audit_remediation.schemas import StatusMappingRemediationRecord, StatusQuarantineRecord
from phyng.audit_remediation.status_quarantine import is_critical_status, quarantine_status


def classify_unmapped_statuses(status_permission_payload: dict) -> tuple[list[StatusMappingRemediationRecord], list[StatusQuarantineRecord]]:
    statuses = status_permission_payload.get("unmapped_statuses", [])
    issue_counts = Counter(issue.get("evidence") for issue in status_permission_payload.get("issues", []))
    records: list[StatusMappingRemediationRecord] = []
    quarantine: list[StatusQuarantineRecord] = []
    for status in statuses:
        critical = is_critical_status(status)
        if critical:
            action = "QUARANTINE_STATUS"
            remediation_status = "CLASSIFIED_QUARANTINED"
            permission = "CLAIM_BLOCKED"
            evidence = "HEURISTIC_ONLY"
            support = "UNSUPPORTED"
            quarantine.append(quarantine_status(status))
            notes = ["Critical marker detected; status cannot unlock claims until mapped or deprecated."]
        elif _looks_deprecated(status):
            action = "DEPRECATE_STATUS"
            remediation_status = "CLASSIFIED_DEPRECATED"
            permission = "REVIEW_REQUIRED"
            evidence = "HEURISTIC_ONLY"
            support = "UNSUPPORTED"
            notes = ["Historical or legacy-looking status; may remain in reports but not as active campaign status."]
        else:
            action = "KEEP_UNMAPPED_INFO_ONLY"
            remediation_status = "CLASSIFIED_RESIDUAL_DEBT"
            permission = "REVIEW_REQUIRED"
            evidence = "HEURISTIC_ONLY"
            support = "UNSUPPORTED"
            notes = ["Noncritical status classified as bounded residual mapping debt."]
        records.append(
            StatusMappingRemediationRecord(
                status=status,
                source_location="data/audits/phygn_status_permission_matrix_v4_4_1.json",
                occurrence_count=issue_counts.get(status, 1),
                current_mapping_state="UNMAPPED",
                proposed_mapping_action=action,
                canonical_permission=permission,
                evidence_level=evidence,
                support_level=support,
                risk_level="SCIENTIFIC_RISK",
                allowed_claims=["Historical reporting", "Audit remediation tracking"],
                blocked_claims=["Claim permission", "Physical validation", "PredictiveGain claim"],
                required_next_gate="v4.4.3 remaining status mapping" if action != "QUARANTINE_STATUS" else "explicit conservative mapping or deprecation",
                remediation_status=remediation_status,
                notes=notes,
            )
        )
    return records, quarantine


def critical_unmapped_after_remediation(records: list[StatusMappingRemediationRecord]) -> int:
    return sum(1 for record in records if is_critical_status(record.status) and record.proposed_mapping_action not in {"QUARANTINE_STATUS", "DEPRECATE_STATUS", "MAP_TO_EXISTING_CANONICAL_PERMISSION", "ALIAS_TO_CANONICAL_STATUS"})


def deprecated_status_can_be_active(record: StatusMappingRemediationRecord) -> bool:
    return record.proposed_mapping_action == "DEPRECATE_STATUS" and record.remediation_status != "CLASSIFIED_DEPRECATED"


def _looks_deprecated(status: str) -> bool:
    upper = status.upper()
    return any(marker in upper for marker in ("LEGACY", "OLD", "DEPRECATED", "NOT_APPLICABLE"))
