# Phygn v4.4.2 — Status Mapping & Quarantine Protocol

## 0. Purpose

This document defines how to remediate `unmapped_status_count = 160`.

---

## 1. Status mapping remediation

Create:

```txt
data/audits/remediation/phygn_status_mapping_remediation_v4_4_2.json
```

Schema:

```python
class StatusMappingRemediationRecord(BaseModel):
    status: str
    source_location: str
    occurrence_count: int
    current_mapping_state: str
    proposed_mapping_action: str
    canonical_permission: str | None
    evidence_level: str | None
    support_level: str | None
    risk_level: str | None
    allowed_claims: list[str]
    blocked_claims: list[str]
    required_next_gate: str | None
    remediation_status: str
    notes: list[str]
```

---

## 2. Mapping actions

Allowed actions:

```txt
MAP_TO_EXISTING_CANONICAL_PERMISSION
MAP_TO_NEW_CANONICAL_PERMISSION
QUARANTINE_STATUS
DEPRECATE_STATUS
ALIAS_TO_CANONICAL_STATUS
KEEP_UNMAPPED_INFO_ONLY
```

---

## 3. Quarantine register

Create:

```txt
data/audits/remediation/phygn_status_quarantine_register_v4_4_2.json
```

Schema:

```python
class StatusQuarantineRecord(BaseModel):
    status: str
    reason: str
    severity: str
    may_appear_in_reports: bool
    may_gate_claims: bool
    may_unlock_next_phase: bool
    replacement_status: str | None
    required_remediation: str
```

Rule:

```txt
A quarantined status may appear in historical reports.
A quarantined status may not grant claim permission.
```

---

## 4. Critical statuses

Critical statuses are any statuses related to:

```txt
VALIDATED
PREDICTIVE_GAIN
YTRUE_AVAILABLE
SOURCE_BACKED
PHYSICAL_CLAIM
GRADIENT_MECHANISM
SLOT4_RESOLVED
CLAIM_ALLOWED
```

Critical unmapped statuses must be either:

```txt
mapped
deprecated
quarantined
```

They cannot remain silently unmapped.

---

## 5. Mapping defaults

If status contains:

```txt
UNDEFINED
MISSING
BLOCKED
NO_YTRUE
NO_VALUES
REQUIRES_MANUAL
REQUIRES_REVIEW
```

default to:

```txt
Canonical Permission: REVIEW_REQUIRED or CLAIM_BLOCKED
Support Level: UNSUPPORTED or LIMITED
Risk Level: SCIENTIFIC_RISK
```

If status contains:

```txt
VALIDATED
READY_FOR_PREDICTIVE_GAIN
PREDICTIVE_GAIN
PHYSICAL
```

require explicit review.

---

## 6. Required tests

Create or update tests to verify:

```txt
no critical unmapped status can unlock a claim
quarantined statuses cannot gate claims
deprecated statuses cannot appear as active campaign status
all active statuses have canonical mapping
```

---

## 7. Final principle

```txt
A status is a permission-bearing object, not a label.
```
