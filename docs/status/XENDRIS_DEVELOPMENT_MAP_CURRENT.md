# Xendris Development Map - Current State

Date: 2026-07-06

## Purpose

This document maps the current development point of Xendris/Phyng after the
benchmark-suite hardening work. It is intended as an operational reference for
what exists, what is admitted as evidence, what remains experimental, and what
is still missing before the suite can be treated as a mature model-enhancement
framework.

## Current Version

| Layer | Current state |
|---|---|
| Python package version | `0.2.0` |
| `xendris.__version__` | `0.2.0` |
| Stable baseline tag | `v0.1.0-baseline` |
| Candidate public framework tag | `v0.2.0-framework-api` |
| Release gate status | `BLOCKED` until working tree and generated-output policy are clean |

Important distinction:

```txt
Package/API version: 0.2.0
Experimental capability documents: v0.3.x through v1.1 exist as internal development layers.
These higher-numbered capability layers do not change the package release version by themselves.
```

## Current Architectural Position

```txt
Xendris = public framework and benchmark/control layer
Phyng = internal/legacy scientific engine
frontend/ = Xendris AI local product shell, still separate from Python benchmark release gates
```

Stable public import surface documented for `v0.2.0`:

- `xendris`
- `xendris.frontera_c`
- `xendris.core.rag` by direct import path
- `xendris.core.response_contract`

Benchmarking and trust modules are currently operational, but should be treated
as experimental framework capabilities until release scope is cleaned and
explicitly tagged.

## Implemented Core Framework Layers

### Response Contract Core

Implemented:

- `xendris.core.response_contract`
- claim type enums;
- confidence/domain validity structures;
- conservative surface-level assessment helpers;
- no model calls;
- no response rewriting;
- no factual-truth validation claims.

Purpose:

```txt
Provide domain-agnostic response discipline:
correctness, calibrated confidence, explicit limits, non-overclaiming.
```

Status:

```txt
IMPLEMENTED_CORE_CONTRACT_LAYER
```

### Trust Kernel and Benchmark Gate

Implemented modules under `xendris.core.trust` include:

- trust claim/evidence primitives;
- benchmark gate;
- quality plan;
- reasoning evaluator;
- diagnostics;
- audit structures.

Purpose:

```txt
Reduce benchmark contamination from unsupported claims, false proxies,
overclaims, fallback responses, runtime failures, and review-required cases.
```

Status:

```txt
IMPLEMENTED_EXPERIMENTAL_TRUST_LAYER
```

### Runtime and Provider Control

Implemented modules under `xendris.core.runtime` include:

- provider adapter;
- sandbox;
- request/response structures;
- orchestrator;
- runtime policy and audit structures.

Purpose:

```txt
Prepare controlled execution around model calls without exposing provider logic
as an uncontrolled benchmark source.
```

Status:

```txt
IMPLEMENTED_EXPERIMENTAL_RUNTIME_LAYER
```

### Algebra, Boundary, Local, Sector, Router, Fingerprint and Ledger Layers

Implemented experimental framework layers include:

- `xendris.core.algebra`
- `xendris.core.boundary`
- `xendris.core.local`
- `xendris.core.sectors`
- `xendris.core.router`
- `xendris.core.fingerprints`
- `xendris.core.ledger`
- `xendris.core.representations`

Purpose:

```txt
Build a broader control architecture around claim objects, sector transitions,
provider selection, local context boundaries, model fingerprints, and audit ledgers.
```

Status:

```txt
IMPLEMENTED_EXPERIMENTAL_FRAMEWORK_LAYERS
```

These layers need separate API audits before being promoted into stable public
surface.

## Implemented Benchmark Suite

### Trust Traps v0.1

Implemented:

- closed dataset loader;
- DeepSeek Base vs Xendris+DeepSeek runner;
- scoring;
- JSONL/JSON export;
- dry-run and provider-capable execution;
- Trust Reasoning Refinement v0.3.5;
- Excellence Gate integration for new runs.

Current admitted dry-run summary:

```txt
runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json
```

Current admitted dry-run result:

| Metric | Value |
|---|---:|
| Samples | 100 |
| DeepSeek score | 0.100 |
| Xendris score | 0.985 |
| Delta | +0.885 |
| Xendris wins | 90 |
| DeepSeek wins | 0 |
| Ties | 10 |

Interpretation:

```txt
Admitted as benchmark-local dry-run evidence only.
Not evidence of universal superiority.
Not real-provider performance.
```

### Programming Reliability v0.1

Implemented:

- closed dataset of 100 programming samples;
- runner with dry-run and provider-capable paths;
- code extraction;
- sandboxed execution;
- scoring;
- JSONL/JSON export;
- Markdown report generation;
- Excellence Gate integration.

