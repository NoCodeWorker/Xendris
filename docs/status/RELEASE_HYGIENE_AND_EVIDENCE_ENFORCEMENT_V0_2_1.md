# Xendris Release Hygiene and Evidence Enforcement v0.2.1

Date: 2026-07-06

## Purpose

Prepare Xendris for a cleaner public framework release by adding explicit
generated-output rules, admitted-evidence-only benchmark citation checks, and a
single local release-gate command.

## Changes

Implemented:

- generated-output policy;
- ignored scratch output patterns;
- benchmark evidence citation checker;
- deterministic tests for citation checking;
- canonical Trust Traps artifact policy;
- v0.2.1 API surface audit skeleton;
- local v0.2.1 release gate command.

No provider integrations were changed. No real-provider benchmarks were run.
No frontend behavior was changed.

## Generated-Output Policy

Policy file:

```txt
docs/policies/GENERATED_OUTPUT_POLICY.md
```

The policy keeps `runs/` available for curated benchmark evidence while
requiring scratch, local, temporary, and log outputs to remain ignored.

## Evidence Citation Checker

Checker:

```txt
scripts/check_benchmark_evidence_citations.py
```

Behavior:

- reads `runs/benchmark_evidence_registry.json`;
- identifies rejected artifacts;
- scans Markdown documents under `docs/`;
- blocks citations to rejected artifacts unless the surrounding text clearly
  marks them as rejected, blocked, historical, not admitted, or superseded.

## Release Command

Release gate command:

```powershell
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_1.py
```

The gate runs:

- focused citation checker tests;
- Benchmark Excellence suite audit;
- Benchmark Evidence Registry build;
- benchmark evidence citation checker;
- `git diff --check` with explicit handling for the known `phyng/api.py`
  whitespace caveat.

## API Audit Skeleton

API skeleton:

```txt
docs/api/API_SURFACE_AUDIT_V0_2_1.md
```

Stable public imports remain:

- `xendris`
- `xendris.frontera_c`
- `xendris.core.rag`
- `xendris.core.response_contract`

Runtime, router, fingerprint, ledger, trust, and benchmark modules remain
experimental unless promoted by a future API audit.

## Commands Run

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_benchmark_evidence_citation_checker.py -q
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_benchmark_evidence_citation_checker.py tests/benchmarking/test_benchmark_evidence_registry.py tests/benchmarking/test_benchmark_suite_excellence_audit.py -q
.\.venv\Scripts\python.exe scripts\check_benchmark_evidence_citations.py
.\.venv\Scripts\python.exe scripts\audit_benchmark_suite_excellence.py --fail-on-blockers
.\.venv\Scripts\python.exe scripts\build_benchmark_evidence_registry.py --require-admitted
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_1.py
```

## Observed Results

Focused citation checker tests:

```txt
7 passed
```

Focused benchmark hygiene tests:

```txt
18 passed
```

Evidence citation checker:

```txt
BENCHMARK_EVIDENCE_CITATIONS rejected=3 violations=0
```

Benchmark Suite Excellence Audit:

```txt
BENCHMARK_SUITE_EXCELLENCE summaries=5 ready=2 blocked=3
```

Benchmark Evidence Registry:

```txt
BENCHMARK_EVIDENCE_REGISTRY total=5 admitted=2 rejected=3
```

Release gate:

```txt
XENDRIS_RELEASE_GATE_V0_2_1
status=BLOCKED
```

Release gate step results:

| Step | Result |
|---|---|
| focused citation checker tests | `PASS` |
| benchmark suite excellence audit | `BLOCKED` |
| benchmark evidence registry | `PASS` |
| benchmark evidence citation checker | `PASS` |
| git diff check | `WARNING` |

The `git diff --check` warning is the known `phyng/api.py` whitespace caveat:

```txt
phyng/api.py:414: trailing whitespace.
phyng/api.py:434: new blank line at EOF.
```

## Remaining Blockers

- Benchmark Suite Excellence Audit still reports 3 blocked historical summaries.
- The global diff check still reports the known `phyng/api.py` whitespace caveat.
- The working tree contains many pre-existing modified/untracked files outside
  this focused hygiene task.

## Release Decision

```txt
BLOCKED
```

The v0.2.1 hygiene layer is implemented, but the repository is not ready for a
clean release tag until the blocked historical summaries and working-tree
hygiene are resolved.

## Interpretation

This task improves release hygiene and evidence enforcement. It does not claim
universal superiority, real-provider performance, production readiness, or
scientific validation.
