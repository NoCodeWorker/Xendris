# Xendris Repository Governance Audit v0.2.3

Date: 2026-07-06

## Objective

Classify the current Xendris/Phyng repository before any destructive cleanup,
large move, or public release tag. The goal is to preserve real progress while
removing ambiguity around source code, historical research material, generated
outputs, admitted benchmark evidence, frontend experiments, and legacy Phyng
artifacts.

This audit is intentionally conservative. It does not delete files, move
modules, change benchmark scores, alter datasets, run providers, or promote
experimental namespaces into stable API.

## Current Release Position

| Area | Current state |
|---|---|
| Package/API version | `0.2.0` |
| Current cleanup phase | `v0.2.3 repository governance cleanup audit` |
| Stable public API | `xendris`, `xendris.frontera_c`, `xendris.core.rag`, `xendris.core.response_contract` |
| Active release gate | `scripts/release_gate_v0_2_2.py` |
| Release gate status | `BLOCKED` because working tree is not clean |
| Python suite evidence | `1446 passed, 4 warnings` |
| Benchmark suite audit | `5 summaries, 2 ready, 0 active blocked, 3 quarantined historical rejected` |
| Evidence registry | `5 reviewed, 2 admitted, 3 rejected` |

## Repository Problem Statement

The repository has accumulated several valid but mixed layers:

- stable Xendris package/API work;
- experimental Xendris trust/runtime/benchmarking layers;
- Phyng scientific legacy code and documents;
- historical benchmark reports;
- generated benchmark outputs;
- frontend product-shell work;
- release hygiene scripts and policies;
- large historical Markdown corpus.

The current risk is not lack of progress. The risk is loss of architectural
clarity: future readers cannot immediately tell which artifacts are current,
which are historical, which are admitted evidence, which are generated outputs,
and which modules are public API.

## Classification Taxonomy

Use the following labels for cleanup decisions:

| Label | Meaning | Default action |
|---|---|---|
| `CORE_SOURCE` | Stable or release-relevant Xendris source | Keep visible and tested |
| `EXPERIMENTAL_SOURCE` | Working Xendris modules not yet public API | Keep, mark experimental |
| `LEGACY_PHYNG` | Historical/internal Phyng engine | Keep, isolate as legacy |
| `PUBLIC_DOCS` | Current docs users should read first | Keep visible |
| `GOVERNANCE_DOCS` | Policies, gates, release rules, audits | Keep visible |
| `HISTORICAL_DOCS` | Old scientific or campaign material | Move under historical namespace later |
| `ADMITTED_EVIDENCE` | Registry-admitted benchmark artifacts | Keep traceable |
| `REJECTED_HISTORICAL_EVIDENCE` | Rejected benchmark artifacts retained for audit | Keep quarantined |
| `GENERATED_OUTPUT` | Runtime outputs, logs, scratch artifacts | Ignore or quarantine |
| `FRONTEND_EXPERIMENTAL` | Xendris AI web shell | Keep separate from Python release |
| `DELETE_CANDIDATE` | Redundant generated/cache/local files | Delete only after manifest approval |

## Top-Level Classification

| Path | Classification | Rationale | Immediate action |
|---|---|---|---|
| `xendris/` | `CORE_SOURCE` + `EXPERIMENTAL_SOURCE` | Public package plus experimental framework layers | Keep; audit public surface |
| `phyng/` | `LEGACY_PHYNG` | Internal/legacy scientific engine | Keep; do not rename in this phase |
| `tests/` | `CORE_SOURCE` + `EXPERIMENTAL_SOURCE` | Regression contract for current code | Keep; separate benchmark/core tests later |
| `docs/status/` | `GOVERNANCE_DOCS` | Release state, maps, roadmaps, gates | Keep visible |
| `docs/policies/` | `GOVERNANCE_DOCS` | Output and quarantine rules | Keep visible |
| `docs/api/` | `GOVERNANCE_DOCS` | API audit docs | Keep visible |
| `docs/benchmarks/` | `GOVERNANCE_DOCS` + benchmark reports | Evidence reports and manifests | Keep; enforce admitted/rejected boundaries |
| `docs/audits/` | `HISTORICAL_DOCS` + audit history | Useful but not primary onboarding | Keep; later index |
| `docs/frontera_c/` | `HISTORICAL_DOCS` | Frontera C-Mayor bridge/legacy docs | Keep; mark historical/bridge |
| `docs/lean/` | `HISTORICAL_DOCS` | Formalization support docs | Keep; not release blocker unless Lean gate is active |
| `docs/rag/` | `HISTORICAL_DOCS` or future `PUBLIC_DOCS` | RAG planning docs | Audit before promotion |
| root `docs/*.md` numbered corpus | `HISTORICAL_DOCS` | Large Phyng campaign history | Move later under `docs/historical/phyng_campaigns/` |
| `runs/` | `ADMITTED_EVIDENCE` + `REJECTED_HISTORICAL_EVIDENCE` | Curated benchmark outputs | Keep only curated; scratch ignored |
| `frontend/` | `FRONTEND_EXPERIMENTAL` | Product shell separate from Python release | Keep separate; build gate only for frontend release |
| `public/` | `FRONTEND_EXPERIMENTAL` | Static product assets | Review with frontend scope |
| `formal/` | `EXPERIMENTAL_SOURCE` | Lean formalization wrapper | Keep; separate Lean gate |
| `rag/` | `LEGACY_PHYNG` or experimental | Legacy/support code | Audit before public use |
| `tools/` | `EXPERIMENTAL_SOURCE` | Utility scripts | Audit individually |
| `data/` | `GENERATED_OUTPUT` or curated data | Currently ignored by policy | Keep local unless curated |
| `reports/` | `GENERATED_OUTPUT` or historical | Currently ignored by policy | Keep local unless curated |
| `.venv/`, `.pytest_cache/`, `.lake/`, `*.egg-info/` | `DELETE_CANDIDATE` | Local environment/build/cache | Keep ignored; do not commit |
| `.api-server.*.log` | `DELETE_CANDIDATE` | Local runtime logs | Keep ignored; delete when safe |

