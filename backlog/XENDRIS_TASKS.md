# Xendris Tasks — Desglose dinámico por hito

Cada tarea sigue el schema `BacklogTask` definido en `phyng.loop.schemas`.

---

## Hito A — v0.2.x Clean Public Framework Release

### A-01: Implementar Historical Artifact Quarantine Policy
- **Tipo:** `POLICY`
- **P0**
- **Bloquea:** A-02, A-03, A-06
- **Acceptance criteria:**
  - Política documentada en `docs/policies/`
  - Define qué es historical, rejected, quarantined, superseded
  - Define qué artefactos pueden/citan ser evidence
  - Integrada con release gate

### A-02: Crear manifest de artefactos rechazados
- **Tipo:** `DATA`
- **P0**
- **Depende de:** A-01
- **Bloquea:** A-03
- **Acceptance criteria:**
  - Manifest JSON en `rag/citations/` o `data/audits/`
  - Cada artefacto tiene status: REJECTED, QUARANTINED_HISTORICAL, SUPERSEDED
  - Razón de rechazo documentada

### A-03: Ejecutar suite audit distinguiendo historical rejected vs active blocker
- **Tipo:** `AUDIT`
- **P0**
- **Depende de:** A-02
- **Bloquea:** A-04
- **Acceptance criteria:**
  - Script audit separa rejected históricos (non-blocking) de active blockers
  - Reporte generado con conteos
  - Cero active blockers

### A-04: Crear release_gate_v0_2_2
- **Tipo:** `SCRIPT`
- **P0**
- **Depende de:** A-03
- **Bloquea:** A-07
- **Acceptance criteria:**
  - `scripts/release_gate_v0_2_2.py` existe
  - Chequea: unsafe citations = 0, active blockers = 0, working tree clean
  - Output: PASS / WARNINGS_PRESENT / BLOCKED

### A-05: Fix whitespace warning en `phyng/api.py`
- **Tipo:** `FIX`
- **P0**
- **Bloquea:** A-07
- **Acceptance criteria:**
  - Whitespace issue corregido o warning explícito documentado
  - Release gate no bloquea por esto (solo warning)

### A-06: Limpiar working tree
- **Tipo:** `CLEANUP`
- **P0**
- **Depende de:** A-01
- **Bloquea:** A-07
- **Acceptance criteria:**
  - `git status` limpio (solo archivos intencionales)
  - Outputs generados en cuarentena o ignorados
  - `.gitignore` actualizado

### A-07: Tag release v0.2.2
- **Tipo:** `RELEASE`
- **P0**
- **Depende de:** A-04, A-05, A-06
- **Acceptance criteria:**
  - Release gate: PASS o WARNINGS_PRESENT
  - Tag `v0.2.2` creado
  - Release notes generadas

### A-08: Verificar exit criteria del hito
- **Tipo:** `VERIFY`
- **P0**
- **Depende de:** A-07
- **Acceptance criteria:**
  - release gate PASS o WARNINGS_PRESENT
  - unsafe rejected citations = 0
  - active benchmark blockers = 0

---

## Hito B — API Boundary Audit

### B-01: Auditar `xendris.benchmarking`
- **Tipo:** `AUDIT`
- **P1**
- **Depende de:** A-07
- **Bloquea:** B-03
- **Acceptance criteria:**
  - Reporte de todos los símbolos exportados
  - Clasificación: stable/experimental/private
  - Dependencias internas documentadas

### B-02: Auditar `xendris.core.trust`
- **Tipo:** `AUDIT`
- **P1**
- **Depende de:** A-07
- **Bloquea:** B-03
- **Acceptance criteria:**
  - Reporte de todos los símbolos exportados
  - Clasificación: stable/experimental/private
  - Dependencias internas documentadas

### B-03: Clasificar módulos restantes
- **Tipo:** `AUDIT`
- **P1**
- **Depende de:** B-01, B-02
- **Bloquea:** B-04, B-05, D-01, G-01
- **Acceptance criteria:**
  - runtime, router, fingerprints, ledger, algebra, boundary, local, sectors, representations
  - Cada módulo tiene clasificación explícita en `__init__.py`

