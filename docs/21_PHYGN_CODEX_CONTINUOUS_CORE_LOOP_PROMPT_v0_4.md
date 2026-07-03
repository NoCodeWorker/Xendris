# Codex Prompt — Phygn Continuous Core Development Loop v0.4

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

You must continue developing the **core lab logic** using the Continuous Core Development Loop.

This is not a frontend task.  
This is not a visual polish task.  
This is not a branding task.

Your mission is to make Phygn continue developing itself through:

```txt
gap detection
RAG feedback
research task generation
claim-source linking
tests
benchmarks
reports
backlog
iteration loop
```

---

# 1. Read first

Read:

```txt
docs/18_PHYGN_CONTINUOUS_CORE_DEVELOPMENT_LOOP_v0_4.md
docs/19_PHYGN_CORE_LOOP_EXECUTION_PROTOCOL_FOR_IDE_AI_v0_4.md
docs/20_PHYGN_RAG_RESEARCH_FEEDBACK_LOOP_v0_4.md
```

Also read previous core docs if available:

```txt
docs/15_PHYGN_CORE_DEVELOPMENT_LOOP_v0_3.md
docs/16_PHYGN_RAG_AND_DEEP_RESEARCH_ENGINE_v0_3.md
docs/17_PHYGN_CORE_LOOP_CODEX_PROMPT_v0_3.md
docs/12_PHYGN_SKILLS_AND_AGENTS_v0_3.md
docs/13_PHYGN_AGENT_WORKFLOWS_v0_3.md
```

---

# 2. First command

Inspect state:

```bash
dir
dir phyng
dir tests
dir docs
dir rag
dir reports
dir backlog
pytest -v
```

If `rag`, `reports`, or `backlog` do not exist, create them.

---

# 3. Current known project state

Phygn already has:

```txt
Python core
FastAPI API
Claim Gatekeeper
Operational Scale L review
Epistemic Trace engine
Predictive Gain
RAG registry concepts
Agent/Skills docs
Next.js cockpit
```

Do not rebuild from scratch.

---

# 4. Core mission

Implement or harden the following:

```txt
run_iteration_once(project_root)
gap detection
RAG claim/source registry
claim-source linking
research task creation
citation audit
core backlog
deterministic reports
anti-hallucination status transitions
tests for all of the above
```

---

# 5. Required modules

Ensure these exist or create them:

```txt
phyng/loop/__init__.py
phyng/loop/schemas.py
phyng/loop/state_scan.py
phyng/loop/gap_detection.py
phyng/loop/iteration.py
phyng/loop/backlog.py
phyng/loop/reporting.py

phyng/rag/__init__.py
phyng/rag/schemas.py
phyng/rag/source_registry.py
phyng/rag/claim_registry.py
phyng/rag/claim_linker.py
phyng/rag/citation_audit.py
phyng/rag/research_planner.py
phyng/rag/retrieval.py
phyng/rag/rag_report.py
```

Do not overengineer. File-based JSON/JSONL is enough for v0.4.

---

# 6. Required directories

Ensure:

```txt
rag/
rag/sources/
rag/chunks/
rag/claims/
rag/citations/
rag/research_tasks/

reports/
backlog/
```

---

# 7. Required registries

Ensure:

```txt
rag/source_manifest.json
rag/claims/claim_registry.json
rag/claims/claim_source_links.json
rag/research_tasks/research_backlog.json
rag/citations/citation_audit.json
backlog/phygn_core_backlog.json
```

If missing, initialize with empty valid structures.

---

# 8. Required schemas

Implement Pydantic models:

```txt
SourceRecord
ClaimRecord
ClaimSourceLink
ResearchTask
GapRecord
BacklogTask
IterationRecord
AuditSummary
```

Enums:

```txt
SourceType
TrustLevel
SupportLevel
ClaimStatus
ResearchStatus
GapType
Priority
TaskStatus
IterationStatus
```

---

# 9. Anti-hallucination transitions

Implement deterministic rules:

```txt
claim without source → REQUIRES_SOURCE
hard claim with LOW source only → REQUIRES_HIGHER_TRUST_SOURCE
source contradicts claim → BLOCKED
background-only support → REQUIRES_DIRECT_SUPPORT
direct support + high trust → ALLOWED_LIMITED or ALLOWED
claim without test when test required → REQUIRES_TEST
```

Do not invent sources.

---

# 10. Gap detection functions

Implement:

```python
detect_claims_without_sources(...)
detect_claims_with_low_trust_only(...)
detect_claims_without_tests(...)
detect_sources_without_claims(...)
detect_research_tasks_pending(...)
detect_blocked_claims_without_safe_rewrite(...)
detect_missing_reports(...)
detect_missing_registries(...)
detect_api_endpoints_without_tests(...)
```

Return `GapRecord`.

---

# 11. Research planner

Implement:

```python
create_research_task_for_claim(...)
```

If a claim needs source, create a task:

```txt
status = AWAITING_SOURCE_INGESTION
```

Do not pretend research happened.

---

# 12. Backlog manager

Implement:

```python
create_backlog_task(...)
load_backlog(...)
save_backlog(...)
render_backlog_markdown(...)
```

Backlog task fields:

```txt
id
title
type
priority
status
blocked_by
acceptance_criteria
linked_gap_id
```

---

# 13. Report generation

Implement deterministic Markdown reports:

```txt
reports/iteration_log.md
reports/rag_status.md
reports/claim_source_matrix.md
reports/research_backlog.md
reports/core_backlog.md
reports/benchmark_status.md
```

---

# 14. Iteration function

Implement:

```python
def run_iteration_once(project_root: Path) -> IterationRecord:
    ...
```

It must:

```txt
load state
ensure registries/directories
detect gaps
rank gaps
select highest priority gap
create/update backlog
create research tasks if needed
generate reports
return iteration summary
```

It should not auto-generate speculative physics.

---

# 15. Tests

Add or ensure tests:

```txt
tests/test_loop_gap_detection.py
tests/test_loop_iteration.py
tests/test_core_backlog.py
tests/test_rag_source_registry.py
tests/test_rag_claim_registry.py
tests/test_rag_claim_linker.py
tests/test_rag_research_planner.py
tests/test_rag_reports.py
```

Minimum cases:

```txt
empty registries initialize
claim without source becomes REQUIRES_SOURCE
hard claim with LOW trust source becomes REQUIRES_HIGHER_TRUST_SOURCE
CONTRADICTS link blocks claim
DIRECT_SUPPORT + HIGH trust allows limited claim
research task created for unsourced claim
gap detection finds unsourced claim
gap detection finds missing tests
backlog task created from gap
reports generated
run_iteration_once returns next best task
```

---

# 16. Optional API endpoints

Only if safe:

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

If adding endpoints risks breaking current API, defer and document.

---

# 17. Acceptance criteria

The task is complete when:

```txt
pytest -v passes
run_iteration_once works
registries initialize
claim-source linking works
research tasks are created
reports are generated
backlog is generated
unsourced claims are blocked/degraded
low-trust hard claims are degraded
contradictions block claims
no existing core functionality breaks
```

---

# 18. Important rule

If you cannot complete all, do one full iteration correctly.

A correct small loop is better than a large fake loop.

---

# 19. Final mantra

```txt
No source, no hard claim.
No test, no feature.
No benchmark, no gain.
No scale, no prediction.
No trace, no detectability.
No report, no iteration.
```

Build the core loop.
