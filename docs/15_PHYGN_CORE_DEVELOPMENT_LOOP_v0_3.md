# Phygn v0.3 — Core Development Super Loop

## 0. Propósito

Este documento define el **super loop de desarrollo lógico** de Phygn.

El objetivo no es mejorar estética, UI ni branding.  
El objetivo es que la IA del IDE continúe desarrollando el **core científico-computacional** del Lab de forma iterativa, auditable, anti-alucinación y orientada a pruebas.

Phygn debe evolucionar como un sistema de investigación computacional:

```txt
hipótesis
→ formalización
→ implementación
→ test
→ auditoría
→ deep research
→ RAG
→ benchmark
→ refactor
→ reporte
→ nueva iteración
```

## 1. Principio rector

```txt
No avanzar por intuición.
Avanzar por cálculo, tests, citas, trazas y benchmarks.
```

## 2. Objetivo del loop

El loop debe permitir que la IA del IDE trabaje continuamente sobre Phygn sin perder rigor.

Cada iteración debe producir al menos una de estas salidas:

```txt
nuevo test
nuevo benchmark
nuevo caso de estudio
nuevo bloqueo de claim
nueva mejora del RAG
nueva cita verificada
nuevo reporte científico
nuevo refactor del core
nueva validación contra literatura
nueva cota negativa
nuevo cálculo reproducible
```

Si una iteración no produce nada de eso, debe considerarse fallida.

## 3. No objetivos

El loop no debe dedicarse a:

```txt
mejorar colores
pulir cards
añadir animaciones
crear landing
añadir marketing
generar hype
expandir teoría sin cálculo
añadir analogías cognitivas
crear claims de nueva física sin traza
```

## 4. Ciclo maestro

Cada iteración debe seguir esta estructura:

```txt
LOOP-0 — State Scan
LOOP-1 — Scientific Gap Detection
LOOP-2 — Research Plan
LOOP-3 — Deep Research
LOOP-4 — Source Ingestion into RAG
LOOP-5 — Formalization
LOOP-6 — Implementation
LOOP-7 — Tests & Benchmarks
LOOP-8 — Agent Audit
LOOP-9 — Claim Gatekeeping
LOOP-10 — Report Generation
LOOP-11 — Backlog Update
LOOP-12 — Next Iteration Selection
```

## 5. LOOP-0 — State Scan

Antes de modificar código, la IA debe inspeccionar el estado real.

Comandos:

```bash
dir
dir docs
dir phyng
dir tests
pytest -v
```

Si existe frontend, ignorarlo salvo que afecte al core.

Debe producir un resumen:

```txt
tests passing/failing
modules present
missing modules
docs present
API status
RAG status
benchmarks present
known failures
```

## 6. LOOP-1 — Scientific Gap Detection

La IA debe detectar huecos científicos, no cosméticos.

Preguntas:

```txt
¿Hay claims sin tests?
¿Hay fórmulas sin validación dimensional?
¿Hay endpoints sin tests?
¿Hay casos de estudio sin benchmark?
¿Hay literatura citada pero no ingerida en RAG?
¿Hay claims que necesitan fuente?
¿Hay una escala L sin justificación?
¿Hay τO(H) sin P(Y|¬H)?
¿Hay Predictive Gain sin modelo base?
¿Hay un resultado que podría ser solo STRUCTURAL_TRACE?
```

Salida:

```json
{
  "gaps": [
    {
      "id": "GAP-001",
      "type": "MISSING_TEST|MISSING_SOURCE|MISSING_BENCHMARK|MISSING_MODEL|CLAIM_RISK|RAG_GAP",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "description": "...",
      "recommended_action": "..."
    }
  ]
}
```

## 7. LOOP-2 — Research Plan

Si el gap requiere conocimiento externo, la IA debe crear un plan de investigación antes de escribir código.

Ejemplo:

```txt
Gap:
La sección sobre longitud de Compton necesita fuente primaria/secundaria confiable.

Plan:
1. buscar fuente estándar sobre reduced Compton wavelength;
2. buscar referencia sobre Schwarzschild radius;
3. buscar literatura sobre Compton-Schwarzschild correspondence;
4. guardar citas;
5. añadir entradas RAG;
6. actualizar claims.
```

No hacer deep research aleatorio.

Cada investigación debe estar asociada a un gap.

## 8. LOOP-3 — Deep Research

La IA debe realizar investigación externa solo cuando sea necesario.

Reglas:

```txt
Usar fuentes primarias o académicas siempre que sea posible.
Preferir papers, libros, documentación universitaria o revisiones técnicas.
No usar blogs como autoridad primaria si hay fuentes mejores.
No citar Wikipedia como fuente principal para claims duros.
No aceptar un resultado sin fuente.
No copiar texto largo.
Registrar cada fuente con metadatos.
```

Campos mínimos:

```json
{
  "source_id": "SRC-0001",
  "title": "...",
  "authors": ["..."],
  "year": "...",
  "url": "...",
  "source_type": "PAPER|BOOK|LECTURE_NOTES|OFFICIAL_DOC|ENCYCLOPEDIC|OTHER",
  "relevance": "HIGH|MEDIUM|LOW",
  "used_for": ["..."],
  "claims_supported": ["..."],
  "claims_not_supported": ["..."],
  "notes": "..."
}
```

## 9. LOOP-4 — Source Ingestion into RAG

