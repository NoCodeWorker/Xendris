# Phygn v4.4 — Dataset Update & Predictive Gate Schema

## 0. Purpose

This document defines the updated y_true dataset and next predictive-gain inputs after manual extraction.

---

## 1. Accepted manual y_true records

Create:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.json
```

Schema:

```python
class AcceptedManualYTrueRecord(BaseModel):
    y_true_id: str
    source_review_id: str
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
    extraction_method: str
    approximate: bool
    qc_status: str
    matched_prediction_ids: list[str]
    limitations: list[str]
```

---

## 2. Rejected manual records

Create:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json
```

Each record:

```txt
review_id
queue_item_id
target_id
source_id
observable_class
rejection_reason
required_next_action
claim_impact
```

---

## 3. Updated assembled dataset

Create:

```txt
data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json
```

Fields:

```txt
dataset_id
created_at
previous_dataset_ref
manual_extraction_ref
target_count
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

## 4. Updated quality report

Create:

```txt
data/y_true/phi_gradient_dataset_quality_report_v4_4.json
```

Fields:

```txt
manual_queue_count
reviewed_count
accepted_count
rejected_count
rerouted_count
qc_pass_count
qc_fail_count
unit_issues
location_issues
hash_issues
prediction_match_issues
ready_for_predictive_gain
recommendations
```

---

## 5. Next predictive-gain inputs

Create:

```txt
data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json
```

Fields:

```txt
ready_for_predictive_gain
y_true_dataset_path
model_predictions_path
accepted_y_true_count
matched_prediction_count
minimum_viable_y_true_count
predictive_gain_status
recommended_next_phase
blocked_claims
allowed_claims
notes
```

---

## 6. Gate statuses

If accepted_y_true_count >= 3 and matched_prediction_count >= 3:

```txt
ready_for_predictive_gain = true
predictive_gain_status = READY_FOR_SMOKE_TEST
recommended_next_phase = v4.5 — PredictiveGain Smoke Test & Error Comparison
```

Otherwise:

```txt
ready_for_predictive_gain = false
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
recommended_next_phase = v4.5 — Continued Manual/Public Data Acquisition
```

---

## 7. Final principle

```txt
A PredictiveGain gate starts with matched pairs: prediction and observed truth.
```
