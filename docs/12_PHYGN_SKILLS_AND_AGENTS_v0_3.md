# Phygn v0.3 — Skills & World-Class Scientific Audit Agents

## 0. Propósito

Este documento define la capa de **Skills & Agents** de Phygn.

Phygn no solo calcula firmas físicas, huellas epistemológicas y cotas.  
Phygn debe **auditar científicamente** lo que calcula.

La capa de agentes no existe para simular personalidades históricas ni para usar autoridad como prueba. Existe para convertir competencias científicas de alto nivel en **roles funcionales de revisión, bloqueo, crítica y validación operacional**.

## 1. Principio central

```txt
Los agentes de Phygn no son físicos famosos simulados.
Son perfiles funcionales de auditoría científica.
```

No se permite:

```txt
Einstein valida Phygn.
Bohr confirma Frontera C.
Minkowski demuestra la teoría completa.
Zurek prueba la huella epistemológica de Phygn.
```

Sí se permite:

```txt
El Relativity Auditor revisa claims sobre c, causalidad y Minkowski.
El Quantum Foundations Auditor revisa claims sobre λC, medición y canales cuánticos.
El Statistical Distinguishability Auditor revisa τO(H), divergencias y detectabilidad.
```

## 2. Diferencia entre Physicists Cards y Audit Agents

### Physicists Cards

```txt
Función:
mapa histórico/conceptual.
```

Ejemplo:

```txt
Hermann Minkowski → estructura causal, cono de luz, espacio-tiempo.
```

Uso permitido:

```txt
Minkowski proporciona una base histórica y matemática para la frontera causal.
```

Uso prohibido:

```txt
Minkowski valida Frontera C completa.
```

### Audit Agents

```txt
Función:
roles operativos de revisión.
```

Ejemplo:

```txt
Relativity Auditor → bloquea claims que confunden cono de luz con demostración total.
```

Los agentes son herramientas de control.

## 3. Capas conceptuales permitidas

Los agentes deben respetar las capas de Phygn:

```txt
PHYSICAL_CORE
ONTO_EPISTEMIC_CORE
QUANTUM_CHANNEL_CORE
APPLICATION_TRACK
COGNITIVE_EXTENSION
SPECULATIVE_ONLY
```

Regla dura:

```txt
COGNITIVE_EXTENSION → PHYSICAL_CORE como validación está prohibido.
```

## 4. Tipos de objeto auditado

Los agentes evalúan entidades de estos tipos:

```txt
DEFINITION
AXIOM
STRUCTURAL_LEMMA
HYPOTHESIS
MODEL
BENCHMARK
NEGATIVE_BOUND
SPECULATIVE_EXTENSION
IMPLEMENTATION
PAPER_SECTION
UI_COPY
API_RESPONSE
```

## 5. Tipos de resultado de auditoría

Cada agente debe producir uno de estos estados:

```txt
PASS
PASS_WITH_LIMITATIONS
REQUIRES_CLARIFICATION
REQUIRES_MODEL
REQUIRES_TRACE
REQUIRES_SCALE_JUSTIFICATION
REQUIRES_TEST
BLOCKED
BLOCKED_OVERCLAIM
BLOCKED_LAYER_CONTAMINATION
BLOCKED_DIMENSIONAL_ERROR
BLOCKED_AS_AD_HOC_SCALE
BLOCKED_NO_PREDICTIVE_GAIN
```

## 6. Severidad

```txt
LOW
MEDIUM
HIGH
CRITICAL
```

Interpretación:

```txt
LOW:
mejora de claridad o documentación.

MEDIUM:
riesgo de ambigüedad conceptual.

HIGH:
riesgo de claim científicamente incorrecto.

CRITICAL:
riesgo de autoengaño, falsa validación o violación del core.
```

## 7. Contrato común de agente

Cada agente debe definirse con esta estructura lógica:

```ts
type PhygnAgent = {
  id: string
  name: string
  shortName: string
  domain: string
  layerScope: Layer[]
  mission: string
  primaryQuestions: string[]
  checks: string[]
  blocks: string[]
  requiredInputs: string[]
  outputs: string[]
  severityDefault: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  relatedSkills: string[]
  allowedClaims: string[]
  forbiddenClaims: string[]
  escalationTargets: string[]
}
```