Toda fuente útil debe entrar en el RAG local.

RAG no debe ser un cajón de PDFs.  
Debe ser una memoria científica trazable.

Estructura recomendada:

```txt
rag/
  sources/
    source_manifest.json
    papers/
    notes/
  chunks/
  embeddings/
  indexes/
  claims/
  citations/
```

Módulos sugeridos:

```txt
phyng/rag/
  __init__.py
  source_registry.py
  ingestion.py
  chunking.py
  embeddings.py
  retrieval.py
  claim_linker.py
  citation_audit.py
```

Para v0.3, si no hay embeddings reales todavía, implementar al menos:

```txt
source registry
claim-source linking
markdown notes
citation audit
```

## 10. LOOP-5 — Formalization

Antes de implementar, convertir el hallazgo en forma Phygn.

Cada nuevo concepto debe clasificarse:

```txt
DEFINITION
AXIOM
STRUCTURAL_LEMMA
HYPOTHESIS
MODEL
BENCHMARK
NEGATIVE_BOUND
SPECULATIVE_EXTENSION
```

Debe asignar:

```txt
layer
trace_type
claim_status
required_sources
required_tests
```

Ejemplo:

```json
{
  "id": "LEM-002",
  "name": "QB scale constraint",
  "type": "STRUCTURAL_LEMMA",
  "layer": "PHYSICAL_CORE",
  "trace_type": "STRUCTURAL_TRACE",
  "requires_empirical_trace": false,
  "required_tests": ["test_QB_constraint"],
  "forbidden_claims": ["proves new physics"]
}
```

## 11. LOOP-6 — Implementation

Implementar solo después de formalizar.

Prioridades:

```txt
core Python > tests > API > reports > RAG > frontend
```

No añadir dependencias sin necesidad.

Cada módulo nuevo debe tener:

```txt
type hints
docstrings
Pydantic si hay modelos
errores claros
tests
```

## 12. LOOP-7 — Tests & Benchmarks

Cada iteración debe ejecutar:

```bash
pytest -v
```

Si se añade funcionalidad, añadir tests.

Tipos de tests obligatorios según cambio:

```txt
new formula → dimensional + numerical tests
new claim rule → gatekeeper tests
new RAG source → source registry tests
new retrieval → retrieval determinism tests
new case study → benchmark tests
new API endpoint → API test
new report → snapshot or content tests
```

## 13. LOOP-8 — Agent Audit

Todo resultado debe pasar por agentes funcionales.

Mínimo:

```txt
Mathematical Consistency Auditor
Claim Gatekeeper Agent
Red Team Physicist
```

Según caso:

```txt
Relativity Auditor
Quantum Foundations Auditor
Gravitation & Horizons Auditor
Statistical Distinguishability Auditor
Operational Scale Auditor
Literature & Citation Auditor
Scientific Software Architect
```

## 14. LOOP-9 — Claim Gatekeeping

Cada claim generado debe clasificarse.

Formato:

```json
{
  "claim": "...",
  "claim_type": "...",
  "layer": "...",
  "trace_type": "...",
  "source_refs": ["..."],
  "allowed": true,
  "safe_rewrite": "...",
  "blocked_reason": null
}
```

Regla:

```txt
Si un claim no puede clasificarse, no puede entrar al paper ni al README.
```

## 15. LOOP-10 — Report Generation

Cada iteración debe generar o actualizar:

```txt
reports/iteration_log.md
reports/benchmark_status.md
reports/rag_status.md
reports/claim_audit.md
```

Cada reporte debe responder:

```txt
qué cambió
por qué cambió
qué tests lo protegen
qué fuentes lo soportan
qué claims permite
qué claims bloquea
qué queda pendiente
```

## 16. LOOP-11 — Backlog Update

Mantener backlog vivo:

```txt
backlog/phygn_core_backlog.md
```

Cada tarea:

```json
{
  "id": "TASK-0001",
  "title": "...",
  "type": "CORE|RAG|BENCHMARK|CASE_STUDY|PAPER|API|TEST",
  "priority": "P0|P1|P2|P3",
  "status": "TODO|IN_PROGRESS|BLOCKED|DONE",
  "blocked_by": ["..."],
  "acceptance_criteria": ["..."]
}
```

## 17. LOOP-12 — Next Iteration Selection

Elegir siguiente tarea según prioridad:

```txt
P0: tests rotos, claims peligrosos, errores físicos.
P1: RAG/citas faltantes para claims centrales.
P2: nuevos benchmarks/casos de estudio.
P3: mejoras API/reportes.
```

No elegir tareas estéticas mientras existan P0/P1 del core.

## 18. Condición de parada

La IA puede detenerse solo si:

```txt
tests pasan
no hay P0
no hay claims críticos sin bloquear
reportes actualizados
siguiente tarea identificada
```

Si no, debe continuar.

## 19. Mantra operativo

```txt
No expandas teoría.
No maquilles resultados.
No cites sin ingerir.
No implementes sin test.
No aceptes claims sin traza.
No uses RAG sin fuente.
No permitas L arbitraria.
No confundas lema con predicción.
```

## 20. Objetivo final

Phygn debe convertirse en un laboratorio que funcione así:

```txt
claim entra
→ agentes lo auditan
→ RAG busca soporte
→ fórmula se valida
→ benchmark se ejecuta
→ claim se permite, limita o bloquea
→ reporte queda trazado
```
