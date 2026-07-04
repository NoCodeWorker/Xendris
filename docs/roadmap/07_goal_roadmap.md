# 07 — Goal de roadmap

## Goal principal

Desarrollar Xendris como una arquitectura algebraica de confianza para gobernar modelos generativos, basada en claims auditables, contextos locales, sectores epistémicos, reglas de no contaminación, ledger y reconstrucción del comportamiento observable de modelos.

“Success does not mean blocking every unsupported claim. Success means assigning the safest useful epistemic status.”

“Xendris should preserve useful outputs whenever they can be safely scoped, downgraded, or admitted with limitations.”

## Resultado esperado

Xendris debe ser capaz de recibir outputs de modelos generativos baratos o potentes y decidir de forma determinista:

```text
ALLOW
ALLOW_WITH_LIMITATIONS
ALLOW_AS_HYPOTHESIS
BLOCK
HUMAN_REVIEW
```

según:

- tipo de claim;
- contexto local;
- evidencia disponible;
- riesgo;
- transición solicitada;
- historial del modelo;
- trazas de ejecución;
- restricciones de benchmark o producción.

## Principios no negociables

1. No afirmar superioridad universal.
2. No usar AQFT como validación física directa.
3. No confundir output plausible con conocimiento admisible.
4. No permitir que un benchmark local se convierta en claim global.
5. No permitir que una afirmación del usuario se convierta en hecho sin evidencia.
6. No permitir que tests locales se conviertan en claim de producción sin trazas.
7. No permitir que latencia dry-run se convierta en latencia real.
8. Registrar cada decisión relevante.
9. Preferir bloqueo o revisión humana ante conflictos irresolubles.
10. Mantener tests deterministas.
11. **Maximizar admisibilidad segura y evitar sobrebloqueo**: Xendris no debe maximizar el bloqueo, sino la admisibilidad segura de claims mediante acotación o degradación controlada.
12. **Advertencia de sobrebloqueo**: Si Xendris bloquea salidas normales, exploratorias, creativas o de bajo riesgo útiles innecesariamente, el hito no es exitoso.


## Roadmap operativo

### Bloque 1 — v0.4 Local Claim Algebras

Implementar:

```text
ClaimObject
LocalContext
LocalClaimAlgebra
EvidenceBridge
ContaminationGuard
```

### Bloque 2 — v0.5 Epistemic Microcausality

Implementar:

```text
Boundary rules
Context contamination checks
Allowed/blocked context transitions
```

### Bloque 3 — v0.6 Sector Transition Engine

Implementar:

```text
Sector enum
Transition rules
Forbidden transitions
Promotion/demotion logic
```

### Bloque 4 — v0.7 Trust Ledger

Implementar:

```text
JSONL writer
PostgreSQL-ready schema
Audit export
Human review queue
```

### Bloque 5 — v0.8 Representation Consistency Gate

Implementar:

```text
Multi-output claim comparison
Equivalence states
Contradiction detection
Unsupported expansion detection
```

### Bloque 6 — v0.9 Model Epistemic Fingerprint

Implementar:

```text
Model behavior metrics
Cost per admissible claim
Sector violation rate
Provider-agnostic profile
```

### Bloque 7 — v1.0 Multi-Model Selector

Implementar:

```text
Risk-based routing
Cost-based routing
Model profile routing
Escalation policy
```

### Bloque 8 — v1.1 Agentic Trust Runtime

Implementar:

```text
Planner
Executor
Tool policy
Claim runtime
Safety gate
Finalizer
```

### Bloque 9 — v1.2 External Benchmark Validation

Implementar:

```text
Trust Traps v0.2+
Third-party adversarial traps
Ablation studies
Multi-model validation
Real latency/cost measurement
```

## Definition of done general

Una fase está terminada solo si:

- tiene tests;
- los tests pasan;
- hay documentación de estado;
- no hay claims no soportados;
- el release gate no detecta incoherencias;
- el sistema conserva compatibilidad hacia atrás o documenta claramente la ruptura.

## Frase guía

> Xendris no hace que un modelo sepa más; hace que sus outputs sean gobernables, auditables y seguros de admitir.