### B-04: Definir deprecation policy
- **Tipo:** `POLICY`
- **P1**
- **Depende de:** B-03
- **Acceptance criteria:**
  - Documento en `docs/policies/api_deprecation.md`
  - Timeline: deprecation warning → removal
  - Versiones semánticas

### B-05: Escribir public import tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** B-03
- **Acceptance criteria:**
  - `tests/test_public_imports.py`
  - Verifica que imports estables funcionan
  - Verifica que imports experimentales son posibles pero advierten
  - Verifica que imports privados fallan

### B-06: Publicar API surface spec
- **Tipo:** `DOCS`
- **P1**
- **Depende de:** B-05
- **Acceptance criteria:**
  - `docs/api/public_api_surface.md`
  - Lista completa de símbolos públicos
  - Ejemplos de uso para cada módulo estable

### B-07: Deprecar o poblar namespaces vacíos
- **Tipo:** `CLEANUP`
- **P2**
- **Depende de:** B-03
- **Acceptance criteria:**
  - `xendris.models`, `xendris.benchmarks`, `xendris.prompts`, `xendris.outputs`, `xendris.scripts`
  - O tienen contenido útil o tienen deprecation warning explícito

---

## Hito C — Real Provider Evidence Import

### C-01: Real-provider Trust Traps
- **Tipo:** `BENCHMARK`
- **P1**
- **Depende de:** A-07
- **Bloquea:** C-03, C-04, C-05, C-06
- **Acceptance criteria:**
  - Script ejecuta Trust Traps contra OpenAI, Anthropic, DeepSeek
  - Resultados guardados en JSONL
  - Misma metodología que dry-run

### C-02: Real-provider Programming Reliability
- **Tipo:** `BENCHMARK`
- **P1**
- **Depende de:** A-07
- **Bloquea:** C-06
- **Acceptance criteria:**
  - Script ejecuta Programming Reliability contra proveedores
  - Resultados guardados en JSONL

### C-03: Provider disclosure gate
- **Tipo:** `GATE`
- **P1**
- **Depende de:** C-01
- **Bloquea:** C-07
- **Acceptance criteria:**
  - Cada reporte incluye proveedor, versión API, fecha
  - Gate bloquea publicación sin disclosure

### C-04: Cost disclosure gate
- **Tipo:** `GATE`
- **P1**
- **Depende de:** C-01
- **Bloquea:** C-07
- **Acceptance criteria:**
  - Cada reporte incluye coste por ejecución
  - Coste por token, por request, total

### C-05: Latency disclosure gate
- **Tipo:** `GATE`
- **P1**
- **Depende de:** C-01
- **Bloquea:** C-07
- **Acceptance criteria:**
  - Cada reporte incluye latencia promedio, p50, p95
  - Modo dry-run vs real provider

### C-06: Dry-run vs real-provider comparison
- **Tipo:** `ANALYSIS`
- **P1**
- **Depende de:** C-01, C-02
- **Bloquea:** C-07
- **Acceptance criteria:**
  - Reporte comparativo: misma métrica, distinto entorno
  - Delta documentado
  - Interpretación permitida/prohibida

### C-07: Evidence registry admission
- **Tipo:** `DATA`
- **P1**
- **Depende de:** C-03, C-04, C-05
- **Bloquea:** C-08, I-06
- **Acceptance criteria:**
  - Artefactos clasificados como ADMITTED/REJECTED/QUARANTINED
  - Registry actualizado

### C-08: Benchmark report conservador
- **Tipo:** `REPORT`
- **P2**
- **Depende de:** C-07
- **Acceptance criteria:**
  - Reporte público con limitaciones explícitas
  - Sin claims de superioridad universal
  - Provider, cost, latency disclosure presente

---

## Hito D — Runtime API MVP

