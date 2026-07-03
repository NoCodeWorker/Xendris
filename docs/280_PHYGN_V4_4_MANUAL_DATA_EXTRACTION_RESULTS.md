# Phygn v4.4 - Manual Data Extraction Sprint Results

Date: 2026-07-01

Source prompt:

```txt
docs/279_PHYGN_CODEX_V4_4_MANUAL_DATA_EXTRACTION_PROMPT.md
```

Supporting specs:

```txt
docs/275_PHYGN_V4_4_MANUAL_DATA_EXTRACTION_SPRINT_docs/status/GOAL.md
docs/276_PHYGN_V4_4_MANUAL_EXTRACTION_REVIEW_PROTOCOL.md
docs/277_PHYGN_V4_4_DATASET_UPDATE_AND_PREDICTIVE_GATE_SCHEMA.md
docs/278_PHYGN_V4_4_REPORTING_AND_NEXT_GATE.md
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v4.4 PROMPT SPECIFICATIONS**

Final campaign status:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
```

Interpretation:

```txt
The v4.3 manual extraction queue was loaded.
All currently queued manual extraction items were reviewed.
No queued item met the strict y_true acceptance requirements.
No PredictiveGain readiness was granted.
SLOT_4 debt remained open and blocking.
No physical claim was upgraded.
```

Validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_ytrue_extraction_loader_v4_3.py tests/test_ytrue_source_coverage_audit_v4_3.py tests/test_ytrue_extraction_candidates_v4_3.py tests/test_ytrue_extraction_queues_v4_3.py tests/test_ytrue_dataset_assembly_v4_3.py tests/test_ytrue_quality_report_v4_3.py tests/test_phi_gradient_real_ytrue_extraction_campaign_v4_3.py tests/test_manual_data_extraction_loader_v4_4.py tests/test_manual_table_review_v4_4.py tests/test_manual_extraction_reviewer_v4_4.py tests/test_manual_dataset_update_v4_4.py tests/test_manual_extraction_audit_trail_v4_4.py tests/test_phi_gradient_manual_data_extraction_campaign_v4_4.py
31 passed in 1.80s
```

Focused v4.4 validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_manual_data_extraction_loader_v4_4.py tests/test_manual_table_review_v4_4.py tests/test_manual_extraction_reviewer_v4_4.py tests/test_manual_dataset_update_v4_4.py tests/test_manual_extraction_audit_trail_v4_4.py tests/test_phi_gradient_manual_data_extraction_campaign_v4_4.py
14 passed in 1.22s
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/manual_data_extraction/
  __init__.py
  schemas.py
  loader.py
  table_review.py
  reviewer.py
  dataset_update.py
  audit_trail.py
  reports.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_manual_data_extraction.py
```

Entrypoint:

```python
run_phi_gradient_manual_data_extraction_campaign(root: str | Path = ".")
```

Campaign command:

```txt
.\.venv\Scripts\python.exe -m phyng.campaigns.phi_gradient_manual_data_extraction
```

Campaign output:

