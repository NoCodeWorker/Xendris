# Phygn v0.8 — Visibility Decay Baseline Protocol

## 0. Propósito

Este documento define un baseline mínimo para CAMPAIGN-002:

\[
V_{base}(t)=e^{-\Gamma t}
\]

como modelo fenomenológico de pérdida de visibilidad/coherencia.

Este baseline no debe presentarse como universal.  
Debe presentarse como una referencia mínima, explícita y auditable.

## 1. Baseline formula

\[
V_{base}(t)=e^{-\Gamma_{env}t}
\]

donde:

```txt
V_base(t): visibility/coherence proxy
Γ_env: environmental decoherence or effective decay rate
t: time
```

## 2. Status inicial

Sin fuentes:

```txt
TOY_INTERNAL
```

Con fuente contextual:

```txt
BACKGROUND_SUPPORTED
```

Con fuente directa:

```txt
SOURCE_BACKED_LIMITED
```

Con fuente + parameter mapping + assumptions:

```txt
SOURCE_BACKED_READY
```

## 3. Required metadata

```python
class VisibilityDecayBaselineSpec(BaseModel):
    model_id: str
    formula: str
    observable: str
    gamma_parameter_name: str
    gamma_value: float | None
    gamma_units: str
    assumptions: list[str]
    source_ids: list[str]
    support_status: str
    allowed_uses: list[str]
    forbidden_uses: list[str]
```

## 4. Allowed uses

```txt
baseline comparison
toy-to-source-backed transition
visibility/coherence decay reference
limited model comparison
```

## 5. Forbidden uses

```txt
universal decoherence model
proof of physical mechanism
validation of boundary candidate
experimental prediction without data
```

## 6. Parameter discipline

If `gamma_value` is arbitrary:

```txt
PARAMETER_TOY
```

If sourced:

```txt
PARAMETER_SOURCE_BACKED
```

If fit to data:

```txt
PARAMETER_FITTED
```

If experimental:

```txt
PARAMETER_EXPERIMENTAL
```

## 7. BaselineReadinessResult

```python
class BaselineReadinessResult(BaseModel):
    model_id: str
    support_status: str
    parameter_status: str
    can_be_used_as_baseline: bool
    max_claim_level: int
    missing_requirements: list[str]
    allowed_claims: list[str]
    blocked_claims: list[str]
```

## 8. Claim ladder effect

```txt
TOY_INTERNAL:
max_claim_level = 3

SOURCE_BACKED_LIMITED:
max_claim_level = 4 or 5 depending benchmark

SOURCE_BACKED_READY:
max_claim_level = 5

EXPERIMENTAL_PARAMETER:
may allow higher readiness but not candidate prediction alone
```

## 9. Tests

```txt
tests/test_visibility_decay_baseline.py
tests/test_baseline_readiness.py
```

Cases:

```txt
test_baseline_without_sources_is_toy_internal
test_arbitrary_gamma_is_parameter_toy
test_source_backed_formula_allows_limited_baseline
test_baseline_does_not_unlock_candidate_prediction
test_missing_assumptions_blocks_ready_status
```

## 10. Report

Generate:

```txt
reports/model_comparison/visibility_decay_baseline_readiness.md
```

Sections:

```txt
Formula
Observable
Parameter Status
Source Support
Allowed Uses
Forbidden Uses
Readiness
Claim Level
```

## 11. Final principle

```txt
Un baseline físico no prueba al candidato.
Solo le da un adversario legítimo.
```
