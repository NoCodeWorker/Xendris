# Phygn v5.7 — Dataset Expansion Protocol

## 0. Purpose

This document defines the v5.7 dataset expansion protocol for visibility/decoherence observables.

---

## 1. Source pool

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_source_pool_v5_7.json
```

Schema:

```python
class SourcePoolRecord(BaseModel):
    source_id: str
    title: str
    year: int | None
    authority: str | None
    external_identity: str | None
    local_pdf_path: str | None
    local_pdf_hash: str | None
    source_status: str
    candidate_relevance: list[str]
    observable_targets: list[str]
    notes: list[str]
```

Source statuses:

```txt
LOCAL_AVAILABLE
EXTERNAL_IDENTITY_ONLY
REQUIRES_DOWNLOAD
REQUIRES_HUMAN_LOOKUP
REJECTED_NOT_RELEVANT
```

---

## 2. Observable location candidates

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_observable_location_candidates_v5_7.json
```

Schema:

```python
class ObservableLocationCandidate(BaseModel):
    location_id: str
    source_id: str
    local_pdf_path: str | None
    local_pdf_hash: str | None
    page_number: int | None
    section_id: str | None
    figure_id: str | None
    table_id: str | None
    equation_id: str | None
    observable_class: str
    variable_name: str | None
    numeric_value_text: str | None
    unit_text: str | None
    condition_text: str | None
    snippet: str
    classification: str
    extraction_blockers: list[str]
    recommended_next_action: str
```

Allowed classifications:

```txt
OBSERVED_MEASUREMENT_CANDIDATE
MODEL_PARAMETER
BOUND_OR_CONSTRAINT
REGIME_VALUE
THEORETICAL_EQUATION
QUALITATIVE_PROSE
SUPPLEMENTARY_POINTER
NOT_YTRUE
```

Only:

```txt
OBSERVED_MEASUREMENT_CANDIDATE
```

may proceed to y_true extraction.

---

## 3. y_true candidates

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_ytrue_candidates_v5_7.json
```

Schema:

```python
class YTrueCandidate(BaseModel):
    ytrue_candidate_id: str
    source_id: str
    source_title: str
    source_year: int | None
    external_identity: str | None
    local_pdf_path: str | None
    local_pdf_hash: str | None
    page_number: int | None
    location_label: str
    observable_class: str
    variable_name: str
    value_numeric: float | None
    original_value_text: str
    unit: str | None
    conditions: dict
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str]
```

QC statuses:

```txt
PASS
PASS_WITH_LIMITATIONS
REJECT
REQUIRES_HUMAN_REVIEW
REQUIRES_FIGURE_REVIEW
REQUIRES_SUPPLEMENTARY_DATA
```

---

## 4. Accepted y_true

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_accepted_ytrue_v5_7.json
```

Accepted records must include:

```txt
complete source identity
source hash or exact external provenance
page/table/figure/section/equation location
observable class
numeric value
unit unless dimensionless
condition mapping
QC PASS or PASS_WITH_LIMITATIONS
```

---

## 5. Rejected y_true

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_rejected_ytrue_v5_7.json
```

Reject reasons include:

```txt
NO_NUMERIC_VALUE
NO_LOCATION
MISSING_UNIT
AMBIGUOUS_CONDITION_MAPPING
MODEL_ONLY
BOUND_ONLY
REGIME_ONLY
QUALITATIVE_ONLY
NO_PROVENANCE
REQUIRES_VISUAL_REVIEW
```

---

## 6. Dataset assembly

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json
```

Dataset schema:

```python
class VisibilityDecoherenceDataset(BaseModel):
    dataset_id: str
    version: str
    records: list[dict]
    source_count: int
    accepted_ytrue_count: int
    observable_class_distribution: dict
    condition_key_distribution: dict
    limitation_flags: list[str]
    notes: list[str]
```

---

## 7. Final principle

```txt
An expanded dataset is a field of judgment, not a rescued candidate.
```
