# Phygn v0.4 — Core Loop Execution Protocol for IDE AI

## 0. Uso

Este documento debe ser pegado o referenciado en la IA del IDE cuando se quiera que continúe el desarrollo del core de Phygn.

La IA debe trabajar en modo:

```txt
CORE DEVELOPMENT LOOP
```

No en modo:

```txt
frontend
estética
landing
copywriting
branding
```

## 1. Mandato principal

Continúa el desarrollo lógico del Lab ejecutando iteraciones completas.

Cada iteración debe:

```txt
leer estado
ejecutar tests
detectar gaps
seleccionar una tarea
desarrollarla
añadir tests
actualizar RAG/backlog/reports
volver a ejecutar tests
proponer siguiente iteración
```

## 2. Primera acción obligatoria

Ejecutar:

```bash
dir
dir phyng
dir tests
dir docs
dir rag
dir reports
dir backlog
pytest -v
```

Si carpetas `rag`, `reports` o `backlog` no existen, crearlas.

## 3. Prohibición de desarrollo ciego

No escribir código hasta saber:

```txt
qué test falla o falta
qué claim falta fuente
qué benchmark falta
qué gap se va a cerrar
qué criterio de aceptación se usará
```

## 4. Modo de selección de tarea

Elegir la tarea de mayor prioridad.

Prioridad:

```txt
P0:
tests fallidos
claim falso permitido
contradicción RAG
error dimensional
endpoint roto

P1:
claim central sin fuente
claim central sin benchmark
RAG incompleto
L no justificada
τ sin modelo alternativo

P2:
nuevo benchmark
nuevo caso de estudio
nuevo modelo base
nuevo reporte científico

P3:
API auxiliar
exportadores
mejoras de reporting

P4:
frontend
UX
visualización
```

## 5. Formato de inicio de iteración

Antes de modificar código, escribir en `reports/iteration_log.md`:

```md
## ITERATION YYYY-MM-DD-HHMM

### Selected Gap
...

### Priority
...

### Mode
...

### Expected Output
...

### Acceptance Criteria
- ...
```

## 6. Modos de desarrollo

### 6.1 Test Repair Mode

Usar cuando `pytest` falla.

Acciones:

```txt
identificar test
identificar módulo
corregir código mínimo
no modificar test salvo que el test esté objetivamente mal
volver a ejecutar pytest
registrar fix
```

### 6.2 Missing Test Mode

Usar cuando existe función sin test.

Acciones:

```txt
crear test
hacerlo fallar si procede
implementar/fijar código
hacerlo pasar
```

### 6.3 RAG Source Mode

Usar cuando claim necesita fuente.

Acciones:

```txt
crear ResearchTask
si hay fuente disponible, crear SourceRecord
si no, dejar AWAITING_SOURCE_INGESTION
marcar claim REQUIRES_SOURCE
```

### 6.4 Claim-Link Mode

Usar cuando fuente existe pero no está vinculada.

Acciones:

```txt
crear ClaimSourceLink
evaluar support_level
actualizar ClaimRecord
actualizar claim_source_matrix
```

### 6.5 Benchmark Mode

Usar cuando hay claim/caso sin benchmark.

Acciones:

```txt
definir case_id
formalizar inputs
crear benchmark function
crear tests
crear report
bloquear claims no soportados
```

### 6.6 Model Baseline Mode

Usar cuando Predictive Gain no tiene modelo base.

Acciones:

```txt
definir M_base
definir M_candidate
definir error metric
crear test de gain
crear report
```

### 6.7 Gatekeeper Hardening Mode

Usar cuando un overclaim no está bloqueado.

Acciones:

```txt
añadir patrón/regla
añadir test de bloqueo
añadir safe rewrite
actualizar docs si necesario
```

### 6.8 Report Mode

Usar cuando hay resultados sin reporte.

Acciones:

```txt
generar Markdown determinista
incluir inputs
outputs
claims
sources
tests
limitations
```

## 7. RAG anti-alucinación

La IA no debe inventar fuentes.

Estados válidos:

```txt
NO_SOURCE
REQUIRES_SOURCE
AWAITING_SOURCE_INGESTION
SOURCE_INGESTED
CLAIM_LINKED
CLAIM_AUDITED
```

Si no puede navegar:

```txt
crear ResearchTask
no fingir que investigó
```

Si puede navegar:

```txt
guardar SourceRecord
guardar nota/chunk
vincular claim
registrar soporte/contradicción
```

## 8. Estructura mínima de RAG

Asegurar:

```txt
rag/source_manifest.json
rag/claims/claim_registry.json
rag/claims/claim_source_links.json
rag/research_tasks/research_backlog.json
rag/citations/citation_audit.json
```

## 9. Estructura mínima de backlog

Asegurar:

```txt
backlog/phygn_core_backlog.json
backlog/phygn_core_backlog.md
```

## 10. Reports mínimos

Asegurar:

```txt
reports/iteration_log.md
reports/rag_status.md
reports/claim_source_matrix.md
reports/research_backlog.md
reports/core_backlog.md
reports/benchmark_status.md
```

## 11. Tests obligatorios del loop

Si no existen, crear progresivamente:

```txt
tests/test_loop_gap_detection.py
tests/test_loop_iteration.py
tests/test_core_backlog.py
tests/test_rag_source_registry.py
tests/test_rag_claim_registry.py
tests/test_rag_claim_linker.py
tests/test_rag_research_planner.py
tests/test_rag_reports.py
```

## 12. Módulos esperados

Asegurar progresivamente:

```txt
phyng/loop/schemas.py
phyng/loop/state_scan.py
phyng/loop/gap_detection.py
phyng/loop/iteration.py
phyng/loop/backlog.py
phyng/loop/reporting.py

phyng/rag/schemas.py
phyng/rag/source_registry.py
phyng/rag/claim_registry.py
phyng/rag/claim_linker.py
phyng/rag/citation_audit.py
phyng/rag/research_planner.py
phyng/rag/retrieval.py
phyng/rag/rag_report.py
```

## 13. Función principal

Debe existir o implementarse:

```python
def run_iteration_once(project_root: Path) -> IterationRecord:
    ...
```

Debe:

```txt
scan state
run/detect test status where possible
detect gaps
rank gaps
select task
create/update backlog
create research tasks if needed
generate reports
return summary
```

No debe fingir haber resuelto lo que solo ha registrado.

## 14. Endpoints opcionales

Solo si la API está estable:

```txt
GET /loop/status
POST /loop/iterate-once
GET /rag/sources
POST /rag/sources
GET /rag/claims
POST /rag/claims
POST /rag/claims/link
POST /rag/audit-claim
GET /rag/report
GET /backlog
POST /backlog
```

## 15. Final de iteración

Al final, escribir:

```md
### Iteration Result
...

### Tests
...

### Files Changed
...

### Claims Affected
...

### RAG Updates
...

### Backlog Updates
...

### Next Best Task
...
```

## 16. Criterios de aceptación

La IA puede considerar completada una iteración si:

```txt
tests pasan o el fallo queda registrado como P0
se cerró al menos un gap o se creó una research task necesaria
reports actualizados
backlog actualizado
no hay claims nuevos sin clasificar
siguiente tarea propuesta
```

## 17. Frase de control

Si no sabes qué hacer, no inventes.

Ejecuta:

```txt
gap detection
```

y deja que el backlog decida.

## 18. Mantra

```txt
No source, no hard claim.
No test, no feature.
No scale, no prediction.
No trace, no detectability.
No benchmark, no gain.
No report, no iteration.
```
