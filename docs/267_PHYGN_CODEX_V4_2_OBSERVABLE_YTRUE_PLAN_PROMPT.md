# Codex Prompt — Phygn v4.2 Observable Dataset Normalization & Real y_true Acquisition Plan

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
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
```

Therefore v4.2 starts at:

```txt
263
```

---

# 1. Read first

Read these v4.2 specs:

```txt
docs/263_PHYGN_V4_2_OBSERVABLE_DATASET_NORMALIZATION_docs/status/GOAL.md
docs/264_PHYGN_V4_2_OBSERVABLE_SCHEMA_AND_NORMALIZATION_RULES.md
docs/265_PHYGN_V4_2_YTRUE_ACQUISITION_PLAN_SCHEMA.md
docs/266_PHYGN_V4_2_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
```

Inspect:

```txt
phyng/model_comparison/
phyng/benchmark_construction/
phyng/scientific_debt/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused prior validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_model_comparison_loader_v4_1.py tests/test_model_registry_v4_1.py tests/test_model_prediction_builder_v4_1.py tests/test_model_scoring_v4_1.py tests/test_model_negative_controls_v4_1.py tests/test_model_claim_permission_v4_1.py tests/test_phi_gradient_debt_bounded_model_comparison_campaign_v4_1.py
```

Expected recent result:

```txt
12 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan
```

Normalize benchmark rows into observable targets and define a plan for acquiring real y_true.

Do not fabricate y_true.

Do not claim PredictiveGain.

---

# 4. Input files

Load:

```txt
data/model_comparison/phi_gradient_model_registry_v4_1.json
data/model_comparison/phi_gradient_model_predictions_v4_1.json
data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json
data/model_comparison/phi_gradient_negative_control_results_v4_1.json
data/model_comparison/phi_gradient_claim_permission_update_v4_1.json
data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/benchmarks/phi_gradient_observable_alignment_v4_0.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

If missing:

```txt
PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON
```

---

# 5. Create package

Create:

```txt
phyng/observable_dataset/
  __init__.py
  schemas.py
  loader.py
  observable_schema.py
  normalization.py
  ytrue_acquisition.py
  dataset_registry.py
  readiness.py
  quality_control.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_observable_ytrue_plan.py
```

Entrypoint:

```python
run_phi_gradient_observable_ytrue_plan_campaign(root: str | Path = ".")
```

---

# 6. Normalize observables

Normalize benchmark rows into:

```txt
VISIBILITY
COHERENCE_LOSS
DECOHERENCE_RATE
CONTRAST_DECAY
MASS_REGIME
TIME_REGIME
SEPARATION_REGIME
TEMPERATURE_PRESSURE_REGIME
PARAMETER_BOUND
LIMITATION_FLAG
EXPERIMENTAL_CONTEXT
```

Create normalized targets.

Every target must include:

```txt
y_true_required = true
predictive_gain_allowed = false
slot4_debt_status = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

unless observed truth is explicitly available.

---

# 7. y_true plan

For each target, assign:

```txt
Y_TRUE_AVAILABLE
Y_TRUE_ACQUIRABLE_PUBLIC_DATA
Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION
Y_TRUE_REQUIRES_EXPERIMENT
Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE
Y_TRUE_BLOCKED_BY_AMBIGUITY
```

Do not set `Y_TRUE_AVAILABLE` unless real observed numeric values are present in input artifacts.

---

# 8. Acquisition methods

Use:

```txt
PUBLIC_DATASET_LOOKUP
MANUAL_TABLE_EXTRACTION
MANUAL_FIGURE_DIGITIZATION
SUPPLEMENTARY_DATA_EXTRACTION
AUTHOR_DATA_REQUEST
NEW_EXPERIMENT_REQUIRED
NOT_ACQUIRABLE_FROM_CURRENT_SOURCES
```

---

# 9. Output files

Create:

```txt
data/observables/phi_gradient_observable_schema_v4_2.json
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json
data/observables/phi_gradient_dataset_source_registry_v4_2.json
data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json
data/observables/phi_gradient_quality_control_rules_v4_2.json
data/observables/phi_gradient_v4_2_next_gate_inputs.json
```

---

# 10. Reports

Generate:

```txt
reports/observables/phi_gradient_observable_schema_v4_2.md
reports/observables/phi_gradient_normalized_observable_targets_v4_2.md
reports/observables/phi_gradient_y_true_acquisition_plan_v4_2.md
reports/observables/phi_gradient_dataset_source_registry_v4_2.md
reports/observables/phi_gradient_measurement_readiness_matrix_v4_2.md
reports/observables/phi_gradient_quality_control_rules_v4_2.md
reports/campaigns/PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2.md
```

---

# 11. Statuses

Add mappings:

```txt
PHI_GRADIENT_OBSERVABLE_DATASET_NORMALIZED
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
PHI_GRADIENT_YTRUE_PLAN_PARTIAL
PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON
PHI_GRADIENT_YTRUE_PLAN_NO_ACQUIRABLE_TARGETS
PHI_GRADIENT_YTRUE_PLAN_REQUIRES_EXPERIMENTAL_DATA
```

---

# 12. Tests

Create:

```txt
tests/test_observable_dataset_loader_v4_2.py
tests/test_observable_schema_v4_2.py
tests/test_observable_normalization_v4_2.py
tests/test_ytrue_acquisition_plan_v4_2.py
tests/test_dataset_source_registry_v4_2.py
tests/test_measurement_readiness_v4_2.py
tests/test_phi_gradient_observable_ytrue_campaign_v4_2.py
```

Minimum tests:

```txt
test_missing_model_comparison_blocks_ytrue_plan
test_observable_schema_contains_required_classes
test_normalized_targets_keep_predictive_gain_blocked
test_no_y_true_available_without_numeric_observed_values
test_visibility_maps_to_dimensionless_float
test_parameter_bounds_not_treated_as_y_true
test_limitation_flags_not_treated_as_y_true
test_dataset_source_registry_created
test_measurement_readiness_matrix_created
test_quality_control_requires_hash_traceability
test_slot4_debt_remains_open_blocking
test_physical_claims_remain_blocked
test_existing_v4_1_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure decision
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
y_true was acquired if it was only planned.
PredictiveGain exists.
Benchmark rows are observed truth.
PHI_GRADIENT is validated.
SLOT_4 debt is resolved.
```

Allowed:

```txt
Observable targets were normalized.
A y_true acquisition plan was generated.
PredictiveGain remains undefined.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
focused v4.1 tests pass
v4.2 tests pass
observable schema generated
normalized targets generated
y_true acquisition plan generated
dataset registry generated
readiness matrix generated
quality-control rules generated
reports generated
PredictiveGain remains undefined
physical claims remain blocked
SLOT_4 debt remains open
```

---

# 16. Final discipline

```txt
No y_true, no PredictiveGain.
No PredictiveGain, no predictive claim.
```
