# Phygn v4.3 — y_true Dataset & Quality Schema

## 0. Purpose

This document defines the assembled y_true dataset, blocked targets and dataset quality report.

---

## 1. Assembled dataset

Create:

```txt
data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json
```

Dataset fields:

```txt
dataset_id
created_at
source_plan_ref
target_count
y_true_record_count
records
ready_for_predictive_gain
predictive_gain_status
slot4_debt_status
physical_claim_permission
notes
```

---

## 2. Blocked y_true targets

Create:

```txt
data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json
```

Each blocked item:

```txt
target_id
benchmark_id
source_id
observable_class
blocked_reason
required_action
priority
can_be_unblocked
```

Blocked reasons:

```txt
MISSING_SOURCE_LOCATION
NEEDS_MANUAL_TABLE_EXTRACTION
NEEDS_FIGURE_DIGITIZATION
NEEDS_PUBLIC_DATA_LOOKUP
NEEDS_SUPPLEMENTARY_DATA
REQUIRES_NEW_EXPERIMENT
CONSTRAINT_NOT_YTRUE
LIMITATION_NOT_YTRUE
AMBIGUOUS_OBSERVABLE
NO_MATCHING_PREDICTION
```

---

## 3. Dataset quality report

Create:

```txt
data/y_true/phi_gradient_dataset_quality_report_v4_3.json
```

Fields:

```txt
target_count
candidate_count
accepted_y_true_count
blocked_count
manual_table_queue_count
figure_digitization_queue_count
public_dataset_lookup_count
supplementary_lookup_count
qc_pass_count
qc_fail_count
unit_normalization_issues
source_coverage_issues
prediction_matching_issues
readiness_status
recommendations
```

Readiness statuses:

```txt
YTRUE_DATASET_READY_PARTIAL
YTRUE_DATASET_EMPTY_NEEDS_EXTRACTION
YTRUE_DATASET_BLOCKED_BY_PROVENANCE
YTRUE_DATASET_BLOCKED_BY_MANUAL_REVIEW
YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN
```

---

## 4. Next PredictiveGain inputs

Create:

```txt
data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json
```

Fields:

```txt
ready_for_predictive_gain
y_true_dataset_path
prediction_dataset_path
matched_prediction_count
minimum_viable_y_true_count
predictive_gain_status
recommended_next_phase
blocked_claims
notes
```

---

## 5. PredictiveGain gate rule

```txt
PredictiveGain remains undefined
```

unless:

```txt
accepted_y_true_count >= minimum_viable_y_true_count
and matched_prediction_count >= minimum_viable_y_true_count
```

Recommended minimum:

```txt
minimum_viable_y_true_count = 3
```

Rationale:

```txt
One y_true value permits a smoke test, not a robust predictive claim.
```

---

## 6. Final principle

```txt
A dataset is not ready because it exists.
It is ready because it can be audited.
```
