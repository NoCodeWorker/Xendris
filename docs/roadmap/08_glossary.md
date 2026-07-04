# 08 — Glosario Xendris

## Xendris

Arquitectura algebraica de confianza para gobernar modelos generativos.

## Frontera C

Nombre de la intuición original: frontera entre outputs probabilísticos y decisiones operativas. Evoluciona hacia la arquitectura Xendris.

## Claim

Afirmación extraída de un output de modelo, input de usuario, benchmark, runtime, código o documento.

## ClaimObject

Representación formal e inmutable de un claim con tipo, estado, riesgo, contexto y evidencia.

## ClaimType

Tipo epistémico del claim.

Ejemplos:

```text
FACTUAL
INFERRED
CALCULATED
CODE_STATE
USER_PROVIDED
POLICY
UNSUPPORTED
```

## ClaimStatus

Estado de soporte del claim.

Ejemplos:

```text
VERIFIED
PARTIALLY_SUPPORTED
UNSUPPORTED
CONTRADICTED
NEEDS_HUMAN_REVIEW
```

## LocalContext

Dominio operativo donde vive un claim.

Ejemplos:

```text
USER
BENCHMARK
CODE
RUNTIME
RAG
POLICY
COST
LATENCY
PRODUCTION
DOCUMENTATION
```

## LocalClaimAlgebra

Conjunto de reglas locales que determinan qué claims son admisibles dentro de un contexto y qué transiciones pueden realizar.

## EvidenceBridge

Evidencia que permite cruzar un claim de un contexto o sector a otro.

Ejemplos:

```text
TEST_RESULT
SOURCE_CITATION
RUNTIME_TRACE
BENCHMARK_ARTIFACT
HUMAN_REVIEW
DEPLOYMENT_LOG
COST_REPORT
LATENCY_MEASUREMENT
BUILD_LOG
```

## Epistemic Microcausality

Regla de no contaminación:

> Un claim no puede cruzar una frontera contextual sin evidencia válida.

## Sector

Clase epistémica o dominio lógico de un claim. Un claim no cambia de sector sin una transición válida.

## Sector Transition

Cambio de un claim desde un sector/contexto a otro.

Ejemplo:

```text
USER_PROVIDED → FACTUAL
```

requiere evidencia.

## Forbidden Transition

Transición prohibida por defecto.

Ejemplo:

```text
BENCHMARK_SCORE → UNIVERSAL_SUPERIORITY
```

## BoundaryDecision

Decisión de frontera.

Valores:

```text
ALLOW
ALLOW_WITH_LIMITATIONS
BLOCK
HUMAN_REVIEW
```

## ContaminationGuard

Componente que impide transiciones inválidas y contaminación entre contextos.

## Trust Ledger

Registro persistente de claims, evidencias, decisiones, riesgos, costes y latencias.

## Representation

Output concreto de un modelo entendido como representación de uno o varios claims.

## Representation Consistency

Evaluación de si varios modelos representan el mismo claim de forma compatible.

Estados:

```text
EQUIVALENT
PARTIALLY_EQUIVALENT
CONTRADICTORY
DISJOINT
UNSUPPORTED_EXPANSION
```

## Model Epistemic Fingerprint

Huella de comportamiento de un modelo reconstruida desde sus outputs observables.

## Trust Router

Producto inicial que enruta outputs de modelos a través del sistema de claims, sectores, evidence bridges y ledger.

## Human Review

Salida legítima cuando un conflicto no puede resolverse de forma determinista sin riesgo.

## Overblocking

The failure mode where a trust gate blocks too many useful, low-risk, exploratory, or normal outputs.

## Safe Admissibility

The principle that a claim should be admitted when it can be safely scoped, limited, supported, or downgraded.

## Usefulness Preservation

A policy that attempts to preserve useful model output while preventing epistemic contamination.

## Downgrade-Before-Block

The rule that Xendris should attempt to convert overstrong claims into weaker admissible claims before blocking, unless the claim is high-risk or a hard forbidden transition.

## Allow As Hypothesis

A decision state for exploratory, speculative, or design-oriented claims that are useful but not verified factual knowledge.

## False Positive Block

A case where Xendris blocks a claim that should have been allowed, limited, or treated as hypothesis.

## Hard Forbidden Transition

A transition that cannot be allowed by usefulness preservation, such as BENCHMARK -> UNIVERSAL_SUPERIORITY or DRY_RUN_LATENCY -> PRODUCTION_LATENCY without evidence.

## Scoped Claim

A claim restricted explicitly to a specific context (v.g. local simulation, closed dataset).

## Limited Claim

A claim admitted under restricted conditions with explicit limitations recorded in metadata.

## Normal Control Pass Rate

The proportion of normal control claims correctly allowed without blocking.

## Useful Answer Preservation Rate

The rate at which useful but partially unsupported outputs are preserved (e.g. downgraded or limited) rather than blocked.

