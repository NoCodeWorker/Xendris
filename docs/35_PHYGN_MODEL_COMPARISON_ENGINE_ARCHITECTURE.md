# Phygn v0.6 — Model Comparison Engine Architecture

## 0. Propósito

Este documento define la arquitectura del motor de comparación de modelos.

El motor debe permitir:

```txt
modelo base
modelo candidato
observable
serie temporal o datos
métrica de error
detectabilidad
Predictive Gain
claim decision
```

## 1. Módulos

```txt
phyng/model_comparison/
  __init__.py
  schemas.py
  models.py
  metrics.py
  detectability.py
  comparison.py
  report.py
```

## 2. Data flow

```txt
ModelComparisonSpec
→ generate y_base
→ generate y_candidate
→ optional y_true
→ error metric
→ Gain_C
→ detectability
→ Gatekeeper
→ report
```

## 3. Schemas

### ModelSeries

```python
class ModelSeries(BaseModel):
    name: str
    t: list[float]
    y: list[float]
    observable: str
    assumptions: list[str]
```

### ModelComparisonSpec

```python
class ModelComparisonSpec(BaseModel):
    comparison_id: str
    system_id: str
    observable: str
    t: list[float]
    parameters: dict[str, float]
    epsilon_exp: float | None
    source_ids: list[str]
    status: str
```

### ModelComparisonResult

```python
class ModelComparisonResult(BaseModel):
    comparison_id: str
    y_base: list[float]
    y_candidate: list[float]
    y_true: list[float] | None
    error_base: float | None
    error_candidate: float | None
    gain_c: float | None
    max_abs_delta: float
    detectability_status: str
    predictive_status: str
    allowed_claims: list[str]
    blocked_claims: list[str]
```

## 4. Toy model functions

```python
def exponential_visibility(t: np.ndarray, gamma: float) -> np.ndarray:
    return np.exp(-gamma * t)
```

Boundary-aware toy:

```python
def boundary_aware_visibility(
    t: np.ndarray,
    gamma_base: float,
    delta_gamma_c: float
) -> np.ndarray:
    return np.exp(-(gamma_base + delta_gamma_c) * t)
```

## 5. Boundary coupling functions

Allowed initial toy functions:

```python
delta_gamma = alpha * B
delta_gamma = alpha * QB
delta_gamma = alpha / abs(log10(B))
```

Rules:

```txt
must be explicit
must be marked TOY
must not be interpreted physically without sources
must be tested
```

## 6. Error metrics

Implement:

```txt
MSE
MAE
RMSE
```

## 7. Predictive Gain calculation

If `y_true` is absent:

```txt
gain_c = None
predictive_status = MODEL_DELTA_ONLY
```

If present:

```txt
gain_c = (error_base - error_candidate) / error_base
```

Handle:

```txt
error_base = 0
division safety
same-length arrays
NaN rejection
```

## 8. Detectability

```python
max_abs_delta = max(abs(y_candidate - y_base))
```

If epsilon missing:

```txt
DETECTABILITY_REQUIRES_EPSILON
```

If:

```txt
max_abs_delta <= epsilon_exp
```

then:

```txt
UNDETECTABLE_DIFFERENCE
```

Else:

```txt
DETECTABLE_TOY_DIFFERENCE
```

## 9. Claim generation

Allowed:

```txt
The candidate produces a computed toy delta.
The delta is below/above the selected epsilon threshold.
The candidate improves the toy benchmark under the selected metric.
```

Blocked:

```txt
The candidate predicts real decoherence.
The candidate validates Frontera C.
The boundary term causes collapse.
```

## 10. Report

Generate:

```txt
reports/model_comparison/{comparison_id}.md
```

Sections:

```txt
Input
Models
Observable
Parameters
Source Status
Series Summary
Error Metric
Gain_C
Detectability
Allowed Claims
Blocked Claims
Limitations
Next Tasks
```

## 11. Tests

```txt
tests/test_model_comparison_metrics.py
tests/test_model_comparison_engine.py
tests/test_model_comparison_report.py
```

Required:

```txt
test_mse
test_mae
test_rmse
test_gain_none_without_y_true
test_gain_positive_when_candidate_better
test_detectability_requires_epsilon
test_delta_below_epsilon
test_report_generated
test_overclaim_blocked
```

## 12. Acceptance

The engine is accepted when it can say:

```txt
This candidate changes the toy observable by X.
That change is or is not above epsilon.
Gain_C is undefined without y_true.
No physical prediction is allowed yet.
```

## 13. Final rule

```txt
A model comparison is not a prophecy.
It is a controlled fight between hypotheses.
```
