# Phygn v3.8.3 — Validation-Ready Extract Pack Schema

## 0. Purpose

This document defines the final v3.8.3 evidence-ready objects passed to v3.9.

---

## 1. Validation-ready extract

```python
class ValidationReadyExtractV383(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    source_filename: str | None
    page_number: int | None
    location_type: str
    location_value: str
    exact_text: str
    source_candidate_id: str
    assigned_slot: str
    component_role: str
    promotion_decision: str
    why_promoted: str
    limitations: list[str]
    possible_pressure_direction: str
    validation_questions: list[str]
    next_gate_required: str
```

Possible pressure directions:

```txt
SUPPORT_CANDIDATE
CONTRADICTION_CANDIDATE
BENCHMARK_CANDIDATE
BASELINE_CANDIDATE
PARAMETER_CONSTRAINT_CANDIDATE
ANALOGY_ONLY
INCONCLUSIVE
```

---

## 2. Validation-ready pack

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
```

Schema:

```python
class ValidationReadyExtractPackV383(BaseModel):
    pack_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    source_manifest_ref: str
    triage_packet_ref: str
    extracts: list[ValidationReadyExtractV383]
    validation_ready_count: int
    source_coverage: dict[str, int]
    slot_coverage: dict[str, int]
    manual_review_count: int
    rejected_count: int
    analogy_only_count: int
    status: str
    ready_for_v3_9: bool
    blocked_claims: list[str]
    notes: list[str]
```

---

## 3. Review decisions file

Create:

```txt
data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json
```

Each decision record:

```txt
review_item_id
candidate_id
source_id
assigned_slot
priority
decision
reason
output_extract_id
notes
```

---

## 4. Rejected file

Create:

```txt
data/real_sources/extracts/phi_gradient_rejected_priority_items_v3_8_3.json
```

Each record:

```txt
review_item_id
candidate_id
source_id
reason
text_preview
decision
```

---

## 5. Analogy-only file

Create:

```txt
data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json
```

Each record:

```txt
review_item_id
candidate_id
source_id
assigned_slot
why_analogy_only
text_preview
```

---

## 6. Manual review queue

Create:

```txt
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json
```

Each record:

```txt
review_item_id
candidate_id
source_id
page_number
assigned_slot
priority
reason
suggested_action
text_preview
```

---

## 7. Next source-pressure inputs

Create:

```txt
data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json
```

Fields:

```txt
ready_for_v3_9
validation_ready_pack_path
validation_ready_count
source_coverage
slot_coverage
recommended_next_phase
blocked_claims
notes
```

---

## 8. Final principle

```txt
The validation-ready pack is the courtroom bundle, not the verdict.
```
