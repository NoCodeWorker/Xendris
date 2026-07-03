# Phygn v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan Goal

## 0. Context

The latest confirmed document is:

```txt
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
```

Therefore, v4.2 starts at:

```txt
263
```

v4.1 produced:

```txt
PHI_GRADIENT_MODEL_COMPARISON_COMPLETED
PredictiveGain = UNDEFINED_NO_REAL_Y_TRUE
physical_claim_permission = BLOCKED
gradient_mechanism_claim_permission = BLOCKED_BY_SLOT4_DEBT
```

v4.1 generated:

```txt
140 prediction records
5 models × 28 benchmark rows
uses_real_y_true = false
y_true_available = false
```

v4.2 must convert benchmark rows into normalized observable targets and define how real observed truth (`y_true`) can be acquired.

---

## 1. Core thesis

```txt
No y_true, no PredictiveGain.
No PredictiveGain, no predictive claim.
```

v4.2 does not validate PHI_GRADIENT.

v4.2 prepares the conditions under which future predictive validation could become possible.

---

## 2. Hard rule

```txt
Do not fabricate y_true.
Do not infer y_true from source text alone.
Do not treat benchmark rows as observed outcomes.
Do not convert literature ranges into truth labels unless explicitly measured.
Do not claim PredictiveGain.
Do not relax SLOT_4 debt.
```

---

## 3. Goal

Create:

```txt
normalized observable schema
observable target dataset
y_true acquisition plan
dataset source registry
measurement readiness matrix
quality-control rules
next acquisition gate inputs
```

---

## 4. Inputs

v4.2 must load:

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

## 5. Outputs

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

## 6. Observable classes

Normalize observables into:

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

---

## 7. y_true classes

For each observable target, define:

```txt
Y_TRUE_AVAILABLE
Y_TRUE_ACQUIRABLE_PUBLIC_DATA
Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION
Y_TRUE_REQUIRES_EXPERIMENT
Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE
Y_TRUE_BLOCKED_BY_AMBIGUITY
```

---

## 8. SLOT_4 debt interaction

SLOT_4 remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

v4.2 may include a field:

```txt
slot4_debt_status
```

but must not close or relax the debt.

---

## 9. Statuses

```txt
PHI_GRADIENT_OBSERVABLE_DATASET_NORMALIZED
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
PHI_GRADIENT_YTRUE_PLAN_PARTIAL
PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON
PHI_GRADIENT_YTRUE_PLAN_NO_ACQUIRABLE_TARGETS
PHI_GRADIENT_YTRUE_PLAN_REQUIRES_EXPERIMENTAL_DATA
```

Expected active status:

```txt
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
```

if at least one target is acquirable.

---

## 10. Acceptance criteria

v4.2 is complete when:

```txt
v4.1 model comparison files loaded
observables normalized
observable targets generated
y_true acquisition plan generated
dataset source registry generated
measurement readiness matrix generated
quality-control rules generated
reports generated
tests pass
PredictiveGain remains undefined
physical claims remain blocked
SLOT_4 debt remains blocking
```

---

## 11. Final principle

```txt
A benchmark becomes scientific only when it can meet observed truth.
```
