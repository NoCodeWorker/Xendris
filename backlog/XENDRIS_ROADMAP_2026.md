# Xendris Roadmap 2026 — De v0.2.x a Producto

**Baseline:** v0.2.0 (xendris), v0.3.0 (phyng), frontend reset limpio  
**Goal:** Trust-routed AI runtime and agent platform  
**Métrica central:** `cost_per_admissible_answer`

---

## Mapa de hitos y dependencias

```txt
Hito A (v0.2.x Release)
  ├── Hito B (API Boundary Audit)
  │     ├── Hito C (Real Provider Evidence)
  │     └── Hito G (Epistemic Frame Layer)
  ├── Hito D (Runtime API MVP) ────────────────────────┐
  │     ├── Hito E (Wallet & Usage Core) ──────────────┤
  │     └── Hito F (Adaptive Council & Sycophancy) ────┤
  └────────────────────────────────────────────────────┼── Hito H (Xendris Agent UI)
                                                       └── Hito I (Trust Dashboard)
```

---

## Hito A — v0.2.x Clean Public Framework Release

**Objetivo:** Release público limpio, sin contaminación de evidencia histórica.

### Estado actual
- v0.2.0 tag existe, release gate v0.2.1/v0.2.2 implementados
- `phyng/api.py` tiene whitespace caveat
- Artefactos históricos bloquean release clean
- Working tree con issues de limpieza

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| A-01 | Implementar Historical Artifact Quarantine Policy | P0 | — |
| A-02 | Crear manifest de artefactos rechazados | P0 | A-01 |
| A-03 | Ejecutar suite audit distinguiendo historical rejected vs active blocker | P0 | A-02 |
| A-04 | Crear release_gate_v0_2_2 | P0 | A-03 |
| A-05 | Fix whitespace warning en `phyng/api.py` | P0 | — |
| A-06 | Limpiar working tree (generated outputs, artefactos en cuarentena) | P0 | A-01 |
| A-07 | Tag release v0.2.2 | P0 | A-04, A-05, A-06 |
| A-08 | Verificar exit criteria | P0 | A-07 |

### Exit criteria
```
release gate: PASS or WARNINGS_PRESENT without blockers
unsafe rejected citations: 0
active benchmark blockers: 0
```

### Tests requeridos
- `test_rejected_artifact_cannot_be_cited_as_evidence`
- `test_quarantined_artifact_is_historical_only`
- `test_public_report_requires_admitted_artifact`
- `test_release_gate_blocks_unsafe_evidence_reference`
- `test_release_gate_reports_historical_rejected_non_blocking`

---

## Hito B — API Boundary Audit

**Objetivo:** Decidir qué módulos son públicos, experimentales o privados.

### Estado actual
- Público estable: `xendris.frontera_c`, `xendris.core.rag`, `xendris.core.response_contract`
- Experimental: `xendris.core.trust`, `xendris.core.runtime`, `xendris.core.algebra`, `xendris.core.boundary`, `xendris.core.local`, `xendris.core.sectors`, `xendris.core.router`, `xendris.core.fingerprints`, `xendris.core.ledger`, `xendris.core.representations`
- Vacíos: `xendris.models`, `xendris.benchmarks`, `xendris.prompts`, `xendris.outputs`, `xendris.scripts`

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| B-01 | Auditar `xendris.benchmarking` | P1 | A-07 |
| B-02 | Auditar `xendris.core.trust` | P1 | A-07 |
| B-03 | Clasificar runtime/router/fingerprint/ledger como public/experimental/private | P1 | B-01, B-02 |
| B-04 | Definir deprecation policy | P1 | B-03 |
| B-05 | Escribir public import tests | P1 | B-03 |
| B-06 | Publicar API surface spec | P1 | B-05 |
| B-07 | Deprecar o poblar namespaces vacíos | P2 | B-03 |

### Exit criteria
```
Cada módulo tiene clasificación explícita
Public import tests pasan para módulos estables
Deprecation policy documentada
```

---

## Hito C — Real Provider Evidence Import

