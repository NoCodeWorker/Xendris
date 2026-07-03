# Phygn v3.4 — Equation, Observable & Parameter Mapping

## 0. Purpose

This document defines how exact extracts are mapped into PHI_GRADIENT source-pressure components.

---

## 1. Mapping output files

Generate:

```txt
data/real_sources/extracts/phi_gradient_equation_observable_map_v3_4.json
data/real_sources/extracts/phi_gradient_parameter_range_map_v3_4.json
```

---

## 2. Equation map fields

```python
class EquationObservableMapEntry(BaseModel):
    source_id: str
    exact_extract_id: str
    equation_text: str | None
    observable_text: str | None
    model_role: str
    slot_id: str
    candidate_relevance: str
    limitations: list[str]
```

Allowed model roles:

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

## 3. Parameter range map fields

```python
class ParameterRangeMapEntry(BaseModel):
    source_id: str
    exact_extract_id: str
    mass_range: str | None
    length_or_separation_range: str | None
    time_range: str | None
    visibility_or_decoherence_measure: str | None
    environmental_conditions: str | None
    alpha_like_constraint: str | None
    gamma_env_constraint: str | None
    comparability_status: str
    missing_requirements: list[str]
```

---

## 4. Comparability statuses

```txt
COMPARABLE_RANGE_READY
PARTIAL_RANGE_REQUIRES_REVIEW
PROPOSAL_RANGE_NOT_DATA
ENVIRONMENTAL_BASELINE_ONLY
NOT_COMPARABLE_TO_PHI_GRADIENT
REQUIRES_EXACT_VALUES
```

---

## 5. Required benchmark comparability fields

To become benchmark-comparable, require:

```txt
mass range
length/separation range
time range
visibility/decoherence measure
environmental limitations
```

If any are missing:

```txt
benchmark_support = false
```

---

## 6. Required source-backed limited fields

To prepare source-backed limited review:

Need at least one extract mapped as:

```txt
DECOHERENCE_BASELINE
or
VISIBILITY_DECAY_OBSERVABLE
```

and at least one extract mapped as:

```txt
GRADIENT_COMPONENT
```

If gradient component is analogy-only:

```txt
source_backed_limited_candidate = false
```

---

## 7. Negative pressure mapping

If an extract maps to:

```txt
NEGATIVE_CONSTRAINT
```

then record:

```txt
affected_component
severity
can_be_addressed
requires_postmortem
```

---

## 8. Final principle

```txt
Equations give shape.
Observables give contact.
Ranges give pain.
```
