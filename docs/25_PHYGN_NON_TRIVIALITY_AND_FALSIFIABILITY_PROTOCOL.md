# Phygn v0.5 — Non-Triviality & Falsifiability Protocol

## 0. Propósito

Este documento define cuándo Phygn produce algo científicamente no trivial.

El core matemático puede ser sólido y aun así no producir nueva física.  
Por eso v0.5 necesita un protocolo de no-trivialidad.

## 1. Problema

Los siguientes resultados son necesarios pero no suficientes:

```txt
λC rg = ℓP²
QB = (ℓP/L)²
Q/B signature
log coordinates
negative bound
```

Pueden ser:

```txt
estructurales
pedagógicos
organizadores
computacionalmente útiles
```

pero no son automáticamente predicciones.

## 2. Test de no-trivialidad

Un resultado de Phygn es no trivial si cumple al menos una condición:

```txt
NT-1:
Produce una cota negativa que bloquea un claim físicamente plausible.

NT-2:
Distingue dos modelos con Gain_C calculable.

NT-3:
Predice una magnitud observable con rango experimental.

NT-4:
Identifica una región prohibida del espacio de parámetros.

NT-5:
Genera una matriz claim-source-test que degrada una hipótesis antes aceptada.

NT-6:
Conecta un invariante estructural a una decisión operacional nueva.

NT-7:
Produce una pregunta experimental cuantitativa que no existía en la formulación inicial.
```

## 3. Clasificación

```txt
TRIVIAL_STRUCTURAL:
identidad matemática o reexpresión dimensional.

STRUCTURAL_USEFUL:
organiza el espacio de parámetros, pero no predice.

NEGATIVE_NONTRIVIAL:
bloquea una familia de claims o descarta una región.

PREDICTIVE_NONTRIVIAL:
produce una predicción cuantitativa diferenciada.

EMPIRICALLY_ACTIONABLE:
propone magnitud observable, rango, sistema y protocolo.
```

## 4. Reglas duras

```txt
STRUCTURAL_TRACE no puede presentarse como PREDICTIVE_TRACE.
NEGATIVE_BOUND_TRACE no puede presentarse como detección positiva.
RAG support no sustituye benchmark.
Benchmark no sustituye fuente.
Fuente no sustituye modelo.
Modelo no sustituye experimento.
```

## 5. Protocolo de falsabilidad

Para que un resultado sea falsable debe tener:

```txt
observable
system
parameters
model_base
model_candidate
error_metric
expected_difference
experimental_threshold
source support
test implementation
```

## 6. Modelo base vs modelo candidato

```python
class ModelComparisonSpec(BaseModel):
    comparison_id: str
    system_id: str
    observable: str
    model_base: str
    model_candidate: str
    parameters: dict
    error_metric: str
    expected_difference: float | None
    experimental_threshold: float | None
    source_ids: list[str]
```

## 7. Predictive Gain

\[
Gain_C = \frac{Error(M_{base}) - Error(M_C)}{Error(M_{base})}
\]

Reglas:

```txt
Gain_C > 0:
candidate improves.

Gain_C = 0:
candidate redundant.

Gain_C < 0:
candidate worse.
```

Pero:

```txt
Gain_C in toy model → limited claim.
Gain_C with real data → stronger claim.
Gain_C without source/model → invalid.
```

## 8. CAMPAIGN-001 status

CAMPAIGN-001 empieza como:

```txt
NEGATIVE_NONTRIVIAL candidate
```

No como:

```txt
PREDICTIVE_NONTRIVIAL
```

Debe producir:

```txt
a reproducible number
a blocked overclaim
a negative bound
a report
```

## 9. CAMPAIGN-002 requirement

Solo si CAMPAIGN-001 está estable:

```txt
CAMPAIGN-002 — Decoherence Model Comparison
```

Debe comparar:

```txt
M_base = standard decoherence model
M_C = boundary-aware modification
```

No implementar hasta tener fuentes.

## 10. Safe language

### Permitido

```txt
Phygn computes a negative bound.
Phygn classifies the claim as unsupported.
Phygn identifies a parameter region where the direct boundary term is negligible.
Phygn generates a research task for missing model support.
```

### Prohibido

```txt
Phygn proves new physics.
Phygn predicts new decoherence without model comparison.
Phygn validates Frontera C.
Phygn detects quantum gravity.
```

## 11. Required report section

Every campaign report must contain:

```txt
Non-triviality status:
TRIVIAL_STRUCTURAL | STRUCTURAL_USEFUL | NEGATIVE_NONTRIVIAL | PREDICTIVE_NONTRIVIAL | EMPIRICALLY_ACTIONABLE

Why:
...

What would falsify/defeat this:
...

What is still missing:
...
```

## 12. Final principle

```txt
Lo no trivial no es lo que suena profundo.
Lo no trivial es lo que cambia una decisión.
```
