# Xendris Product Goal - Cognitive Certainty Membrane for AI

Date: 2026-07-06
Status: Product goal / north star / convergence roadmap

## Purpose

This document defines the product direction for Xendris as an epistemic trust
runtime for AI systems.

The central thesis is:

```txt
Model providers provide compute.
Xendris provides admissibility.
```

Xendris should not compete as another foundation model or as a thin provider
wrapper. Its product space is the boundary between generated text and admitted
operational knowledge.

## Definition

Xendris is an epistemic trust runtime for AI agents, model outputs, and
benchmark evidence.

It evaluates whether an AI output may be treated as:

- an admitted fact;
- a limited inference;
- a calculation;
- a hypothesis;
- a creative output;
- a useful but unverified answer;
- a blocked claim;
- a case requiring human review.

Xendris does not make every output true. It prevents useful, persuasive, cheap,
or fluent outputs from crossing the boundary as certainty without evidence,
scope, and admission.

## Foundational Principle

Frontera C is the cognitive-certainty membrane:

```txt
No output crosses as cognitive certainty without evidence, context, and
admission.
```

Frontera C applies to individual claims. Frontera C Mayor applies to the whole
representation frame that produces those claims.

Operational rule:

```txt
Every local certainty must declare its frame.
No local frame may pose as total certainty.
```

Direct consequences:

- a local benchmark cannot become universal superiority;
- a dry-run cannot become real-provider performance;
- a convincing answer cannot become truth;
- user validation cannot become evidence;
- a useful interface cannot become cognitive certainty.

## Product Positioning

```txt
OpenRouter routes model calls.
Vercel AI SDK helps build AI applications.
Xendris governs what model outputs may become operational knowledge.
```

Public safe formula:

```txt
Xendris does not make AI true.
Xendris prevents unsupported outputs from being treated as admitted operational
knowledge.
```

## Non-Claims

Xendris must not claim:

- hallucination elimination;
- universal model superiority;
- cheap models becoming frontier models in general;
- production readiness without deployment evidence;
- universal security;
- direct scientific validation from AQFT, Hoffman, or Frontera C;
- benchmark gains beyond the evaluated dataset, provider, and configuration.

Allowed conservative claims, when supported locally:

- Xendris reduces admission of unsupported claims under specific benchmarks;
- Xendris blocks or limits overclaims in closed datasets;
- Xendris improves response discipline in evaluated scenarios;
- Xendris audits benchmark-local evidence;
- Xendris can reduce cost by avoiding unjustified escalation;
- Xendris preserves useful outputs as hypotheses when they should not pass as
  certainty.

## Current Public Baseline

Current package/API version:

```txt
0.2.0
```

Stable public import surface:

- `xendris`
- `xendris.frontera_c`
- `xendris.core.rag`
- `xendris.core.response_contract`

Experimental layers exist under `xendris.core.trust`, `xendris.core.runtime`,
`xendris.core.algebra`, `xendris.core.boundary`, `xendris.core.local`,
`xendris.core.sectors`, `xendris.core.router`, `xendris.core.fingerprints`,
`xendris.core.ledger`, and `xendris.core.representations`.

These experimental layers must not be promoted to stable API without explicit
API audit.

## Evidence System Principle

Benchmark gains are not merely generated. They are admitted, rejected, or
constrained by explicit evidence gates.

Required evidence pipeline:

```txt
runner
-> summary/report
-> excellence gate
-> suite audit
-> evidence registry
-> public claim policy
```

Only admitted artifacts may support public benchmark claims. Rejected artifacts
may remain for history, but cannot be used as strong evidence.

## Target Product Surfaces

Xendris should converge into four product surfaces.

### Xendris Framework

Python framework for:

- response contracts;
- claim evaluation;
- evidence gates;
- benchmark governance;
- deterministic trust checks;
- release and evidence policy.

### Xendris Runtime API

API for governed AI execution:

```txt
GET  /v1/health
POST /v1/runtime/execute
POST /v1/claims/evaluate
POST /v1/routes/select
POST /v1/representations/compare
GET  /v1/ledger/runs/{run_id}
POST /v1/sandbox/provider-call
```

Primary modes:

```txt
Full Runtime Mode:
client -> Xendris -> provider -> gates -> ledger -> response

External Gate Mode:
client output -> Xendris gates -> audit decision
```

### Xendris Agent

User-facing agent:

```txt
One agent. All models. Trust-routed.
```

Capabilities should include model routing, visible trust decisions, cost
explanation, ledger per conversation, and future local-model support.

### Xendris Dashboard

Dashboard for:

- prepaid balance;
- provider spend;
- Xendris margin;
- cost per admissible answer;
- claims blocked or limited;
- model routing;
- human review rate;
- evidence registry;
- trust ledger.

## Core Metric

The central product metric is not token price or raw speed:

```txt
cost_per_admissible_answer = total_ai_cost / admitted_or_limited_answers
```

Related metrics:

- cost per admitted claim;
- latency per admissible answer;
- premium model avoidance rate;
- local guard resolution rate;
- trust cache hit rate;
- blocked overclaim rate;
- hypothesis preservation rate.

## Execution Architecture Target

Ideal flow:

