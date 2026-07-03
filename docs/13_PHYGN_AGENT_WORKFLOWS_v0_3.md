# Phygn v0.3 — Agent Workflows & Orchestration

## 0. Propósito

Este documento define la orquestación de agentes y skills en Phygn.

La meta no es crear personajes conversacionales.  
La meta es construir una **arquitectura de revisión científica funcional**.

Phygn debe poder tomar un objeto:

```txt
claim
formula
signature
scale L
trace calculation
case study
paper section
UI copy
API response
```

y enviarlo por una cadena de auditoría adecuada.

## 1. Principio de orquestación

```txt
Cada claim debe ser revisado por el agente mínimo necesario.
Cada claim fuerte debe pasar por agentes adversariales.
Cada claim físico debe pasar por consistencia matemática.
Cada claim predictivo debe pasar por huella o gain.
```

## 2. Objetos auditables

```ts
type AuditableObject =
  | FormulaAudit
  | ClaimAudit
  | ScaleAudit
  | TraceAudit
  | SignatureAudit
  | CaseStudyAudit
  | PaperSectionAudit
  | UIMessageAudit
  | APIResponseAudit
```

## 3. Contrato universal de auditoría

```ts
type AuditRequest = {
  id: string
  objectType:
    | "FORMULA"
    | "CLAIM"
    | "SCALE"
    | "TRACE"
    | "SIGNATURE"
    | "CASE_STUDY"
    | "PAPER_SECTION"
    | "UI_COPY"
    | "API_RESPONSE"

  content: unknown

  declaredLayer?: Layer
  declaredClaimType?: ClaimType
  declaredTraceType?: TraceType

  context?: {
    system?: string
    observer?: string
    channel?: string
    scale?: OperationalScale
    modelBase?: string
    modelCandidate?: string
    citations?: string[]
  }

  requestedOutcome?: "review" | "block" | "rewrite" | "benchmark" | "paper-ready"
}
```

## 4. Respuesta universal de auditoría

```ts
type AuditResult = {
  requestId: string
  agentId: string
  decision:
    | "PASS"
    | "PASS_WITH_LIMITATIONS"
    | "REQUIRES_CLARIFICATION"
    | "REQUIRES_MODEL"
    | "REQUIRES_TRACE"
    | "REQUIRES_SCALE_JUSTIFICATION"
    | "REQUIRES_TEST"
    | "REQUIRES_CITATION"
    | "BLOCKED"
    | "BLOCKED_OVERCLAIM"
    | "BLOCKED_LAYER_CONTAMINATION"
    | "BLOCKED_DIMENSIONAL_ERROR"
    | "BLOCKED_AS_AD_HOC_SCALE"
    | "BLOCKED_NO_PREDICTIVE_GAIN"

  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"

  reason: string
  safeRewrite?: string
  requiredActions?: string[]
  suggestedTests?: string[]
  escalationTargets?: string[]
  relatedSkills?: string[]
}
```

## 5. Orchestrator

Crear conceptualmente:

```txt
AgentOrchestrator
```

Responsabilidad:

```txt
recibir un auditable object
seleccionar agentes
ejecutar skills
fusionar resultados
decidir estado final
producir recomendaciones
```

## 6. Pseudocódigo

```ts
function orchestrateAudit(request: AuditRequest): OrchestratedAuditResult {
  const agents = selectAgents(request)
  const skillPlan = buildSkillPlan(request, agents)

  const results = []

  for (const agent of agents) {
    const result = runAgentReview(agent, request, skillPlan)
    results.push(result)

    if (result.severity === "CRITICAL" && result.decision.startsWith("BLOCKED")) {
      break
    }
  }

  return aggregateAuditResults(results)
}
```

## 7. Selección de agentes

### Si objeto es FORMULA

Ejecutar:

```txt
Mathematical Consistency Auditor
```

Si aparecen \(c\), Minkowski, cono de luz:

```txt
Relativity Auditor
```

Si aparecen \(\lambda_C\), \(\hbar\), medición:

```txt
Quantum Foundations Auditor
```

Si aparecen \(G\), \(r_g\), \(R_S\), horizonte:

```txt
Gravitation & Horizons Auditor
```

### Si objeto es SCALE

Ejecutar:

```txt
Operational Scale Auditor
Mathematical Consistency Auditor
Claim Gatekeeper Agent
```

### Si objeto es TRACE

Ejecutar:

```txt
Statistical Distinguishability Auditor
Mathematical Consistency Auditor
Claim Gatekeeper Agent
```

### Si objeto es CLAIM

Seleccionar según contenido:

```txt
"c", "Minkowski", "light cone" → Relativity Auditor
"λC", "Compton", "measurement", "quantum" → Quantum Foundations Auditor
"rg", "Schwarzschild", "horizon", "gravity" → Gravitation & Horizons Auditor
"τ", "distribution", "KL", "JS", "detectable" → Statistical Distinguishability Auditor
"L", "scale", "Q/B" → Operational Scale Auditor
"new physics", "demonstrates", "proves" → Claim Gatekeeper + Red Team
```

Siempre ejecutar:

