# Phygn v2.2 — Heuristic Output Permission Protocol

## 0. Purpose

This document defines the permissions that heuristic outputs may and may not receive.

The goal is to preserve discovery speed without weakening epistemic discipline.

---

## 1. Core rule

```txt
HEURISTIC_OUTPUT_IS_NOT_EVIDENCE
```

A heuristic output may be promising, elegant, useful or prioritizable.

It is not evidence.

---

## 2. Allowed heuristic permissions

A heuristic output may receive:

```txt
CanonicalPermission.IDEA_ALLOWED
CanonicalPermission.EXPLORE_ALLOWED
CanonicalPermission.TEST_DESIGN_ALLOWED
CanonicalPermission.REVIEW_REQUIRED
```

A heuristic output may not receive by itself:

```txt
CanonicalPermission.CLAIM_LIMITED_ALLOWED
CanonicalPermission.ACTION_LIMITED_ALLOWED
CanonicalPermission.EXECUTION_ALLOWED
CanonicalPermission.SCALE_ALLOWED
```

---

## 3. Required canonical status record

Every heuristic output must produce a `CanonicalStatusRecord`.

Default:

```txt
domain_status: HEURISTIC_SEED
canonical_permission: EXPLORE_ALLOWED
blocked_reasons:
  - MISSING_SOURCE_SUPPORT
  - MISSING_BENCHMARK
evidence_level: HEURISTIC_ONLY
support_level: HEURISTIC
risk_level: TECHNICAL_RISK or domain-specific risk
```

For heuristic candidates ready for formal testing:

```txt
domain_status: HEURISTIC_TEST_DESIGN_READY
canonical_permission: TEST_DESIGN_ALLOWED
blocked_reasons:
  - MISSING_BENCHMARK
  - MISSING_EXPERIMENTAL_DATA
evidence_level: HEURISTIC_ONLY
support_level: HEURISTIC
```

For high-risk heuristic outputs:

```txt
domain_status: HEURISTIC_REVIEW_REQUIRED
canonical_permission: REVIEW_REQUIRED
blocked_reasons:
  - HUMAN_REVIEW_REQUIRED
evidence_level: HEURISTIC_ONLY
support_level: HEURISTIC
```

---

## 4. Forbidden transitions

Forbidden without non-heuristic evidence:

```txt
HEURISTIC_SEED → CLAIM_LIMITED_ALLOWED
HEURISTIC_SEED → BENCHMARK_SUPPORTED
HEURISTIC_SEED → ACTION_LIMITED_ALLOWED
HEURISTIC_SEED → EXECUTION_ALLOWED
```

Allowed transition path:

```txt
HEURISTIC_SEED
→ FORMALIZING_HYPOTHESIS
→ TESTABLE_HYPOTHESIS
→ SYNTHETIC_SUPPORT
→ SOURCE_BACKED_LIMITED
→ BENCHMARK_SUPPORTED
```

Only the last two require external support beyond heuristic generation.

---

## 5. Required blocked reasons

Heuristic outputs must explicitly carry missing-evidence reasons.

Typical blocked reasons:

```txt
MISSING_SOURCE_SUPPORT
MISSING_BENCHMARK
MISSING_EXPERIMENTAL_DATA
MISSING_OBSERVABLE
MISSING_FAILURE_CONDITION
HUMAN_REVIEW_REQUIRED
```

---

## 6. User-facing wording

Avoid:

```txt
This heuristic candidate is likely true.
This is validated by heuristic reasoning.
The model discovered a physical law.
```

Prefer:

```txt
This is a heuristic candidate worth testing.
It is not evidence yet.
The next step is to define the observable and failure condition.
```

---

## 7. Final principle

```txt
Heuristics can decide where to look.
They cannot decide what is real.
```
