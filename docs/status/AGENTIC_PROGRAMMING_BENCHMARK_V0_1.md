# Agentic Programming Benchmark v0.1

**Status:** Implemented  
**Version:** 0.1  
**Date:** 2026-07-06

## Objective

Measure whether Xendris makes a cheap coding model more reliable as an agent inside small repository fixtures. The benchmark evaluates three agent variants:

| Variant | Description |
|---------|-------------|
| `base_agent` | Raw model with no scaffolding |
| `xendris_agent` | Model with Xendris epistemic scaffolding |
| `xendris_calibrated_agent` | Model with Xendris scaffolding + calibration |

## Dataset

20 synthetic programming tasks across 10 categories:

| Category | Count | Description |
|----------|-------|-------------|
| bug_fixing | 4 | Off-by-one, wrong operator, slice error |
| feature_addition | 3 | Stub implementation, median, word frequency |
| api_contracts | 2 | dict.get, deep merge (preserve signature) |
| edge_cases | 2 | None/empty/zero guards |
| unit_tests | 2 | ValueError on invalid input |
| refactor_safety | 1 | Safe rename across files |
| performance | 1 | O(n²) → O(n) with set() |
| security_basics | 2 | eval() → ast, subprocess → stdlib |
| dependency_discipline | 1 | os → pathlib |
| multi_file_reasoning | 2 | Cross-file key mismatch, tuple unpack |

Each task has fixture repository with `src/` and `tests/` (visible + hidden tests).

## Scoring

7 weighted components with hard penalties:

| Component | Weight |
|-----------|--------|
| hidden_tests_pass | 0.35 |
| visible_tests_pass | 0.20 |
| api_contract_preserved | 0.15 |
| no_forbidden_files_touched | 0.10 |
| no_false_success_claim | 0.10 |
| minimal_patch | 0.05 |
| security_clean | 0.05 |

Hard penalties: critical error (-1.0), forbidden file (-0.5), false success (-0.5).

### Excellence Gate

| Score | Decision |
|-------|----------|
| ≥ 0.80 + pass_rate ≥ 0.60 | READY_FOR_INTERPRETATION |
| < 0.40 or pass_rate < 0.20 | BLOCKED_FOR_INTERPRETATION |
| Otherwise | WARNINGS_PRESENT |

## Files

| Path | Purpose |
|------|---------|
| `benchmarks/agentic_programming/v0_1/` | Dataset root |
| `benchmarks/agentic_programming/v0_1/dataset.json` | 20-sample manifest |
| `benchmarks/agentic_programming/v0_1/fixtures/task_NNN/` | Per-task fixture repos |
| `xendris/benchmarking/agentic_programming/` | Python module |
| `xendris/benchmarking/agentic_programming/types.py` | Data classes & enums |
| `xendris/benchmarking/agentic_programming/dataset.py` | Dataset loading & validation |
| `xendris/benchmarking/agentic_programming/sandbox.py` | Test execution |
| `xendris/benchmarking/agentic_programming/patcher.py` | Patch application |
| `xendris/benchmarking/agentic_programming/runner.py` | Benchmark orchestration |
| `xendris/benchmarking/agentic_programming/scorer.py` | Scoring & weights |
| `xendris/benchmarking/agentic_programming/export_jsonl.py` | JSONL export |
| `xendris/benchmarking/agentic_programming/report.py` | Markdown report |
| `xendris/benchmarking/agentic_programming/excellence_gate.py` | Gate evaluation |
| `scripts/run_agentic_programming_benchmark.py` | CLI entry point |

## Usage

## Evidence Admission

### Canonical Dry-Run Artifacts

| Artifact | Path |
|----------|------|
| Summary | `runs/agentic_programming_v0_1_dry_run/summary.json` |
| Results | `runs/agentic_programming_v0_1_dry_run/results.jsonl` |
| Report | `runs/agentic_programming_v0_1_dry_run/report.md` |

### Evidence Decision

**ADMITTED — Pipeline Validated Only.** See `docs/benchmarks/AGENTIC_PROGRAMMING_EVIDENCE_REGISTRY_V0_1.md` for full registry entry.

### Interpretation Scope

- Admitted only as **pipeline-valid dry-run evidence**
- **NOT** admissible as evidence of real-provider agent improvement
- **NOT** admissible as evidence of general coding superiority
- **NOT** admissible as evidence of production readiness
- **NOT** admissible to compare against any other model or framework

### Excellence Gate (Dry-Run)

All 3 variants: **BLOCKED_FOR_INTERPRETATION** — correct behavior. Dry-run stub patches cannot pass real tests.

### Full-Suite Caveat

Pre-existing `fitz` import error in `test_master_goal_frontera_c_decision.py` is unrelated and persists. Not caused by this benchmark.

## Usage

```bash
# Dry-run (default, validates pipeline end-to-end)
python scripts/run_agentic_programming_benchmark.py

# Canonical dry-run to runs/
python scripts/run_agentic_programming_benchmark.py \
  --output-dir runs/agentic_programming_v0_1_dry_run

# Live run with real agents
python scripts/run_agentic_programming_benchmark.py --execution-mode live

# Single variant
python scripts/run_agentic_programming_benchmark.py --agent-variants xendris_agent

# Custom dataset
python scripts/run_agentic_programming_benchmark.py --dataset-path benchmarks/agentic_programming/v0_1

# Fail on gate blockers (CI use)
python scripts/run_agentic_programming_benchmark.py \
  --output-dir runs/agentic_programming_v0_1_dry_run \
  --fail-on-gate-blockers
```
