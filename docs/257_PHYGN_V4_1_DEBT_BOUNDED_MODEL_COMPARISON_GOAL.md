# Phygn v4.1 — Debt-Bounded Benchmark Model Comparison Goal

## 0. Context

The latest confirmed document is:

```txt
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
```

Therefore, v4.1 starts at:

```txt
257
```

v4.0 produced:

```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
row_count = 28
alignment_count = 28
negative_control_count = 6
DEBT-SLOT4-GRADIENT-COMPONENT-GAP = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

All benchmark rows must keep:

```txt
gradient_claim_allowed = false
```

v4.1 compares models only inside this debt-bounded space.

---

## 1. Core thesis

```txt
Compare what survived.
Quarantine what did not.
```

v4.1 may compare benchmark behavior.

v4.1 must not claim PHI_GRADIENT is physically validated.

v4.1 must not use benchmark progress to launder SLOT_4 debt.

---

## 2. Hard rule

```txt
No gradient-mechanism claim.
No physical validation.
No Frontera C validation.
No invariant empirical confirmation.
No claim crossing from benchmark fit into mechanism support.
```

---

## 3. Model comparison scope

Compare:

```txt
M_base
M_candidate_debt_bounded
M_negative_control_no_slot4
M_parameter_constrained_variant
M_observable_only_variant
```

Do not compare:

```txt
M_gradient_mechanism_claimed
```

unless SLOT_4 debt is resolved in a later track.

---

## 4. Inputs

v4.1 must load:

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

If SLOT_4 debt is not open/blocking, fail unless explicitly resolved by a valid debt closure artifact.

---

## 5. Outputs

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

## 6. Statuses

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

Expected active status should be conservative.

---

## 7. Metrics

Compute:

```txt
coverage_score
observable_alignment_score
benchmark_fit_score
negative_control_survival_score
parameter_constraint_score
debt_compliance_score
claim_permission_score
```

Do not compute real PredictiveGain unless real observed y_true data exists.

If no y_true exists:

```txt
PredictiveGain = undefined
BenchmarkComparisonScore = allowed
```

---

## 8. Acceptance criteria

v4.1 is complete when:

```txt
v4.0 benchmark loaded
SLOT_4 debt boundary enforced
model registry generated
model predictions generated
benchmark comparison scores generated
negative-control results generated
claim permission update generated
reports generated
tests pass
physical claims remain blocked
```

---

## 9. Final principle

```txt
A model may win a benchmark and still lose permission to make a claim.
```
