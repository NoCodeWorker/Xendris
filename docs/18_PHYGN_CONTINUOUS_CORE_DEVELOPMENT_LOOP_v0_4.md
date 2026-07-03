# Phygn v0.4 — Continuous Core Development Loop

## 0. Propósito

Este documento redefine el loop de Phygn como una **máquina de continuación del desarrollo del core científico**.

La finalidad del loop no es observar pasivamente el estado del proyecto.  
La finalidad del loop es **continuar desarrollando Phygn de forma rigurosa, iterativa y blindada contra alucinaciones**.

Phygn debe funcionar así:

```txt
estado actual
→ detección de huecos
→ selección de siguiente tarea
→ investigación si falta fuente
→ alimentación RAG
→ formalización
→ implementación
→ tests
→ auditoría
→ reporte
→ actualización del backlog
→ siguiente iteración
```

## 1. Principio rector

```txt
El loop existe para continuar el desarrollo.
Pero solo puede continuar desarrollando si cada avance queda trazado por cálculo, fuente, test, benchmark o bloqueo explícito.
```

No se permite:

```txt
seguir desarrollando por intuición
añadir teoría sin test
añadir claim sin fuente
añadir código sin aceptación
añadir RAG sin link a claims
añadir caso de estudio sin benchmark
```

## 2. Diferencia entre "continuar" y "alucinar"

### Continuar desarrollo válido

```txt
Detectar un gap real
Crear una tarea
Buscar soporte
Registrar fuente
Vincular claim
Implementar módulo
Añadir test
Generar reporte
Actualizar backlog
Elegir siguiente gap
```

### Continuar desarrollo inválido

```txt
Inventar nuevas leyes
Crear fórmulas no justificadas
Añadir módulos sin tests
Simular deep research
Afirmar citas no ingeridas
Mejorar estética mientras hay P0/P1 del core
```

## 3. Entradas del loop

El loop debe leer:

```txt
/phyng
/tests
/docs
/rag
/reports
/backlog
pyproject.toml
README.md
```

Y debe conocer el estado de:

```txt
tests
API
RAG
claims
sources
benchmarks
case studies
agents
workflows
backlog
```

## 4. Salidas obligatorias del loop

Cada iteración debe producir al menos una salida útil:

```txt
nuevo test
nuevo benchmark
nuevo caso de estudio
nuevo source record
nuevo claim-source link
nuevo bloqueo de claim
nuevo safe rewrite
nueva tarea de backlog
nuevo reporte
nuevo refactor del core
nueva mejora API
nueva formalización
```

Si la iteración no produce ninguna de estas salidas, debe marcarse como:

```txt
ITERATION_NO_CORE_PROGRESS
```

## 5. Estados de iteración

```txt
PLANNED
RUNNING
BLOCKED_BY_TESTS
BLOCKED_BY_SOURCE
BLOCKED_BY_MODEL
BLOCKED_BY_SCALE
BLOCKED_BY_TRACE
COMPLETED_WITH_CODE
COMPLETED_WITH_RESEARCH_TASK
COMPLETED_WITH_REPORT_ONLY
FAILED_NO_PROGRESS
```

## 6. Prioridad del loop

Orden de prioridad:

```txt
P0 — tests rotos, errores físicos, claims peligrosos, corrupción de RAG
P1 — claims centrales sin fuente, RAG incompleto, benchmark ausente
P2 — nuevos casos de estudio, nuevas cotas, nuevos modelos base
P3 — API/reportes/exportadores
P4 — frontend, visualizaciones, UX
```

Mientras existan P0/P1, el loop no debe trabajar estética.

## 7. Loop maestro

```txt
STEP 0 — Load State
STEP 1 — Run Tests
STEP 2 — Detect Core Gaps
STEP 3 — Rank Gaps
STEP 4 — Select Next Development Target
STEP 5 — Decide Mode
STEP 6A — Research Mode
STEP 6B — Implementation Mode
STEP 6C — Benchmark Mode
STEP 6D — Refactor Mode
STEP 7 — Run Agent Audit
STEP 8 — Run Claim Gatekeeper
STEP 9 — Run Tests Again
STEP 10 — Generate Reports
STEP 11 — Update Backlog
STEP 12 — Select Next Iteration
```

## 8. STEP 0 — Load State

Debe cargar:

```txt
source_manifest
claim_registry
claim_source_links
research_backlog
core_backlog
test status
reports
```

Si un archivo no existe, debe crearlo con estructura mínima válida.

## 9. STEP 1 — Run Tests

Comando:

```bash
pytest -v
```

Regla:

```txt
Si los tests fallan, la siguiente tarea P0 es reparar tests o código.
```

No se permite añadir features con tests rotos salvo que el feature sea la corrección.

## 10. STEP 2 — Detect Core Gaps

Tipos de gap:

