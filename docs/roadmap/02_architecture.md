# 02 — Arquitectura objetivo

## Arquitectura general

```text
User Input
  ↓
Prompt Context Builder
  ↓
Model Provider / Multi-Model Selector
  ↓
Raw Model Output
  ↓
Claim Extraction
  ↓
Claim Algebra
  ↓
Local Claim Algebra
  ↓
Contamination Guard
  ↓
Usefulness Preservation Policy
  ↓
Sector Transition Engine
  ↓
Epistemic Microcausality Guard
  ↓
Benchmark / Runtime / Policy Gate
  ↓
Trust Ledger
  ↓
Final Answer / Block / Limited Answer / Human Review
```

## Paquetes objetivo

```text
xendris/
  core/
    trust/
    algebra/
    local/
    boundary/
    sectors/
    representations/
    ledger/
    router/
  agent/
  benchmarks/
    trust_traps/
    ablations/
    multimodel/
  providers/
    deepseek/
    kimi/
    qwen/
    openai/
    anthropic/
    google/
    local/
  reports/
  cli/
```

## Capas

### 1. Trust Kernel

Ya iniciado.

Responsable de:

- tipos de claims;
- estados;
- riesgos;
- decisiones;
- auditoría básica.

### 2. Claim Algebra

Nueva capa.

Responsable de convertir claims en objetos formales y aplicar operaciones deterministas:

```text
combine
restrict
support
contradict
downgrade
promote
block
escalate
```

### 3. Local Claim Algebras

Responsable de separar dominios:

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

### 4. Boundary / Epistemic Microcausality

Responsable de evitar contaminación entre contextos.

Regla:

```text
No claim may cross context boundary without an EvidenceBridge.
```

### 4b. UsefulnessPreservationPolicy

Nueva política de preservación de utilidad y anti-sobrebloqueo.

* **Ejecución**: Se ejecuta después del análisis de clasificación y del `ContaminationGuard`, antes del bloqueo final.
* **Responsabilidad**: Verifica si un claim que de otro modo sería bloqueado puede ser admitido de forma segura mediante su degradación, acotación o establecimiento de limitaciones.
* **Restricción absoluta**: Nunca anula transiciones prohibidas rígidas (hard forbidden transitions), nunca promueve claims de alto riesgo no soportados y nunca permite contaminación epistémica simplemente porque el output sea útil.
* **Invariante de seguridad**:
  > Usefulness preservation may soften BLOCK into ALLOW_WITH_LIMITATIONS or ALLOW_AS_HYPOTHESIS only when no forbidden transition, contradiction, or high-risk unsupported claim remains.
* **Orden de preferencia de decisiones**:
  1. `ALLOW`
  2. `ALLOW_WITH_LIMITATIONS`
  3. `ALLOW_AS_HYPOTHESIS` (o `ALLOW_WITH_LIMITATIONS` con la limitación `"hypothesis_only"` si no se soporta el enum extendido directamente en el kernel).
  4. `HUMAN_REVIEW`
  5. `BLOCK`

### 5. Sector Transition Engine

Responsable de validar transiciones entre sectores.

Ejemplo:

```text
USER_PROVIDED → FACTUAL
```

solo si existe evidencia válida.

### 6. Representation Consistency Gate

Responsable de comparar outputs de distintos modelos como representaciones de claims.

Estados:

```text
EQUIVALENT
PARTIALLY_EQUIVALENT
CONTRADICTORY
DISJOINT
UNSUPPORTED_EXPANSION
```

### 7. Trust Ledger

Responsable de persistir decisiones:

```text
claim_id
run_id
model_id
provider
prompt_hash
output_hash
claim_type
source_context
target_context
evidence_refs
decision
risk_level
transition_allowed
reason
latency_ms
cost_estimate
created_at
```

### 8. Model Epistemic Fingerprint

Responsable de reconstruir el perfil de cada modelo desde outputs observables.

Métricas:

```text
unsupported_claim_rate
false_truth_proxy_rate
universalization_rate
evidence_conflict_handling_rate
human_review_alignment
fallback_contamination_rate
latency_proxy_bias
cost_per_admissible_claim
tokens_per_verified_claim
sector_violation_rate
```

### 9. Multi-Model Selector

Responsable de elegir modelo según riesgo, coste y tipo de tarea.

Decisiones:

```text
use_cheap_model
use_strong_model
use_local_model
ask_two_models
require_tool_verification
block
human_review
```

### 10. Agentic Trust Runtime

Responsable de convertir Xendris en agente con verificación antes, durante y después de actuar.

```text
planner → model call → claim extraction → local algebra check → sector transition check → tool execution → ledger → final answer
```
