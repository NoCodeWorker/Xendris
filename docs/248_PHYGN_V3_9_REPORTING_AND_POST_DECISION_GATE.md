# Phygn v3.9 — Reporting & Post-Decision Gate

## 0. Purpose

This document defines reports and what may happen after the first source-pressure decision.

---

## 1. Required reports

Generate:

```txt
reports/source_pressure/phi_gradient_source_pressure_decision_v3_9.md
reports/source_pressure/phi_gradient_extract_pressure_map_v3_9.md
reports/source_pressure/phi_gradient_slot_pressure_summary_v3_9.md
reports/source_pressure/phi_gradient_benchmark_alignment_v3_9.md
reports/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.md
reports/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.md
reports/campaigns/PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9.md
```

---

## 2. Report requirements

Reports must include:

```txt
validation-ready extract count
global decisions
primary decision
slot pressure summary
benchmark alignment
gradient-component status
contradictions
limitations
allowed claims
blocked claims
physical claim permission
next recommendations
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_READY
PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
PHI_GRADIENT_SOURCE_PRESSURE_BENCHMARK_RELEVANT
PHI_GRADIENT_SOURCE_PRESSURE_CONTRADICTED
PHI_GRADIENT_SOURCE_PRESSURE_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK
```

Suggested mappings:

### Limited support or benchmark relevant

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

### Contradicted

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: REAL_SOURCE_PRESSURE
Support Level: CONTRADICTED
Risk Level: SCIENTIFIC_RISK
```

### Analogy-only / inconclusive

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Allowed claims after v3.9

Depending on decision, allowed claims may include:

```txt
The literature supports baseline decoherence framing.
The literature supports visibility/coherence as a relevant observable.
The literature contains benchmark ranges relevant for model comparison.
The current extract pack does not support the gradient-component mechanism.
The current source pressure is inconclusive.
The current source pressure is analogy-only.
The candidate requires revision before model comparison.
```

Blocked always:

```txt
PHI_GRADIENT is physically validated.
Frontera C is validated.
The invariant has empirical confirmation.
Source pressure is experimental proof.
```

---

## 5. Possible next phases

If benchmark relevant:

```txt
v4.0 — Benchmark Dataset Construction & Observable Alignment
```

If contradicted:

```txt
v4.0 — Candidate Revision or Kill/Pivot Gate
```

If analogy-only:

```txt
v4.0 — Literature Gap Expansion for SLOT_4
```

If inconclusive:

```txt
v4.0 — Targeted Source Acquisition & Manual Review
```

---

## 6. Final principle

```txt
A result that limits the hypothesis is progress.
```
