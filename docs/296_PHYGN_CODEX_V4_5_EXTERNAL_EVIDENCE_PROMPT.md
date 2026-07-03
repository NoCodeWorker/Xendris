# Codex Prompt — Phygn v4.5 External Evidence Sprint: Table/Supplement/Public Dataset Acquisition

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current latest result document:

```txt
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
```

Therefore v4.5 starts at:

```txt
292
```

---

# 1. Read first

Read these v4.5 specs:

```txt
docs/292_PHYGN_V4_5_EXTERNAL_EVIDENCE_SPRINT_docs/status/GOAL.md
docs/293_PHYGN_V4_5_EVIDENCE_ACQUISITION_PROTOCOL.md
docs/294_PHYGN_V4_5_DATASET_UPDATE_AND_FREEZE_DECISION.md
docs/295_PHYGN_V4_5_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
docs/285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
```

---

# 2. First action

Run focused remediation validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_audit_remediation_loader_v4_4_2.py tests/test_status_remediation_v4_4_2.py tests/test_status_quarantine_v4_4_2.py tests/test_test_hardening_v4_4_2.py tests/test_claim_metric_remediation_v4_4_2.py tests/test_residual_debt_v4_4_2.py tests/test_audit_remediation_continuation_gate_v4_4_2.py tests/test_phygn_audit_remediation_campaign_v4_4_2.py
```

Expected recent result: v4.4.2 tests pass.

---

# 3. Mission

Implement:

```txt
v4.5 — External Evidence Sprint: Table/Supplement/Public Dataset Acquisition
```

Do not create new governance layer.

Do not create new benchmark abstraction.

Do not compute PredictiveGain.

Only acquire external evidence or freeze PHI_GRADIENT.

---

# 4. Required inputs

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

Inspect:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
```

If prior artifacts missing:

```txt
PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS
```

---

# 5. Create package

Create:

```txt
phyng/external_evidence/
  __init__.py
  schemas.py
  loader.py
  table_review.py
  supplementary_search.py
  public_dataset_search.py
  ytrue_candidates.py
  dataset_update.py
  freeze_decision.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_external_evidence_sprint.py
```

Entrypoint:

```python
run_phi_gradient_external_evidence_sprint_campaign(root: str | Path = ".")
```

---

# 6. Acquisition tracks

Only these tracks are allowed:

```txt
TRACK_A_TABLE_REVIEW
TRACK_B_SUPPLEMENTARY_SEARCH
TRACK_C_PUBLIC_DATASET_SEARCH
```

No new governance track.

---

# 7. Table review

For each rejected/manual item:

```txt
inspect source_id
inspect local PDF path availability
search/extract page/table hints if available
only produce candidate if numeric value and location are explicit
```

Do not fabricate page/table locations.

If no exact location:

```txt
TABLE_NOT_FOUND or PAGE_LOCATION_MISSING
```

---

# 8. Supplementary search

Inspect local supplementary directory.

If no files:

```txt
SUPPLEMENTARY_NOT_FOUND
```

If expected but missing:

```txt
SUPPLEMENTARY_REQUIRES_DOWNLOAD
```

Do not invent URLs.

---

# 9. Public dataset search

Inspect local external dataset directory and known repository references in artifacts.

If no local/known repository data:

```txt
PUBLIC_DATASET_NOT_FOUND
```

Do not fabricate repository results.

---

# 10. External y_true acceptance

Accept only if:

```txt
numeric_value exists
unit exists when dimensional
source_hash exists
source location exists
local or external artifact provenance exists
QC status is PASS or PASS_WITH_LIMITATIONS
matched_prediction_ids is non-empty
```

---

# 11. Freeze decision

If:

```txt
total_y_true_count < 3
```

create freeze decision:

```txt
FROZEN_NO_YTRUE_AVAILABLE
```

or:

```txt
FROZEN_REQUIRES_NEW_EXPERIMENT
```

depending on whether unresolved acquisition paths remain realistic.

---

# 12. Output files

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

# 13. Reports

Generate:

```txt
reports/external_evidence/phi_gradient_table_review_results_v4_5.md
reports/external_evidence/phi_gradient_supplementary_search_results_v4_5.md
reports/external_evidence/phi_gradient_public_dataset_search_results_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_candidates_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_accepted_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_rejected_v4_5.md
reports/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.md
reports/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.md
reports/y_true/phi_gradient_assembled_y_true_dataset_v4_5.md
reports/y_true/phi_gradient_next_predictive_gain_inputs_v4_5.md
reports/campaigns/PHI-GRADIENT-EXTERNAL-EVIDENCE-SPRINT-v4_5.md
```

---

# 14. Statuses

Add mappings:

```txt
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_COMPLETED
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL
PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS
PHI_GRADIENT_EXTERNAL_EVIDENCE_NO_YTRUE_FOUND
PHI_GRADIENT_EXTERNAL_EVIDENCE_YTRUE_THRESHOLD_REACHED
PHI_GRADIENT_EXTERNAL_EVIDENCE_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE
```

---

# 15. Tests

Create:

```txt
tests/test_external_evidence_loader_v4_5.py
tests/test_external_table_review_v4_5.py
tests/test_external_supplementary_search_v4_5.py
tests/test_external_public_dataset_search_v4_5.py
tests/test_external_ytrue_candidates_v4_5.py
tests/test_external_dataset_update_v4_5.py
tests/test_external_freeze_decision_v4_5.py
tests/test_phi_gradient_external_evidence_campaign_v4_5.py
```

Minimum tests:

```txt
test_missing_prior_artifacts_blocks_external_evidence
test_only_three_acquisition_tracks_allowed
test_table_review_does_not_fabricate_page_location
test_supplementary_search_reports_not_found_without_files
test_public_dataset_search_reports_not_found_without_local_data
test_external_ytrue_requires_numeric_value
test_external_ytrue_requires_provenance
test_external_ytrue_requires_prediction_match
test_threshold_reached_allows_next_predictive_gate
test_insufficient_ytrue_freezes_candidate
test_no_predictive_gain_created
test_slot4_debt_remains_open
test_physical_claims_remain_blocked
```

---

# 16. Behavior preservation

Do not alter:

```txt
v4.4.2 audit remediation
v4.4 manual extraction
v4.3 y_true extraction
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure
historical reports
```

---

# 17. Do not overclaim

Do not write:

```txt
Search performed means evidence found.
Candidate found means y_true accepted.
External evidence sprint validates PHI_GRADIENT.
PredictiveGain exists.
SLOT_4 debt is resolved.
```

Allowed:

```txt
External evidence acquisition was attempted.
Accepted y_true records were added if QC passed.
Candidate was frozen if threshold was not reached.
PredictiveGain remains undefined until a later gate computes it.
```

---

# 18. Acceptance criteria

Complete when:

```txt
v4.4.2 continuation gate loaded
v4.5 tests pass
table review results generated
supplementary search results generated
public dataset search results generated
external candidates generated
accepted/rejected y_true generated
assembled dataset updated
candidate freeze decision generated
reports generated
no PredictiveGain created
no physical claim upgraded
SLOT_4 debt remains open
```

---

# 19. Final discipline

```txt
External evidence is the only valid currency now.
```
