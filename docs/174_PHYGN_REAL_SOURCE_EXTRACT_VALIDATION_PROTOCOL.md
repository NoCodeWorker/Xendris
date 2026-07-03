# Phygn v2.9 — Real Source Extract Validation Protocol

## 0. Purpose

This document defines how real source extracts are validated.

A source can only pressure PHI_GRADIENT if a validated extract supports, constrains, contradicts or benchmarks a concrete component.

---

## 1. Source extract schema

```python
class RealSourceExtract(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    extracted_text_or_paraphrase: str
    exact_quote_available: bool
    equation_text: str | None
    observable_text: str | None
    parameter_constraint_text: str | None
    benchmark_data_text: str | None
    supported_components: list[str]
    contradicted_components: list[str]
    limitations: list[str]
    extractor_notes: list[str]
    validation_status: str
```

---

## 2. Validation statuses

```txt
EXTRACT_VALID_SUPPORTS_OBSERVABLE
EXTRACT_VALID_SUPPORTS_BASELINE
EXTRACT_VALID_SUPPORTS_COMPONENT
EXTRACT_VALID_CONSTRAINS_PARAMETER
EXTRACT_VALID_PROVIDES_BENCHMARK_DATA
EXTRACT_VALID_CONTRADICTS_CANDIDATE
EXTRACT_REJECTED_ANALOGY_ONLY
EXTRACT_REJECTED_NO_COMPONENT_SUPPORT
EXTRACT_REJECTED_NO_OBSERVABLE
EXTRACT_REJECTED_NOT_COMPARABLE
EXTRACT_REQUIRES_MANUAL_REVIEW
```

---

## 3. Component support requirements

A valid extract must support or constrain at least one of:

```txt
visibility_decay_observable
environmental_decoherence_baseline
Gamma_env_rate
gradient_transition_operator
log_or_scale_coordinate_formulation
mesoscopic_mass_length_time_range
alpha_like_parameter_constraint
negative_or_exclusion_constraint
benchmark_dataset_or_table
```

---

## 4. Analogy blocker

Reject if the extract only contains:

```txt
general decoherence discussion
generic gradient language
generic boundary metaphor
log plot without model role
scale language without equation/constraint
conceptual resemblance without observable
```

Status:

```txt
EXTRACT_REJECTED_ANALOGY_ONLY
```

---

## 5. Benchmark extract validation

To validate benchmark data, require:

```txt
observable
parameter ranges
comparison variable
data table or numerical values or explicit benchmark range
limitations
source id
```

If missing:

```txt
EXTRACT_REJECTED_NOT_COMPARABLE
```

---

## 6. Negative extract validation

Negative sources must be recorded when they:

```txt
exclude a parameter range
contradict a candidate mechanism
show environmental baseline dominates
make alpha implausible
make observable mismatch unavoidable
```

Negative evidence is not failure of the pipeline.

It is evidence pressure.

---

## 7. Final principle

```txt
An extract is valid when it can be traced to a component and can change the candidate's permissions.
```
