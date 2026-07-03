# Phygn v0.6 — CAMPAIGN-002: Decoherence Model Comparison

## 0. Propósito

CAMPAIGN-002 intenta pasar de:

```txt
negative bound
```

a:

```txt
model comparison
```

Sin afirmar nueva física.

La campaña debe comparar:

```txt
M_base
```

contra:

```txt
M_C
```

donde:

```txt
M_base = modelo base de decoherencia mesoscópica
M_C = modelo candidato boundary-aware
```

## 1. Estado inicial

CAMPAIGN-001 mostró:

```txt
B = rg/L = 7.43e-38
```

para:

```txt
m = 1e-17 kg
L = 1e-7 m
```

Esto bloquea claims directos de decoherencia gravitacional basada solo en \(B\).

CAMPAIGN-002 no debe ignorar ese bloqueo.  
Debe partir de él.

## 2. Pregunta científica

```txt
¿Puede un modelo candidato que use la firma Q/B producir una diferencia cuantificable frente a un modelo base de decoherencia, sin violar las cotas negativas ya calculadas?
```

## 3. Modo inicial seguro

Antes de fuentes y modelo físico real, CAMPAIGN-002 debe arrancar como:

```txt
TOY_MODEL_COMPARISON
```

No como:

```txt
PHYSICAL_PREDICTION
```

## 4. ModelComparisonSpec

```python
class ModelComparisonSpec(BaseModel):
    comparison_id: str
    campaign_id: str
    system_id: str

    observable: str
    parameters: dict[str, float]

    model_base_name: str
    model_candidate_name: str

    model_base_description: str
    model_candidate_description: str

    error_metric: str
    epsilon_exp: float | None

    source_ids: list[str]
    benchmark_ids: list[str]
    claim_ids: list[str]

    status: str
```

## 5. ModelComparisonResult

```python
class ModelComparisonResult(BaseModel):
    comparison_id: str
    y_true: list[float] | None
    y_base: list[float]
    y_candidate: list[float]

    error_base: float
    error_candidate: float
    gain_c: float

    delta_series: list[float]
    max_abs_delta: float

    detectability_status: str
    predictive_status: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    required_sources: list[str]
    required_tests: list[str]
    required_next_steps: list[str]
```

## 6. Observable inicial

Observable permitido para toy benchmark:

```txt
visibility_loss
```

o:

```txt
coherence_decay
```

No afirmar que representa un experimento real hasta tener fuentes.

## 7. Modelo base toy

El modelo base puede ser:

\[
V_{base}(t)=e^{-\Gamma_{base} t}
\]

donde:

```txt
Γ_base = gamma_env
```

Estado:

```txt
TOY_BASELINE
REQUIRES_SOURCE_FOR_PHYSICAL_INTERPRETATION
```

## 8. Modelo candidato boundary-aware toy

Debe ser mínimo y explícito.

Ejemplo permitido:

\[
V_C(t)=e^{-(\Gamma_{base} + \Delta\Gamma_C)t}
\]

donde:

\[
\Delta\Gamma_C = \alpha \cdot f(Q,B,L)
\]

Pero por defecto debe estar bloqueado para interpretación física fuerte.

## 9. Funciones candidatas permitidas

Solo toy:

```txt
f(Q,B,L) = B
f(Q,B,L) = QB
f(Q,B,L) = abs(log10(B))^-1
```

Prohibido:

```txt
f arbitraria elegida para producir buen resultado
```

Todo \(f\) debe registrarse con:

```txt
formula
reason
status
forbidden_interpretations
```

## 10. Detectabilidad

Dado:

```txt
epsilon_exp
```

calcular:

```txt
max_abs_delta = max(|V_C(t)-V_base(t)|)
```

Clasificar:

```txt
if max_abs_delta <= epsilon_exp:
    UNDETECTABLE_DIFFERENCE

else:
    DETECTABLE_TOY_DIFFERENCE
```

No usar "detectable" como claim físico real salvo fuente experimental.

## 11. Predictive Gain

Si hay `y_true`:

\[
Gain_C = \frac{Error(M_{base}) - Error(M_C)}{Error(M_{base})}
\]

Si no hay `y_true`, no hay Predictive Gain real.

Puede haber:

```txt
MODEL_DELTA_ONLY
```

pero no:

```txt
POSITIVE_GAIN
```

## 12. Estados permitidos

```txt
REQUIRES_SOURCE
REQUIRES_MODEL
MODEL_DELTA_ONLY
UNDETECTABLE_DIFFERENCE
DETECTABLE_TOY_DIFFERENCE
ZERO_GAIN
NEGATIVE_GAIN
POSITIVE_TOY_GAIN
PREDICTIVE_CANDIDATE
```

## 13. Claims permitidos

Si solo hay toy benchmark:

```txt
The boundary-aware toy candidate produces a computed delta under explicit assumptions.
```

Si delta no detectable:

```txt
The candidate difference is below the selected detectability threshold.
```

Si hay positive toy gain:

```txt
The candidate improves the toy benchmark under the selected metric, but no physical prediction is claimed.
```

## 14. Claims bloqueados

```txt
Phygn predicts gravitational decoherence.
Phygn explains collapse.
Boundary C causes decoherence.
This validates Frontera C.
```

## 15. RAG requirements

Crear ResearchTasks para:

```txt
standard decoherence visibility decay
environmental decoherence in matter-wave interferometry
Caldeira-Leggett if used
Diósi-Penrose if used
MAQRO-like expected visibility/noise if referenced
experimental visibility thresholds
```

## 16. Reporte

Generar:

```txt
reports/campaigns/CAMPAIGN-002_decoherence_model_comparison.md
```

Debe incluir:

```txt
Scientific Question
CAMPAIGN-001 inherited bound
Model Base
Model Candidate
Observable
Parameters
Source Status
Benchmark Data
Error Metric
Gain_C
Detectability
Allowed Claims
Blocked Claims
Next Required Research
```

## 17. Tests

```txt
tests/test_campaign_002_model_comparison.py
tests/test_model_comparison_gain.py
tests/test_model_comparison_detectability.py
tests/test_campaign_002_gatekeeper.py
```

Casos:

```txt
test_no_y_true_means_no_predictive_gain
test_candidate_delta_below_epsilon_is_undetectable
test_positive_toy_gain_not_physical_prediction
test_decoherence_overclaim_blocked
test_missing_sources_create_research_tasks
test_campaign_002_report_generated
```

## 18. Criterio de éxito

CAMPAIGN-002 es exitosa aunque concluya:

```txt
NO_PREDICTIVE_GAIN
```

si lo hace de forma rigurosa.

Éxito mínimo:

```txt
modelo base toy
modelo candidato toy
delta calculado
detectabilidad clasificada
overclaims bloqueados
research tasks creadas
tests pasan
reporte generado
```

## 19. Frase final

```txt
Una predicción que no pasa por benchmark no es una predicción.
Es una tentación.
```
