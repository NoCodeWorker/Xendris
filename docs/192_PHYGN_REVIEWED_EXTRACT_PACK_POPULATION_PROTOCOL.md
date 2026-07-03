# Phygn v3.2 — Reviewed Extract Pack Population Protocol

## 0. Purpose

This document defines the seed extract pack.

The extract pack gives the validator something concrete to evaluate.

---

## 1. Extract pack file

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

---

## 2. Extract statuses

Initial extract status:

```txt
EXTRACT_CANDIDATE_REQUIRES_REVIEW
```

Allowed validated statuses after review:

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

## 3. Required extract fields

Each seed extract must include:

```txt
extract_id
source_id
slot_id
extract_text_or_paraphrase
exact_quote_available
quote_location
equation_text
observable_text
parameter_constraint_text
benchmark_data_text
supported_components
contradicted_components
limitations
manual_review_required
extraction_notes
initial_validation_status
```

---

## 4. No automatic validation

v3.2 may include paraphrased candidate extracts, but they must remain:

```txt
manual_review_required: true
initial_validation_status: EXTRACT_CANDIDATE_REQUIRES_REVIEW
```

unless an exact reviewed extract is manually confirmed.

---

## 5. Minimum positive path

A future positive limited source-backed status requires:

```txt
one validated observable/baseline extract from SLOT_1 or SLOT_8
one validated gradient/transition component extract from SLOT_4
no unaddressed contradiction from SLOT_7
```

A future benchmark-supported status requires:

```txt
validated comparable benchmark extract from SLOT_5
observable match
mass/length/time/visibility ranges
limitations recorded
```

---

## 6. Final principle

```txt
The extract pack is where bibliography becomes pressure.
```
