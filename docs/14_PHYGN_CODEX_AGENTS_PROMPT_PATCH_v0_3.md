# Codex Prompt Patch — Phygn Agents & Skills Layer

## Context

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

The project is:

```txt
Phygn — Physical Signatures Lab
```

A backend already exists. A frontend based on shadcn dashboard-01 may exist or is being built.  
You must now add the **Agents & Skills** layer.

Read first:

```txt
docs/12_PHYGN_SKILLS_AND_AGENTS_v0_3.md
docs/13_PHYGN_AGENT_WORKFLOWS_v0_3.md
```

Do not rewrite the whole project. Extend it.

---

# 1. Goal

Add a complete **Agents & Skills** section to Phygn.

This layer must expose:

```txt
scientific audit agents
reusable scientific skills
workflow orchestration maps
agent-to-skill relationships
claim/blocking philosophy
future deterministic orchestrator architecture
```

Important:

```txt
Agents are not simulated famous physicists.
Agents are functional scientific audit roles.
```

---

# 2. Documentation files

Ensure these docs exist:

```txt
docs/12_PHYGN_SKILLS_AND_AGENTS_v0_3.md
docs/13_PHYGN_AGENT_WORKFLOWS_v0_3.md
docs/14_PHYGN_CODEX_AGENTS_PROMPT_PATCH_v0_3.md
```

If they already exist, preserve user content and improve only where necessary.

---

# 3. Frontend additions

Add route:

```txt
frontend/app/agents/page.tsx
```

Add components:

```txt
frontend/components/phygn/AgentCard.tsx
frontend/components/phygn/SkillCard.tsx
frontend/components/phygn/WorkflowCard.tsx
frontend/components/phygn/AuditPipeline.tsx
frontend/components/phygn/AuditResultPanel.tsx
```

Add data files:

```txt
frontend/lib/agents.ts
frontend/lib/skills.ts
frontend/lib/workflows.ts
```

Update sidebar navigation to include:

```txt
Agents & Skills
```

Suggested icon:

```txt
Network
```

or:

```txt
BrainCircuit
```

But avoid making it look like cognitive validation. This is scientific audit orchestration.

---

# 4. Agent data

Create `frontend/lib/agents.ts`.

It must export at least these agents:

```txt
Relativity Auditor
Quantum Foundations Auditor
Gravitation & Horizons Auditor
Statistical Distinguishability Auditor
Mathematical Consistency Auditor
Operational Scale Auditor
Claim Gatekeeper Agent
Scientific Software Architect
Red Team Physicist
Paper Reviewer Agent
Literature & Citation Auditor
UI Scientific Integrity Auditor
```

Each agent object must include:

```ts
export type AgentSeverity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"

export type PhygnAgent = {
  id: string
  name: string
  shortName: string
  domain: string
  layerScope: string[]
  mission: string
  primaryQuestions: string[]
  checks: string[]
  blocks: string[]
  requiredInputs: string[]
  outputs: string[]
  severityDefault: AgentSeverity
  relatedSkills: string[]
  allowedClaims: string[]
  forbiddenClaims: string[]
  escalationTargets: string[]
}
```

Do not use real physicists as agents.  
Real physicists belong only in `/physicists` conceptual map.

---

# 5. Skills data

Create `frontend/lib/skills.ts`.

It must export at least:

```txt
Dimensional Analysis
Boundary Signature Calculation
Operational Scale Review
Epistemic Trace Evaluation
Predictive Gain Assessment
Claim Classification
Negative Bound Detection
Red Team Critique
Paper Readiness Review
API/Test Validation
Literature Positioning
UI Claim Semantics
```

Each skill object:

```ts
export type PhygnSkill = {
  id: string
  name: string
  description: string
  inputs: string[]
  outputs: string[]
  relatedAgents: string[]
  failureModes: string[]
}
```

---

# 6. Workflows data

Create `frontend/lib/workflows.ts`.

It must export these workflows:

```txt
Formula Integrity Review
Operational Scale Gate
Boundary Signature Review
Epistemic Trace Review
Predictive Gain Review
Claim Gatekeeper Review
Case Study Audit
Paper Readiness Review
UI Scientific Integrity Review
```

Each workflow:

```ts
export type PhygnWorkflow = {
  id: string
  name: string
  objective: string
  inputTypes: string[]
  agents: string[]
  gates: string[]
  output: string[]
  blocks: string[]
}
```

