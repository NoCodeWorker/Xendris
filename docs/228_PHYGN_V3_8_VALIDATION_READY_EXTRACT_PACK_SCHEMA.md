# Phygn v3.8 — Validation-Ready Extract Pack Schema

## 0. Purpose

This document defines the v3.8 validation-ready extract pack.

---

## 1. Main pack

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
```

Schema:

```python
class ValidationReadyExtract(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    source_filename: str | None
    page_number: int | None
    location_type: str
    location_value: str
    exact_text: str
    candidate_type: str
    component_role: str
    supported_components: list[str]
    contradicted_components: list[str]
    limitations: list[str]
    review_status: str
    validation_ready: bool
    next_gate_required: str
```

---

## 2. Pack schema

```python
class ValidationReadyExtractPack(BaseModel):
    pack_id: str
    candidate_family: str
    phi_family: str
    source_manifest_ref: str
    extraction_manifest_ref: str
    extracts: list[ValidationReadyExtract]
    rejected_count: int
    manual_review_count: int
    validation_ready_count: int
    status: str
    notes: list[str]
```

---

## 3. Rejected candidates file

Create:

```txt
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
```

Each record:

```txt
candidate_id
source_id
reason
original_candidate_type
short_text_preview
review_status
```

---

## 4. Manual review queue

Create:

```txt
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
```

Each record:

```txt
candidate_id
source_id
page_number
candidate_type
text_preview
reason
priority
suggested_action
```

Priority levels:

```txt
HIGH
MEDIUM
LOW
```

Pedernales blocked extraction should create a HIGH priority manual-review item.

---

## 5. Reviewed candidate map

Create:

```txt
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
```

Fields:

```txt
candidate_id
source_id
review_decision
component_role
output_record_id
notes
```

---

## 6. Next validation gate inputs

Create:

```txt
data/real_sources/extracts/phi_gradient_v3_8_next_validation_gate_inputs.json
```

Fields:

```txt
validation_ready_pack_path
manual_review_queue_path
rejected_candidates_path
recommended_next_phase
status
blocked_claims
```

---

## 7. Final principle

```txt
The pack is not the verdict.
The pack is what makes a verdict possible.
```
