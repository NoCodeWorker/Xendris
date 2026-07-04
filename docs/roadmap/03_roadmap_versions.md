# 03 — Roadmap por versiones

## v0.3 — Trust Kernel actual

Estado: iniciado / parcialmente implementado.

Incluye:

- `ClaimType`;
- `ClaimStatus`;
- `RiskLevel`;
- `AuditDecision`;
- `Benchmark Gate`;
- `Trust Traps Dataset v0.1`;
- corrida A/B DeepSeek Base vs Xendris + DeepSeek.

Objetivo de esta fase:

> Demostrar que una capa determinista puede evitar contaminación de scoring en un dataset cerrado de trampas epistémicas.

## v0.4 — Local Claim Algebras

Objetivo:

> Convertir claims en objetos formales y asignarlos a contextos locales con políticas de preservación de utilidad y anti-sobrebloqueo.

Entregables:

```text
xendris/core/algebra/
xendris/core/local/
xendris/core/boundary/
```

Capacidades:

- `ClaimObject`;
- `LocalContext`;
- `LocalClaimAlgebra`;
- `EvidenceBridge`;
- `ContaminationGuard`;
- `UsefulnessPreservationPolicy` (para degradar claims sobremedidos y evitar sobrebloqueo);
- Monitoreo inicial de métricas de sobrebloqueo y preservación de respuestas normales de control.

Criterios de éxito de v0.4:
- Xendris bloquea la contaminación insegura (v.g. superioridad universal, dry-run a producción).
- Xendris preserva respuestas normales de control sin bloqueos innecesarios.
- Xendris distingue claims operativos factuales de hipótesis exploratorias de bajo riesgo.
- Xendris implementa el comportamiento de degradación antes del bloqueo (downgrade-before-block).
- Xendris mide de manera formal el riesgo de sobrebloqueo.

## v0.5 — Epistemic Microcausality

Objetivo:

> Impedir que claims de un dominio contaminen otro sin evidencia puente, aplicando políticas de mitigación y preservación de utilidad.

Ejemplos bloqueados:

```text
benchmark_score → universal_superiority
dry_run_latency → production_latency
user_provided → verified_factual
```

Capacidades nuevas:
- Richer sector transitions para hipótesis, exploración y contenido creativo/explicativo.
- Eventos de preservación de utilidad registrados en el trust ledger.
- Seguimiento y registro de la métrica `false_positive_block_rate`.

## v0.6 — Sector Transition Engine

Objetivo:

> Formalizar reglas de paso entre sectores epistémicos.

Sectores iniciales:

```text
FACTUAL
INFERRED
CALCULATED
CODE_STATE
USER_PROVIDED
POLICY
UNSUPPORTED
BENCHMARK
RUNTIME
COST
LATENCY
PRODUCTION
```

## v0.7 — Trust Ledger

Objetivo:

> Persistir cada decisión de confianza.

Entregables:

```text
trust_ledger.jsonl
summary.md
blocked_claims.csv
human_review_queue.json
model_epistemic_profile.json
```

## v0.8 — Representation Consistency Gate

Objetivo:

> Comparar outputs de modelos como representaciones de claims.

Estados:

```text
EQUIVALENT
PARTIALLY_EQUIVALENT
CONTRADICTORY
DISJOINT
UNSUPPORTED_EXPANSION
```

## v0.9 — Model Epistemic Fingerprint

Objetivo:

> Reconstruir la huella epistémica de cada modelo desde su comportamiento observable.

Métricas:

```text
unsupported_claim_rate
universalization_rate
sector_violation_rate
cost_per_admissible_claim
latency_proxy_bias
```

## v1.0 — Multi-Model Selector

Objetivo:

> Elegir modelo según riesgo, coste, latencia y perfil epistémico.

Decisiones:

```text
use_cheap_model
use_strong_model
use_local_model
ask_two_models
block
human_review
```

## v1.1 — Agentic Trust Runtime

Objetivo:

> Convertir Xendris en agente gobernado por gates.

Diferencia frente a agentes normales:

```text
Agente normal: planifica → ejecuta → responde
Xendris Agent: planifica → propone → verifica → ejecuta → audita → responde con límites
```

## v1.2 — External Benchmark Validation

Objetivo:

> Validar fuera del dataset propio.

Datasets objetivo:

```text
Trust Traps v0.2 — 500 muestras
Trust Traps v0.3 — 1.000 muestras
Third-party adversarial traps
Code claim validation set
RAG hallucination set
Benchmark contamination set
Production claim set
Cost/latency proxy set
```

## v1.3 — Commercial Trust Router

Objetivo:

> Producto inicial vendible como Trust Firewall para modelos generativos.

Capacidades:

- API;
- CLI;
- ledger;
- informes;
- selector básico;
- integración con proveedores baratos;
- modo benchmark;
- modo código;
- modo RAG.