### D-01: FastAPI service para Xendris Runtime
- **Tipo:** `INFRA`
- **P1**
- **Depende de:** B-03
- **Bloquea:** D-02—D-10, E-01—E-10, F-01—F-10, H-01—H-11, I-01—I-12
- **Acceptance criteria:**
  - Servicio FastAPI standalone o extensión de `phyng.api.py`
  - Configurable por env vars
  - Health endpoint básico

### D-02: API key authentication
- **Tipo:** `SECURITY`
- **P1**
- **Depende de:** D-01
- **Bloquea:** I-08
- **Acceptance criteria:**
  - Middleware de API key
  - Keys almacenadas (hash) en DB o env
  - 401/403 para requests no autorizados

### D-03: `POST /v1/runtime/execute`
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** D-01
- **Bloquea:** H-01, H-02, H-10
- **Acceptance criteria:**
  - Acepta prompt + config (model, risk, etc.)
  - Pasa por: selector → provider sandbox → gates → ledger
  - Devuelve response + trust metadata
  - Modo full runtime y external gate

### D-04: `POST /v1/claims/evaluate`
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** D-01
- **Bloquea:** H-03, I-05
- **Acceptance criteria:**
  - Acepta texto + metadata opcional
  - Extrae claims, evalúa, devuelve decisiones
  - Sin llamar a modelo externo (solo evaluación)

### D-05: `GET /v1/ledger/{run_id}`
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** D-01
- **Bloquea:** H-05, I-07, I-10
- **Acceptance criteria:**
  - Devuelve eventos del ledger para un run_id
  - Filtrable por tipo de evento
  - Hash chain verificable

### D-06: `GET /v1/health`
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** D-01
- **Acceptance criteria:**
  - Responde 200 OK
  - Incluye version, uptime, status de módulos

### D-07: `POST /v1/routes/select`
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** D-01
- **Acceptance criteria:**
  - Dado prompt + risk + budget → devuelve modelo seleccionado + razón
  - Sin ejecutar el modelo

### D-08: Provider sandbox integration
- **Tipo:** `INTEGRATION`
- **P1**
- **Depende de:** D-03
- **Acceptance criteria:**
  - Sandbox bloquea network por defecto
  - Mocks deterministas disponibles
  - Quotas y cost tracking

### D-09: Deterministic test mode
- **Tipo:** `TEST`
- **P1**
- **Depende de:** D-01
- **Acceptance criteria:**
  - Modo donde todas las decisiones son deterministas
  - Mocks reemplazan llamadas a proveedores
  - Útil para CI/CD

### D-10: Integration tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** D-03—D-09
- **Acceptance criteria:**
  - Tests para cada endpoint
  - Tests de autenticación
  - Tests de modo determinista

---

## Hito E — Wallet & Usage Core

### E-01: Tenant wallet model
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** D-01
- **Bloquea:** E-02, E-05, E-06, E-07, I-01, I-09
- **Acceptance criteria:**
  - Modelo Pydantic: tenant_id, balance, currency, hard_cap, daily_limit, monthly_limit
  - Persistencia en DB
  - Operaciones atómicas (cargo, abono)

### E-02: Usage meter
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** D-01
- **Bloquea:** I-01
- **Acceptance criteria:**
  - Registra por request: tenant_id, project_id, api_key, model, tokens, cost, timestamp
  - Consultable por periodo

### E-03: Provider cost records
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** D-03
- **Bloquea:** E-04, H-04, I-02, I-04
- **Acceptance criteria:**
  - Registra coste real por provider call
  - Modelo, tokens in/out, coste, timestamp
  - Asociado a run_id

### E-04: Xendris margin calculator
- **Tipo:** `SERVICE`
- **P1**
- **Depende de:** E-03
- **Bloquea:** H-04, I-02
- **Acceptance criteria:**
  - Calcula: provider_cost + Xendris_margin = total
  - Margen configurable por tenant/plan
  - Fórmula: margin = provider_cost * rate + fixed_fee

