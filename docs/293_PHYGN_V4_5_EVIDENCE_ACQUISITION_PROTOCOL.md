# Phygn v4.5 — Evidence Acquisition Protocol

## 0. Purpose

This document defines how v4.5 acquires external evidence.

---

## 1. Track A — Table Review

Input priority:

```txt
manual_extraction_rejected_v4_4
manual_extraction_review_records_v4_4
local PDFs
source hashes
normalized observable targets
```

Create:

```txt
data/external_evidence/phi_gradient_table_review_results_v4_5.json
```

Schema:

```python
class TableReviewResult(BaseModel):
    review_id: str
    target_id: str
    source_id: str
    local_pdf_path: str | None
    page_number: int | None
    table_number: str | None
    candidate_value_text: str | None
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    evidence_status: str
    blockers: list[str]
    next_action: str
```

Allowed evidence statuses:

```txt
TABLE_VALUE_FOUND
TABLE_NOT_FOUND
PDF_NOT_AVAILABLE
PAGE_LOCATION_MISSING
VALUE_AMBIGUOUS
REQUIRES_HUMAN_REVIEW
```

---

## 2. Track B — Supplementary Search

Create:

```txt
data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json
```

Schema:

```python
class SupplementarySearchResult(BaseModel):
    search_id: str
    source_id: str
    target_ids: list[str]
    supplementary_path: str | None
    supplementary_url_or_reference: str | None
    file_hash: str | None
    expected_observables: list[str]
    found_numeric_values: bool
    candidate_records: list[dict]
    evidence_status: str
    blockers: list[str]
```

Allowed evidence statuses:

```txt
SUPPLEMENTARY_FOUND_VALUES
SUPPLEMENTARY_FOUND_NO_VALUES
SUPPLEMENTARY_NOT_FOUND
SUPPLEMENTARY_REQUIRES_DOWNLOAD
SUPPLEMENTARY_REQUIRES_MANUAL_REVIEW
```

---

## 3. Track C — Public Dataset Search

Create:

```txt
data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json
```

Schema:

```python
class PublicDatasetSearchResult(BaseModel):
    search_id: str
    source_id: str
    target_ids: list[str]
    repository_name: str | None
    repository_reference: str | None
    local_dataset_path: str | None
    dataset_hash: str | None
    expected_observables: list[str]
    found_numeric_values: bool
    candidate_records: list[dict]
    evidence_status: str
    blockers: list[str]
```

Allowed evidence statuses:

```txt
PUBLIC_DATASET_FOUND_VALUES
PUBLIC_DATASET_FOUND_NO_VALUES
PUBLIC_DATASET_NOT_FOUND
PUBLIC_DATASET_REQUIRES_DOWNLOAD
PUBLIC_DATASET_REQUIRES_MANUAL_REVIEW
```

---

## 4. External y_true candidate

Create:

```txt
data/external_evidence/phi_gradient_external_y_true_candidates_v4_5.json
```

Schema:

```python
class ExternalYTrueCandidate(BaseModel):
    candidate_id: str
    acquisition_track: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    normalized_variable_name: str
    candidate_value_text: str
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    source_location_type: str
    source_location_value: str
    local_artifact_path: str | None
    local_artifact_hash: str | None
    extraction_method: str
    provenance_status: str
    qc_status: str
    matched_prediction_ids: list[str]
    can_enter_dataset: bool
    blockers: list[str]
```

---

## 5. Acceptance rule

Accept as external y_true only if:

```txt
numeric_value exists
unit exists when dimensional
source_hash exists
source location exists
local or external artifact provenance exists
QC status is PASS or PASS_WITH_LIMITATIONS
matched prediction exists
```

---

## 6. Final principle

```txt
Looking for data is not finding data.
Finding data is not accepting data.
Accepting data requires provenance.
```