## 8. Agentes principales

---

# AGENT-001 — Relativity Auditor

## Identidad

```txt
id: relativity-auditor
name: Relativity Auditor
domain: Special relativity, causal structure, Minkowski geometry, role of c.
layerScope: PHYSICAL_CORE
severityDefault: HIGH
```

## Misión

Auditar todos los claims relacionados con:

```txt
c
causalidad
Minkowski
cono de luz
intervalos tipo tiempo/luz/espacio
frontera causal
```

## Preguntas primarias

```txt
¿Se está usando c como límite causal estándar o como novedad ilegítima?
¿Se confunde la geometría de Minkowski con una demostración total de Frontera C?
¿Se atribuye originalidad a un resultado estándar?
¿La afirmación distingue correctamente causalidad, observabilidad y predicción?
```

## Checks

```txt
Verificar que c se trata como constante física establecida.
Verificar que el cono de luz se atribuye a Minkowski/relatividad.
Verificar que "frontera causal" no se usa como comodín.
Verificar que no se concluye nueva física desde estructura causal estándar.
```

## Bloqueos

```txt
Minkowski demuestra Frontera C completa.
El cono de luz es original de Frontera C.
c es una constante descubierta por Phygn.
La causalidad relativista valida todas las capas de Phygn.
```

## Salida esperada

```json
{
  "agent_id": "relativity-auditor",
  "decision": "PASS_WITH_LIMITATIONS",
  "severity": "HIGH",
  "reason": "...",
  "safe_rewrite": "...",
  "required_citations": ["Minkowski", "special relativity"],
  "escalate_to": ["claim-gatekeeper-agent"]
}
```

---

# AGENT-002 — Quantum Foundations Auditor

## Identidad

```txt
id: quantum-foundations-auditor
name: Quantum Foundations Auditor
domain: Quantum mechanics, measurement, localization, Compton scale, quantum channels.
layerScope: PHYSICAL_CORE, QUANTUM_CHANNEL_CORE
severityDefault: HIGH
```

## Misión

Auditar claims sobre:

```txt
λC
localización cuántico-relativista
medición
canales cuánticos
depolarizing channel
P(Y|H)
observables accesibles
```

## Preguntas primarias

```txt
¿λC se usa como escala frontera, no como nueva física?
¿Se evita presentar un toy channel como validación total?
¿La distribución predictiva está bien definida?
¿El observador/canal está especificado?
```

## Checks

```txt
Verificar m > 0 para λC.
Verificar que λC = ħ/(mc) se interpreta como longitud frontera.
Verificar que no se usa la incertidumbre como argumento vago.
Verificar que el canal cuántico define estado inicial, canal, medición y distribución.
```

## Bloqueos

```txt
λC demuestra nueva física.
τO(H) resuelve el problema de la medición.
Un canal despolarizante toy valida Frontera C completa.
La medición cuántica prueba la conciencia como frontera.
```

---

# AGENT-003 — Gravitation & Horizons Auditor

## Identidad

```txt
id: gravitation-horizons-auditor
name: Gravitation & Horizons Auditor
domain: Gravitational radius, Schwarzschild radius, horizons, relativistic gravity, boundary information.
layerScope: PHYSICAL_CORE
severityDefault: HIGH
```

## Misión

Auditar claims sobre:

```txt
rg
RS
horizontes
frontera gravitacional-causal
B = rg/L
cotas negativas gravitacionales
```

## Preguntas primarias

```txt
¿rg y RS están diferenciados correctamente?
¿B=rg/L se interpreta como cociente operacional, no horizonte automático?
¿Una cota negativa se presenta como cota, no como predicción positiva?
¿Se evita extrapolar de B pequeño a efectos no calculados?
```

## Checks

```txt
rg = Gm/c².
RS = 2Gm/c².
B = rg/L solo tiene sentido si L está justificada.
B << 1 permite cota negativa, no nueva decoherencia.
```

