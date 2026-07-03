# Phygn v0.7 — Source-Backed Model Comparison Protocol

## 0. Propósito

Este documento define cómo CAMPAIGN-002 puede evolucionar desde toy model comparison hacia source-backed model comparison.

## 1. Estados del modelo

```txt
TOY_MODEL:
interno, matemáticamente explícito, sin claim físico fuerte.

SOURCE_BACKED_BASELINE:
modelo base soportado por fuente.

SOURCE_BACKED_CANDIDATE:
modelo candidato soportado por fuente o justificado como hipótesis explícita.

BENCHMARK_READY:
existe dataset válido.

GAIN_READY:
se puede calcular Gain bajo etiqueta correcta.

PREDICTIVE_CANDIDATE:
diferencia cuantificada, fuente y benchmark, pero aún no experimento propio.

EMPIRICALLY_ACTIONABLE:
observable, protocolo, umbral y datos permiten propuesta experimental.
```

## 2. SourceBackedModelSpec

```python
class SourceBackedModelSpec(BaseModel):
    model_id: str
    name: str
    model_role: str  # BASELINE | CANDIDATE
    formula: str
    parameters: dict[str, float]
    assumptions: list[str]
    source_ids: list[str]
    support_status: str
    allowed_claims: list[str]
    forbidden_claims: list[str]
```

## 3. Model support statuses

```txt
UNSUPPORTED
TOY_INTERNAL
BACKGROUND_SUPPORTED
DIRECTLY_SUPPORTED
CONTRADICTED
REQUIRES_SOURCE
```

## 4. Comparison readiness

```python
class SourceBackedComparisonReadiness(BaseModel):
    comparison_id: str
    baseline_status: str
    candidate_status: str
    benchmark_status: str
    can_compute_gain: bool
    can_claim_physical_prediction: bool
    max_claim_level: int
    missing_requirements: list[str]
```

## 5. Minimum transition rules

### From TOY to SOURCE_BACKED_BASELINE

Need:

```txt
baseline formula source
parameter interpretation
observable source
```

### From SOURCE_BACKED_BASELINE to BENCHMARK_READY

Need:

```txt
BenchmarkDataset valid
provenance not PLACEHOLDER
compatible observable
```

### From BENCHMARK_READY to GAIN_READY

Need:

```txt
y_true
y_base
y_candidate
metric
error_base > 0
```

### From GAIN_READY to PREDICTIVE_CANDIDATE

Need:

```txt
Gain_C result
detectability threshold
source-backed model status
claim gatekeeper pass
```

## 6. Candidate model discipline

The candidate model may initially be:

```txt
hypothesis model
```

but must be marked:

```txt
HYPOTHETICAL_CANDIDATE
```

unless source-backed.

Allowed:

```txt
The candidate is a testable hypothesis under explicit assumptions.
```

Blocked:

```txt
The candidate is physically validated.
```

## 7. Comparison report

Generate:

```txt
reports/model_comparison/source_backed_readiness.md
```

Include:

```txt
baseline support
candidate support
benchmark readiness
Gain permissions
claim ladder
blocked overclaims
next missing evidence
```

## 8. Tests

```txt
tests/test_source_backed_model_spec.py
tests/test_source_backed_comparison_readiness.py
```

Cases:

```txt
test_unsupported_baseline_blocks_physical_comparison
test_source_backed_baseline_allows_model_comparison
test_placeholder_benchmark_blocks_gain
test_synthetic_benchmark_allows_synthetic_gain_only
test_candidate_hypothesis_limits_claim_level
```

## 9. Final rule

```txt
Un modelo candidato no tiene derecho predictivo.
Debe ganárselo contra un baseline.
```