**Objetivo:** Ejecutar benchmarks reales fuera de Codex y admitir solo artefactos evidenciados.

### Estado actual
- Trust Traps v0.1 y Programming Reliability v0.1 existen como dry-run
- Resultados dry-run: DeepSeek vs Xendris
- No hay ejecución real contra proveedores

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| C-01 | Implementar ejecución real de Trust Traps contra proveedores (OpenAI, Anthropic, DeepSeek) | P1 | A-07 |
| C-02 | Implementar ejecución real de Programming Reliability contra proveedores | P1 | A-07 |
| C-03 | Implementar provider disclosure gate | P1 | C-01 |
| C-04 | Implementar cost disclosure gate | P1 | C-01 |
| C-05 | Implementar latency disclosure gate | P1 | C-01 |
| C-06 | Implementar dry-run vs real-provider comparison | P1 | C-01, C-02 |
| C-07 | Ejecutar evidence registry admission | P1 | C-03, C-04, C-05 |
| C-08 | Publicar benchmark report conservador | P2 | C-07 |

### Exit criteria
```
Benchmarks ejecutados contra ≥2 proveedores reales
Provider disclosure presente en cada reporte
Cost/latency disclosure presente
Dry-run vs real delta documentado
Evidence registry clasifica artefactos como ADMITTED/REJECTED/QUARANTINED
```

---

## Hito D — Runtime API MVP

**Objetivo:** Exponer Xendris como Trust Runtime API HTTP.

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| D-01 | Crear FastAPI service para Xendris Runtime (o extender `phyng.api.py`) | P1 | B-03 |
| D-02 | Implementar API key authentication + middleware | P1 | D-01 |
| D-03 | Implementar `POST /v1/runtime/execute` | P1 | D-01 |
| D-04 | Implementar `POST /v1/claims/evaluate` | P1 | D-01 |
| D-05 | Implementar `GET /v1/ledger/{run_id}` | P1 | D-01 |
| D-06 | Implementar `GET /v1/health` | P1 | D-01 |
| D-07 | Implementar `POST /v1/routes/select` | P1 | D-01 |
| D-08 | Integrar provider adapter sandbox con Runtime API | P1 | D-03 |
| D-09 | Implementar deterministic test mode | P1 | D-01 |
| D-10 | Escribir integration tests para API | P1 | D-03—D-09 |

### Endpoints MVP
```
GET  /v1/health
POST /v1/runtime/execute
POST /v1/claims/evaluate
POST /v1/routes/select
GET  /v1/ledger/{run_id}
```

### Exit criteria
```
Endpoints MVP responden con autenticación
Runtime execute pasa por gates completos
Ledger retrieval funciona
Integration tests pasan
```

---

## Hito E — Wallet & Usage Core

**Objetivo:** Prepaid PAYG con hard caps y trazabilidad de coste.

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| E-01 | Implementar modelo tenant wallet (balance, currency, hard caps) | P1 | D-01 |
| E-02 | Implementar usage meter por tenant/project/API key | P1 | D-01 |
| E-03 | Implementar provider cost records | P1 | D-03 |
| E-04 | Implementar Xendris margin calculator | P1 | E-03 |
| E-05 | Implementar budget policy engine (daily/monthly/hard cap) | P1 | E-01 |
| E-06 | Implementar balance check gate (block when insufficient) | P1 | E-01 |
| E-07 | Implementar wallet top-up endpoint | P1 | E-01 |
| E-08 | Implementar wallet/billing API para dashboard | P1 | E-03, E-04 |
| E-09 | Implementar alerts (low balance, budget exceeded) | P2 | E-05 |
| E-10 | Escribir wallet/billing tests | P1 | E-01—E-09 |

### Exit criteria
```
Wallet funciona con balance prepago
Usage meter registra por request
Budget policy bloquea al exceder
Provider cost + Xendris margin trazables
```

---

## Hito F — Adaptive Council & Sycophancy Layer