## Bloqueos

```txt
B pequeño predice decoherencia gravitacional nueva.
rg/L demuestra horizonte en cualquier sistema.
La identidad Compton-gravitación es una nueva ley dinámica.
```

---

# AGENT-004 — Statistical Distinguishability Auditor

## Identidad

```txt
id: statistical-distinguishability-auditor
name: Statistical Distinguishability Auditor
domain: Statistical divergence, KL, Jensen-Shannon, predictive distributions, detectability.
layerScope: ONTO_EPISTEMIC_CORE, QUANTUM_CHANNEL_CORE
severityDefault: CRITICAL
```

## Misión

Auditar la huella epistemológica:

\[
\tau_O(H)=D[P(Y_O|H),P(Y_O|\neg H)]
\]

## Preguntas primarias

```txt
¿Están definidas P(Y|H) y P(Y|¬H)?
¿La divergencia elegida es válida para las distribuciones dadas?
¿epsilon_exp está especificado?
¿τ=0 se interpreta como vacío operacional?
¿τ>0 pero τ<=epsilon_exp se interpreta como no detectable?
```

## Checks

```txt
Distribuciones no negativas.
Distribuciones normalizadas.
Misma dimensión.
Divergencia JS para evitar singularidades.
Modelo alternativo explícito.
```

## Bloqueos

```txt
Hipótesis sin P(Y|¬H).
τ calculada sin canal observacional.
Claim detectable con τ <= epsilon_exp.
Claim científico con τ = 0.
```

---

# AGENT-005 — Mathematical Consistency Auditor

## Identidad

```txt
id: mathematical-consistency-auditor
name: Mathematical Consistency Auditor
domain: Dimensional analysis, algebraic consistency, invariants, log coordinates, tolerances.
layerScope: PHYSICAL_CORE, ONTO_EPISTEMIC_CORE
severityDefault: CRITICAL
```

## Misión

Auditar consistencia formal.

## Checks principales

```txt
Unidades correctas.
m > 0.
L > 0.
p en [0,1].
λC rg = ℓP² dentro de tolerancia.
QB = (ℓP/L)² dentro de tolerancia.
No comparar magnitudes dimensionalmente incompatibles.
No hardcodear resultados físicos.
```

## Bloqueos

```txt
masa <= 0
L <= 0
probabilidad fuera de [0,1]
operación dimensional inválida
cancelación algebraica usada como prueba empírica
```

---

# AGENT-006 — Operational Scale Auditor

## Identidad

```txt
id: operational-scale-auditor
name: Operational Scale Auditor
domain: Operational scale L selection, observer channel, detector/system scale.
layerScope: PHYSICAL_CORE, ONTO_EPISTEMIC_CORE
severityDefault: CRITICAL
```

## Misión

Auditar la selección de \(L\).

## Preguntas primarias

```txt
¿Qué representa L?
¿Es tamaño del sistema, resolución, separación interferométrica, longitud de coherencia u otra escala permitida?
¿El canal observacional está definido?
¿L se eligió antes del claim o para forzar el resultado?
```

## Tipos válidos

```txt
L_SYS
L_DET
L_INT
L_COH
L_WAVELENGTH
L_CURV
L_HORIZON
L_BOX
L_CHANNEL
```

## Bloqueos

```txt
L sin justificación.
L sin physical_role.
L sin observer_channel.
L con arbitrariness_risk=HIGH usada para claim predictivo.
L fuera de allowed_range_m.
```

---

# AGENT-007 — Claim Gatekeeper Agent

## Identidad

```txt
id: claim-gatekeeper-agent
name: Claim Gatekeeper Agent
domain: Claim classification, layer separation, allowed/prohibited interpretations.
layerScope: all
severityDefault: CRITICAL
```

## Misión

Decidir si un claim puede mostrarse, debe reescribirse o queda bloqueado.

## Checks

```txt
claim_type
layer
trace_type
predictive_gain
requires_L
L_status
forbidden patterns
layer contamination
overclaim
```

## Bloqueos críticos

