# Phygn v4.5 — Dataset Update & Candidate Freeze Decision

## 0. Purpose

This document defines how v4.5 updates the y_true dataset and decides whether PHI_GRADIENT remains active.

---

## 1. Accepted external y_true

Create:

```txt
data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json
```

Schema:

```python
class AcceptedExternalYTrueRecord(BaseModel):
    y_true_id: str
    candidate_id: str
    acquisition_track: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    normalized_variable_name: str
    value: float
    unit: str
    uncertainty: float | None
    source_location_type: str
    source_location_value: str
    local_artifact_path: str | None
    local_artifact_hash: str | None
    extraction_method: str
    approximate: bool
    qc_status: str
    matched_prediction_ids: list[str]
    limitations: list[str]
```

---

## 2. Rejected external y_true

Create:

```txt
data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json
```

Fields:

```txt
candidate_id
target_id
source_id
acquisition_track
rejection_reason
required_next_action
claim_impact
```

---

## 3. Updated assembled y_true dataset

Create:

```txt
data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json
```

Fields:

```txt
dataset_id
created_at
previous_dataset_ref
external_evidence_ref
previous_y_true_count
new_y_true_count
total_y_true_count
records
ready_for_predictive_gain
predictive_gain_status
minimum_viable_y_true_count
matched_prediction_count
slot4_debt_status
physical_claim_permission
notes
```

---

## 4. Next PredictiveGain inputs

Create:

```txt
data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json
```

If threshold reached:

```txt
ready_for_predictive_gain = true
predictive_gain_status = READY_FOR_SMOKE_TEST
recommended_next_phase = v4.6 — PredictiveGain Smoke Test & Error Comparison
```

If threshold not reached:

```txt
ready_for_predictive_gain = false
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
recommended_next_phase = candidate freeze or new experiment design
```

---

## 5. Candidate freeze decision

Create:

```txt
data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json
```

Schema:

```python
class CandidateFreezeDecision(BaseModel):
    decision_id: str
    accepted_y_true_count: int
    minimum_viable_y_true_count: int
    ready_for_predictive_gain: bool
    freeze_status: str
    freeze_reason: str | None
    allowed_future_work: list[str]
    blocked_future_work: list[str]
    required_to_unfreeze: list[str]
    recommended_next_phase: str
```

Freeze statuses:

```txt
NOT_FROZEN_THRESHOLD_REACHED
FROZEN_NO_YTRUE_AVAILABLE
FROZEN_REQUIRES_NEW_EXPERIMENT
FROZEN_PENDING_HUMAN_DATA_REVIEW
```

---

## 6. Allowed future work when frozen

Allowed:

```txt
new experiment design
public dataset discovery
source acquisition
manual extraction with new locations
SLOT_4 resolution
candidate redesign
kill/pivot analysis
```

Blocked:

```txt
PredictiveGain claim
validation claim
physical claim
gradient mechanism claim
new benchmark-only score inflation
```

---

## 7. Final principle

```txt
Freezing a candidate is progress when the alternative is fiction.
```
