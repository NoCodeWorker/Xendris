# Phygn v2.1 — Canonical Status Mapping & Compatibility Layer Goal

## 0. Context

The latest confirmed document is:

```txt
123_PHYGN_V2_0_REPOSITORY_ORCHESTRATION_AUDIT_RESULTS.md
```

Therefore, v2.1 starts at:

```txt
124
```

v2.0 discovered that Phygn now contains a large number of states, status strings, enums, gates and report labels across multiple domains:

```txt
physics candidates
detectability
source support
epistemic modes
truth boundary
copilot permissions
business validation
prediction accuracy
model runtime
repository audit
```

v2.0 correctly avoided aggressive refactor.

v2.1 now implements the safest next step:

```txt
canonical status mapping tables
permission grammar
blocked reason registry
compatibility aliases
report contract canonicalization
```

without changing existing behavior.

---

## 1. Core thesis

```txt
Different domains may keep their own statuses,
but every status must map to a common permission grammar.
```

A blocked claim, a blocked trade, an undetectable candidate and a blocked business scale-up are different events.

But they should all be expressible through a shared grammar:

```txt
permission
blocked_reason
evidence_level
risk_level
truth_boundary
audit_event
```

---

## 2. v2.1 is not a destructive refactor

v2.1 must not:

```txt
rename public statuses
remove existing enums
change gate decisions
change campaign outputs silently
force all domains into one enum
break reports
delete history
```

v2.1 must:

```txt
add canonical mapping tables
add compatibility aliases
add status normalization helpers
add report contract helpers
add meta-tests
produce reports
preserve behavior
```

---

## 3. Main deliverable

Create a new core compatibility layer:

```txt
phyng/core/
  __init__.py
  permissions.py
  blocked_reasons.py
  evidence_levels.py
  risk_levels.py
  status_mapping.py
  compatibility.py
  report_contract.py
```

If `phyng/core/` already exists, extend it conservatively.

---

## 4. Canonical grammar

At minimum, define canonical families:

```txt
CanonicalPermission
CanonicalBlockedReason
CanonicalEvidenceLevel
CanonicalRiskLevel
CanonicalTruthBoundary
CanonicalSupportLevel
CanonicalAuditEventType
```

Domain statuses must map into these families without replacing the original domain status.

---

## 5. Example mapping

```txt
BUSINESS_BLOCKED_NO_WTP
→ permission: SCALE_BLOCKED
→ blocked_reason: NO_PAYMENT_SIGNAL
→ evidence_level: NO_PAYMENT_SIGNAL
→ risk_level: BUSINESS_RISK
```

```txt
UNDETECTABLE_SYNTHETIC_DELTA
→ permission: CLAIM_BLOCKED
→ blocked_reason: UNDETECTABLE_DELTA
→ evidence_level: SYNTHETIC_ONLY
```

```txt
OUTSIDE_CLAIM_BOUNDARY
→ permission: CLAIM_BLOCKED
→ blocked_reason: OUTSIDE_CLAIM_BOUNDARY
```

---

## 6. Acceptance criteria

v2.1 is complete when:

```txt
canonical permission grammar exists
blocked reason registry exists
evidence/support levels exist
domain status mapping table exists
compatibility aliases exist
normalization helpers exist
report contract helper exists
meta-tests pass
existing behavior remains unchanged
reports are generated
```

---

## 7. Final principle

```txt
Canonicalization must increase clarity without erasing domain meaning.
```