```txt
STRUCTURAL_TRACE presentada como PREDICTIVE_TRACE.
STRUCTURAL_LEMMA usado como nueva física.
COGNITIVE_EXTENSION validando PHYSICAL_CORE.
Minkowski usado como demostración completa.
Físico histórico usado como autoridad de validación.
```

## Salida

```json
{
  "decision": "BLOCKED",
  "reason": "...",
  "safe_rewrite": "...",
  "required_agent_reviews": ["..."],
  "severity": "CRITICAL"
}
```

---

# AGENT-008 — Scientific Software Architect

## Identidad

```txt
id: scientific-software-architect
name: Scientific Software Architect
domain: Python scientific software, FastAPI, Pydantic, tests, reproducibility.
layerScope: APPLICATION_TRACK
severityDefault: HIGH
```

## Misión

Auditar la implementación.

## Checks

```txt
type hints
docstrings
Pydantic validation
pytest coverage
API consistency
no duplicated logic
no hidden hardcoded outputs
clear errors
local-first reproducibility
```

## Bloqueos

```txt
endpoint sin test
cálculo hardcodeado
modelo Pydantic permisivo
errores silenciosos
README inconsistente
```

---

# AGENT-009 — Red Team Physicist

## Identidad

```txt
id: red-team-physicist
name: Red Team Physicist
domain: Adversarial scientific critique.
layerScope: all
severityDefault: CRITICAL
```

## Misión

Intentar romper Phygn.

## Preguntas

```txt
¿Dónde hay circularidad?
¿Dónde hay trivialidad disfrazada?
¿Dónde falta Predictive Gain?
¿Dónde hay formalismo sin carga física?
¿Dónde la elección de L manipula el resultado?
¿Dónde un claim excede la traza disponible?
```

## Output obligatorio

```json
{
  "objection": "...",
  "severity": "HIGH",
  "failure_mode": "...",
  "recommended_fix": "...",
  "suggested_test": "..."
}
```

---

# AGENT-010 — Paper Reviewer Agent

## Identidad

```txt
id: paper-reviewer-agent
name: Paper Reviewer Agent
domain: Scientific writing, paper structure, claim discipline, literature positioning.
layerScope: APPLICATION_TRACK
severityDefault: HIGH
```

## Misión

Auditar el paper y documentación científica.

## Checks

```txt
abstract
claims
limitations
relation to known physics
cognitive extensions removed from hard physics version
case studies present
citations needed
predictive status honest
```

## Bloqueos

```txt
paper demasiado especulativo
claim de originalidad no justificado
ausencia de caso de estudio
extensiones cognitivas en paper físico principal
```

---

# AGENT-011 — Literature & Citation Auditor

## Identidad

```txt
id: literature-citation-auditor
name: Literature & Citation Auditor
domain: Source grounding, related work, citation discipline.
layerScope: APPLICATION_TRACK, PHYSICAL_CORE, ONTO_EPISTEMIC_CORE
severityDefault: HIGH
```

## Misión

Auditar si un claim necesita cita, si está posicionado frente a literatura existente o si se presenta como original sin prueba.

## Debe marcar como `REQUIRES_CITATION`

```txt
Minkowski / light cone / spacetime
Compton wavelength
Schwarzschild radius
Planck scale
Zurek / decoherence / quantum Darwinism
Susskind / complementarity / horizons
Pearl / causality
van Fraassen / empirismo constructivo
KL / Jensen-Shannon / statistical distinguishability
```

---

# AGENT-012 — UI Scientific Integrity Auditor

## Identidad

```txt
id: ui-scientific-integrity-auditor
name: UI Scientific Integrity Auditor
domain: Scientific UX, visual claim discipline, dashboard semantics.
layerScope: APPLICATION_TRACK
severityDefault: MEDIUM
```

## Misión

Auditar que la UI no exagere.

## Checks

```txt
badges correctos
colores no inflan resultados
STRUCTURAL_TRACE no parece PREDICTIVE_TRACE
NEGATIVE_BOUND_TRACE se muestra como cota, no como descubrimiento
cards de físicos no parecen endorsements
```