Current admitted dry-run summary:

```txt
runs/deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json
```

Current admitted dry-run result:

| Metric | Value |
|---|---:|
| Samples | 100 |
| DeepSeek score | 0.700 |
| Xendris score | 1.000 |
| Delta | +0.300 |
| Xendris wins | 30 |
| DeepSeek wins | 0 |
| Ties | 70 |

Interpretation:

```txt
Admitted as benchmark-local dry-run evidence only.
It measures executable benchmark behavior, contract preservation, security basics,
and production-overclaim control under the closed dataset.
It does not prove general programming superiority.
```

### Ablation Benchmark v0.1

Implemented:

- ablation result structures;
- variant execution;
- summary metrics;
- JSON/JSONL export;
- category breakdown;
- cost/latency/exclusion metrics.

Purpose:

```txt
Identify which Xendris layers contribute to measured benchmark improvement.
```

Status:

```txt
IMPLEMENTED_ANALYSIS_LAYER
```

### Cheap-to-Frontier Gap Benchmark v0.1

Implemented:

- cheap/base/frontier comparison structures;
- gap-closed calculation;
- cost-per-gap-point analysis;
- latency overhead analysis;
- conservative interpretation text.

Purpose:

```txt
Estimate how much Xendris closes a measured benchmark gap between a cheap model
and a frontier model under a specific dataset.
```

Status:

```txt
IMPLEMENTED_ANALYSIS_LAYER
```

## Benchmark Excellence and Evidence Control

### Benchmark Excellence Gate v0.1

Implemented:

- `xendris.benchmarking.excellence_gate`
- public export through `xendris.benchmarking`
- CLI validator:

```txt
scripts/validate_benchmark_excellence.py
```

Checks:

- dataset hash;
- execution mode;
- dataset name/version;
- model/system identity;
- total sample count;
- comparable score pair;
- average delta;
- no-universal-superiority warning;
- limitations section;
- provider disclosure;
- external data disclosure;
- pricing assumptions;
- cost and latency metrics.

Decisions:

- `READY_FOR_INTERPRETATION`
- `WARNINGS_PRESENT`
- `BLOCKED_FOR_INTERPRETATION`

Status:

```txt
IMPLEMENTED_BENCHMARK_INTERPRETATION_GATE
```

### Benchmark Suite Excellence Audit

Implemented:

```txt
scripts/audit_benchmark_suite_excellence.py
docs/benchmarks/BENCHMARK_SUITE_EXCELLENCE_AUDIT.md
runs/benchmark_suite_excellence_audit.json
```

Current audit result:

| Metric | Value |
|---|---:|
| Summary files reviewed | 5 |
| Ready | 2 |
| Blocked | 3 |

Status:

```txt
IMPLEMENTED_SUITE_LEVEL_INTERPRETATION_AUDIT
```

### Benchmark Evidence Registry

Implemented:

```txt
xendris.benchmarking.evidence_registry
scripts/build_benchmark_evidence_registry.py
docs/benchmarks/BENCHMARK_EVIDENCE_REGISTRY.md
runs/benchmark_evidence_registry.json
```

Current registry result:

| Metric | Value |
|---|---:|
| Total artifacts reviewed | 5 |
| Admitted | 2 |
| Rejected | 3 |

Admitted evidence:

- Programming Reliability v0.1 dry-run summary.
- Trust Traps v0.1 dry-run summary generated through the excellence-aware runner.

Rejected historical artifacts:

- older Trust Traps summaries with dry-run/real-provider wording conflict;
- older Trust Traps v2 summary with incomplete metadata;
- older template-derived summary.

Status:

```txt
IMPLEMENTED_EVIDENCE_ADMISSION_LAYER
```

## Frontend Product Shell

Implemented under `frontend/`:

- Xendris homepage;
- `/x` chat interface;
- local conversations;
- provider abstraction;
- mock provider;
- DeepSeek provider behind environment configuration;
- streaming/non-streaming routes;
- runtime status panel;
- response evaluation/controller/repair loop;
- local cache;
- Xendris branding and favicon/logo work.

Status:

```txt
IMPLEMENTED_PRODUCT_SHELL_EXPERIMENTAL
```

Release relationship:

```txt
Frontend is not currently the primary evidence source for Python benchmark-suite excellence.
It should be validated separately with `npm run build` before any frontend release.
```

## Current Validation Evidence

Most recent Python suite result observed during current benchmark hardening:

```txt
1446 passed, 4 warnings
```

Most recent targeted Benchmark Excellence validation:

```txt
56 passed
```

Most recent Benchmark Evidence Registry validation:

```txt
29 passed
```

Known caveat:

```txt
git diff --check currently fails globally because of whitespace in phyng/api.py.
That file is outside the benchmark-gate scope and was not modified during the
Benchmark Excellence work.
```

Scoped diff check for Benchmark Excellence / Evidence Registry files:

```txt
PASS
```

## What Is Still Missing

### Release Hygiene

- Clean or intentionally stage the current dirty working tree.
- Separate generated outputs from source/docs.
- Decide what belongs in Git and what belongs in ignored runtime output.
- Re-run release gate after cleanup.
- Fix or explicitly accept the `phyng/api.py` whitespace issue.

### Evidence Hardening

- Regenerate historical Trust Traps summaries using the excellence-aware runner.
- Avoid using older rejected summaries as evidence.
- Add a policy that public benchmark reports may only reference admitted artifacts.
- Add CI or local pre-release command that runs:

```powershell
.\.venv\Scripts\python.exe scripts\audit_benchmark_suite_excellence.py --fail-on-blockers
.\.venv\Scripts\python.exe scripts\build_benchmark_evidence_registry.py --require-admitted
```

### Real Provider Runs

The environment blocked direct execution of real DeepSeek runs from Codex due
to external data disclosure policy.

Still missing:

- user-executed real-provider Trust Traps run;
- user-executed real-provider Programming Reliability run;
- evidence-gated real-provider artifacts;
- explicit comparison between dry-run and real-provider behavior.

### Multi-Model Frontier Evaluation

Still missing:

- GPT/Claude/Gemini/GLM frontier baseline summaries;
- cheap-to-frontier gap computation using measured frontier scores;
- evidence-gated frontier comparison report.

### Benchmark Coverage Expansion

Potential benchmark domains still missing or immature:

- reasoning under conflicting instructions;
- factual QA with source-backed evaluation;
- tool-use reliability;
- long-context consistency;
- code repair with multi-file projects;
- safety/security prompt resistance;
- cost/latency stress tests;
- multilingual reliability.

### API Stabilization

Still missing:

- explicit API audit for `xendris.benchmarking`;
- explicit API audit for `xendris.core.trust`;
- public/private boundary for runtime/router/fingerprint/ledger modules;
- versioning decision for experimental capability layers v0.3 through v1.1.

### CI and Automation

Still missing:

- one command for full benchmark validation;
- one command for evidence registry build;
- CI gate for benchmark evidence admission;
- CI gate preventing benchmark claims from rejected artifacts;
- reproducible run manifest per benchmark.

### Documentation

Still missing:

- consolidated benchmark operations guide;
- evidence policy guide;
- generated-output policy;
- public claim policy;
- release checklist for v0.2.x / v0.3.x.

## Current Conservative Status

```txt
XENDRIS_BENCHMARK_SUITE_STATUS:
  package_version: 0.2.0
  benchmark_excellence_gate: IMPLEMENTED
  benchmark_suite_audit: IMPLEMENTED
  benchmark_evidence_registry: IMPLEMENTED
  admitted_benchmark_artifacts: 2
  rejected_benchmark_artifacts: 3
  python_suite: PASSING_WITH_WARNINGS
  release_status: NOT_READY_FOR_TAG_UNTIL_WORKTREE_AND_OUTPUT_POLICY_ARE_CLEAN
  universal_superiority_claims: FORBIDDEN
  real_provider_performance_claims: NOT_ESTABLISHED_BY_CODEX_RUNS
```

## Recommended Next Development Steps

1. Clean release hygiene:
   - decide ignored/generated output policy;
   - fix or isolate `phyng/api.py` whitespace;
   - separate frontend changes from Python benchmark-suite changes.

2. Regenerate Trust Traps canonical artifact:
   - run the excellence-aware Trust runner into canonical `runs/`;
   - rebuild suite audit and evidence registry;
   - confirm rejected historical artifacts are no longer used in docs.

3. Add evidence policy enforcement:
   - create a checker that scans docs for references to rejected summaries;
   - block public benchmark reports that cite rejected artifacts.

4. Add release command:
   - one local command to run tests, excellence audit, evidence registry, and diff check.

5. Only after local dry-run evidence is clean:
   - execute real-provider runs manually outside Codex if external disclosure is acceptable;
   - import only resulting summaries/reports;
   - run Excellence Gate and Evidence Registry on them.

## Final Interpretation

Xendris has moved from isolated benchmark scripts toward a controlled benchmark
evidence system:

```txt
runner -> summary/report -> excellence gate -> suite audit -> evidence registry
```

This is the correct direction for a model-enhancement suite: benchmark gains are
not merely generated; they are admitted, blocked, or constrained according to
explicit contracts.