```txt
MISSING_TEST
MISSING_SOURCE
MISSING_CLAIM_LINK
MISSING_BENCHMARK
MISSING_MODEL_BASELINE
MISSING_SCALE_JUSTIFICATION
MISSING_TRACE
MISSING_SAFE_REWRITE
CLAIM_OVERREACH
RAG_CONTRADICTION
API_SCHEMA_GAP
REPORT_GAP
```

## 11. STEP 3 — Rank Gaps

Ranking:

```txt
CRITICAL:
claim falso permitido
source contradice claim permitido
tests rotos en core físico
dimensional inconsistency

HIGH:
claim fuerte sin fuente
benchmark ausente para claim central
L arbitraria usada en claim
τ sin modelo alternativo

MEDIUM:
endpoint sin test
reporte incompleto
source sin claim link
claim sin safe rewrite

LOW:
limpieza
naming
docs menores
```

## 12. STEP 4 — Select Next Development Target

El loop debe elegir una única tarea por iteración.

Debe registrar:

```json
{
  "selected_gap": "GAP-XXXX",
  "reason": "...",
  "expected_output": "...",
  "acceptance_criteria": ["..."]
}
```

## 13. STEP 5 — Decide Mode

Modo según gap:

```txt
MISSING_SOURCE → Research Mode
MISSING_CLAIM_LINK → RAG Link Mode
MISSING_TEST → Test Implementation Mode
MISSING_BENCHMARK → Benchmark Mode
CLAIM_OVERREACH → Gatekeeper Mode
MISSING_MODEL_BASELINE → Model Formalization Mode
API_SCHEMA_GAP → API Implementation Mode
REPORT_GAP → Reporting Mode
```

## 14. STEP 6A — Research Mode

No simular browsing.

El código local debe:

```txt
crear ResearchTask
marcar AWAITING_SOURCE_INGESTION
preparar plantilla de fuente
bloquear claim hasta ingesta
```

Si la IA del IDE sí tiene navegación, debe:

```txt
buscar fuente primaria/secundaria fiable
guardar SourceRecord
añadir nota o chunk
vincular con ClaimRecord
actualizar citation audit
```

## 15. STEP 6B — Implementation Mode

Reglas:

```txt
implementar mínimo código necesario
añadir type hints
añadir docstrings
usar Pydantic si hay schema
no duplicar lógica
no hardcodear outputs científicos
```

## 16. STEP 6C — Benchmark Mode

Todo benchmark debe tener:

```txt
case_id
inputs
assumptions
expected outputs
allowed claims
blocked claims
tests
report
```

## 17. STEP 6D — Refactor Mode

Solo permitido si:

```txt
reduce duplicación
mejora validación
mejora testabilidad
elimina riesgo de error físico
```

No refactorizar por gusto.

## 18. STEP 7 — Agent Audit

Toda iteración debe pasar por:

```txt
Mathematical Consistency Auditor
Claim Gatekeeper Agent
Red Team Physicist
Scientific Software Architect
```

Y según dominio:

```txt
Relativity Auditor
Quantum Foundations Auditor
Gravitation & Horizons Auditor
Statistical Distinguishability Auditor
Operational Scale Auditor
Literature & Citation Auditor
```

## 19. STEP 8 — Claim Gatekeeper

Todo claim nuevo o modificado debe clasificarse:

```txt
ALLOWED
ALLOWED_LIMITED
REQUIRES_SOURCE
REQUIRES_MODEL
REQUIRES_TRACE
REQUIRES_SCALE_JUSTIFICATION
BLOCKED
```

## 20. STEP 9 — Run Tests Again

Al final:

```bash
pytest -v
```

Si falla:

```txt
ITERATION_FAILED_TESTS
```

Y se crea P0.

## 21. STEP 10 — Reports

Actualizar:

```txt
reports/iteration_log.md
reports/rag_status.md
reports/claim_source_matrix.md
reports/research_backlog.md
reports/core_backlog.md
reports/benchmark_status.md
```

## 22. STEP 11 — Backlog Update

Cada gap cerrado debe pasar a:

```txt
DONE
```

Cada bloqueo debe crear nueva tarea:

```txt
BLOCKED
```

Cada source pendiente debe crear:

```txt
RESEARCH_TASK
```

## 23. STEP 12 — Next Iteration

El loop debe terminar cada iteración diciendo:

```txt
NEXT_BEST_TASK: ...
WHY: ...
MODE: ...
EXPECTED_OUTPUT: ...
```

## 24. Condición de continuación

Si existe cualquier P0/P1:

```txt
CONTINUE_CORE_LOOP = true
```

Si no hay P0/P1 pero sí P2:

```txt
CONTINUE_CORE_LOOP = true
```

Solo puede parar si:

```txt
tests pasan
no hay P0
no hay P1
reportes actualizados
siguiente tarea recomendada
```

## 25. Regla de oro

```txt
El loop no es documentación.
El loop es el sistema nervioso del desarrollo científico de Phygn.
```