### E-05: Budget policy engine
- **Tipo:** `SERVICE`
- **P1**
- **Depende de:** E-01
- **Bloquea:** E-09
- **Acceptance criteria:**
  - Evaluación pre-request: hard cap, daily, monthly
  - BLOCK si budget excedido
  - Alerta configurable

### E-06: Balance check gate
- **Tipo:** `GATE`
- **P1**
- **Depende de:** E-01
- **Acceptance criteria:**
  - Gate en runtime: si balance < estimated_cost → BLOCK
  - Mensaje claro al usuario

### E-07: Wallet top-up endpoint
- **Tipo:** `ENDPOINT`
- **P1**
- **Depende de:** E-01
- **Bloquea:** I-09
- **Acceptance criteria:**
  - POST /v1/wallet/topup
  - Simulación de pago (sin integración real inicial)
  - Saldo actualizado

### E-08: Wallet/billing API
- **Tipo:** `API`
- **P1**
- **Depende de:** E-03, E-04
- **Acceptance criteria:**
  - GET /v1/usage
  - GET /v1/wallet/balance
  - GET /v1/billing/history

### E-09: Alerts system
- **Tipo:** `SERVICE`
- **P2**
- **Depende de:** E-05
- **Acceptance criteria:**
  - Alerta configurable al N% de budget consumido
  - Canal: email, dashboard notification

### E-10: Wallet/billing tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** E-01—E-09
- **Acceptance criteria:**
  - Tests de cargo/abono atómico
  - Tests de budget policy
  - Tests de balance check gate

---

## Hito F — Adaptive Council & Sycophancy Layer

### F-01: SycophancyGuard
- **Tipo:** `GATE`
- **P1**
- **Depende de:** D-01
- **Bloquea:** H-01
- **Acceptance criteria:**
  - Detecta cuando el usuario propone conclusión y el modelo asiente sin evidencia
  - Regla: user conclusion → limited hypothesis, no fact
  - Tests: `test_user_hypothesis_not_promoted_without_evidence`

### F-02: AdaptiveCouncilPolicy
- **Tipo:** `POLICY`
- **P1**
- **Depende de:** D-01
- **Bloquea:** F-03—F-08, H-06
- **Acceptance criteria:**
  - No council by default
  - Council solo por evidence of need
  - Reglas de escalado definidas

### F-03: ContrarianGuard
- **Tipo:** `GATE`
- **P1**
- **Depende de:** F-02
- **Acceptance criteria:**
  - Genera contraargumento cuando hay sycophancy
  - Tests: `test_sycophantic_answer_requires_contraargument`

### F-04: FirstPrinciplesGuard
- **Tipo:** `GATE`
- **P1**
- **Depende de:** F-02
- **Acceptance criteria:**
  - Evalúa si respuesta es consistente con primeros principios
  - Para claims científicos/técnicos

### F-05: EvidenceGuard
- **Tipo:** `GATE`
- **P1**
- **Depende de:** F-02
- **Acceptance criteria:**
  - Verifica si claim tiene evidencia asociada
  - Si no, degrada a hypothesis

### F-06: Marginal certainty gain metric
- **Tipo:** `METRIC`
- **P1**
- **Depende de:** F-02
- **Bloquea:** F-08, I-03
- **Acceptance criteria:**
  - `marginal_certainty_gain_per_token`
  - Registrada por escalación de council

### F-07: Council escalation logging
- **Tipo:** `FEATURE`
- **P1**
- **Depende de:** F-02
- **Bloquea:** H-03
- **Acceptance criteria:**
  - Cada escalación registrada en trust ledger
  - Incluye: razón, modelos usados, tokens, coste, certainty gain

### F-08: Token avoidance tracking
- **Tipo:** `METRIC`
- **P1**
- **Depende de:** F-06
- **Bloquea:** I-03
- **Acceptance criteria:**
  - `tokens_avoided_by_local_guards`
  - `cost_saved_vs_always_council`