**Objetivo:** No escalar tokens sin justificación epistémica.

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| F-01 | Implementar SycophancyGuard | P1 | D-01 |
| F-02 | Implementar AdaptiveCouncilPolicy | P1 | D-01 |
| F-03 | Implementar ContrarianGuard | P1 | F-02 |
| F-04 | Implementar FirstPrinciplesGuard | P1 | F-02 |
| F-05 | Implementar EvidenceGuard | P1 | F-02 |
| F-06 | Implementar marginal certainty gain metric | P1 | F-02 |
| F-07 | Implementar council escalation logging in ledger | P1 | F-02 |
| F-08 | Implementar token avoidance tracking | P1 | F-06 |
| F-09 | Escribir sycophancy tests | P1 | F-01—F-08 |
| F-10 | Escribir council tests | P1 | F-01—F-08 |

### Tests clave
```
test_user_hypothesis_not_promoted_without_evidence
test_model_agreement_without_evidence_is_limited
test_sycophantic_answer_requires_contraargument
test_low_risk_prompt_uses_local_guard_not_multi_model_council
test_medium_risk_can_use_second_model_when_needed
test_high_risk_requires_stronger_review
test_council_escalation_records_token_cost
test_adaptive_council_reduces_unnecessary_model_calls
```

### Regla de escalado
Escalar solo si:
- contradicción fuerte
- claim de alto riesgo
- evidencia insuficiente y alto impacto
- posible sycophancy de alto impacto
- acción irreversible
- conflicto entre modelos
- usuario lo solicita
- presupuesto lo permite

No escalar si:
- basta limitar el claim
- basta degradarlo a hipótesis
- hay regla local determinista aplicable
- riesgo bajo
- coste esperado > ganancia marginal de certeza

---

## Hito G — Epistemic Frame Layer

**Objetivo:** Implementar Frontera C Mayor a nivel de marcos representacionales.

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| G-01 | Implementar EpistemicFrame enum (marcos iniciales: EXPLORATION, CREATIVE, MARKETING, BENCHMARK, PRODUCTION, CODE_STATE, LEGAL, MEDICAL, FINANCIAL, SECURITY, EDUCATIONAL, RESEARCH) | P1 | B-03 |
| G-02 | Implementar FrameShiftGuard | P1 | G-01 |
| G-03 | Implementar InterfaceTruthGap | P1 | G-01 |
| G-04 | Implementar ActionabilityGate | P1 | G-01 |
| G-05 | Implementar frame-specific evidence requirements | P1 | G-01 |
| G-06 | Implementar PresentationBoundary | P1 | G-01 |
| G-07 | Implementar InterfaceMode y ActionIntent | P1 | G-01 |
| G-08 | Escribir frame layer tests | P1 | G-01—G-07 |

### Tests clave
```
test_same_claim_has_different_decision_in_exploration_and_production_frames
test_marketing_frame_allows_limited_claim_but_blocks_overclaim
test_benchmark_frame_requires_dataset_scope
test_production_frame_requires_deployment_evidence
test_frame_shift_requires_evidence_bridge
test_interface_utility_cannot_promote_to_truth
test_persuasive_output_without_evidence_has_high_interface_truth_gap
test_actionable_claim_requires_stronger_gate_than_explanatory_claim
```

---

## Hito H — Xendris Agent UI

**Objetivo:** Producto usable: un agente, todos los modelos, trust-routed.

### Estado actual
- Frontend reset limpio (sin features de producto)
- Shell de chat experimental (`xendris-shell.tsx`, `chat-panel.tsx`)
- API endpoints de chat con streaming
- 30+ componentes shadcn/ui disponibles

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| H-01 | Rebuild chat UI sobre shell existente con routing de modelos | P1 | D-03, F-01 |
| H-02 | Implementar model route explanation panel (por qué este modelo) | P1 | D-03 |
| H-03 | Implementar trust panel (claims evaluados, decisiones, evidencias) | P1 | D-04, F-07 |
| H-04 | Implementar cost panel (coste por respuesta, ahorro acumulado) | P1 | E-03, E-04 |
| H-05 | Implementar ledger per conversation (eventos en tiempo real) | P1 | D-05 |
| H-06 | Implementar user-selectable modes (eco, normal, precision, custom) | P1 | F-02, G-01 |
| H-07 | Implementar selector manual de modelo override | P1 | D-03 |
| H-08 | Implementar visualización de Frontera C (claims bloqueados/limitados/admitidos) | P1 | H-03 |
| H-09 | Implementar local model connector UI (Ollama futuro) | P2 | H-01 |
| H-10 | Implementar streaming de confianza (decisiones en tiempo real mientras el modelo genera) | P2 | D-03 |
| H-11 | Escribir user acceptance tests | P1 | H-01—H-10 |

