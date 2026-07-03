# Phygn v2.1 — Compatibility Alias Layer

## 0. Purpose

v2.1 must improve consistency without breaking existing behavior.

The compatibility layer allows old domain statuses to keep working while exposing canonical interpretations.

---

## 1. No destructive renames

Do not rename existing statuses such as:

```txt
BUSINESS_BLOCKED_NO_WTP
UNDETECTABLE_SYNTHETIC_DELTA
OUTSIDE_CLAIM_BOUNDARY
ACTION_BLOCKED
SURVIVES_AS_TOY_NEGATIVE_CONTROL
```

Instead, map them.

---

## 2. Required functions

Implement:

```python
normalize_status(domain_status: str, domain: str | None = None) -> CanonicalStatusRecord
```

```python
get_canonical_permission(domain_status: str, domain: str | None = None) -> CanonicalPermission
```

```python
get_blocked_reasons(domain_status: str, domain: str | None = None) -> list[CanonicalBlockedReason]
```

```python
is_blocked(domain_status: str, domain: str | None = None) -> bool
```

```python
requires_human_review(domain_status: str, domain: str | None = None) -> bool
```

---

## 3. Unknown status behavior

Unknown statuses must not be treated as valid claims.

Default:

```txt
permission: REVIEW_REQUIRED
blocked_reason: HUMAN_REVIEW_REQUIRED
evidence_level: NO_EVIDENCE
support_level: UNSUPPORTED
```

This prevents accidental elevation.

---

## 4. Alias table structure

Create a mapping table:

```python
STATUS_COMPATIBILITY_MAP: dict[str, CanonicalStatusRecord]
```

Include at least representative mappings from:

```txt
business_validation
copilot/truth_boundary
candidate/detectability
epistemic_modes
financial/action gates
source/benchmark gates
prediction/calibration
```

---

## 5. Behavior preservation test

v2.1 must include a test proving that normalization does not change gate outputs.

Example:

```python
result = evaluate_business_validation_gate(...)
before = result.status
normalized = normalize_status(before)
after = result.status
assert before == after
assert normalized.canonical_permission in {...}
```

---

## 6. Forward compatibility

Any new gate added after v2.1 should either:

```txt
return a canonical status record directly
```

or:

```txt
return a domain status that is added to the compatibility map.
```

---

## 7. Final principle

```txt
Compatibility first.
Consolidation second.
Renaming last.
```