```txt
Claim Gatekeeper Agent
```

para claims de usuario.

### Si objeto es CASE_STUDY

Ejecutar:

```txt
Mathematical Consistency Auditor
Operational Scale Auditor
Statistical Distinguishability Auditor si hay τ
Scientific Software Architect
Red Team Physicist
Claim Gatekeeper Agent
```

### Si objeto es PAPER_SECTION

Ejecutar:

```txt
Paper Reviewer Agent
Literature & Citation Auditor
Claim Gatekeeper Agent
Red Team Physicist
```

### Si objeto es UI_COPY

Ejecutar:

```txt
UI Scientific Integrity Auditor
Claim Gatekeeper Agent
```

## 8. Workflows principales

---

# WORKFLOW-001 — Formula Integrity Review

## Entrada

```txt
formula
variables
units
claimed_interpretation
```

## Agentes

```txt
Mathematical Consistency Auditor
Relevant physics auditor
Claim Gatekeeper Agent
```

## Ejemplo

Formula:

\[
\lambda_C r_g = \ell_P^2
\]

Resultado esperado:

```txt
PASS as STRUCTURAL_LEMMA
BLOCK if used as proof of new physics
```

## Output

```json
{
  "workflow": "formula-integrity-review",
  "finalDecision": "PASS_WITH_LIMITATIONS",
  "classification": "STRUCTURAL_LEMMA",
  "traceType": "STRUCTURAL_TRACE",
  "safeInterpretation": "Consistency lemma only",
  "blockedInterpretations": ["Proof of new physics"]
}
```

---

# WORKFLOW-002 — Operational Scale Gate

## Entrada

```txt
L_value_m
L_type
physical_role
observer_channel
justification
allowed_range_m
arbitrariness_risk
```

## Agentes

```txt
Operational Scale Auditor
Mathematical Consistency Auditor
Claim Gatekeeper Agent
```

## Gating

```txt
ACCEPTED → signature can support limited claims
REQUIRES_JUSTIFICATION → calculate but block predictive claims
REJECTED → block claim
```

## Output

```json
{
  "workflow": "operational-scale-gate",
  "scaleStatus": "ACCEPTED",
  "canSupportPredictiveClaims": true,
  "limitations": ["Scale is operational, not absolute invariant"]
}
```

---

# WORKFLOW-003 — Boundary Signature Review

## Entrada

```txt
m
L
lambda_C
rg
Q
B
QB
delta_QB
scaleReview
```

## Agentes

```txt
Mathematical Consistency Auditor
Operational Scale Auditor
Quantum Foundations Auditor
Gravitation & Horizons Auditor
Claim Gatekeeper Agent
```

## Gating

```txt
delta_QB invalid → BLOCKED_DIMENSIONAL_ERROR or implementation error
L rejected → BLOCKED_AS_AD_HOC_SCALE
B below threshold → NEGATIVE_BOUND_TRACE
Q/B valid only → STRUCTURAL_TRACE
```

## Output

```json
{
  "workflow": "boundary-signature-review",
  "finalDecision": "PASS_WITH_LIMITATIONS",
  "traceType": "NEGATIVE_BOUND_TRACE",
  "allowedClaim": "Direct gravitational boundary contribution is negligible in this regime.",
  "blockedClaim": "Phygn predicts new gravitational decoherence."
}
```

---

# WORKFLOW-004 — Epistemic Trace Review

## Entrada

```txt
H
not_H
P(Y|H)
P(Y|not_H)
D
epsilon_exp
tau
```

## Agentes

```txt
Statistical Distinguishability Auditor
Mathematical Consistency Auditor
Claim Gatekeeper Agent
```

## Gating

```txt
missing P(Y|not_H) → REQUIRES_MODEL
invalid distributions → BLOCKED_DIMENSIONAL_ERROR
tau = 0 → NULL_TRACE
0 < tau <= epsilon_exp → NOT_DETECTABLE
tau > epsilon_exp → DETECTABLE_TRACE
```

## Output

```json
{
  "workflow": "epistemic-trace-review",
  "tau": 0.012,
  "traceType": "DETECTABLE_TRACE",
  "allowedClaim": "The hypotheses are distinguishable in this channel.",
  "blockedClaim": "This validates the entire Frontera C framework."
}
```

---

# WORKFLOW-005 — Predictive Gain Review

## Entrada

```txt
Error(M_base)
Error(M_C)
Gain_C
system
dataset or simulation
```

## Agentes

```txt
Statistical Distinguishability Auditor
Scientific Software Architect
Red Team Physicist
Claim Gatekeeper Agent
```

## Gating

```txt
Gain_C > 0 → POSITIVE_GAIN
Gain_C = 0 → ZERO_GAIN
Gain_C < 0 → NEGATIVE_GAIN
```

## Reglas

```txt
Positive gain in a toy model cannot validate full theory.
Zero gain must be reported without spin.
Negative gain must be reported as failure.
```

---

# WORKFLOW-006 — Claim Gatekeeper Review

## Entrada

```txt
claim text
claim_type
layer
trace_type
predictive_gain
requires_L
L_status
```

