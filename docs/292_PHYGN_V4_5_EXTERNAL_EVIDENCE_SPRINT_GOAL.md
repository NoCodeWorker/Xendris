# Phygn v4.5 — External Evidence Sprint: Table/Supplement/Public Dataset Acquisition Goal

## 0. Context

The latest confirmed result document is:

```txt
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
```

Therefore, v4.5 starts at:

```txt
292
```

v4.4.2 produced:

```txt
PHYGN_AUDIT_REMEDIATION_PARTIAL
continuation_gate = RESUME_ALLOWED_WITH_RESIDUAL_DEBT
can_continue_pipeline = true
status_mapping_records = 160
quarantine_records = 11
status_only_tests_classified = 95
residual_debt_count = 2
```

v4.4 produced:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
accepted_y_true_count = 0
matched_prediction_count = 0
ready_for_predictive_gain = false
predictive_gain_status = UNDEFINED_INSUFFICIENT_YTRUE
```

v4.5 must not create more internal governance.

v4.5 must bring external evidence or freeze the candidate.

---

## 1. Core thesis

```txt
The next phase must bring numbers or stop the candidate.
```

---

## 2. Hard rule

```txt
No new governance.
No new scoring.
No new benchmark abstraction.
Only external evidence acquisition or candidate freeze.
```

---

## 3. Mission

Implement:

```txt
v4.5 — External Evidence Sprint: Table/Supplement/Public Dataset Acquisition
```

Target:

```txt
accepted_y_true_count >= 3
matched_prediction_count >= 3
```

If the target is reached:

```txt
YTRUE_MINIMUM_THRESHOLD_REACHED
```

If not:

```txt
NO_YTRUE_AVAILABLE_FOR_CURRENT_CANDIDATE
```

or:

```txt
PHI_GRADIENT_REQUIRES_NEW_EXPERIMENT
```

---

## 4. Inputs

Load:

```txt
data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json
data/y_true/phi_gradient_dataset_quality_report_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json
data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json
data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json
data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
data/model_comparison/phi_gradient_model_predictions_v4_1.json
data/real_sources/source_hashes_v3_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json
```

Inspect local assets:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
```

If required prior artifacts are missing:

```txt
PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS
```

---

## 5. Evidence acquisition tracks

v4.5 has exactly three acquisition tracks:

```txt
TRACK_A_TABLE_REVIEW
TRACK_B_SUPPLEMENTARY_SEARCH
TRACK_C_PUBLIC_DATASET_SEARCH
```

No fourth governance track.

---

## 6. Outputs

Create:

```txt
data/external_evidence/phi_gradient_table_review_results_v4_5.json
data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json
data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json
data/external_evidence/phi_gradient_external_y_true_candidates_v4_5.json
data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json
data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json
data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json
data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json
data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json
```

---

## 7. Statuses

```txt
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_COMPLETED
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL
PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS
PHI_GRADIENT_EXTERNAL_EVIDENCE_NO_YTRUE_FOUND
PHI_GRADIENT_EXTERNAL_EVIDENCE_YTRUE_THRESHOLD_REACHED
PHI_GRADIENT_EXTERNAL_EVIDENCE_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE
```

Expected conservative status:

```txt
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL
```

unless the evidence threshold is reached or freeze is triggered.

---

## 8. Candidate freeze logic

If after table/supplement/public search:

```txt
accepted_y_true_count < 3
```

then emit one of:

```txt
PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE
PHI_GRADIENT_EXTERNAL_EVIDENCE_REQUIRES_NEW_EXPERIMENT
```

Do not continue to new internal phases.

---

## 9. SLOT_4 debt interaction

SLOT_4 remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

External y_true for non-SLOT_4 observables may support future benchmark predictive evaluation, but never gradient mechanism support.

---

## 10. Acceptance criteria

v4.5 is complete when:

```txt
v4.4.2 continuation gate loaded
table review completed or explicitly blocked
supplementary search completed or explicitly blocked
public dataset search completed or explicitly blocked
external candidates generated
accepted/rejected y_true generated
assembled y_true dataset updated
PredictiveGain readiness updated
candidate freeze decision generated
reports generated
tests pass
no physical claim upgraded
SLOT_4 debt remains open
```

---

## 11. Final principle

```txt
External evidence is the only valid currency now.
```