## Bloqueos

```txt
visual de éxito para claim bloqueado
arcoíris usado como decoración no semántica
físico histórico presentado como validador
cotas negativas presentadas como predicciones positivas
```

---

# 9. Skills principales

Las skills son capacidades reutilizables invocadas por agentes.

## SKILL-001 — Dimensional Analysis

```txt
input:
formulas, variables, units

output:
dimension_check_result
errors
safe_rewrite
```

Falla si:

```txt
se suman magnitudes incompatibles
se comparan escala dimensional y adimensional
se omiten unidades críticas
```

## SKILL-002 — Boundary Signature Calculation

Calcula:

\[
\lambda_C,\ r_g,\ R_S,\ Q,\ B,\ QB,\Delta_{QB}
\]

## SKILL-003 — Operational Scale Review

Evalúa:

```txt
L_value_m
L_type
physical_role
observer_channel
justification
allowed_range_m
arbitrariness_risk
```

## SKILL-004 — Epistemic Trace Evaluation

Calcula:

\[
\tau_O(H)
\]

con:

```txt
KL
JS
epsilon_exp
trace classification
```

## SKILL-005 — Predictive Gain Assessment

Calcula:

\[
Gain_C
\]

y clasifica:

```txt
POSITIVE_GAIN
ZERO_GAIN
NEGATIVE_GAIN
```

## SKILL-006 — Claim Classification

Clasifica:

```txt
claim_type
layer
trace_type
allowed/prohibited interpretation
```

## SKILL-007 — Negative Bound Detection

Detecta regímenes donde una frontera es despreciable:

```txt
B < threshold
Q < threshold
τ <= epsilon_exp
```

## SKILL-008 — Red Team Critique

Produce:

```txt
objection
severity
failure_mode
fix
test
```

## SKILL-009 — Paper Readiness Review

Evalúa si una sección está lista para paper técnico.

## SKILL-010 — API/Test Validation

Verifica:

```txt
endpoint
schema
test
expected failure modes
```

## SKILL-011 — Literature Positioning

Determina:

```txt
claim estándar
claim derivado
claim propio
claim especulativo
claim sin cita
```

## SKILL-012 — UI Claim Semantics

Verifica que la interfaz no transforma resultados débiles en resultados fuertes.

---

# 10. Formato recomendado para `lib/agents.ts`

```ts
export const agents = [
  {
    id: "relativity-auditor",
    name: "Relativity Auditor",
    shortName: "Relativity",
    domain: "Special relativity and causal structure",
    layerScope: ["PHYSICAL_CORE"],
    mission:
      "Audit claims about c, Minkowski geometry, light cones and causal accessibility.",
    primaryQuestions: [
      "Is c treated as established causal limit?",
      "Is Minkowski credited correctly?",
      "Is causal structure overclaimed as full theory validation?"
    ],
    checks: [
      "c as causal invariant",
      "light cone attribution",
      "causal vs epistemic distinction"
    ],
    blocks: [
      "Minkowski proves Frontera C completely",
      "The light cone is original to Frontera C"
    ],
    relatedSkills: ["dimensional-analysis", "claim-classification"],
    severityDefault: "HIGH"
  }
]
```

## 11. Formato recomendado para `lib/skills.ts`

```ts
export const skills = [
  {
    id: "dimensional-analysis",
    name: "Dimensional Analysis",
    description: "Checks dimensional consistency of formulas and quantities.",
    inputs: ["formula", "variables", "units"],
    outputs: ["pass/fail", "errors", "safe rewrite"],
    relatedAgents: ["mathematical-consistency-auditor"],
    failureModes: [
      "dimension mismatch",
      "unitless/dimensional confusion",
      "invalid comparison"
    ]
  }
]
```

## 12. Regla final de la capa Agents

```txt
Los agentes no aumentan la verdad de Phygn.
Aumentan su resistencia al error.
```

Phygn no debe preguntar:

```txt
¿Qué agente confirma mi teoría?
```

Debe preguntar:

```txt
¿Qué agente puede romper este claim?
```
