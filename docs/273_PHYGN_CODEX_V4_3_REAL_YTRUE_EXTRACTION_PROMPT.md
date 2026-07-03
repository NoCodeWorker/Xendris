# Codex Prompt — Phygn v4.3 Real y_true Extraction, Source-Coverage Audit & Dataset Assembly

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
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
```

Therefore v4.3 starts at:

```txt
269
```

---

# 1. Read first

Read these v4.3 specs:

```txt
docs/269_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_docs/status/GOAL.md
docs/270_PHYGN_V4_3_SOURCE_COVERAGE_AUDIT_AND_EXTRACTION_RULES.md
docs/271_PHYGN_V4_3_YTRUE_DATASET_AND_QUALITY_SCHEMA.md
docs/272_PHYGN_V4_3_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
```

Inspect:

```txt
phyng/observable_dataset/
phyng/model_comparison/
phyng/benchmark_construction/
phyng/scientific_debt/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused prior validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_observable_dataset_loader_v4_2.py tests/test_observable_schema_v4_2.py tests/test_observable_normalization_v4_2.py tests/test_ytrue_acquisition_plan_v4_2.py tests/test_dataset_source_registry_v4_2.py tests/test_measurement_readiness_v4_2.py tests/test_phi_gradient_observable_ytrue_campaign_v4_2.py
```

Expected recent result:

```txt
15 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v4.3 — Real y_true Extraction, Source-Coverage Audit & Dataset Assembly
```

Attempt extraction of real observed y_true values from available local/source artifacts.

Do not fabricate data.

Do not infer numeric outcomes from vague prose.

Do not claim PredictiveGain unless the gate criteria are met.

---

# 4. Input files

Load:

```txt
data/observables/phi_gradient_observable_schema_v4_2.json
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json
data/observables/phi_gradient_dataset_source_registry_v4_2.json
data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json
data/observables/phi_gradient_quality_control_rules_v4_2.json
data/observables/phi_gradient_v4_2_next_gate_inputs.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/real_sources/source_hashes_v3_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/model_comparison/phi_gradient_model_predictions_v4_1.json
```

Optional directories:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
```

If required inputs are missing:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN
```

---

# 5. Create package

Create:

```txt
phyng/ytrue_extraction/
  __init__.py
  schemas.py
  loader.py
  source_coverage_audit.py
  extraction_candidates.py
  extraction_queues.py
  dataset_assembly.py
  quality_report.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_real_ytrue_extraction.py
```

Entrypoint:

```python
run_phi_gradient_real_ytrue_extraction_campaign(root: str | Path = ".")
```

---

# 6. Source coverage audit

For every normalized target, audit:

```txt
source hash
local PDF availability
page reference
table reference
figure reference
supplementary availability
public dataset reference
prediction match
```

Do not mark coverage complete unless provenance is sufficient.

---

# 7. Extraction candidates

Attempt extraction only when candidate text contains explicit numeric value with unit or accepted dimensionless variable.

Allowed sources:

```txt
table text
figure digitization metadata
supplementary data
public dataset file
explicit quantitative source text
```

Rejected:

```txt
generic prose
range without measurement
constraint-only values as y_true
limitation flags as y_true
unlocated values
```

---

# 8. Queues

Generate:

```txt
manual_table_extraction_queue
figure_digitization_queue
public_dataset_lookup_queue
supplementary_lookup_queue
```

Do not silently discard blocked targets.

---

# 9. Dataset assembly

Create assembled dataset even if empty.

Only admit y_true records if QC passes.

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

# 10. Output files

Create:

```txt
data/y_true/phi_gradient_source_coverage_audit_v4_3.json
data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json
data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json
data/y_true/phi_gradient_figure_digitization_queue_v4_3.json
data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json
data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json
data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json
data/y_true/phi_gradient_dataset_quality_report_v4_3.json
data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json
```

---

# 11. Reports

Generate:

```txt
reports/y_true/phi_gradient_source_coverage_audit_v4_3.md
reports/y_true/phi_gradient_y_true_extraction_candidates_v4_3.md
reports/y_true/phi_gradient_manual_table_extraction_queue_v4_3.md
reports/y_true/phi_gradient_figure_digitization_queue_v4_3.md
reports/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.md
reports/y_true/phi_gradient_supplementary_lookup_queue_v4_3.md
reports/y_true/phi_gradient_assembled_y_true_dataset_v4_3.md
reports/y_true/phi_gradient_blocked_y_true_targets_v4_3.md
reports/y_true/phi_gradient_dataset_quality_report_v4_3.md
reports/campaigns/PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3.md
```

---

# 12. Statuses

Add mappings:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_COMPLETED
PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL
PHI_GRADIENT_YTRUE_EXTRACTION_NO_VALUES_FOUND
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_FIGURE_DIGITIZATION
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_PUBLIC_DATA_LOOKUP
PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN
PHI_GRADIENT_YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN
```

---

# 13. Tests

Create:

```txt
tests/test_ytrue_extraction_loader_v4_3.py
tests/test_ytrue_source_coverage_audit_v4_3.py
tests/test_ytrue_extraction_candidates_v4_3.py
tests/test_ytrue_extraction_queues_v4_3.py
tests/test_ytrue_dataset_assembly_v4_3.py
tests/test_ytrue_quality_report_v4_3.py
tests/test_phi_gradient_real_ytrue_extraction_campaign_v4_3.py
```

Minimum tests:

```txt
test_missing_ytrue_plan_blocks_extraction
test_source_coverage_requires_hash
test_source_coverage_requires_location_for_complete
test_prose_without_numeric_value_not_ytrue
test_constraint_values_not_admitted_as_ytrue
test_limitation_flags_not_admitted_as_ytrue
test_manual_table_queue_created_for_table_targets
test_public_lookup_queue_created_for_public_targets
test_assembled_dataset_created_even_if_empty
test_predictive_gain_requires_minimum_ytrue_count
test_prediction_matching_required_for_predictive_gain
test_slot4_debt_remains_open_blocking
test_physical_claims_remain_blocked
test_existing_v4_2_behavior_preserved
```

---

# 14. Behavior preservation

Do not alter:

```txt
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure decision
historical reports
```

---

# 15. Do not overclaim

Do not write:

```txt
PredictiveGain exists unless accepted y_true threshold is met.
Extraction candidate is y_true.
Queued target is y_true.
Prose-derived range is observed truth.
PHI_GRADIENT is validated.
SLOT_4 debt is resolved.
```

Allowed:

```txt
y_true extraction was attempted.
Source coverage was audited.
Some targets were queued or blocked.
Accepted y_true records were assembled if QC passed.
PredictiveGain remains undefined unless the threshold is met.
```

---

# 16. Acceptance criteria

Complete when:

```txt
focused v4.2 tests pass
v4.3 tests pass
source coverage audit generated
extraction candidates generated
queues generated
assembled dataset generated
blocked targets generated
quality report generated
next predictive-gain inputs generated
reports generated
physical claims remain blocked
SLOT_4 debt remains open
```

---

# 17. Final discipline

```txt
No provenance, no y_true.
No y_true, no PredictiveGain.
```
