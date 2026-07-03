# Phygn v0.4 — RAG Research Feedback Loop

## 0. Propósito

Este documento define cómo el RAG retroalimenta el desarrollo de Phygn.

El RAG no debe ser una biblioteca pasiva.  
Debe ser una infraestructura activa de evidencia.

Su función:

```txt
detectar claims sin fuente
crear tareas de investigación
ingerir fuentes
vincular claims
auditar soporte/contradicción
actualizar gatekeeper
generar nuevas tareas de desarrollo
```

## 1. Ciclo RAG

```txt
Claim detectado
→ ClaimRecord
→ Citation Audit
→ Source Search Needed?
→ ResearchTask
→ SourceRecord
→ Chunk/Note
→ ClaimSourceLink
→ Claim Status Update
→ Backlog Update
→ Test/Benchmark Needed?
```

## 2. Estados de claim

```txt
DRAFT
REQUIRES_SOURCE
REQUIRES_HIGHER_TRUST_SOURCE
REQUIRES_MODEL
REQUIRES_TRACE
REQUIRES_SCALE_JUSTIFICATION
ALLOWED_LIMITED
ALLOWED
BLOCKED
CONTRADICTED
```

## 3. Estados de investigación

```txt
NO_TASK
RESEARCH_TASK_CREATED
AWAITING_SOURCE_INGESTION
SOURCE_INGESTED
CHUNKED
CLAIM_LINKED
CLAIM_AUDITED
BACKLOG_UPDATED
```

## 4. Fuentes

### Trust level

```txt
PRIMARY:
paper fundacional, libro técnico, documentación académica primaria.

HIGH:
review académico, lecture notes universitarias, documentación técnica fiable.

MEDIUM:
artículo enciclopédico, blog técnico muy citado, documentación secundaria.

LOW:
blog casual, foro, resumen no verificado.
```

## 5. Reglas de soporte

```txt
DIRECT_SUPPORT:
la fuente sostiene directamente el claim.

INDIRECT_SUPPORT:
la fuente sostiene una parte o antecedente.

BACKGROUND:
sirve de contexto, no valida.

CONTRADICTS:
contradice el claim.

INSUFFICIENT:
no basta.
```

## 6. Hard claim

Un claim es duro si afirma:

```txt
new physics
demonstrates
proves
predicts
validates
empirical evidence
experimental detection
```

En español:

```txt
demuestra
prueba
valida
predice
evidencia
descubre
nueva física
```

Regla:

```txt
Hard claim + no PRIMARY/HIGH source + no test/benchmark → BLOCKED or REQUIRES_HIGHER_TRUST_SOURCE
```

## 7. RAG como generador de desarrollo

Cuando RAG detecta:

```txt
claim sin fuente
```

crea:

```txt
ResearchTask
```

Cuando detecta:

```txt
claim con fuente pero sin test
```

crea:

```txt
BacklogTask type=TEST
```

Cuando detecta:

```txt
claim con fuente y test pero sin benchmark
```

crea:

```txt
BacklogTask type=BENCHMARK
```

Cuando detecta:

```txt
source contradice claim permitido
```

crea:

```txt
P0 BLOCKING TASK
```

## 8. Matriz claim-source-test

Todo claim importante debe aparecer en:

```txt
reports/claim_source_matrix.md
```

Columnas:

```txt
claim_id
claim_text
status
layer
trace_type
sources
support_level
tests
benchmarks
safe_rewrite
blocked_reason
```

## 9. Auditoría de citas

Cada SourceRecord debe responder:

```txt
¿qué claims soporta?
¿qué claims contradice?
¿qué claims solo contextualiza?
¿qué tests o benchmarks exige?
```

## 10. Búsqueda local MVP

Si no hay vector DB, usar lexical retrieval:

```txt
lowercase
tokenize
score by keyword overlap
boost by topic match
boost by trust level
return support + contradiction candidates
```

Nunca devolver solo soporte favorable.

## 11. Auto Deep Research asistido

En entorno local sin navegación:

```txt
crear ResearchTask
generar query sugerida
indicar source types necesarios
dejar claim bloqueado hasta ingesta
```

En entorno con navegación:

```txt
buscar
registrar fuente
guardar notas/chunks
vincular claim
recalcular status
```

## 12. ResearchTask schema

```json
{
  "task_id": "RT-0001",
  "question": "What is the standard interpretation of the reduced Compton wavelength as localization boundary?",
  "reason": "Claim requires support.",
  "linked_claim_id": "CLAIM-0001",
  "priority": "P1",
  "required_source_types": ["PAPER", "BOOK", "LECTURE_NOTES"],
  "suggested_queries": [
    "reduced Compton wavelength localization quantum field theory",
    "Compton wavelength localization limit relativistic quantum mechanics"
  ],
  "status": "AWAITING_SOURCE_INGESTION"
}
```

## 13. Source ingestion minimum

Si una fuente se ingiere manualmente:

```txt
title
authors
year
url or local_path
source_type
trust_level
topics
used_for
notes
```

No inventar datos faltantes. Usar null.

## 14. Test hooks

Cada transición debe tener test.

Ejemplos:

```txt
claim without source → REQUIRES_SOURCE
hard claim with LOW source → REQUIRES_HIGHER_TRUST_SOURCE
CONTRADICTS link → BLOCKED
DIRECT_SUPPORT with HIGH source → ALLOWED_LIMITED or ALLOWED
BACKGROUND only → still REQUIRES_DIRECT_SUPPORT
```

## 15. Endpoint futuro

```txt
POST /rag/audit-claim
```

Request:

```json
{
  "claim_id": "CLAIM-0001"
}
```

Response:

```json
{
  "claim_id": "CLAIM-0001",
  "status": "REQUIRES_SOURCE",
  "reason": "No source linked.",
  "research_task_created": "RT-0001"
}
```

## 16. Integración con Claim Gatekeeper

El gatekeeper debe consultar RAG:

```txt
if claim.status == REQUIRES_SOURCE:
    block hard claim

if claim.status == CONTRADICTED:
    block

if claim has DIRECT_SUPPORT + tests:
    allow limited
```

## 17. Integración con agentes

Agentes que usan RAG:

```txt
Literature & Citation Auditor
Paper Reviewer Agent
Red Team Physicist
Claim Gatekeeper Agent
Scientific Software Architect
```

## 18. Objetivo v0.4

Al final de v0.4, Phygn debe poder decir:

```txt
Este claim está soportado por estas fuentes.
Este claim solo tiene soporte contextual.
Este claim está contradicho.
Este claim necesita investigación.
Este claim necesita test.
Este claim necesita benchmark.
```

## 19. Regla final

```txt
RAG no es memoria.
RAG es trazabilidad epistémica.
```
