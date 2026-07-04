# 04 — Especificación v0.4: Local Claim Algebras

## Objetivo

Implementar `Xendris v0.4 Local Claim Algebras` como extensión determinista del Trust Kernel existente.

Esta fase debe introducir:

- objetos formales de claim;
- contextos locales;
- algebras locales de claims;
- puentes de evidencia;
- guardia de contaminación epistémica.

## Restricciones

No modificar salvo necesidad estricta:

```text
frontend/
providers/
benchmarks/datasets/
public APIs existentes
```

No actualizar documentación con conteos de tests inventados. Solo documentar resultados observados.

## Nuevos paquetes

```text
xendris/core/algebra/
    __init__.py
    claim_object.py
    claim_ops.py
    claim_set.py
    support.py
    transformations.py

xendris/core/local/
    __init__.py
    context.py
    local_algebra.py
    local_rules.py
    quasilocal_registry.py
    contamination.py

xendris/core/boundary/
    __init__.py
    evidence_bridge.py
    boundary_rule.py
    contamination_guard.py
    allowed_transitions.py
```

## ClaimObject

Objeto inmutable que envuelve o complementa la semántica existente de `Claim`.

Campos mínimos:

```text
claim_id: str
content: str
claim_type: ClaimType
claim_status: ClaimStatus
risk_level: RiskLevel
context: LocalContext
source: str | None
evidence_refs: tuple[str, ...]
metadata: Mapping[str, Any]
```

## LocalContext

Enum inicial:

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

Representa reglas locales de un contexto.

Campos:

```text
context: LocalContext
allowed_claim_types: frozenset[ClaimType]
allowed_outgoing_transitions: frozenset[TransitionRule]
blocked_outgoing_transitions: frozenset[TransitionRule]
default_risk: RiskLevel
```

## EvidenceBridge

Puente que permite mover un claim entre contextos o sectores.

Campos:

```text
bridge_type: EvidenceBridgeType
source_context: LocalContext
target_context: LocalContext
evidence_ref: str
confidence: float
metadata: Mapping[str, Any]
```

Tipos iniciales:

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

## ContaminationGuard

Función principal:

```text
assess_transition(
    source_claim,
    target_context,
    requested_target_claim_type,
    evidence_bridge=None,
) -> BoundaryDecision
```

Decisiones:

```text
ALLOW
ALLOW_WITH_LIMITATIONS
BLOCK
HUMAN_REVIEW
```

## Transiciones bloqueadas explícitas

```text
BENCHMARK -> UNIVERSAL_SUPERIORITY
LATENCY -> ACCURACY
USER_PROVIDED -> VERIFIED without evidence
CODE_STATE -> PRODUCTION_READY without tests/build/deployment evidence
DRY_RUN_LATENCY -> PRODUCTION_LATENCY without real measurement
BENCHMARK_SCORE -> GENERAL_MODEL_QUALITY without external validation
TESTS_PASSED -> BUSINESS_READY without deployment/commercial evidence
```

## Transiciones permitidas con límites

```text
BENCHMARK_SCORE -> LIMITED_BENCHMARK_CLAIM
requiere: BENCHMARK_ARTIFACT

USER_PROVIDED -> USER_ASSERTION
requiere: none

CODE_STATE -> VERIFIED_CODE_STATE
requiere: TEST_RESULT or BUILD_LOG

LATENCY_DRY_RUN -> SIMULATED_LATENCY_CLAIM
requiere: benchmark artifact or run metadata

RUNTIME_ERROR -> EXCLUDED_FROM_SCORING
requiere: runtime trace
```

## Usefulness Preservation Policy

“Before returning BLOCK, Xendris must evaluate whether the claim can be safely admitted as-is, admitted with limitations, downgraded to a hypothesis, scoped to a local context, or escalated to human review.”

### Decision Preference Order
1. **ALLOW**
2. **ALLOW_WITH_LIMITATIONS**
3. **ALLOW_AS_HYPOTHESIS** (o `ALLOW_WITH_LIMITATIONS` con la limitación `"hypothesis_only"` si no se soporta el enum extendido directamente en el kernel).
4. **HUMAN_REVIEW**
5. **BLOCK**

### Comportamiento por Tipo de Contenido
* **A. Claims Operacionales**:
  * Ejemplos: "This is proven.", "This is production-ready.", "This model is universally superior.", "The tests passed.", "The cost will be X.", "The system is secure."
  * Comportamiento: Requieren evidencia obligatoria. Si son de alto riesgo y no están soportados, se bloquean o se escalan a revisión humana.
* **B. Claims Exploratorios**:
  * Ejemplos: "This architecture could be useful.", "A reasonable hypothesis is...", "This may indicate...", "We could explore..."
  * Comportamiento: No se bloquean por defecto. Se admiten como hipótesis (`ALLOW_AS_HYPOTHESIS`) o con limitaciones.
* **C. Contenido Creativo o Explicativo**:
  * Ejemplos: nombres, pitches, explicaciones simplificadas, brainstorming, metáforas, borradores.
  * Comportamiento: Se admiten por defecto, a menos que introduzcan claims factuales no soportados de alto riesgo.
* **D. Claims de Benchmark**:
  * Comportamiento: Se admiten únicamente cuando se acotan explícitamente al dataset, versión, configuración de corrida, configuración de modelo y fecha. Se bloquea la universalización.
* **E. Claims de Código/Producción**:
  * Comportamiento: Requieren tests, resultados de compilación, trazas de ejecución o evidencia de despliegue.

### Ejemplos Prácticos
* **Ejemplo 1**:
  * *Claim de entrada*: "Xendris solves hallucinations."
  * *Decisión incorrecta*: `BLOCK` únicamente.
  * *Decisión preferida*: `ALLOW_WITH_LIMITATIONS` con claim corregido/limitado: "Xendris does not eliminate hallucinations, but can reduce hallucination contamination by preventing unsupported claims from being admitted as verified operational knowledge."
* **Ejemplo 2**:
  * *Claim de entrada*: "Xendris is universally superior to DeepSeek."
  * *Decisión preferida*: `BLOCK` o degradación (`DOWNGRADE`) según el contexto.
  * *Claim degradado admisible*: "Xendris outperformed DeepSeek Base in Trust Traps v0.1 under the closed deterministic rubric and configuration used in the run."
* **Ejemplo 3**:
  * *Claim de entrada*: "This architecture could become useful for benchmark governance."
  * *Decisión preferida*: `ALLOW_AS_HYPOTHESIS`.
* **Ejemplo 4**:
  * *Claim de entrada*: "Dry-run latency proves production performance."
  * *Decisión preferida*: `BLOCK`.
  * *Claim degradado admisible*: "Dry-run latency only indicates local simulated overhead and does not prove production latency."

## Criterio de aceptación

v0.4 está terminada cuando Xendris puede impedir automáticamente la contaminación insegura:

```text
benchmark_score → universal_quality_claim
dry_run_latency → production_latency_claim
tests_passed → production_ready_claim
user_says_true → factual_verified_claim
```

Y simultáneamente maximizar la admisibilidad segura, permitiendo con límites o degradando:

```text
benchmark_score + artifact → limited_benchmark_claim
code_state + tests/build → verified_code_state
runtime_error + trace → excluded_from_scoring
overstrong_hallucination_claim → limited_hallucination_reduction_claim
exploratory_hypothesis → allow_as_hypothesis
creative_explanation → allow
normal_control_claims → allow (sin sobrebloqueo)
```

