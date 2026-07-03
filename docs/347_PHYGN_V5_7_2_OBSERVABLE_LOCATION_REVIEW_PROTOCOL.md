# Phygn v5.7.2 — Observable Location Review Protocol

## 0. Purpose

This document defines observable-location review after source download and hash registration.

---

## 1. Candidate location records

Create:

```txt
data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json
```

Schema:

```python
class TargetedObservableLocationCandidate(BaseModel):
    location_id: str
    source_candidate_id: str
    source_id: str | None
    local_pdf_path: str
    local_pdf_hash: str
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
    reviewer_decision: str
    extraction_blockers: list[str]
    recommended_next_action: str
```

---

## 2. Observed measurement candidates

Create:

```txt
data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json
```

A record may enter this file only if:

```txt
classification = OBSERVED_MEASUREMENT_CANDIDATE
source identity complete
local PDF hash exists
page/table/figure/section/equation location exists
numeric value text exists or figure/table likely contains numeric observed values
observable class is allowed
```

If numeric value requires visual extraction, mark:

```txt
REQUIRES_HUMAN_FIGURE_REVIEW
```

not accepted y_true.

---

## 3. Rejected/context records

Create:

```txt
data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json
```

Reject/context reasons:

```txt
MODEL_PARAMETER
BOUND_OR_CONSTRAINT
REGIME_VALUE
THEORETICAL_EQUATION
QUALITATIVE_PROSE
NO_NUMERIC_VALUE
NO_LOCATION
SUPPLEMENTARY_POINTER_ONLY
DATA_REPOSITORY_POINTER_ONLY
NOT_OBSERVED_MEASUREMENT
```

---

## 4. Location completeness

A location is complete if it has at least one of:

```txt
page_number + figure_id
page_number + table_id
page_number + section_id
page_number + equation_id
```

If not, mark:

```txt
LOCATION_INCOMPLETE
```

---

## 5. Next-gate decision

Create:

```txt
data/frontera_c/observable_location/v5_7_2_next_gate_decision.json
```

Fields:

```txt
final_status
downloaded_source_count
verified_source_object_count
candidate_location_count
observed_measurement_candidate_count
human_figure_review_required_count
supplementary_required_count
allowed_next_phase
blocked_next_phases
rationale
```

---

## 6. Final principle

```txt
A visible figure is not data until its observable is located and classified.
```
