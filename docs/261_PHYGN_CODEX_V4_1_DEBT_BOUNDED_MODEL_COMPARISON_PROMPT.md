# Codex Prompt — Phygn v4.1 Debt-Bounded Benchmark Model Comparison

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
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
```

Therefore v4.1 starts at:

```txt
257
```

---

# 1. Read first

Read these v4.1 specs:

```txt
docs/257_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_docs/status/GOAL.md
docs/258_PHYGN_V4_1_MODEL_REGISTRY_AND_COMPARISON_PROTOCOL.md
docs/259_PHYGN_V4_1_NEGATIVE_CONTROLS_AND_CLAIM_PERMISSION.md
docs/260_PHYGN_V4_1_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
```

Inspect:

```txt
phyng/benchmark_construction/
phyng/scientific_debt/
phyng/source_pressure_decision/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused prior validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_debt_aware_benchmark_loader_v4_0.py tests/test_benchmark_observable_alignment_v4_0.py tests/test_benchmark_rows_v4_0.py tests/test_negative_control_plan_v4_0.py tests/test_scientific_debt_slot4_v4_0.py tests/test_debt_aware_benchmark_reports_v4_0.py tests/test_phi_gradient_debt_aware_benchmark_campaign_v4_0.py
```

Expected recent result:

```txt
14 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v4.1 — Debt-Bounded Benchmark Model Comparison
```

Compare benchmark behavior without using SLOT_4 debt as support.

Do not validate PHI_GRADIENT.

---

# 4. Input files

Load:

```txt
data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json
data/benchmarks/phi_gradient_observable_alignment_v4_0.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/debts/slot4_resolution_plan_v4_0.json
data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json
```

If missing:

```txt
PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK
```

---

# 5. Create package

Create:

```txt
phyng/model_comparison/
  __init__.py
  schemas.py
  loader.py
  model_registry.py
  prediction_builder.py
  scoring.py
  negative_controls.py
  claim_permission.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_debt_bounded_model_comparison.py
```

Entrypoint:

```python
run_phi_gradient_debt_bounded_model_comparison_campaign(root: str | Path = ".")
```

---

# 6. Required models

Create registry for:

```txt
M_base
M_candidate_debt_bounded
M_negative_control_no_slot4
M_parameter_constrained_variant
M_observable_only_variant
```

All models must have:

```txt
uses_slot4_gradient_mechanism = false
```

unless explicitly negative-control annotated.

No model may enable gradient mechanism claim.

---

# 7. Predictions

Generate prediction records for benchmark rows.

These are not real predictions if no observed y_true exists.

Mark:

```txt
uses_real_y_true = false
y_true_available = false
```

unless real observed outcome fields exist.

---

# 8. Scoring

Compute debt-bounded benchmark comparison scores.

If no y_true:

```txt
predictive_gain = null
predictive_gain_status = UNDEFINED_NO_REAL_Y_TRUE
```

Never report synthetic/benchmark ranking as real PredictiveGain.

---

# 9. Negative controls

Run or queue all controls from:

```txt
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
```

Mandatory:

```txt
NO_SLOT4_CONTROL
```

If real observed data is unavailable:

```txt
CONTROL_INCONCLUSIVE
```

Do not fabricate results.

---

# 10. Claim permission

Generate:

```txt
data/model_comparison/phi_gradient_claim_permission_update_v4_1.json
```

Must keep:

```txt
physical_claim_permission = BLOCKED
gradient_mechanism_claim_permission = BLOCKED_BY_SLOT4_DEBT
```

Benchmark claim may be:

```txt
BENCHMARK_COMPARISON_PERFORMED_LIMITED
```

---

# 11. Output files

Create:

```txt
data/model_comparison/phi_gradient_model_registry_v4_1.json
data/model_comparison/phi_gradient_model_predictions_v4_1.json
data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json
data/model_comparison/phi_gradient_negative_control_results_v4_1.json
data/model_comparison/phi_gradient_claim_permission_update_v4_1.json
data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json
```

---

# 12. Reports

Generate:

```txt
reports/model_comparison/phi_gradient_model_registry_v4_1.md
reports/model_comparison/phi_gradient_model_predictions_v4_1.md
reports/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.md
reports/model_comparison/phi_gradient_negative_control_results_v4_1.md
reports/model_comparison/phi_gradient_claim_permission_update_v4_1.md
reports/campaigns/PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1.md
```

---

# 13. Statuses

Add mappings:

```txt
PHI_GRADIENT_MODEL_COMPARISON_COMPLETED
PHI_GRADIENT_MODEL_COMPARISON_PARTIAL
PHI_GRADIENT_MODEL_COMPARISON_BASELINE_WINS
PHI_GRADIENT_MODEL_COMPARISON_CANDIDATE_WINS_LIMITED
PHI_GRADIENT_MODEL_COMPARISON_NEGATIVE_CONTROL_FAIL
PHI_GRADIENT_MODEL_COMPARISON_INCONCLUSIVE
PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK
PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_BY_SLOT4_DEBT
```

---

# 14. Tests

Create:

```txt
tests/test_model_comparison_loader_v4_1.py
tests/test_model_registry_v4_1.py
tests/test_model_prediction_builder_v4_1.py
tests/test_model_scoring_v4_1.py
tests/test_model_negative_controls_v4_1.py
tests/test_model_claim_permission_v4_1.py
tests/test_phi_gradient_debt_bounded_model_comparison_campaign_v4_1.py
```

Minimum tests:

```txt
test_missing_benchmark_blocks_model_comparison
test_model_registry_contains_required_models
test_models_do_not_use_slot4_claim
test_prediction_records_mark_y_true_unavailable
test_predictive_gain_undefined_without_y_true
test_no_slot4_control_is_present
test_negative_controls_inconclusive_without_y_true
test_claim_permission_blocks_physical_claims
test_gradient_claim_blocked_by_slot4_debt
test_reports_include_canonical_section
test_existing_v4_0_behavior_preserved
```

---

# 15. Behavior preservation

Do not alter:

```txt
v4.0 benchmark construction
v3.9 source pressure decision
v3.8.3 priority packet review
v3.8.2 semantic triage
v3.8.1 PDF reader integration
historical reports
```

---

# 16. Do not overclaim

Do not write:

```txt
PHI_GRADIENT has PredictiveGain.
PHI_GRADIENT is validated.
Benchmark win proves physics.
SLOT_4 debt is resolved.
Frontera C is validated.
```

Allowed:

```txt
Debt-bounded model comparison was performed.
Benchmark rows were used for comparison.
PredictiveGain remains undefined without y_true.
Physical and gradient claims remain blocked.
```

---

# 17. Acceptance criteria

Complete when:

```txt
focused v4.0 tests pass
v4.1 tests pass
model registry generated
prediction records generated
comparison scores generated
negative-control results generated
claim permission update generated
reports generated
physical claims remain blocked
```

---

# 18. Final discipline

```txt
A model may win a benchmark and still lose permission to make a claim.
```
