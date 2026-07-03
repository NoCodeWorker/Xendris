# Phygn v3.5 — Priority Exact Fill Schema & Files

## 0. Purpose

This document defines v3.5 exact-fill data structures and files.

---

## 1. Main output file

```txt
data/real_sources/extracts/phi_gradient_priority_exact_extracts_v3_5.json
```

---

## 2. Priority exact fill schema

```python
class PriorityExactFillRecord(BaseModel):
    fill_id: str
    source_id: str
    priority_rank: int
    slot_ids: list[str]
    source_text_status: str
    exact_extract_id: str | None
    location_type: str
    location_value: str
    exact_quote: str | None
    equation_text: str | None
    observable_text: str | None
    parameter_range_text: str | None
    benchmark_range_text: str | None
    negative_constraint_text: str | None
    component_interpretation: str
    risk_flags: list[str]
    review_status: str
    validation_ready: bool
    reviewer_notes: list[str]
```

---

## 3. Location file

```txt
data/real_sources/extracts/phi_gradient_priority_exact_extract_locations_v3_5.json
```

Fields:

```txt
fill_id
source_id
location_type
location_value
location_confidence
requires_manual_location_check
```

---

## 4. Equation/observable map

```txt
data/real_sources/extracts/phi_gradient_priority_equation_observable_map_v3_5.json
```

Fields:

```txt
fill_id
source_id
equation_text
observable_text
model_role
slot_id
candidate_relevance
limitations
```

Model roles:

```txt
DECOHERENCE_BASELINE
VISIBILITY_DECAY_OBSERVABLE
GRADIENT_COMPONENT
BENCHMARK_MODEL
PARAMETER_CONSTRAINT
NEGATIVE_CONSTRAINT
ANALOGY_ONLY
REQUIRES_REVIEW
```

---

## 5. Parameter range map

```txt
data/real_sources/extracts/phi_gradient_priority_parameter_range_map_v3_5.json
```

Fields:

```txt
fill_id
source_id
mass_range
length_or_separation_range
time_range
visibility_or_decoherence_measure
environmental_conditions
alpha_like_constraint
gamma_env_constraint
comparability_status
missing_requirements
```

---

## 6. Review notes

```txt
data/real_sources/extracts/phi_gradient_priority_review_notes_v3_5.md
```

Must include:

```txt
what was reviewed
what remains unavailable
what is validation-ready
what is unresolved
what may be negative
what is likely analogy-only
```

---

## 7. Validation-ready rule

A priority fill is validation-ready only if:

```txt
source_text_status is not unavailable
location_type is known
location_value is non-empty
at least one exact content field is non-empty
manual review has been resolved
validation_ready = true
```

---

## 8. Final principle

```txt
A filled extract is not evidence yet.
It is evidence-ready material.
```
