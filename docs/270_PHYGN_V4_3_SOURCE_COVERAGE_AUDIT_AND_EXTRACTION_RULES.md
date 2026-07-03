# Phygn v4.3 — Source-Coverage Audit & Extraction Rules

## 0. Purpose

This document defines the audit layer before y_true values may enter the dataset.

---

## 1. Source coverage audit

Create:

```txt
data/y_true/phi_gradient_source_coverage_audit_v4_3.json
```

Schema:

```python
class SourceCoverageAuditRecord(BaseModel):
    audit_id: str
    target_id: str
    benchmark_id: str
    source_id: str
    extract_id: str
    source_hash_present: bool
    local_pdf_present: bool
    supplementary_present: bool
    public_dataset_reference_present: bool
    page_reference_present: bool
    table_reference_present: bool
    figure_reference_present: bool
    source_coverage_status: str
    blockers: list[str]
    next_action: str
```

Source coverage statuses:

```txt
SOURCE_COVERAGE_COMPLETE
SOURCE_COVERAGE_LOCAL_PDF_ONLY
SOURCE_COVERAGE_NEEDS_TABLE_REVIEW
SOURCE_COVERAGE_NEEDS_FIGURE_DIGITIZATION
SOURCE_COVERAGE_NEEDS_SUPPLEMENTARY
SOURCE_COVERAGE_NEEDS_PUBLIC_DATA
SOURCE_COVERAGE_BLOCKED_INSUFFICIENT_PROVENANCE
```

---

## 2. y_true extraction candidate

Create:

```txt
data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json
```

Schema:

```python
class YTrueExtractionCandidate(BaseModel):
    candidate_id: str
    target_id: str
    observable_class: str
    source_id: str
    extract_id: str
    candidate_value_text: str
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    extraction_method: str
    source_location: str
    provenance_status: str
    qc_status: str
    can_enter_dataset: bool
    blockers: list[str]
```

---

## 3. Accepted y_true record

Create:

```txt
data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json
```

Schema:

```python
class YTrueRecord(BaseModel):
    y_true_id: str
    target_id: str
    benchmark_id: str
    observable_class: str
    normalized_variable_name: str
    value: float | str | bool
    unit: str | None
    uncertainty: float | None
    source_id: str
    extract_id: str
    source_hash: str
    source_location_type: str
    source_location_value: str
    extraction_method: str
    approximate: bool
    qc_status: str
    limitations: list[str]
    matched_prediction_ids: list[str]
```

Allowed QC statuses:

```txt
PASS
PASS_WITH_LIMITATIONS
FAIL_MISSING_PROVENANCE
FAIL_NO_NUMERIC_VALUE
FAIL_UNIT_AMBIGUOUS
FAIL_LOCATION_MISSING
FAIL_SOURCE_HASH_MISSING
FAIL_REQUIRES_MANUAL_REVIEW
```

---

## 4. Extraction queues

Generate separate queues:

```txt
manual_table_extraction_queue
figure_digitization_queue
public_dataset_lookup_queue
supplementary_lookup_queue
```

Each queue item must include:

```txt
target_id
source_id
observable_class
expected_measurement
source_location_hint
required_action
priority
blocking_reason
```

---

## 5. Dataset admission rules

A value can enter the assembled y_true dataset only if:

```txt
target_id present
source_id present
source_hash present
observable_class present
numeric value or accepted categorical value present
unit present when numeric dimensional variable
source location present
QC status PASS or PASS_WITH_LIMITATIONS
matched prediction exists or can be matched later
```

---

## 6. Rejection rules

Reject or block if:

```txt
value is prose-only
unit is missing for dimensional numeric value
source hash missing
source location missing
numeric value inferred from non-quantitative prose
figure value has no digitization metadata
table value has no table/page reference
```

---

## 7. Final principle

```txt
Traceability is part of the measurement.
```