### F-09: Sycophancy tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** F-01—F-08
- **Acceptance criteria:**
  - 5+ tests de casos de sycophancy
  - Cubren low, medium, high risk

### F-10: Council tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** F-01—F-08
- **Acceptance criteria:**
  - Tests de escalado/desescalado
  - Tests de marginal certainty gain
  - Tests de no-council por defecto

---

## Hito G — Epistemic Frame Layer

### G-01: EpistemicFrame enum
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** B-03
- **Bloquea:** G-02—G-08, H-06
- **Acceptance criteria:**
  - Enum con 12+ frames iniciales
  - Cada frame tiene: evidence_requirements, actionability_level, default_gates

### G-02: FrameShiftGuard
- **Tipo:** `GATE`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - Detecta intento de cambiar frame sin evidencia puente
  - Regla: frame_shift_requires_evidence_bridge

### G-03: InterfaceTruthGap
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - Mide distancia entre utilidad de interfaz y certeza cognitiva
  - A mayor actionability, mayor gap requiere evidencia

### G-04: ActionabilityGate
- **Tipo:** `GATE`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - Clasifica output como: explanatory / actionable / critical
  - Crítico requiere más evidencia

### G-05: Frame-specific evidence requirements
- **Tipo:** `POLICY`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - Cada frame define qué evidencia es necesaria
  - PRODUCTION: deployment evidence
  - BENCHMARK: dataset scope
  - MARKETING: no universal language

### G-06: PresentationBoundary
- **Tipo:** `GATE`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - Distingue entre contenido presentado y certeza afirmada
  - Interfaz útil ≠ certeza cognitiva

### G-07: InterfaceMode y ActionIntent
- **Tipo:** `MODEL`
- **P1**
- **Depende de:** G-01
- **Acceptance criteria:**
  - InterfaceMode: CHAT, DASHBOARD, API, REPORT, CANVAS
  - ActionIntent: EXPLAIN, PERSUADE, INSTRUCT, DECIDE, CREATE
  - Cada combinación tiene perfil de riesgo

### G-08: Frame layer tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** G-01—G-07
- **Acceptance criteria:**
  - 8+ tests cubriendo frames y transitions
  - Tests de gap y actionability

---

## Hito H — Xendris Agent UI

### H-01: Rebuild chat UI with model routing
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-03, F-01
- **Acceptance criteria:**
  - Shell de chat funcional
  - Selector automático de modelo visible
  - Streaming de respuesta

### H-02: Model route explanation panel
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-03
- **Acceptance criteria:**
  - Panel que explica: por qué este modelo, riesgo, coste estimado
  - Tooltip o expandable section

### H-03: Trust panel
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-04, F-07
- **Acceptance criteria:**
  - Muestra claims evaluados por respuesta
  - Cada claim: status (APPROVED/BLOCKED/LIMITED), evidencia, frame
  - Visualización clara de Frontera C

### H-04: Cost panel
- **Tipo:** `UI`
- **P1**
- **Depende de:** E-03, E-04
- **Acceptance criteria:**
  - Coste por respuesta
  - Ahorro acumulado vs frontier
  - Coste por respuesta admisible

### H-05: Ledger per conversation
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-05
- **Acceptance criteria:**
  - Timeline de eventos de confianza por conversación
  - Expandible para ver detalles

### H-06: User-selectable modes
- **Tipo:** `UI`
- **P1**
- **Depende de:** F-02, G-01
- **Acceptance criteria:**
  - Selector: Eco / Normal / Precision / Custom
  - Cada modo configura risk, model tier, gates
  - Visualización del perfil activo

### H-07: Manual model override
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-03
- **Acceptance criteria:**
  - Usuario puede override temporal del modelo
  - Advertencia de coste/riesgo

### H-08: Frontera C visualization
- **Tipo:** `UI`
- **P1**
- **Depende de:** H-03
- **Acceptance criteria:**
  - Visualización de claims que cruzaron/no cruzaron Frontera C
  - Indicador visual por claim

