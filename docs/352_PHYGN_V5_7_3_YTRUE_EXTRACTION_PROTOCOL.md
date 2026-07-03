# Phygn v5.7.3 — y_true Extraction Protocol

## 0. Purpose

This document defines the strict extraction protocol for converting observed measurement candidates into accepted y_true records.

---

## 1. y_true candidates

Create:

```txt
data/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.json
```

Schema:

```python
class TargetedYTrueCandidate(BaseModel):
    ytrue_candidate_id: str
    source_id: str
    source_title: str
    source_year: int | None
    source_identity: dict
    local_pdf_path: str
    local_pdf_hash: str
    page_number: int | None
    location_label: str
    observable_class: str
    variable_name: str
    numeric_value: float | None
    original_value_text: str | None
    unit: str | None
    normalized_unit: str | None
    conditions: dict
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str]
    rejection_reason: str | None
```

---

## 2. Accepted y_true

Create:

```txt
data/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.json
```

Accepted schema:

```python
class AcceptedTargetedYTrue(BaseModel):
    y_true_id: str
    dataset_version: str
    source_id: str
    source_title: str
    source_authors_or_authority: str
    source_year: int
    source_doi_or_arxiv_or_url: str
    local_pdf_path: str
    local_pdf_hash: str
    page_number: int
    location_label: str
    observable_class: str
    variable_name: str
    value_numeric: float
    original_value_text: str
    unit: str
    normalized_unit: str
    conditions: dict
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str]
    claim_impact: str
```

Required claim impact:

```txt
DATASET_EXPANSION_ONLY
```

---

## 3. Rejected y_true

Create:

```txt
data/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.json
```

Reject reasons:

```txt
SOURCE_IDENTITY_INCOMPLETE
LOCAL_SOURCE_OBJECT_MISSING
LOCAL_HASH_MISSING
LOCATION_MISSING
NUMERIC_VALUE_MISSING
UNIT_UNRESOLVED
CONDITION_MAPPING_AMBIGUOUS
MODEL_ONLY
BOUND_OR_CONSTRAINT_ONLY
REGIME_ONLY
QUALITATIVE_ONLY
REQUIRES_HUMAN_FIGURE_REVIEW
REQUIRES_SUPPLEMENTARY_DATA
PROVENANCE_FAILURE
DUPLICATE_YTRUE
```

---

## 4. Audit trail

Create:

```txt
data/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.json
```

For every candidate, record:

```txt
candidate_id
input_location_id
source_id
decision
decision_reason
checks_passed
checks_failed
normalization_actions
deduplication_actions
reviewer_notes
```

---

## 5. Deduplication

Do not duplicate existing v5.3 Hackermueller y_true records.

Deduplicate by:

```txt
source_id
page_number
location_label
observable_class
variable_name
value_numeric
conditions
```

If duplicate:

```txt
reject with DUPLICATE_YTRUE
```

or include only in merged dataset as existing record.

---

## 6. Unit normalization

Examples:

```txt
percent visibility -> dimensionless_fraction
ms -> s
microseconds -> s
mbar -> Pa or preserve mbar with normalized field
K -> K
W -> W
amu -> amu or kg with explicit conversion
```

Unit conversion must be explicit.

---

## 7. Human figure review

If a figure clearly contains observed data but values cannot be extracted from text/caption:

```txt
qc_status = REQUIRES_HUMAN_FIGURE_REVIEW
```

Do not accept as y_true.

---

## 8. Final principle

```txt
A number without provenance is not truth.
A figure without extracted values is not y_true.
```
