# Phygn v2.2 — Heuristic-to-Testable-Hypothesis Pipeline

## 0. Purpose

This document defines the pipeline that turns heuristic candidates into testable hypotheses without granting them evidential authority.

---

## 1. Pipeline

```txt
Raw idea or open search problem
→ Heuristic candidate generation
→ Candidate scorecard
→ Canonical heuristic status mapping
→ Missing-field detection
→ Next Best Question
→ Hypothesis Seed Card
→ Testability gate
→ Synthetic benchmark design
→ Source/benchmark requirements
```

---

## 2. Candidate states

```txt
HEURISTIC_SEED
HEURISTIC_PRIORITIZED
HEURISTIC_TEST_DESIGN_READY
HEURISTIC_REVIEW_REQUIRED
HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY
HEURISTIC_REJECTED_AD_HOC
HEURISTIC_REJECTED_NO_OBSERVABLE
```

---

## 3. Canonical mapping

Default mapping:

```txt
HEURISTIC_SEED
→ EXPLORE_ALLOWED
→ HEURISTIC_ONLY
→ HEURISTIC
→ blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

```txt
HEURISTIC_TEST_DESIGN_READY
→ TEST_DESIGN_ALLOWED
→ HEURISTIC_ONLY
→ HEURISTIC
→ blocked: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

```txt
HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY
→ CLAIM_BLOCKED
→ HEURISTIC_ONLY
→ HEURISTIC
→ blocked: HUMAN_REVIEW_REQUIRED or CONTRADICTION if applicable
```

---

## 4. Testability gate

A heuristic candidate cannot become `TESTABLE_HYPOTHESIS` unless it has:

```txt
observable
proxy or measurement method
time/parameter range
baseline
failure condition
dimensional sanity
non-ad-hoc rationale
```

---

## 5. Synthetic benchmark design

A candidate can move to synthetic benchmark only if it has:

```txt
baseline equation or model
candidate equation or rule
parameter ranges
detectability metric
epsilon/threshold
expected failure mode
```

Synthetic benchmark may produce:

```txt
SYNTHETIC_SUPPORT
UNDETECTABLE_SYNTHETIC_DELTA
DETECTABLE_SYNTHETIC_DELTA
```

But still cannot produce physical validation.

---

## 6. Source/benchmark transition

To move beyond synthetic support:

```txt
source support is required
benchmark data is required
experimental or external outcome data is required where applicable
```

---

## 7. Integration with Copilot

The copilot should expose heuristic outputs as:

```txt
Candidate worth exploring
Candidate ready for test design
Candidate blocked as ad hoc
Candidate blocked due to missing observable
Candidate blocked due to dimensional inconsistency
```

It must not expose:

```txt
Candidate is true
Candidate is physically validated
Candidate proves the theory
```

---

## 8. Final principle

```txt
The heuristic layer opens doors.
The gates decide which doors lead anywhere.
```
