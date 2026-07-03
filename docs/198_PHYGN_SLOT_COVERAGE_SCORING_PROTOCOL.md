# Phygn v3.3 — Slot Coverage Scoring Protocol

## 0. Purpose

This document defines the slot coverage and scoring protocol for PHI_GRADIENT source-pack validation.

---

## 1. Coverage matrix inputs

```txt
validated_extracts
rejected_extracts
manifest_entries
target_slots
negative_sources
benchmark_comparability_records
```

---

## 2. Coverage statuses

```txt
SLOT_UNTOUCHED
SLOT_CANDIDATES_FOUND
SLOT_ANALOGY_ONLY
SLOT_REQUIRES_MANUAL_REVIEW
SLOT_PARTIALLY_COVERED
SLOT_COVERED_LIMITED
SLOT_CONTRADICTED
SLOT_BENCHMARK_COMPARABLE
```

---

## 3. Slot coverage record

```python
class SourcePackSlotCoverageRecord(BaseModel):
    slot_id: str
    candidate_source_count: int
    extract_count: int
    validated_support_count: int
    analogy_rejection_count: int
    manual_review_count: int
    contradiction_count: int
    benchmark_comparable_count: int
    coverage_status: str
    missing_requirements: list[str]
```

---

## 4. Required slot pressure

### For source-backed limited

Need:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
or
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

plus:

```txt
SLOT_4_GRADIENT_TRANSITION_OPERATORS
```

### For benchmark-supported

Need:

```txt
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
```

with comparable record.

### For parameter pressure

Need:

```txt
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
```

This is not strictly required for source-backed limited, but should block stronger progression if missing.

### For contradiction pressure

Need:

```txt
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
```

A validated contradiction can override positive limited support.

---

## 5. Scoring

Recommended scores:

```txt
observable_baseline_score: 0 or 1
gradient_component_score: 0 or 1
benchmark_score: 0 or 1
parameter_constraint_score: 0 or 1
negative_pressure_score: 0 or 1
analogy_penalty: count or normalized score
manual_review_debt: count
```

Aggregate:

```txt
source_pressure_score =
  0.35 * observable_baseline_score
+ 0.35 * gradient_component_score
+ 0.20 * parameter_constraint_score
- 0.10 * analogy_penalty
```

Benchmark score is reported separately.

Contradiction overrides promotion.

---

## 6. Decision priority

```txt
validation blocked
contradicted
benchmark data found
source-backed limited
analogy only
manual review required
inconclusive
```

---

## 7. Final principle

```txt
Slot coverage is pressure topology.
It tells us where the candidate is supported, exposed, or bleeding.
```