```txt
status = PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
manual_queue_count = 16
reviewed_count = 16
accepted_y_true_count = 0
rejected_count = 16
rerouted_count = 0
matched_prediction_count = 0
ready_for_predictive_gain = false
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
slot4_debt_status = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Note:

```txt
The prompt summary referenced a 5-item queue, but the live v4.3 artifact contains 16 manual table extraction items.
v4.4 reviewed the full artifact instead of truncating it.
```

---

## 3. Input Artifacts

Loaded:

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

---

## 4. Manual Review Metrics

Summary:

| Metric | Result |
|---|---:|
| Manual queue items | 16 |
| Reviewed items | 16 |
| Accepted y_true records | 0 |
| Rejected records | 16 |
| Rerouted records | 0 |
| QC pass count | 0 |
| QC fail count | 16 |
| Location issues | 7 |
| Unit issues | 0 |
| Hash issues | 0 |
| Matched prediction count | 0 |

Decision counts:

| Decision | Count |
|---|---:|
| `REJECT_CONSTRAINT_NOT_YTRUE` | 6 |
| `REJECT_LIMITATION_NOT_YTRUE` | 3 |
| `REJECT_MISSING_LOCATION` | 7 |

Interpretation:

```txt
Parameter bounds and limitation flags were rejected as non-y_true.
Visibility/decoherence-rate candidates were not accepted because the live queue lacks exact page/table/figure location.
No item provided the required table/page/value/unit/hash combination.
```

---

## 5. Generated Data Artifacts

Created:

```txt
data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json
data/y_true/phi_gradient_dataset_quality_report_v4_4.json
data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json
```

Next PredictiveGain inputs:

```txt
ready_for_predictive_gain = false
accepted_y_true_count = 0
matched_prediction_count = 0
minimum_viable_y_true_count = 3
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
recommended_next_phase = v4.5 - Continued Manual/Public Data Acquisition
```

---

## 6. Generated Reports

Created:

```txt
reports/y_true_manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.md
reports/y_true_manual_extraction/phi_gradient_assembled_y_true_dataset_v4_4.md
reports/y_true_manual_extraction/phi_gradient_dataset_quality_report_v4_4.md
reports/y_true_manual_extraction/phi_gradient_next_predictive_gain_inputs_v4_4.md
reports/campaigns/PHI-GRADIENT-MANUAL-DATA-EXTRACTION-v4_4.md
```

All generated reports include the canonical status section.

---

## 7. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_COMPLETED
PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
PHI_GRADIENT_MANUAL_EXTRACTION_READY_FOR_PREDICTIVE_GAIN
PHI_GRADIENT_MANUAL_EXTRACTION_REQUIRES_HUMAN_REVIEW
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

The active status remains:

```txt
Canonical Permission: REVIEW_REQUIRED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 8. New Tests

Created:

```txt
tests/test_manual_data_extraction_loader_v4_4.py
tests/test_manual_table_review_v4_4.py
tests/test_manual_extraction_reviewer_v4_4.py
tests/test_manual_dataset_update_v4_4.py
tests/test_manual_extraction_audit_trail_v4_4.py
tests/test_phi_gradient_manual_data_extraction_campaign_v4_4.py
```

Coverage includes:

```txt
test_missing_manual_queue_blocks_extraction
test_manual_review_requires_source_hash
test_manual_review_requires_location
test_manual_review_rejects_prose_only_visibility
test_manual_review_rejects_missing_unit_for_rate
test_manual_review_accepts_valid_dimensionless_visibility
test_manual_review_accepts_valid_decoherence_rate
test_accepted_ytrue_requires_prediction_match_for_gain
test_predictive_gain_ready_requires_three_records
test_audit_trail_records_every_decision
test_slot4_debt_remains_open_blocking
test_physical_claims_remain_blocked
test_existing_v4_3_behavior_preserved
```

---

## 9. Blocked Claims

The campaign explicitly blocks:

```txt
PHI_GRADIENT is predictively validated.
PHI_GRADIENT has PredictiveGain unless v4.5 computes it.
Gradient mechanism is supported.
SLOT_4 debt is resolved.
Frontera C is validated.
Invariant is empirically confirmed.
```

Allowed statements:

```txt
Manual data extraction was performed.
Accepted y_true records were added if QC passed.
PredictiveGain readiness was evaluated.
SLOT_4 debt remained blocking.
```

---

## 10. Next Gate

Recommended next phase:

```txt
v4.5 - Continued Manual/Public Data Acquisition
```

Immediate blockers:

```txt
No accepted y_true records.
No matched y_true/prediction pairs.
Manual queue lacks exact page/table/figure locations for observable values.
SLOT_4 debt remains OPEN_BLOCKING_FOR_GRADIENT_CLAIMS.
```

---

## 11. Final Assessment

v4.4 did not lower standards to create a dataset.

The useful result is:

```txt
16 manual extraction items were reviewed.
0 items met y_true QC.
PredictiveGain remains undefined.
```

Final discipline note:

```txt
No table/page/value/unit/hash, no y_true.
No y_true threshold, no PredictiveGain.
```

