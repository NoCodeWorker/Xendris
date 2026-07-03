# Phygn v2.0 — Core Ontology & State Consistency Audit

## 0. Purpose

Phygn now contains many domain-specific states.

This document defines the audit required to ensure that all states, enums, permissions and gate results are coherent.

---

## 1. State families to audit

The audit must discover and classify:

```txt
EpistemicMode
RiskLevel
FrictionLevel
LadderLevel
TruthBoundaryStatus
PermissionLevel
ClaimStatus
ActionStatus
EvidenceLevel
SourceSupportStatus
BenchmarkStatus
DetectabilityStatus
CandidateSurvivalStatus
FailureConditionStatus
PredictionStatus
CalibrationStatus
BusinessValidationStatus
WTPLevel
ChannelValidationLevel
UnitEconomicsStatus
BusinessRiskStatus
```

---

## 2. Main questions

For every state family, answer:

```txt
Where is it defined?
Is it duplicated elsewhere?
Is it a string literal or enum?
Does another module define an equivalent concept?
Who consumes it?
Who produces it?
Is it serialized in reports?
Is it tested?
Does it have a canonical definition?
```

---

## 3. Canonicalization candidates

Likely core concepts:

```txt
mode
risk
friction
ladder_level
truth_boundary
permission
evidence_level
support_level
gate_result
blocked_reason
audit_event
```

Domain-specific concepts should remain domain-specific but map to canonical core concepts.

Example:

```txt
BUSINESS_BLOCKED_NO_WTP
→ permission: SCALE_BLOCKED
→ blocked_reason: NO_PAYMENT_SIGNAL
→ evidence_level: NO_PAYMENT_SIGNAL
```

Example:

```txt
UNDETECTABLE_SYNTHETIC_DELTA
→ permission: CLAIM_BLOCKED
→ blocked_reason: UNDETECTABLE_DELTA
→ evidence_level: SYNTHETIC_ONLY
```

---

## 4. Anti-patterns to detect

```txt
same state with different names
different states with same name
string-based status without enum
gate returns plain dict with inconsistent keys
reports use terminology not present in schemas
tests assert implementation details instead of contracts
status implies truth instead of permission
```

---

## 5. Proposed core schema shape

```python
class CoreGateResult(BaseModel):
    gate_name: str
    status: str
    permission: str
    allowed_uses: list[str]
    blocked_uses: list[str]
    blocked_reasons: list[str]
    evidence_level: str | None
    risk_level: str | None
    audit_event: dict
```

---

## 6. Mapping table required

v2.0 must produce a mapping table:

```txt
domain_status
domain_module
canonical_permission
canonical_blocked_reason
canonical_evidence_level
canonical_risk_level
notes
```

---

## 7. Final principle

```txt
A blocked claim, a blocked trade and a blocked business scale-up are different events,
but they must share a common permission grammar.
```