### Arquitectura de modos

```txt
Eco mode:    cheap model + local guards
Normal mode: medium model + gates + optional second opinion
Precision:   frontier model + full gates + representation consistency
Custom:      user-configured risk/cost profile
```

### UX principles
- El usuario siempre sabe por qué se eligió un modelo
- El usuario siempre sabe qué claims fueron bloqueados/limitados
- El usuario siempre sabe cuánto cuesta cada respuesta
- El ledger es visible por conversación

---

## Hito I — Trust Dashboard

**Objetivo:** Hacer visible el valor diferencial de Xendris.

### Tareas

| ID | Tarea | Prioridad | Depende de |
|----|-------|-----------|------------|
| I-01 | Implementar dashboard overview (saldo, consumo, ahorro) | P1 | E-01, E-02 |
| I-02 | Implementar cost per admissible answer display | P1 | E-03, E-04 |
| I-03 | Implementar tokens avoided y escalations avoided display | P1 | F-08 |
| I-04 | Implementar model spend breakdown chart | P1 | E-03 |
| I-05 | Implementar trust decisions display (blocked/limited/admitted) | P1 | D-04 |
| I-06 | Implementar evidence reports view | P1 | C-07 |
| I-07 | Implementar exportable audit (JSON/JSONL/Markdown) | P1 | D-05 |
| I-08 | Implementar API key management UI | P1 | D-02 |
| I-09 | Implementar wallet/billing views | P1 | E-01, E-07 |
| I-10 | Implementar ledger viewer con búsqueda por run_id | P1 | D-05 |
| I-11 | Implementar gráfico de ahorro vs baseline premium | P1 | I-02 |
| I-12 | Escribir dashboard tests | P1 | I-01—I-11 |

### Métricas del dashboard

```txt
cost_per_admissible_answer       (métrica central)
cost_per_admitted_claim
latency_per_admissible_answer
premium_model_avoidance_rate
local_guard_resolution_rate
trust_cache_hit_rate
human_review_avoidance_rate
blocked_overclaim_rate
hypothesis_preservation_rate
```

---

## Resumen de versiones vs hitos

| Release | Hitos | Contenido |
|---------|-------|-----------|
| v0.2.2  | A     | Clean public framework release |
| v0.3.0  | B     | API audit, clasificación de módulos |
| v0.4.0  | C, G  | Real provider evidence + Epistemic Frame Layer |
| v0.5.0  | D     | Runtime API MVP |
| v0.6.0  | E     | Wallet & Usage Core |
| v0.7.0  | F     | Adaptive Council & Sycophancy |
| v0.8.0  | H     | Xendris Agent UI |
| v0.9.0  | I     | Trust Dashboard |
| v1.0.0  | H+I   | Producto completo |

---

## Principios de ejecución

1. **No overclaiming**: Cada hito se valida con tests antes de declararse completo
2. **Evidencia primero**: Ningún claim de rendimiento sin artefacto admitido en evidence registry
3. **Compatibilidad**: Las capas experimentales no rompen la API pública estable
4. **Coste consciente**: Cada decisión de arquitectura considera coste por respuesta admisible
5. **Sobriedad**: Sin afirmaciones de superioridad universal, validación física directa o production readiness sin evidencia

---

## Definition of Done (por hito)

Un hito está completo solo si:
- todas sus tareas están implementadas
- los tests asociados existen y pasan
- hay documentación de estado
- no hay claims no soportados sobre el hito
- el release gate no detecta incoherencias
- no hay regresiones sobre hitos anteriores
