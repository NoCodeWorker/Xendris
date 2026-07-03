# Phygn v3.1 — Real Source Extract Pack & Slot Coverage

## 0. Purpose

This document defines the real source extract pack and how it updates slot coverage.

---

## 1. Extract pack schema

```python
class ReviewedSourceExtract(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    extract_text_or_paraphrase: str
    exact_quote_available: bool
    quote_location: str | None
    equation_text: str | None
    observable_text: str | None
    parameter_constraint_text: str | None
    benchmark_data_text: str | None
    supported_components: list[str]
    contradicted_components: list[str]
    limitations: list[str]
    manual_review_required: bool
    extraction_notes: list[str]
```

```python
class ReviewedSourceExtractPack(BaseModel):
    extract_pack_id: str
    manifest_id: str
    candidate_family: str
    phi_family: str
    extracts: list[ReviewedSourceExtract]
    notes: list[str]
```

---

## 2. Required extract rule

No manifest entry contributes support unless it has at least one validated extract.

```txt
manifest entry != evidence
extract candidate != evidence
validated extract = possible pressure
```

---

## 3. Valid support components

Accepted components:

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

## 4. Extract validation reuse

v3.1 must reuse the v2.9 validator:

```txt
phyng.real_source_ingestion.extract_validation.validate_real_source_extract
```

or adapt it without weakening any rule.

Allowed validation statuses:

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

## 5. Slot coverage update

v3.1 must reuse or extend the v3.0 slot coverage matrix.

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

## 6. Minimum source-backed rule

To reach:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

require:

```txt
validated observable/baseline extract from SLOT_1 or SLOT_8
validated gradient/transition component extract from SLOT_4
no unaddressed contradiction from SLOT_7
fixture/test-double exclusion
```

---

## 7. Minimum benchmark-supported rule

To reach:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

require:

```txt
validated benchmark extract or benchmark record from SLOT_5
observable match
mass/length/time/visibility comparability
limitations recorded
fixture/test-double exclusion
```

---

## 8. Negative evidence rule

If any extract validates as:

```txt
EXTRACT_VALID_CONTRADICTS_CANDIDATE
```

then campaign status must be:

```txt
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

unless contradiction is explicitly addressed in the report.

---

## 9. Final principle

```txt
Slot coverage is earned by validated extracts, not by bibliography size.
```
