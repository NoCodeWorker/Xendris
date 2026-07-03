# Phygn v4.4.1 — Audit Rules & Invariants

## 0. Purpose

This document defines the invariants that the full suite logic audit must enforce.

---

## 1. Claim permission invariant

Every scientific claim must pass through a permission gate.

Required permissions:

```txt
DREAM_ALLOWED
HYPOTHESIS_ALLOWED
SIMULATION_ALLOWED
SOURCE_REVIEW_ALLOWED
SOURCE_PRESSURE_ALLOWED
BENCHMARK_COMPARISON_ALLOWED
YTRUE_EXTRACTION_ALLOWED
PREDICTIVE_GAIN_ALLOWED
PHYSICAL_CLAIM_ALLOWED
```

Blocked states:

```txt
CLAIM_BLOCKED
REVIEW_REQUIRED
UNSUPPORTED
SYNTHETIC_ONLY
MISSING_BENCHMARK
MISSING_YTRUE
MISSING_SOURCE_SUPPORT
BLOCKED_BY_SCIENTIFIC_DEBT
```

Audit rule:

```txt
No report or data artifact may contain a stronger claim than its permission level.
```

---

## 2. PredictiveGain invariant

```txt
PredictiveGain requires real y_true.
```

Allowed:

```txt
BenchmarkComparisonScore
SyntheticGain
CoverageScore
ObservableAlignmentScore
SourcePressureScore
```

Blocked as PredictiveGain:

```txt
synthetic benchmark score
source pressure score
benchmark ranking
documentary alignment
negative-control ranking
```

Required representation when no y_true:

```txt
predictive_gain = null
predictive_gain_status = UNDEFINED_NO_REAL_Y_TRUE
```

or:

```txt
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
```

---

## 3. Source support invariant

Raw extraction is not source support.

```txt
Raw extraction is contact.
Reviewed extraction is evidence-ready.
Validated extraction is pressure.
```

Required gates:

```txt
raw candidate
reviewed candidate
validation-ready extract
source-pressure decision
claim permission update
```

Audit rule:

```txt
No extract should be marked support before a source-pressure decision.
```

---

## 4. y_true invariant

```txt
A y_true value requires provenance.
```

Required fields:

```txt
target_id
source_id
source_hash
source location
numeric value or accepted categorical observed outcome
unit when dimensional
QC status
matched prediction id
```

Blocked:

```txt
prose-only values
regime bounds as y_true
constraints as y_true
limitations as y_true
unlocated values
unhashed values
```

---

## 5. SLOT_4 debt invariant

SLOT_4 debt remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

unless there is a valid closure artifact.

While open, it blocks:

```txt
gradient mechanism claim
PHI_GRADIENT as source-backed gradient mechanism
Frontera C empirical validation
invariant empirical confirmation
```

It does not block:

```txt
benchmark construction
observable alignment
model comparison without gradient claim
y_true extraction for non-SLOT_4 observables
```

Audit rule:

```txt
Any artifact implying gradient support while SLOT_4 debt is open is BLOCKER.
```

---

## 6. Negative-control invariant

Negative controls must be allowed to fail the candidate.

Audit rule:

```txt
A negative control whose failure cannot change claim permission is decorative, not scientific.
```

---

## 7. Test logic invariant

Tests must not merely assert that the implementation returns the hardcoded desired status.

Audit for:

```txt
tautological tests
fixture-only success
absence of negative fixtures
status-only assertions
missing claim-block tests
missing contradiction tests
missing debt-bypass tests
missing stale-artifact tests
```

---

## 8. Status monotonicity invariant

Permission may increase only through explicit gates.

Examples:

```txt
SYNTHETIC_ONLY → REAL_SOURCE_EXTRACTS_UNVALIDATED
REAL_SOURCE_EXTRACTS_UNVALIDATED → REAL_SOURCE_PRESSURE_LIMITED
REAL_SOURCE_PRESSURE_LIMITED → REAL_OBSERVED_YTRUE_PARTIAL
REAL_OBSERVED_YTRUE_PARTIAL → PREDICTIVE_GAIN_SMOKE_TEST
```

Audit rule:

```txt
No artifact may skip a gate.
```

---

## 9. Final principle

```txt
An invariant is valuable only if it can block progress.
```
