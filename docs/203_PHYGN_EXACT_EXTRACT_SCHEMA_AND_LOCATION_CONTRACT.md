# Phygn v3.4 — Exact Extract Schema & Location Contract

## 0. Purpose

This document defines the exact extract contract.

The goal is to make every source claim traceable to a reviewable location.

---

## 1. Exact extract schema

```python
class ExactReviewedExtract(BaseModel):
    exact_extract_id: str
    source_id: str
    slot_id: str
    source_title: str | None
    location_type: str
    location_value: str
    exact_quote: str | None
    paraphrase_context: str | None
    equation_text: str | None
    observable_text: str | None
    parameter_range_text: str | None
    benchmark_range_text: str | None
    negative_constraint_text: str | None
    supported_components: list[str]
    contradicted_components: list[str]
    limitations: list[str]
    review_status: str
    reviewer_notes: list[str]
    validation_ready: bool
```

---

## 2. Location types

Allowed location types:

```txt
PAGE
SECTION
EQUATION_NUMBER
FIGURE
TABLE
APPENDIX
ARXIV_ABSTRACT
ARXIV_SECTION
DOI_PAGE
LOCAL_PDF_PAGE
URL_ANCHOR
UNKNOWN_LOCATION_REQUIRES_REVIEW
```

If location is unknown:

```txt
validation_ready = false
review_status = EXACT_EXTRACT_REQUIRES_LOCATION
```

---

## 3. Review statuses

```txt
EXACT_EXTRACT_REVIEWED
EXACT_EXTRACT_PARTIAL
EXACT_EXTRACT_REQUIRES_LOCATION
EXACT_EXTRACT_REQUIRES_EQUATION
EXACT_EXTRACT_REQUIRES_OBSERVABLE
EXACT_EXTRACT_REQUIRES_BENCHMARK_RANGE
EXACT_EXTRACT_REQUIRES_PARAMETER_RANGE
EXACT_EXTRACT_NEGATIVE_CANDIDATE
EXACT_EXTRACT_REJECTED_NO_VALIDATABLE_CONTENT
```

---

## 4. Validation-ready rule

An extract is validation-ready only if:

```txt
source_id exists in manifest
slot_id is valid
location_type is not UNKNOWN_LOCATION_REQUIRES_REVIEW
location_value is non-empty
at least one exact content field is non-empty
manual_review_required is false
```

Exact content fields:

```txt
exact_quote
equation_text
observable_text
parameter_range_text
benchmark_range_text
negative_constraint_text
```

---

## 5. Quote policy

A short exact quote may be stored for local review.

Reports should avoid over-quoting.

Prefer:

```txt
short quote
location
paraphrased interpretation
component classification
limitation
```

---

## 6. Anti-contamination rule

The following may not become validation-ready:

```txt
unlocated quote
paraphrase-only extract
title-only inference
abstract-only broad analogy
source name without component mapping
```

---

## 7. Final principle

```txt
A source without location is a rumor in formal clothing.
```
