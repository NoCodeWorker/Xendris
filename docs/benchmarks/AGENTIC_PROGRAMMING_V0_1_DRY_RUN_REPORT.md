# Agentic Programming Benchmark v0.1 — Dry-Run Report

## Scope

This report documents the first canonical execution of the Agentic Programming Benchmark v0.1 pipeline in **dry-run mode**.

**Purpose:** Validate the end-to-end pipeline (dataset → runner → scorer → excellence gate → output) before piloting with real providers.

**No real provider was called.** All patches are generic stubs (`def solve(): pass`). No model output was evaluated.

## Dataset

20 synthetic programming tasks across 10 categories:

| Category | Count | Example Task |
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

## Variants Evaluated

- `base_agent`
- `xendris_agent`
- `xendris_calibrated_agent`

## Score Table

| Variant | Total Score | Tasks Passed | Pass Rate |
|---------|-------------|--------------|-----------|
| base_agent | 0.45 | 0 / 20 | 0.0 |
| xendris_agent | 0.45 | 0 / 20 | 0.0 |
| xendris_calibrated_agent | 0.45 | 0 / 20 | 0.0 |

Score 0.45 is the baseline for stub patches (api_contract 0.15 + no_forbidden 0.10 + no_false_success 0.10 + minimal_patch 0.05 + security 0.05 = 0.45).

## Excellence Gate Decision

| Variant | Decision |
|---------|----------|
| base_agent | BLOCKED_FOR_INTERPRETATION |
| xendris_agent | BLOCKED_FOR_INTERPRETATION |
| xendris_calibrated_agent | BLOCKED_FOR_INTERPRETATION |

All variants correctly blocked. A dry-run with stub patches cannot be interpreted as real-provider performance.

## What This Dry-Run Validates

- Dataset loading works for all 20 samples across all 10 categories
- Fixture validation passes for all 20 repos (src/, tests/, manifest.json)
- Runner dispatches 20 tasks × 3 variants = 60 total results
- Scorer computes weighted components with hard penalties correctly
- Excellence gate correctly blocks dry-run (pass_rate = 0.0 < 0.20 threshold)
- JSONL export produces valid per-result serialization
- Markdown report includes scores, limitations, warnings
- Canonical summary JSON includes all required schema fields
- --fail-on-gate-blockers flag exits non-zero when blocked

## What This Dry-Run Does NOT Validate

- Does NOT validate real-provider agent programming capability
- Does NOT measure improvement from Xendris scaffolding
- Does NOT compare against Claude, Codex, GPT, or any other model
- Does NOT measure latency, cost, or throughput
- Does NOT validate hidden test execution against real patches
- Does NOT validate security or dependency checks on real code
- Does NOT represent real-world programming diversity

## Limitations

1. **Execution mode is dry-run:** no real provider was called, no real model output was evaluated.
2. **Provider mode is mock:** patches are generic stubs, not real agent output.
3. **These results are NOT evidence of real-provider agent programming performance.**
4. **These results are NOT evidence of general programming superiority.**
5. **These results are NOT evidence of production readiness.**
6. **Dataset is closed synthetic (20 samples);** does not represent real-world programming diversity.
7. **Pre-existing fitz import error in test_master_goal_frontera_c_decision.py** is unrelated and persists.

## Next Real-Provider Pilot Plan

### Phase 1 (current)
- [x] Dataset: 20 synthetic tasks across 10 categories
- [x] Pipeline: end-to-end dry-run validated
- [x] Excellence gate: correctly blocks dry-run
- [x] Evidence registry: dry-run admitted as pipeline evidence only

### Phase 2 (next)
- [ ] Implement real agent adapters (base_agent, xendris_agent, xendris_calibrated_agent)
- [ ] Configure provider credentials (OpenRouter, DeepSeek, etc.)
- [ ] Run live-mode pilot with 20 tasks × 3 variants
- [ ] Measure latency, cost, token usage per variant
- [ ] Collect real hidden test pass/fail results
- [ ] Evaluate excellence gate on real results
- [ ] Admit real-provider evidence separately (if gate passes)

### Phase 3 (future)
- [ ] Expand dataset from 20 → 100 samples
- [ ] Add real-world programming tasks
- [ ] Multi-provider comparison
- [ ] Cost-per-admissible-answer analysis

## Artifact Paths

| Artifact | Path |
|----------|------|
| Summary | `runs/agentic_programming_v0_1_dry_run/summary.json` |
| Results | `runs/agentic_programming_v0_1_dry_run/results.jsonl` |
| Report | `runs/agentic_programming_v0_1_dry_run/report.md` |
| Evidence registry | `docs/benchmarks/AGENTIC_PROGRAMMING_EVIDENCE_REGISTRY_V0_1.md` |
