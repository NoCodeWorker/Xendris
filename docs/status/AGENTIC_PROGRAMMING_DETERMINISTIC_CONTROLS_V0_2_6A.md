# Agentic Programming — Deterministic Controls v0.2.6A

**Status:** Implemented  
**Version:** v0.2.6A  
**Date:** 2026-07-06

## Purpose

Add deterministic non-provider agent variants that validate the Agentic Programming Benchmark scoring system before running real providers.

These controls prove that the benchmark can distinguish:

- a **good agent** that applies expected patches (oracle_agent)
- a **partial/minimal agent** (partial_agent)
- a **bad agent** that touches forbidden files, breaks APIs, or makes false success claims (bad_agent)

## Why Deterministic Controls Before Real Providers

1. **Validate the scorer** — ensure weights, penalties, and averaging work correctly
2. **Validate the excellence gate** — ensure it distinguishes passing/warning/blocked
3. **Validate the sandbox** — ensure test execution works end-to-end
4. **Establish baseline bounds** — know what a perfect (oracle) score looks like
5. **Catch regressions** — run controls as CI checks before any real-provider run

## Variants

| Variant | Description | Expected Score Range |
|---------|-------------|---------------------|
| `oracle_agent` | Applies expected solution from fixture's `expected/` directory for all tasks | High (≥0.80) |
| `partial_agent` | Fixes only bug_fixing + some feature/performance tasks (10/20) | Medium (0.40–0.80) |
| `bad_agent` | Touches forbidden files, disables assertions, breaks API signatures, makes false success claims | Low (<0.30) |

## Implementation

**Deterministic agents module:** `xendris/benchmarking/agentic_programming/deterministic_agents.py`

Functions:
- `oracle_agent(repo_path, ..., working_dir, fixture_dir)` — copies all files from `fixture_dir/expected/` to working_dir
- `partial_agent(repo_path, ..., working_dir, fixture_dir)` — applies expected fix only to tasks in a fixed subset
- `bad_agent(repo_path, ..., working_dir, fixture_dir)` — creates forbidden test files, disables assertions, renames functions, makes false success claims

**Runner integration:** `xendris/benchmarking/agentic_programming/runner.py`

- `_run_deterministic_task()` — dedicated code path that calls deterministic agents, runs real tests (not dry-run stubs), and evaluates all 7 scoring components
- `_snapshot_files()` / `_find_changed_files()` — detects files added or modified by the agent to evaluate forbidden file and security checks

## Results

| Metric | oracle_agent | partial_agent | bad_agent |
|--------|-------------|---------------|-----------|
| Total Score | 0.8525 | 0.6575 | 0.0 |
| Tasks Passed | 18/20 | 10/20 | 2/20 |
| Pass Rate | 0.9 | 0.5 | 0.1 |
| Excellence Gate | READY_FOR_INTERPRETATION | WARNINGS_PRESENT | BLOCKED_FOR_INTERPRETATION |

### Key Observations

1. **oracle_agent above bad_agent:** Score 0.8525 > 0.0 ✓
2. **oracle_agent above partial_agent:** Score 0.8525 > 0.6575 ✓
3. **Penalties detected:** bad_agent triggers forbidden file touch, false success claim, API contract violation
4. **Gate correctly blocks bad_agent:** BLOCKED_FOR_INTERPRETATION ✓
5. **Gate correctly approves oracle_agent:** READY_FOR_INTERPRETATION ✓

## Interpretation Scope

**ADMITTED — Benchmark Control Evidence Only**

- These results are deterministic, not from any real model or provider
- oracle_agent results must NOT be interpreted as Xendris or model performance
- These results validate that the benchmark scoring system works correctly
- They establish upper-bound (oracle) and lower-bound (bad) score baselines for the current fixture set
- They do NOT measure real-world agent programming capability

## Output Paths

| Artifact | Path |
|----------|------|
| Summary | `runs/agentic_programming_v0_1_deterministic_controls/summary.json` |
| Results | `runs/agentic_programming_v0_1_deterministic_controls/results.jsonl` |
| Report | `runs/agentic_programming_v0_1_deterministic_controls/report.md` |

## Tests

**Test file:** `tests/benchmarking/test_agentic_programming_deterministic_controls.py`

Verifies:
- oracle_agent variant exists and is classified as deterministic
- oracle_agent scores above bad_agent on fixtures
- bad_agent has low score (penalties applied)
- partial_agent scores between oracle and bad
- Historical dry-run artifacts are not overwritten
- Evidence warnings and scoping are present in summary

## CLI Usage

```bash
# Run deterministic controls (default dry-run mode)
python scripts/run_agentic_programming_benchmark.py \
  --variants oracle_agent,partial_agent,bad_agent \
  --output-dir runs/agentic_programming_v0_1_deterministic_controls

# Run with fail-on-gate-blockers (bad_agent will fail gate - expected)
python scripts/run_agentic_programming_benchmark.py \
  --variants oracle_agent,partial_agent,bad_agent \
  --output-dir runs/agentic_programming_v0_1_deterministic_controls \
  --fail-on-gate-blockers
```

## Next Real-Provider Pilot

With deterministic controls validated:
1. Implement real agent adapters for base_agent, xendris_agent, xendris_calibrated_agent
2. Configure provider credentials (OpenRouter)
3. Run live-mode pilot: 20 tasks × 3 variants
4. Compare oracle_agent (upper bound) to real agent scores
5. If real agents score below oracle_agent, identify gaps
6. If real agents trigger penalties, investigate root causes
