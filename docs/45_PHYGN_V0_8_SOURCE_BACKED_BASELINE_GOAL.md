# Phygn v0.8 — Source-Backed Baseline Goal

## 0. Propósito

Phygn v0.8 tiene una misión precisa:

```txt
convertir el baseline de CAMPAIGN-002 desde TOY_INTERNAL hacia SOURCE_BACKED_BASELINE
```

No convertir todavía el candidato boundary-aware en predicción física.  
No declarar PredictiveGain físico.  
No afirmar decoherencia nueva.

El objetivo es más humilde y más fuerte:

```txt
hacer que el modelo base sea físicamente defendible.
```

## 1. Estado heredado

De v0.5:

```txt
CAMPAIGN-001:
B = 7.43e-38
region = NEGATIVE_GRAVITY_BOUND
decoherence overclaim = BLOCKED
```

De v0.6:

```txt
CAMPAIGN-002:
toy model comparison
MODEL_DELTA_ONLY
Gain_C undefined without y_true
evidence_level = 3
```

De v0.7:

```txt
Benchmark protocol
Source requirements
SyntheticGain only
baseline_status = TOY_INTERNAL
candidate_status = HYPOTHETICAL_CANDIDATE
benchmark_status = SYNTHETIC_READY
can_claim_physical_prediction = False
```

## 2. Goal v0.8

Cambiar:

```txt
baseline_status = TOY_INTERNAL
```

a:

```txt
baseline_status = SOURCE_BACKED_BASELINE
```

o, si faltan fuentes:

```txt
baseline_status = BASELINE_REQUIRES_SOURCE
```

## 3. Pregunta científica

```txt
¿Qué modelo base de decoherencia/visibilidad puede Phygn usar como referencia física mínima para comparar candidatos boundary-aware sin inflar claims?
```

## 4. Qué cuenta como baseline físico

Un baseline físico mínimo necesita:

```txt
observable
formula
parameters
assumptions
source support
allowed uses
forbidden uses
```

Ejemplo:

```txt
V_base(t) = exp(-Γ_env t)
```

puede ser un baseline matemático de visibilidad/coherencia solo si está respaldado por fuentes o limitado como aproximación fenomenológica.

## 5. Estados nuevos

```txt
BASELINE_TOY_INTERNAL
BASELINE_REQUIRES_SOURCE
BASELINE_BACKGROUND_SUPPORTED
BASELINE_SOURCE_BACKED_LIMITED
BASELINE_SOURCE_BACKED_READY
BASELINE_CONTRADICTED
```

## 6. Reglas de transición

```txt
TOY_INTERNAL + no source → BASELINE_REQUIRES_SOURCE
BACKGROUND source only → BASELINE_BACKGROUND_SUPPORTED
DIRECT_SUPPORT + HIGH/PRIMARY source → BASELINE_SOURCE_BACKED_LIMITED
DIRECT_SUPPORT + source + parameter mapping + observable → BASELINE_SOURCE_BACKED_READY
CONTRADICTS → BASELINE_CONTRADICTED
```

## 7. Qué puede desbloquear v0.8

Puede desbloquear:

```txt
source-backed baseline comparison
limited physical interpretation of M_base
better campaign report
clear missing requirements for M_C
```

No puede desbloquear todavía:

```txt
physical prediction by M_C
Frontera C validation
gravitational decoherence claim
PredictiveGain from synthetic benchmark
```

## 8. Qué debe seguir bloqueado

```txt
Phygn predicts decoherence.
Boundary C causes decoherence.
The invariant explains decoherence.
SyntheticGain is PredictiveGain.
The baseline source validates the candidate.
```

## 9. Retroalimentación de campañas

v0.8 debe leer resultados anteriores:

```txt
reports/campaigns/CAMPAIGN-001_mesoscopic_boundary_number.md
reports/campaigns/CAMPAIGN-002_decoherence_model_comparison.md
reports/model_comparison/source_backed_readiness.md
reports/rag/source_requirements.md
reports/benchmarks/benchmark_registry.md
```

Y usar esos estados para decidir:

```txt
what is unlocked
what remains blocked
what source is missing
what benchmark is admissible
```

## 10. Criterio de éxito mínimo

v0.8 está completa si:

```txt
1. baseline source requirements are explicit;
2. source-backed baseline schema exists;
3. baseline readiness classifier exists;
4. CAMPAIGN-002 can update baseline_status;
5. reports explain why physical prediction remains blocked;
6. tests pass.
```

## 11. Mantra

```txt
No queremos que el candidato gane todavía.
Queremos que el baseline sea digno de combate.
```
