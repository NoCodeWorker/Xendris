# Phygn v4.1 — Model Registry & Comparison Protocol

## 0. Purpose

This document defines debt-bounded model comparison.

---

## 1. Model registry

Create:

```txt
data/model_comparison/phi_gradient_model_registry_v4_1.json
```

Required model records:

```txt
M_base
M_candidate_debt_bounded
M_negative_control_no_slot4
M_parameter_constrained_variant
M_observable_only_variant
```

---

## 2. Model record schema

```python
class ModelRegistryRecord(BaseModel):
    model_id: str
    model_name: str
    model_family: str
    allowed_claim_scope: str
    uses_slot4_gradient_mechanism: bool
    slot4_debt_compliant: bool
    input_features: list[str]
    output_observables: list[str]
    parameter_constraints_used: list[str]
    limitations: list[str]
    blocked_claims: list[str]
```

---

## 3. Required model definitions

### M_base

```txt
baseline decoherence / observable benchmark model
```

Allowed:

```txt
baseline comparison
observable alignment
benchmark range reference
```

Blocked:

```txt
gradient mechanism claim
```

### M_candidate_debt_bounded

```txt
PHI_GRADIENT-derived benchmark candidate without gradient mechanism claim
```

Allowed:

```txt
compare benchmark behavior
use source-pressure-limited observables
use parameter constraints
```

Blocked:

```txt
physical gradient mechanism
SLOT_4 support
Frontera C validation
```

### M_negative_control_no_slot4

```txt
candidate with SLOT_4 dynamics zeroed or removed
```

Purpose:

```txt
test whether benchmark behavior depends on unsupported SLOT_4 mechanism
```

### M_parameter_constrained_variant

```txt
candidate constrained by SLOT_5 parameter extracts
```

### M_observable_only_variant

```txt
model using only source-backed observable alignment
```

---

## 4. Prediction records

Create:

```txt
data/model_comparison/phi_gradient_model_predictions_v4_1.json
```

Schema:

```python
class ModelPredictionRecord(BaseModel):
    prediction_id: str
    model_id: str
    benchmark_id: str
    source_id: str
    observable_type: str
    predicted_behavior: str
    prediction_basis: str
    uses_real_y_true: bool
    y_true_available: bool
    comparison_allowed: bool
    limitations: list[str]
```

---

## 5. Comparison scores

Create:

```txt
data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json
```

Schema:

```python
class BenchmarkComparisonScore(BaseModel):
    score_id: str
    model_id: str
    benchmark_row_count: int
    observable_alignment_score: float
    benchmark_coverage_score: float
    parameter_constraint_score: float
    negative_control_score: float
    debt_compliance_score: float
    aggregate_score: float
    predictive_gain: float | None
    predictive_gain_status: str
    verdict: str
    limitations: list[str]
```

---

## 6. PredictiveGain rule

```txt
If y_true is unavailable:
  predictive_gain = null
  predictive_gain_status = UNDEFINED_NO_REAL_Y_TRUE
```

Never report synthetic score as PredictiveGain.

---

## 7. Final principle

```txt
Comparison without observed truth is ranking, not prediction validation.
```
