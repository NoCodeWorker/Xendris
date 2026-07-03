# Phygn v3.0 — Real Extract Ingestion & Slot Coverage Protocol

## 0. Purpose

This document defines how acquired real sources become validated extracts and slot coverage.

---

## 1. Ingestion flow

```txt
source candidate
→ acquisition record
→ manifest entry
→ extract attempt
→ extract validation
→ slot coverage update
→ source gate decision
→ benchmark comparability check
→ loop feedback
```

---

## 2. Required extract fields

Each extract must capture:

```txt
source_id
slot_id
supported_component
contradicted_component
equation_text or no_equation_reason
observable_text or no_observable_reason
parameter_constraint_text or no_constraint_reason
benchmark_data_text or no_benchmark_reason
limitations
validation_status
```

---

## 3. Slot coverage matrix

Create a slot coverage matrix:

```txt
slot_id
required_component
candidate_sources
validated_extracts
accepted_support_count
analogy_only_count
negative_count
coverage_status
missing_requirements
```

Coverage statuses:

```txt
SLOT_UNTOUCHED
SLOT_CANDIDATES_FOUND
SLOT_ANALOGY_ONLY
SLOT_PARTIALLY_COVERED
SLOT_COVERED_LIMITED
SLOT_CONTRADICTED
SLOT_BENCHMARK_COMPARABLE
```

---

## 4. Minimum source-backed limited rule

To reach:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

require:

```txt
SLOT_1 or SLOT_8 covered by observable/baseline extract
SLOT_4 covered by gradient/transition component extract
no unaddressed SLOT_7 contradiction
fixtures/test doubles excluded
```

---

## 5. Minimum benchmark-supported rule

To reach:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

require:

```txt
SLOT_5 or SLOT_2 benchmark comparable record
observable match
parameter range match or justified transform
limitations recorded
fixtures/test doubles excluded
```

Note:

```txt
Benchmark-supported still does not mean experimental validation of PHI_GRADIENT.
```

---

## 6. Negative evidence rule

If negative source says:

```txt
environmental baseline dominates completely
candidate parameter range excluded
observable mismatch unavoidable
model structure incompatible
```

then classify affected component and block upgrade unless addressed.

---

## 7. Final principle

```txt
Slot coverage is not a count of papers.
It is a count of constraints.
```
