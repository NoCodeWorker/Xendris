# Phygn v0.9 — Real Source Ingestion & Baseline Upgrade Attempt

## 0. Propósito

Phygn v0.8 dejó el baseline en:

```txt
baseline_before = TOY_INTERNAL
baseline_after  = BASELINE_REQUIRES_SOURCE
max_claim_level = 3
can_be_used_as_baseline = False
```

Eso fue correcto.

v0.9 debe intentar el siguiente paso:

```txt
BASELINE_REQUIRES_SOURCE
→ BASELINE_SOURCE_BACKED_LIMITED
```

pero solo si existen fuentes reales, registradas y auditadas.

No se permite fingir ingesta.
No se permite desbloquear claims físicos del candidato.
No se permite convertir fuente del baseline en validación de Frontera C.

## 1. Objetivo central

Crear una campaña ejecutable de ingesta real de fuentes para el baseline de decoherencia/visibilidad:

```txt
CAMPAIGN-002 baseline physicalization attempt
```

La meta es responder:

```txt
¿Existen fuentes suficientes para tratar V_base(t)=exp(-Γt) como baseline físico limitado?
```

No:

```txt
¿Frontera C queda validada?
```

## 2. Estado heredado

De v0.5:

```txt
NEGATIVE_GRAVITY_BOUND
B = 7.43e-38
decoherence overclaim blocked
```

De v0.6:

```txt
MODEL_DELTA_ONLY
Gain_C undefined without y_true
```

De v0.7:

```txt
SyntheticGain only
no PredictiveGain
```

De v0.8:

```txt
BASELINE_REQUIRES_SOURCE
4 baseline ResearchTasks created
candidate prediction blocked
169 tests passed
```

## 3. Goal v0.9

Implementar:

```txt
SourceCandidate
SourceIngestionPipeline
CitationAudit
BaselineSourcePack
BaselineUpgradeAttempt
```

y producir:

```txt
SOURCE_INGESTED
SOURCE_REJECTED
SOURCE_CANDIDATE_ONLY
BASELINE_SOURCE_BACKED_LIMITED
BASELINE_STILL_REQUIRES_SOURCE
```

## 4. Tipos de fuente

```txt
LOCAL_FILE:
PDF/MD/TXT/HTML local dentro del proyecto.

MANUAL_RECORD:
metadata introducida manualmente con campos explícitos.

EXTERNAL_URL_RECORD:
URL registrada pero no ingerida.

RESEARCH_TASK_ONLY:
tarea pendiente, sin fuente real.

BIBTEX_RECORD:
registro bibliográfico, requiere validación.
```

## 5. Regla dura

```txt
EXTERNAL_URL_RECORD alone is not SOURCE_INGESTED.
MANUAL_RECORD without metadata audit is not DIRECT_SUPPORT.
RESEARCH_TASK_ONLY never unlocks baseline.
```

## 6. Condiciones para baseline limited

El baseline puede pasar a:

```txt
BASELINE_SOURCE_BACKED_LIMITED
```

si tiene, como mínimo:

```txt
1. una fuente HIGH o PRIMARY;
2. support_type = FORMULA_SUPPORT;
3. support_type = OBSERVABLE_SUPPORT;
4. CitationAudit passed;
5. no contradiction active;
6. report generated;
7. tests passed.
```

## 7. Condiciones para baseline ready

El baseline puede pasar a:

```txt
BASELINE_SOURCE_BACKED_READY
```

solo si además tiene:

```txt
PARAMETER_SUPPORT
assumptions support
units support
allowed uses
forbidden uses
```

v0.9 no necesita alcanzar READY.  
El objetivo realista es LIMITED.

## 8. Lo que v0.9 puede desbloquear

Permitido:

```txt
CAMPAIGN-002 uses a source-backed limited baseline.
The baseline formula has direct support for limited comparison.
The candidate remains hypothetical.
Physical prediction remains blocked.
```

No permitido:

```txt
Phygn predicts decoherence.
Frontera C is validated.
Boundary C causes decoherence.
Baseline source validates candidate.
```

## 9. Retroalimentación epistémica

v0.9 debe leer:

```txt
reports/rag/baseline_source_requirements.md
reports/rag/baseline_literature_ingestion.md
reports/model_comparison/visibility_decay_baseline_readiness.md
reports/campaigns/CAMPAIGN-002_baseline_physicalization.md
```

y actualizar:

```txt
source registry
claim-source matrix
baseline readiness
campaign result
backlog
```

## 10. Criterio de éxito mínimo

v0.9 está completa si:

```txt
source ingestion pipeline exists;
source candidates can be registered;
citation audit exists;
baseline upgrade attempt runs;
baseline remains blocked if sources are insufficient;
baseline upgrades to LIMITED only if direct source support exists;
candidate claims remain blocked;
reports generated;
tests pass.
```

## 11. Frase guía

```txt
La arquitectura ya sabe rechazar fuentes ausentes.
Ahora debe aceptar fuentes reales sin perder el freno.
```

## 12. Principio final

```txt
Una fuente no es una victoria.
Una fuente es una pieza admisible en el juicio.
```
