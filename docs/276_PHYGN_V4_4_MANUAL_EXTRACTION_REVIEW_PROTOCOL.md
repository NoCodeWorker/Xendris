# Phygn v4.4 — Manual Extraction Review Protocol

## 0. Purpose

This document defines how manual table extraction queue items are reviewed.

---

## 1. Review record

Create:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json
```

Schema:

```python
class ManualExtractionReviewRecord(BaseModel):
    review_id: str
    queue_item_id: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    expected_measurement: str
    local_pdf_path: str | None
    page_number: int | None
    table_number: str | None
    figure_number: str | None
    extracted_value_text: str | None
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    extraction_method: str
    reviewer_decision: str
    qc_status: str
    blockers: list[str]
    notes: list[str]
```

---

## 2. Reviewer decisions

```txt
ACCEPT_AS_YTRUE
REJECT_NO_NUMERIC_VALUE
REJECT_MISSING_UNIT
REJECT_MISSING_LOCATION
REJECT_PROSE_ONLY
REJECT_CONSTRAINT_NOT_YTRUE
REJECT_LIMITATION_NOT_YTRUE
SEND_TO_FIGURE_DIGITIZATION
SEND_TO_SUPPLEMENTARY_LOOKUP
SEND_TO_PUBLIC_DATA_LOOKUP
SEND_TO_HUMAN_REVIEW
```

---

## 3. Allowed extraction methods

```txt
MANUAL_TABLE_EXTRACTION
MANUAL_FIGURE_DIGITIZATION
SUPPLEMENTARY_DATA_EXTRACTION
PUBLIC_DATASET_EXTRACTION
EXPLICIT_QUANTITATIVE_TEXT_EXTRACTION
```

v4.4 should primarily handle:

```txt
MANUAL_TABLE_EXTRACTION
```

but may reroute items when table evidence is not present.

---

## 4. Accepted y_true requirements

An item can be accepted only if all hold:

```txt
source_id present
source_hash present and matches registry
target_id present
benchmark_id present
observable_class present
numeric_value present for numeric observables
unit present for dimensional observables
source location present
extraction_method present
qc_status in [PASS, PASS_WITH_LIMITATIONS]
matched model prediction exists or can be matched
```

---

## 5. Observable-specific acceptance

### VISIBILITY

```txt
numeric_value in [0, 1]
unit = dimensionless
accepted if page/table/figure/text location exists
```

### DECOHERENCE_RATE

```txt
numeric_value >= 0
unit = s^-1 or convertible to s^-1
accepted if source location exists
```

### CONTRAST_DECAY

```txt
numeric_value >= 0
unit = s^-1, dimensionless/time, or explicitly normalized decay measure
```

### COHERENCE_LOSS

```txt
numeric_value >= 0
unit = dimensionless or explicitly described loss metric
```

---

## 6. Rejection logic

Reject if:

```txt
text says only qualitative change, e.g. halve, reduce, enhance, suppress, without actual numeric observed value
value is a parameter constraint rather than observed outcome
value is a regime boundary rather than measured y_true
unit missing for dimensional numeric value
location missing
source hash missing
```

---

## 7. Audit trail

Every decision must be auditable.

Create:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.json
```

The audit trail must include:

```txt
input queue item
decision
reason
accepted/rejected output path
timestamp
claim impact
```

---

## 8. Final principle

```txt
If the reviewer cannot point to the number, Phygn cannot use the number.
```