```txt
User/App
  -> Xendris API / Agent UI
    -> Runtime Policy
      -> Risk Classification
      -> Epistemic Frame Detection
      -> Model Selector
      -> Provider Sandbox
      -> Model Call or Local Model
      -> Claim Extraction
      -> Local Guards
      -> Evidence Bridge
      -> Sector Transition Engine
      -> Representation Consistency Gate
      -> SycophancyGuard
      -> Adaptive Council Policy
      -> Trust Ledger
      -> Billing Meter
      -> Response Renderer
```

Cost principle:

```txt
Use local CPU first.
Use cheap models when sufficient.
Use frontier models only when justified.
Use council only when epistemically necessary.
```

Intervention principle:

```txt
No intervention without domain-calibrated benefit.
```

This means Xendris must not add stronger checks, imports, model calls, council
steps, or code transformations merely because they look safer in the abstract.
Intervention strength must be calibrated to the domain, category, execution
mode, and measured harm/benefit.

Xendris must calibrate intervention intensity by domain, category and execution
mode.

## Adaptive Council Policy

More tokens do not imply more certainty.

Policy:

```txt
No council by default.
Council only by evidence of need.
No token escalation without epistemic justification.
```

Escalate only when there is strong contradiction, high-risk claims, insufficient
evidence with high impact, sycophancy risk, irreversible action, explicit user
request, or justified budget.

Do not escalate when local deterministic guards can limit, block, or downgrade
the claim.

## SycophancyGuard

Rule:

```txt
If the user proposes a conclusion, the model may not promote it to fact without
evidence.
```

Xendris should require counterpoints, limits, or evidence before user-proposed
claims are admitted.

## Epistemic Frame Layer

Xendris must audit not only what the model says, but the frame from which the
output claims certainty.

Initial frames:

- `EXPLORATION`
- `CREATIVE`
- `MARKETING`
- `BENCHMARK`
- `PRODUCTION`
- `CODE_STATE`
- `LEGAL`
- `MEDICAL`
- `FINANCIAL`
- `SECURITY`
- `EDUCATIONAL`
- `RESEARCH`

Rule:

```txt
The more actionable an interface is, the stronger its evidence requirement.
```

## Commercial Model

Xendris should not be sold as another generic AI subscription. The target model
is prepaid governed AI usage:

```txt
provider cost + Xendris trust margin
```

Safety rule:

```txt
No open-ended provider spend.
```

Required controls:

- prepaid balance;
- hard caps;
- daily/monthly budgets;
- model premium lock;
- alerts;
- optional auto-recharge;
- project/API-key budgets.

## Roadmap Milestones

### A. Clean Public Framework Release

Goal: clean public framework release without historical evidence contamination.

Exit criteria:

```txt
release gate: pass or warnings without blockers
unsafe rejected citations: 0
active benchmark blockers: 0
```

### B. API Boundary Audit

Goal: classify public, experimental, and private modules.

### C. Real Provider Evidence Import

Goal: import real-provider benchmark artifacts only after metadata, cost,
latency, provider disclosure, and evidence gate admission are complete.

### D. Runtime API MVP

Goal: expose Xendris as a trust runtime API.

### E. Wallet and Usage Core

Goal: prepaid PAYG with hard caps and cost traceability.

### F. Adaptive Council and Sycophancy Layer

Goal: avoid token escalation without epistemic justification.

### G. Epistemic Frame Layer

Goal: implement Frontera C Mayor at representation-frame level.

### H. Agentic Programming Benchmark v0.1

Agentic Programming benchmarks must distinguish pipeline-valid dry-run evidence from real-provider agent performance evidence. Dry-run artifacts are admissible only as pipeline validation; real-provider claims require separate live-mode execution with provider disclosure, cost, and latency metrics.

Exit criteria:

Goal: evaluate whether Xendris scaffolding improves agent reliability on small programming tasks, through a closed synthetic dataset with excellence-gated scoring.

Exit criteria:

```txt
dataset: 20 tasks across 10 categories (bug_fixing, feature_addition,
  api_contracts, edge_cases, unit_tests, refactor_safety, performance,
  security_basics, dependency_discipline, multi_file_reasoning)
module: xendris.benchmarking.agentic_programming (10 files)
scoring: 7 weighted components with hard penalties
excellence gate: READY_FOR_INTERPRETATION / WARNINGS_PRESENT /
  BLOCKED_FOR_INTERPRETATION
tests: 4 test files covering dataset, scorer, runner, excellence_gate
```

### Milestone H Result

Agentic Programming v0.1 produced admitted real-provider evidence that, on a closed 20-task mini-repo benchmark using direct DeepSeek v4 Flash, Xendris calibrated increased measured agentic programming score from 0.585 to 0.9625 and pass rate from 15% to 90%, remaining explicitly scoped to this dataset, provider, model, and configuration.

### I. Xendris Agent UI

Goal: usable product surface: one agent, all models, trust-routed.

### J. Trust Dashboard

Goal: make the differential value of Xendris visible.

## Final North Star

```txt
Xendris exists to stop useful AI interfaces from being mistaken for certain
knowledge.
```

Final rule:

```txt
No output becomes operational knowledge until it crosses the right membrane.
```