### H-09: Local model connector UI
- **Tipo:** `UI`
- **P2**
- **Depende de:** H-01
- **Acceptance criteria:**
  - UI para conectar Ollama/local model
  - Estado: conectado/desconectado
  - Sin implementación de seguridad NAT (futuro)

### H-10: Streaming de confianza
- **Tipo:** `UI`
- **P2**
- **Depende de:** D-03
- **Acceptance criteria:**
  - Decisiones de confianza aparecen en tiempo real mientras el modelo genera
  - Claims evaluados aparecen progresivamente

### H-11: User acceptance tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** H-01—H-10
- **Acceptance criteria:**
  - Tests E2E de flujo de chat
  - Tests de cambio de modo
  - Tests de panels

---

## Hito I — Trust Dashboard

### I-01: Dashboard overview
- **Tipo:** `UI`
- **P1**
- **Depende de:** E-01, E-02
- **Acceptance criteria:**
  - Cards: saldo, consumo mes, ahorro estimado, coste por respuesta admisible
  - Actualización en tiempo real (o polling)

### I-02: Cost per admissible answer
- **Tipo:** `UI`
- **P1**
- **Depende de:** E-03, E-04
- **Acceptance criteria:**
  - `cost_per_admissible_answer` como métrica central del dashboard
  - Gráfico de tendencia

### I-03: Tokens and escalations avoided
- **Tipo:** `UI`
- **P1**
- **Depende de:** F-08
- **Acceptance criteria:**
  - Tokens avoided counter
  - Escalations avoided counter
  - Cost saved vs always-frontier

### I-04: Model spend breakdown
- **Tipo:** `UI`
- **P1**
- **Depende de:** E-03
- **Acceptance criteria:**
  - Gráfico de gasto por modelo
  - % del total

### I-05: Trust decisions display
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-04
- **Acceptance criteria:**
  - Tabla/gráfico: blocked / limited / admitted / human_review
  - Tendencias

### I-06: Evidence reports view
- **Tipo:** `UI`
- **P1**
- **Depende de:** C-07
- **Acceptance criteria:**
  - Lista de artefactos de evidencia
  - Status: ADMITTED / REJECTED / QUARANTINED
  - Detalles del benchmark

### I-07: Exportable audit
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-05
- **Acceptance criteria:**
  - Export ledger como JSON, JSONL, Markdown
  - Botón de descarga

### I-08: API key management
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-02
- **Acceptance criteria:**
  - CRUD de API keys
  - Mostrar key parcial, fecha creación, último uso
  - Revocar

### I-09: Wallet/billing views
- **Tipo:** `UI`
- **P1**
- **Depende de:** E-01, E-07
- **Acceptance criteria:**
  - Balance actual
  - Historial de recargas
  - Top-up button (simulado)

### I-10: Ledger viewer
- **Tipo:** `UI`
- **P1**
- **Depende de:** D-05
- **Acceptance criteria:**
  - Búsqueda por run_id
  - Timeline de eventos
  - Hash chain status

### I-11: Savings vs baseline chart
- **Tipo:** `UI`
- **P1**
- **Depende de:** I-02
- **Acceptance criteria:**
  - Comparación: coste actual vs siempre-frontier
  - Ahorro acumulado

### I-12: Dashboard tests
- **Tipo:** `TEST`
- **P1**
- **Depende de:** I-01—I-11
- **Acceptance criteria:**
  - Tests de renderizado de componentes
  - Tests de datos mock

---

## Resumen de dependencias entre hitos

```txt
A ──> B ──> C ──> (C-07, C-08 alimentan I-06)
│     └──> G ──> H (frame layer para modos de agente)
└──> D ──> E ──> I (wallet para dashboard)
      └──> F ──> H (sycophancy + council para agente)
            └──> I (métricas de ahorro)
B ──> G ──> H (epistemic frames para UX de agente)
```

Los hitos D, E, F pueden ejecutarse en paralelo después de A y B.
Los hitos H e I pueden ejecutarse en paralelo después de D, E, F, G.
