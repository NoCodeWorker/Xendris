# Phygn v4.4 — Manual Data Extraction Sprint Goal

## 0. Context

The latest confirmed document is:

```txt
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
```

Therefore, v4.4 starts at:

```txt
275
```

v4.3 produced:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW
y_true_record_count = 0
ready_for_predictive_gain = false
PredictiveGain = UNDEFINED
manual_table_extraction_queue = 5
public_dataset_lookup_queue = 12
supplementary_lookup_queue = 11
figure_digitization_queue = 0
SLOT_4 debt = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
physical_claim_permission = BLOCKED
```

v4.4 focuses on the 5 critical/high-priority manual table extraction targets.

---

## 1. Core thesis

```txt
No table/page/value/unit/hash, no y_true.
No y_true threshold, no PredictiveGain.
```

v4.4 is not a theory phase.

v4.4 is not a benchmark-scoring phase.

v4.4 is a manual numeric data extraction sprint with strict provenance.

---

## 2. Hard rule

```txt
No accepted y_true without source hash.
No accepted y_true without page/table/figure/source-location.
No accepted y_true without numeric value.
No accepted dimensional value without unit.
No accepted approximate figure value without digitization metadata.
No accepted extracted value without QC status.
No PredictiveGain unless minimum viable y_true threshold is met.
```

---

## 3. Goal

Convert:

```txt
manual_table_extraction_queue_v4_3
```

into:

```txt
reviewed manual extraction records
accepted y_true records if QC passes
rejected extraction attempts
manual extraction audit trail
updated assembled y_true dataset
PredictiveGain readiness update
```

---

## 4. Inputs

v4.4 must load:

```txt
data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json
data/y_true/phi_gradient_source_coverage_audit_v4_3.json
data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json
data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json
data/y_true/phi_gradient_dataset_quality_report_v4_3.json
data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
data/observables/phi_gradient_quality_control_rules_v4_2.json
data/model_comparison/phi_gradient_model_predictions_v4_1.json
data/real_sources/source_hashes_v3_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Optional source locations:

```txt
data/real_sources/pdfs/
data/real_sources/extracts/
data/real_sources/supplementary/
```

If inputs are missing:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

---

## 5. Outputs

Create:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json
data/y_true/phi_gradient_dataset_quality_report_v4_4.json
data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json
```

---

## 6. Statuses

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_COMPLETED
PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
PHI_GRADIENT_MANUAL_EXTRACTION_READY_FOR_PREDICTIVE_GAIN
PHI_GRADIENT_MANUAL_EXTRACTION_REQUIRES_HUMAN_REVIEW
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

Expected conservative status:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL
```

unless enough accepted y_true records exist.

---

## 7. Minimum viable threshold

To enable predictive-gain smoke test:

```txt
accepted_y_true_count >= 3
matched_prediction_count >= 3
```

If not:

```txt
PredictiveGain remains undefined.
```

---

## 8. SLOT_4 debt interaction

SLOT_4 remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

v4.4 must not close or weaken debt.

Accepted y_true from visibility/decoherence-rate targets can only support future benchmark/predictive evaluation, not gradient-mechanism claims.

---

## 9. Acceptance criteria

v4.4 is complete when:

```txt
v4.3 manual extraction queue loaded
all queue items reviewed
accepted/rejected records generated
audit trail generated
assembled y_true dataset updated
quality report updated
next predictive-gain inputs updated
reports generated
tests pass
physical claims remain blocked
SLOT_4 debt remains open
```

---

## 10. Final principle

```txt
Manual extraction is not manual permission to lower standards.
```
