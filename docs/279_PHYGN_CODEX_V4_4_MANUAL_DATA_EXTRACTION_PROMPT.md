# Codex Prompt — Phygn v4.4 Manual Data Extraction Sprint

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
```

Therefore v4.4 starts at:

```txt
275
```

---

# 1. Read first

Read these v4.4 specs:

```txt
docs/275_PHYGN_V4_4_MANUAL_DATA_EXTRACTION_SPRINT_docs/status/GOAL.md
docs/276_PHYGN_V4_4_MANUAL_EXTRACTION_REVIEW_PROTOCOL.md
docs/277_PHYGN_V4_4_DATASET_UPDATE_AND_PREDICTIVE_GATE_SCHEMA.md
docs/278_PHYGN_V4_4_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
```

Inspect:

```txt
phyng/ytrue_extraction/
phyng/observable_dataset/
phyng/model_comparison/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused prior validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_ytrue_extraction_loader_v4_3.py tests/test_ytrue_source_coverage_audit_v4_3.py tests/test_ytrue_extraction_candidates_v4_3.py tests/test_ytrue_extraction_queues_v4_3.py tests/test_ytrue_dataset_assembly_v4_3.py tests/test_ytrue_quality_report_v4_3.py tests/test_phi_gradient_real_ytrue_extraction_campaign_v4_3.py
```

Expected recent result:

```txt
141 passed for full regression; focused v4.3 tests should pass.
```

Full-suite may remain blocked by unrelated local dependency issues only if already documented.

---

# 3. Mission

Implement:

```txt
v4.4 — Manual Data Extraction Sprint
```

Review the 5-item manual table extraction queue.

Accept y_true only if numeric value, unit, source location, source hash and QC requirements are satisfied.

Do not fabricate y_true.

Do not claim PredictiveGain.

---

# 4. Inputs

Load:

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

Optional:

```txt
data/real_sources/pdfs/
data/real_sources/extracts/
data/real_sources/supplementary/
```

If queue is missing:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

---

# 5. Create package

Create:

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

Create wrapper:

```txt
phyng/campaigns/phi_gradient_manual_data_extraction.py
```

Entrypoint:

```python
run_phi_gradient_manual_data_extraction_campaign(root: str | Path = ".")
```

---

# 6. Review protocol

For each queue item:

```txt
inspect target
inspect source hash
inspect source location hint
inspect available extraction text
attempt to identify explicit numeric measurement
accept only if QC passes
otherwise reject or reroute
```

Do not admit:

```txt
qualitative phrases
constraints
regime bounds
unlocated values
unitless dimensional values
ambiguous numbers
```

---

# 7. Output files

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

# 8. PredictiveGain readiness

Set:

```txt
ready_for_predictive_gain = true
```

only if:

```txt
accepted_y_true_count >= 3
matched_prediction_count >= 3
```

Otherwise:

```txt
PredictiveGain remains undefined.
```

---

# 9. Statuses

Add mappings:

```txt
PHI_GRADIENT_MANUAL_EXTRACTION_COMPLETED
PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
PHI_GRADIENT_MANUAL_EXTRACTION_READY_FOR_PREDICTIVE_GAIN
PHI_GRADIENT_MANUAL_EXTRACTION_REQUIRES_HUMAN_REVIEW
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

---

# 10. Reports

Generate:

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

---

# 11. Tests

Create:

```txt
tests/test_manual_data_extraction_loader_v4_4.py
tests/test_manual_table_review_v4_4.py
tests/test_manual_extraction_reviewer_v4_4.py
tests/test_manual_dataset_update_v4_4.py
tests/test_manual_extraction_audit_trail_v4_4.py
tests/test_phi_gradient_manual_data_extraction_campaign_v4_4.py
```

Minimum tests:

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

# 12. Behavior preservation

Do not alter:

```txt
v4.3 y_true extraction
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
Queued item is y_true.
Manual review candidate is y_true.
PredictiveGain exists before v4.5.
PHI_GRADIENT is validated.
SLOT_4 debt is resolved.
```

Allowed:

```txt
Manual extraction was performed.
Accepted y_true records were added if QC passed.
PredictiveGain readiness was evaluated.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
focused v4.3 tests pass
v4.4 tests pass
all manual queue items reviewed
accepted/rejected records generated
audit trail generated
assembled dataset updated
quality report updated
next predictive-gain inputs generated
reports generated
physical claims remain blocked
SLOT_4 debt remains open
```

---

# 15. Final discipline

```txt
No table/page/value/unit/hash, no y_true.
No y_true threshold, no PredictiveGain.
```
