# Codex Prompt — Phygn Core Development Super Loop

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Your task is to continue development of the **core lab logic**, not aesthetics.

Do not focus on frontend styling.  
Do not add animations.  
Do not improve branding.  
Do not expand speculative theory.

You must build the core scientific development loop.

---

# 1. Read first

Read all docs in:

```txt
docs/
```

Especially:

```txt
15_PHYGN_CORE_DEVELOPMENT_LOOP_v0_3.md
16_PHYGN_RAG_AND_DEEP_RESEARCH_ENGINE_v0_3.md
12_PHYGN_SKILLS_AND_AGENTS_v0_3.md
13_PHYGN_AGENT_WORKFLOWS_v0_3.md
```

---

# 2. First action

Inspect the project:

```bash
dir
dir phyng
dir tests
dir docs
pytest -v
```

Do not modify code before understanding current state.

---

# 3. Mission

Implement a continuous core development loop architecture for Phygn:

```txt
state scan
gap detection
research planning
RAG/source registry
formalization
implementation
tests
agent audit
claim gatekeeping
reports
backlog update
next iteration selection
```

---

# 4. New backend modules to add

Create:

```txt
phyng/loop/
  __init__.py
  schemas.py
  state_scan.py
  gap_detection.py
  iteration.py
  backlog.py
  reporting.py

phyng/rag/
  __init__.py
  schemas.py
  source_registry.py
  claim_registry.py
  claim_linker.py
  citation_audit.py
  research_planner.py
  retrieval.py
  rag_report.py
```

Optional future modules, only if simple:

```txt
phyng/agents.py
phyng/skills.py
phyng/orchestrator.py
phyng/audit_schemas.py
```

Do not overengineer.

---

# 5. Data directories to add

Create:

```txt
reports/
backlog/
rag/
rag/sources/
rag/chunks/
rag/claims/
rag/citations/
rag/research_tasks/
```

Add `.gitkeep` where needed.

---

# 6. Core schemas

Implement Pydantic schemas for:

```txt
GapRecord
ResearchTask
SourceRecord
ClaimRecord
ClaimSourceLink
IterationRecord
BacklogTask
AuditSummary
```

Use strict enums.

---

# 7. Gap detection

Implement deterministic functions that inspect current registries and reports.

Examples:

```python
detect_claims_without_sources(...)
detect_claims_without_tests(...)
detect_sources_without_claims(...)
detect_research_tasks_pending(...)
detect_blocked_claims_without_safe_rewrite(...)
```

Do not rely on LLM for these.

---

# 8. RAG MVP

Implement RAG MVP as file-based JSON/JSONL registry.

Do not implement vector DB yet unless trivial.

MVP must support:

```txt
add source
list sources
add claim
link claim to source
audit claim support
create research task for unsourced claim
generate RAG status report
basic lexical retrieval over source notes/chunks
```

---

# 9. Anti-hallucination rules

Implement status transitions:

```txt
claim without source → REQUIRES_SOURCE
hard claim with low-trust source only → REQUIRES_HIGHER_TRUST_SOURCE
claim contradicted by source → BLOCKED
claim with direct support → ALLOWED or ALLOWED_LIMITED
```

Never invent citation metadata.

If metadata unknown, store null.

---

# 10. Reports

Implement report generation:

```txt
reports/iteration_log.md
reports/rag_status.md
reports/claim_source_matrix.md
reports/research_backlog.md
reports/core_backlog.md
```

Each report should be deterministic Markdown.

---

# 11. Backlog

Create:

```txt
backlog/phygn_core_backlog.json
backlog/phygn_core_backlog.md
```

Backlog tasks must have:

```txt
id
title
type
priority
status
blocked_by
acceptance_criteria
```

---

# 12. Tests

Add tests:

```txt
tests/test_loop_gap_detection.py
tests/test_rag_source_registry.py
tests/test_rag_claim_registry.py
tests/test_rag_claim_linker.py
tests/test_rag_research_planner.py
tests/test_rag_reports.py
tests/test_core_backlog.py
```

Minimum test cases:

```txt
source record validates
claim without source becomes REQUIRES_SOURCE
low-trust source cannot support hard physical claim
claim-source direct support works
contradicting source blocks claim
research task created for unsourced claim
rag report generated
backlog task created
gap detection finds missing source
gap detection finds missing test
```

---

# 13. API extensions

If backend API is stable, add endpoints:

```txt
GET /loop/status
POST /loop/iterate-once
GET /rag/sources
POST /rag/sources
GET /rag/claims
POST /rag/claims
POST /rag/claims/link
POST /rag/audit-claim
GET /rag/report
GET /backlog
POST /backlog
```

If adding endpoints risks breaking existing API, defer but document.

---

# 14. Do not fake deep research

Important:

In local code, you cannot actually browse unless an external tool is wired.

So implement deep research as:

```txt
ResearchTask generation
source registry
manual/assisted ingestion
citation audit
RAG update
```

Do not pretend that the code has browsed the web.

Add clear status:

```txt
RESEARCH_TASK_CREATED
AWAITING_SOURCE_INGESTION
SOURCE_INGESTED
CLAIM_AUDITED
```

---

# 15. Integration with agents

For now, agents are static knowledge from docs.

Create deterministic mappings:

```txt
claim about c → Relativity Auditor
claim about λC → Quantum Foundations Auditor
claim about rg/RS → Gravitation Auditor
claim about τ/distributions → Statistical Auditor
claim about L → Operational Scale Auditor
claim about new physics → Claim Gatekeeper + Red Team
```

This can be implemented as a simple rule router.

Do not connect to external LLMs.

---

# 16. Iteration loop function

Implement:

```python
def run_iteration_once(project_root: Path) -> IterationRecord:
    ...
```

It should:

```txt
scan state
detect gaps
create/update backlog
create research tasks for source gaps
generate reports
return summary
```

It does not need to auto-code new physics.

It must not hallucinate.

---

# 17. Acceptance criteria

Task complete when:

```txt
pytest -v passes
RAG registries exist
claim-source linking works
unsourced claims create research tasks
reports generated
backlog generated
run_iteration_once works
no existing backend functionality broken
```

---

# 18. Final principle

Phygn must become a scientific machine that says:

```txt
I do not know yet.
This claim needs a source.
This claim needs a model.
This claim needs a test.
This claim is blocked.
This claim is allowed only as structural.
```

That is the core.

Build that.
