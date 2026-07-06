# Xendris Repository Cleanup Execution Plan v0.2.3

Date: 2026-07-06

## Objective

Execute a controlled repository cleanup that improves governance, release
readiness, and maintainability without losing benchmark evidence, historical
traceability, or the current Xendris goal.

This plan is intentionally incremental. It avoids large destructive changes and
keeps rollback simple.

## Non-Goals

- Do not delete historical Phyng documents in the first cleanup pass.
- Do not rename `phyng/`.
- Do not modify benchmark scores.
- Do not modify datasets to improve results.
- Do not run real providers.
- Do not claim universal superiority.
- Do not merge frontend release concerns into the Python package release.
- Do not promote v0.3.x-v1.1 experimental layers into stable API without audit.

## Commit Boundary Strategy

Use small commits with one responsibility each.

Recommended boundaries:

1. `docs: add repository governance audit`
2. `chore: enforce benchmark evidence quarantine`
3. `docs: add current documentation index`
4. `docs: quarantine historical phyng documents`
5. `refactor: clarify xendris experimental namespaces`
6. `chore: clean generated output boundaries`
7. `chore: pass v0.2.x release gate`

Do not combine frontend UI changes with benchmark governance changes.

## Phase 0 - Freeze and Inventory

Goal:

```txt
Know what exists before moving anything.
```

Actions:

- keep `REPOSITORY_GOVERNANCE_AUDIT_V0_2_3.md` as the classification source;
- capture `git status --short`;
- capture file counts by top-level directory;
- identify untracked files that are source vs generated output;
- ensure no secrets are present in staged or untracked files.

Exit criteria:

- classification exists;
- dirty tree is understood;
- no deletion has occurred.

## Phase 1 - Commit Existing Release Hygiene Work

Goal:

```txt
Persist the release hygiene and evidence enforcement layer as its own coherent
unit.
```

Scope:

- generated-output policy;
- evidence citation checker;
- release gate v0.2.1/v0.2.2;
- quarantine policy;
- historical rejected artifact manifest;
- suite audit and evidence registry outputs;
- whitespace-only cleanup in `phyng/api.py`.

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_benchmark_evidence_citation_checker.py tests/benchmarking/test_historical_artifact_quarantine.py -q
.\.venv\Scripts\python.exe scripts\check_benchmark_evidence_citations.py
.\.venv\Scripts\python.exe scripts\audit_benchmark_suite_excellence.py --fail-on-blockers
.\.venv\Scripts\python.exe scripts\build_benchmark_evidence_registry.py --require-admitted
git diff --check
```

Expected result:

```txt
historical rejected artifacts: quarantined
active benchmark blockers: 0
evidence citation violations: 0
```

## Phase 2 - Separate Frontend Product Shell

Goal:

```txt
Keep the Xendris AI web shell separate from the Python framework release.
```

Actions:

- review `frontend/` changes;
- decide whether frontend should be committed as experimental product shell;
- run `npm run build` before any frontend commit;
- document frontend release independence under `docs/frontend/`.

Exit criteria:

- frontend changes are either committed in their own scope or left unstaged;
- Python release gate does not depend on frontend build.

## Phase 3 - Benchmark Source Consolidation

Goal:

```txt
Make benchmarking source structure understandable without promoting it all to
stable public API.
```

Actions:

- classify `xendris/benchmarking/` as experimental operational framework;
- keep `xendris.benchmarking` out of stable API docs until audited;
- ensure tests clearly map to benchmark modules;
- keep generated outputs governed by evidence registry.

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking -q
```

## Phase 4 - Historical Documentation Quarantine

Goal:

```txt
Move the large Phyng campaign corpus out of the current-reader path.
```

Proposed target:

```txt
docs/historical/phyng_campaigns/
docs/historical/frontera_c/
docs/historical/lean/
docs/historical/rag/
```

Rules:

- move, do not delete;
- create a move manifest;
- preserve filenames unless there is a strong reason;
- update references only when broken references matter to current docs;
- do not reinterpret old scientific claims.

Validation:

```powershell
git status --short
git diff --check
```

Optional reference checks:

```powershell
rg "FRONTERA_C_MAYOR|VALIDATION_LADDER|PROJECT_STATUS" docs
```

## Phase 5 - Current Documentation Index

Goal:

```txt
Make the repo readable without opening historical files first.
```

Create:

```txt
docs/INDEX.md
docs/architecture/README.md
docs/benchmarks/README.md
docs/governance/README.md
docs/status/README.md
```

Minimum index sections:

- start here;
- current package/API version;
- current stable public imports;
- current benchmark evidence;
- release gates;
- historical archive;
- non-claims.

## Phase 6 - API and Namespace Governance

Goal:

```txt
Prevent experimental layers from being mistaken for stable public API.
```

Actions:

- extend `docs/api/API_SURFACE_AUDIT_V0_2_1.md`;
- create follow-up audits for:
  - `xendris.benchmarking`;
  - `xendris.core.trust`;
  - `xendris.core.runtime`;
  - `xendris.core.router`;
  - `xendris.core.ledger`;
- decide whether `xendris.experimental` is warranted.

Do not move code until imports and tests are mapped.

## Phase 7 - Clean Release Gate

Goal:

```txt
Make the release gate pass from a clean working tree.
```

Required command:

```powershell
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_2.py
```

Tag readiness requires:

- no active benchmark blockers;
- no unsafe rejected-artifact citations;
- evidence registry has admitted artifacts;
- `git diff --check` passes;
- working tree is clean;
- release docs reflect actual validation.

## Current Blockers

```txt
working_tree_clean: BLOCKED
frontend_changes: MIXED_WITH_PYTHON_RELEASE_SCOPE
experimental_source_changes: MIXED_WITH_RELEASE_HYGIENE_SCOPE
generated_outputs: NEED_CURATED_TRACKING_DECISION
historical_docs: TOO_VISIBLE_IN_CURRENT_DOCS_PATH
```

## Cleanup Safety Rules

Before moving or deleting anything:

1. produce a manifest;
2. run focused tests;
3. run `git diff --check`;
4. keep rollback possible;
5. avoid combining unrelated scopes.

## Recommended Immediate Next Step

Prepare a surgical commit for the governance audit documents only:

```powershell
git add docs/status/REPOSITORY_GOVERNANCE_AUDIT_V0_2_3.md docs/status/REPOSITORY_CLEANUP_EXECUTION_PLAN_V0_2_3.md
git commit -m "docs: add repository governance cleanup audit"
```

Then prepare a separate commit for release hygiene and quarantine changes.

## Decision

```txt
CLEANUP_PLAN_READY
execution_mode: phased_non_destructive
current_release_status: BLOCKED_UNTIL_WORKING_TREE_CLEAN
```
