# Phygn v2.1 — Permission Grammar & Blocked Reason Registry

## 0. Purpose

This document defines the canonical permission grammar for Phygn.

The goal is not to flatten all domain statuses.

The goal is to make every domain status interpretable through a shared permission and blocked-reason language.

---

## 1. Canonical Permission

Recommended enum:

```python
class CanonicalPermission(str, Enum):
    IDEA_ALLOWED = "IDEA_ALLOWED"
    EXPLORE_ALLOWED = "EXPLORE_ALLOWED"
    TEST_DESIGN_ALLOWED = "TEST_DESIGN_ALLOWED"
    CLAIM_LIMITED_ALLOWED = "CLAIM_LIMITED_ALLOWED"
    CLAIM_BLOCKED = "CLAIM_BLOCKED"
    ACTION_LIMITED_ALLOWED = "ACTION_LIMITED_ALLOWED"
    ACTION_BLOCKED = "ACTION_BLOCKED"
    EXECUTION_ALLOWED = "EXECUTION_ALLOWED"
    EXECUTION_BLOCKED = "EXECUTION_BLOCKED"
    SCALE_ALLOWED = "SCALE_ALLOWED"
    SCALE_BLOCKED = "SCALE_BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
```

---

## 2. Canonical Blocked Reasons

Recommended enum:

```python
class CanonicalBlockedReason(str, Enum):
    NO_BLOCK = "NO_BLOCK"
    MISSING_OBSERVABLE = "MISSING_OBSERVABLE"
    MISSING_FAILURE_CONDITION = "MISSING_FAILURE_CONDITION"
    MISSING_SOURCE_SUPPORT = "MISSING_SOURCE_SUPPORT"
    MISSING_BENCHMARK = "MISSING_BENCHMARK"
    MISSING_EXPERIMENTAL_DATA = "MISSING_EXPERIMENTAL_DATA"
    UNDETECTABLE_DELTA = "UNDETECTABLE_DELTA"
    UNPHYSICAL_PARAMETER = "UNPHYSICAL_PARAMETER"
    OUTSIDE_CLAIM_BOUNDARY = "OUTSIDE_CLAIM_BOUNDARY"
    OUTSIDE_ACTION_BOUNDARY = "OUTSIDE_ACTION_BOUNDARY"
    OUTSIDE_EXECUTION_BOUNDARY = "OUTSIDE_EXECUTION_BOUNDARY"
    OVERCLAIM = "OVERCLAIM"
    CONTRADICTION = "CONTRADICTION"
    NO_CUSTOMER = "NO_CUSTOMER"
    NO_PROBLEM = "NO_PROBLEM"
    NO_PAYMENT_SIGNAL = "NO_PAYMENT_SIGNAL"
    NO_CHANNEL_SIGNAL = "NO_CHANNEL_SIGNAL"
    NEGATIVE_UNIT_ECONOMICS = "NEGATIVE_UNIT_ECONOMICS"
    BLOCKING_RISK = "BLOCKING_RISK"
    NO_KILL_CRITERIA = "NO_KILL_CRITERIA"
    MODEL_OUTPUT_UNTRUSTED = "MODEL_OUTPUT_UNTRUSTED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
```

---

## 3. Canonical Evidence Levels

Recommended enum:

```python
class CanonicalEvidenceLevel(str, Enum):
    NO_EVIDENCE = "NO_EVIDENCE"
    HEURISTIC_ONLY = "HEURISTIC_ONLY"
    SYNTHETIC_ONLY = "SYNTHETIC_ONLY"
    SOURCE_BACKED_LIMITED = "SOURCE_BACKED_LIMITED"
    BENCHMARK_SUPPORTED = "BENCHMARK_SUPPORTED"
    EXPERIMENTAL_DATA_SUPPORTED = "EXPERIMENTAL_DATA_SUPPORTED"
    PAYMENT_SIGNAL = "PAYMENT_SIGNAL"
    REPEAT_PAYMENT_SIGNAL = "REPEAT_PAYMENT_SIGNAL"
    OPERATIONALLY_VALIDATED = "OPERATIONALLY_VALIDATED"
```

---

## 4. Canonical Support Levels

```python
class CanonicalSupportLevel(str, Enum):
    UNSUPPORTED = "UNSUPPORTED"
    HEURISTIC = "HEURISTIC"
    SYNTHETIC = "SYNTHETIC"
    SOURCE_LIMITED = "SOURCE_LIMITED"
    BENCHMARK = "BENCHMARK"
    EXPERIMENTAL = "EXPERIMENTAL"
    OPERATIONAL = "OPERATIONAL"
```

---

## 5. Canonical Risk Levels

Do not replace existing risk levels immediately.

Create canonical compatibility levels:

```python
class CanonicalRiskLevel(str, Enum):
    RISK_0_PRIVATE_THOUGHT = "RISK_0_PRIVATE_THOUGHT"
    RISK_1_INTERNAL_NOTE = "RISK_1_INTERNAL_NOTE"
    RISK_2_INTERNAL_RESEARCH = "RISK_2_INTERNAL_RESEARCH"
    RISK_3_PUBLIC_CONTENT = "RISK_3_PUBLIC_CONTENT"
    RISK_4_CLIENT_DELIVERABLE = "RISK_4_CLIENT_DELIVERABLE"
    RISK_5_FINANCIAL_RECOMMENDATION = "RISK_5_FINANCIAL_RECOMMENDATION"
    RISK_6_REAL_WORLD_ACTION = "RISK_6_REAL_WORLD_ACTION"
    RISK_7_AUTOMATED_EXECUTION = "RISK_7_AUTOMATED_EXECUTION"
    BUSINESS_RISK = "BUSINESS_RISK"
    TECHNICAL_RISK = "TECHNICAL_RISK"
```

---

## 6. CanonicalStatusRecord

```python
class CanonicalStatusRecord(BaseModel):
    domain_status: str
    domain: str
    canonical_permission: CanonicalPermission
    blocked_reasons: list[CanonicalBlockedReason]
    evidence_level: CanonicalEvidenceLevel
    support_level: CanonicalSupportLevel
    risk_level: CanonicalRiskLevel | None = None
    notes: str | None = None
```

---

## 7. Rule

Domain status remains the source of local meaning.

Canonical mapping provides cross-system interpretability.

---

## 8. Final principle

```txt
A status can be domain-specific.
A permission must be system-readable.
```