## Xendris Source Classification

| Module | Classification | Notes |
|---|---|---|
| `xendris/__init__.py` | `CORE_SOURCE` | Package version and minimal public API boundary |
| `xendris/frontera_c/` | `CORE_SOURCE` bridge | Public bridge, not scientific validation claim |
| `xendris/core/rag/` | `CORE_SOURCE` import surface | Public by direct import path |
| `xendris/core/response_contract/` | `CORE_SOURCE` | v0.2 contract core |
| `xendris/benchmarking/` | `EXPERIMENTAL_SOURCE` | Operational but needs API audit before public stabilization |
| `xendris/core/trust/` | `EXPERIMENTAL_SOURCE` | Trust kernel/gate layer, not stable public API yet |
| `xendris/core/runtime/` | `EXPERIMENTAL_SOURCE` | Provider/runtime layer, not public API yet |
| `xendris/core/router/` | `EXPERIMENTAL_SOURCE` | Multi-model routing, needs API audit |
| `xendris/core/fingerprints/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/ledger/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/representations/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/algebra/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/boundary/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/local/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/core/sectors/` | `EXPERIMENTAL_SOURCE` | Needs API audit |
| `xendris/benchmarks/false_formality/` | `EXPERIMENTAL_SOURCE` | Benchmark suite, keep behind experimental boundary |
| `xendris/models/`, `outputs/`, `prompts/`, `scripts/` | `EXPERIMENTAL_SOURCE` | Importable but not stable API |

## Documentation Classification

Current Markdown inventory by directory:

| Directory | Count | Classification |
|---|---:|---|
| `docs/status` | 28 | `GOVERNANCE_DOCS` |
| `docs/benchmarks` | 13 | `GOVERNANCE_DOCS` + benchmark reports |
| `docs/policies` | 2 | `GOVERNANCE_DOCS` |
| `docs/api` | 1 | `GOVERNANCE_DOCS` |
| `docs/audits` | 21 | `HISTORICAL_DOCS` + audit history |
| `docs/frontera_c` | 16 | `HISTORICAL_DOCS` / bridge framework |
| `docs/lean` | 3 | `HISTORICAL_DOCS` / formalization support |
| `docs/rag` | 3 | `HISTORICAL_DOCS` or future public docs |
| `docs/models` | 2 | `HISTORICAL_DOCS` |
| `docs/roadmap` | 10 | roadmap archive |
| root numbered docs under `docs/` | 389 | `HISTORICAL_DOCS` |

Primary problem:

```txt
The root of docs/ still contains a large numbered Phyng campaign corpus.
Those files preserve useful history, but they overwhelm current Xendris
governance and should be moved under a historical namespace after manifesting.
```

## Benchmark Evidence Classification

Admitted benchmark evidence:

- `runs/deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json`
- `runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json`

Rejected historical evidence:

- `runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_summary.json`
- `runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_v2_summary.json`
- `runs/deepseek_vs_xendris_trust_traps_v0_1_summary.json`

Current policy:

```txt
Rejected historical artifacts remain traceable, but must not be used as public
evidence. The release gate separates them from active blockers.
```

## Current Working Tree Risk

The working tree is not clean. It includes:

- release hygiene changes;
- historical artifact quarantine changes;
- benchmark-source additions;
- frontend product-shell modifications;
- runtime/provider modifications;
- trust/core test additions;
- generated run outputs;
- public/static asset changes.

Risk:

```txt
A single commit or tag from this state would mix unrelated scopes and make
future rollback difficult.
```

## Governance Architecture Target

Target repository shape:

```txt
README.md
docs/
  api/
  architecture/
  benchmarks/
  governance/
  policies/
  status/
  historical/
    phyng_campaigns/
    frontera_c/
    lean/
    rag/
  frontend/
xendris/
  core/
  benchmarking/
  frontera_c/
phyng/
frontend/
runs/
  admitted/
  historical/
  local/       # ignored
scripts/
tests/
formal/
```

This is a target shape, not a command to execute blindly.

## Cleanup Principles

1. Do not delete first.
2. Classify before moving.
3. Move documents before moving code.
4. Keep evidence lineage intact.
5. Keep `phyng/` as legacy/internal until a migration plan exists.
6. Keep frontend release separate from Python framework release.
7. Do not promote experimental modules without API audit.
8. Do not let rejected benchmark artifacts support claims.
9. Keep generated-output policy enforceable.
10. Require a clean working tree before tagging.

## Immediate Recommendations

1. Create a cleanup execution plan with commit boundaries.
2. Stage and commit release-hygiene/quarantine work separately.
3. Separate frontend changes into their own commit or branch.
4. Separate experimental trust/runtime/benchmarking source additions into their
   own commit.
5. Move historical docs only after creating a move manifest.
6. Add a docs index so current readers do not start in the historical corpus.
7. Re-run `scripts/release_gate_v0_2_2.py` after each cleanup commit.

## Decision

```txt
REPOSITORY_GOVERNANCE_AUDIT_COMPLETED
release_status: BLOCKED_BY_DIRTY_WORKTREE
next_action: phased cleanup execution plan
destructive_cleanup_allowed: false
```