---

# 7. Agents page design

The `/agents` page must include:

## Hero

```txt
Agents & Skills
Functional scientific auditors for Phygn.
```

Subtext:

```txt
These agents do not validate Phygn by authority. They audit formulas, claims, traces, scales, case studies, UI copy and paper sections.
```

## Section 1 — Audit Agents

Grid of `AgentCard`.

Each card shows:

```txt
name
domain
mission
severityDefault
layerScope
checks
blocks
relatedSkills
```

## Section 2 — Scientific Skills

Grid of `SkillCard`.

Each card shows:

```txt
name
description
inputs
outputs
failureModes
relatedAgents
```

## Section 3 — Orchestration Workflows

Grid/list of `WorkflowCard`.

Show:

```txt
workflow name
objective
agents
gates
output
blocks
```

## Section 4 — Audit Pipeline

Render a static pipeline:

```txt
Auditable Object
→ Agent Selection
→ Skill Plan
→ Agent Reviews
→ Aggregation
→ Decision
→ Safe Rewrite / Tests / Block
```

## Section 5 — Example Reviews

Include three example cards:

### Example 1

Input:

```txt
El invariante demuestra nueva física.
```

Expected:

```txt
BLOCKED_OVERCLAIM
```

Agents:

```txt
Mathematical Consistency Auditor
Claim Gatekeeper Agent
Red Team Physicist
```

Safe rewrite:

```txt
El invariante es un lema estructural de consistencia, no una prueba de nueva física.
```

### Example 2

Input:

```txt
L = 1e-7 m without justification.
```

Expected:

```txt
BLOCKED_AS_AD_HOC_SCALE
```

Agents:

```txt
Operational Scale Auditor
Claim Gatekeeper Agent
```

### Example 3

Input:

```txt
τ = 0 but claim says detectable.
```

Expected:

```txt
BLOCKED_NO_EMPIRICAL_OR_PREDICTIVE_TRACE
```

Agents:

```txt
Statistical Distinguishability Auditor
Claim Gatekeeper Agent
```

---

# 8. Sidebar update

Find the sidebar from dashboard-01 and add:

```txt
Agents & Skills
```

Suggested route:

```txt
/agents
```

Suggested icon:

```tsx
Network
```

or:

```tsx
BrainCircuit
```

Use `Network` if avoiding cognitive association.

---

# 9. Dashboard card

Add dashboard card:

```txt
World-Class Audit Agents
```

Description:

```txt
Functional scientific reviewers for claims, traces, scales and boundary calculations.
```

Metric:

```txt
12 agents
12 skills
9 workflows
```

CTA:

```txt
Open Agents & Skills
```

---

# 10. Docs page update

Add links to:

```txt
12_PHYGN_SKILLS_AND_AGENTS_v0_3.md
13_PHYGN_AGENT_WORKFLOWS_v0_3.md
14_PHYGN_CODEX_AGENTS_PROMPT_PATCH_v0_3.md
```

---

# 11. Scientific integrity rules

Do not write:

```txt
Einstein agent
Bohr agent
Planck agent
These agents prove Phygn
World-class physicists validate the theory
```

Write instead:

```txt
Functional scientific auditors
World-class review roles
Audit agents
Scientific skill system
Claim resistance layer
```

---

# 12. Future backend architecture note

Do not implement backend LLM orchestration yet unless asked.

But document future modules:

```txt
phyng/agents.py
phyng/skills.py
phyng/orchestrator.py
phyng/audit_schemas.py
```

and future endpoints:

```txt
GET /agents
GET /skills
GET /workflows
POST /audit/claim
POST /audit/signature
POST /audit/case-study
POST /audit/paper-section
```

---

# 13. Acceptance criteria

The task is complete when:

```txt
/agents page exists
sidebar includes Agents & Skills
lib/agents.ts exports 12 agents
lib/skills.ts exports 12 skills
lib/workflows.ts exports 9 workflows
AgentCard works
SkillCard works
WorkflowCard works
AuditPipeline works
Dashboard has World-Class Audit Agents card
Docs page links docs 12, 13, 14
No fake famous-physicist agents are created
No authority-based validation language appears
```

---

# 14. Final principle

Phygn agents do not make the framework true.

They make false confidence harder.

```txt
An agent does not validate a claim.
An agent audits the claim.
```