## Agentes

```txt
Claim Gatekeeper Agent
Red Team Physicist if strong claim
Relevant domain auditor
```

## Gating

```txt
contains "demuestra nueva física" → high scrutiny
contains "valida Frontera C completa" → high scrutiny
contains cognitive validation of physics → layer contamination
```

## Output

```json
{
  "decision": "BLOCKED",
  "reason": "Structural lemma is being used as empirical proof.",
  "safeRewrite": "The invariant is a structural consistency lemma, not evidence of new physics."
}
```

---

# WORKFLOW-007 — Case Study Audit

## Entrada

```txt
case_id
system
inputs
formulas
outputs
claims
limitations
tests
```

## Agentes

```txt
Mathematical Consistency Auditor
Operational Scale Auditor
Relevant physics auditors
Statistical Distinguishability Auditor if trace
Scientific Software Architect
Red Team Physicist
Paper Reviewer Agent
```

## Gating

A case study is publishable only if:

```txt
inputs explicit
L justified
formulas shown
outputs reproducible
claims limited
failure modes listed
tests pass
```

## Output

```json
{
  "caseStudyStatus": "PAPER_READY_WITH_LIMITATIONS",
  "missing": [],
  "claimsAllowed": ["..."],
  "claimsBlocked": ["..."],
  "recommendedNextCase": "..."
}
```

---

# WORKFLOW-008 — Paper Readiness Review

## Entrada

```txt
section
abstract
claims
figures
formulas
case studies
limitations
citations
```

## Agentes

```txt
Paper Reviewer Agent
Literature & Citation Auditor
Red Team Physicist
Claim Gatekeeper Agent
```

## Gating

```txt
No case study → not paper-ready for physics audience
No citations for standard physics → requires citation
Cognitive extensions in hard physics paper → move to appendix/external document
Overclaim → blocked
```

## Output

```json
{
  "paperReadiness": "NOT_READY|READY_WITH_LIMITATIONS|READY",
  "requiredChanges": ["..."],
  "sectionsToMove": ["..."],
  "claimsToRewrite": ["..."]
}
```

---

# WORKFLOW-009 — UI Scientific Integrity Review

## Entrada

```txt
page
component
copy
badge
color
metric
claim
```

## Agentes

```txt
UI Scientific Integrity Auditor
Claim Gatekeeper Agent
```

## Checks

```txt
Does the UI imply success where result is limited?
Does color exaggerate?
Does card copy overclaim?
Do physicists appear as endorsers?
Is a negative bound visually shown as discovery?
```

## Output

```json
{
  "uiIntegrity": "PASS_WITH_LIMITATIONS",
  "copyFixes": ["..."],
  "badgeFixes": ["..."]
}
```

---

# 9. Aggregation logic

## Severity aggregation

```txt
If any CRITICAL BLOCKED → final BLOCKED
If any HIGH REQUIRES_* → final REQUIRES_ACTION
If all PASS/PASS_WITH_LIMITATIONS → final PASS_WITH_LIMITATIONS or PASS
```

## Decision priority

```txt
BLOCKED_LAYER_CONTAMINATION
BLOCKED_OVERCLAIM
BLOCKED_DIMENSIONAL_ERROR
BLOCKED_AS_AD_HOC_SCALE
REQUIRES_MODEL
REQUIRES_TRACE
REQUIRES_SCALE_JUSTIFICATION
REQUIRES_TEST
REQUIRES_CITATION
PASS_WITH_LIMITATIONS
PASS
```

## Final result schema

```ts
type OrchestratedAuditResult = {
  id: string
  finalDecision: string
  maxSeverity: string
  agentResults: AuditResult[]
  allowedClaims: string[]
  blockedClaims: string[]
  requiredActions: string[]
  suggestedTests: string[]
  safeSummary: string
}
```

## 10. Frontend representation

Add page:

```txt
/agents
```

Sections:

```txt
Agent grid
Skill grid
Workflow map
Audit pipeline diagram
Example: invariant review
Example: Q/B signature review
Example: claim blocked
```

Components:

```txt
AgentCard
SkillCard
WorkflowCard
AuditPipeline
AuditResultPanel
```

## 11. Backend future extension

Phase v0.3:

```txt
agents are static structured knowledge + UI + docs.
```

Phase v0.4:

```txt
implement deterministic rule-based agent orchestrator.
```

Suggested backend modules:

```txt
phyng/agents.py
phyng/skills.py
phyng/orchestrator.py
phyng/audit_schemas.py
```

Future endpoints:

```txt
GET /agents
GET /skills
GET /workflows
POST /audit/claim
POST /audit/signature
POST /audit/case-study
POST /audit/paper-section
```

## 12. No-LLM rule for v0.3

For v0.3:

```txt
Do not connect external LLMs.
Do not simulate conversations.
Do not create fake Einstein/Bohr personas.
```

The agents are:

```txt
structured scientific audit roles
```

not:

```txt
chatbot personalities
```

## 13. Final principle

```txt
An agent does not make a claim true.
An agent makes a claim harder to fake.
```
