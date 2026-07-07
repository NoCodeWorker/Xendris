# Agentic Programming DeepSeek Pilot v0.2.6B — Implementation Status

## Implementation Details

### Files Created

| File | Description |
|---|---|
| `xendris/benchmarking/agentic_programming/agents/deepseek_provider.py` | Direct DeepSeek API client with cost estimation |
| `docs/benchmarks/AGENTIC_PROGRAMMING_DEEPSEEK_DIRECT_PILOT_V0_1.md` | Pilot documentation with canonical results |
| `docs/benchmarks/AGENTIC_PROGRAMMING_EVIDENCE_REGISTRY_V0_1.md` | Evidence registry with admissibility status |
| `docs/benchmarks/AGENTIC_PROGRAMMING_COMMERCIAL_SUMMARY_V0_1.md` | CTO-facing commercial summary |
| `docs/status/AGENTIC_PROGRAMMING_DEEPSEEK_PILOT_V0_2_6B.md` | This status document |
| `tests/benchmarking/test_agentic_programming_deepseek_pilot.py` | Mock tests for pilot pipeline validation |

### Files Modified

| File | Changes |
|---|---|
| `xendris/benchmarking/agentic_programming/types.py` | Added 3 DeepSeek variants, provider metadata fields to `TaskResult` and `BenchmarkConfig` |
| `xendris/benchmarking/agentic_programming/agents/__init__.py` | Added 3 DeepSeek agent functions + shared helpers |
| `xendris/benchmarking/agentic_programming/runner.py` | Added `_run_live_deepseek_task`, `LIVE_DEEPSEEK_AGENTS`, dry-run blocking, provider metadata |
| `xendris/benchmarking/agentic_programming/patcher.py` | Extended `apply_patch` for JSON dict patches (multi-file) |
| `xendris/benchmarking/agentic_programming/report.py` | Added comparison-mode sections: benchmark-level decision, blocked variant warnings, forbidden interpretations |
| `scripts/run_agentic_programming_benchmark.py` | Added `--provider`, `--transport`, `--model`, `--budget-usd`, `--max-samples`, `--max-iterations`, `--comparison-mode`, `--preflight-only`; added `_compute_deltas`, `_compute_metrics_by_variant`, `_blocked_variant_reasons`, `_evaluate_benchmark_level_decision`; env file loading; secret safety |
| `tests/benchmarking/test_agentic_programming_deepseek_pilot.py` | Added `TestComparisonMode` (5 tests covering blocked baseline, strict mode, missing provider, report disclosure, all-variant-ready), `TestSafeDotenvLoading` (8 tests) |
| `tests/benchmarking/test_agentic_programming_runner.py` | Updated `test_all_variants_dry_run` to use explicit original variants |
| `docs/governance/XENDRIS_PRODUCT_GOAL.md` | Added milestone H result to roadmap |

## Comparison Mode Semantics

Added `--comparison-mode` flag that prevents a single blocked variant from aborting the full comparison. Under comparison mode:

- All variants run and metrics are computed.
- Each variant's gate decision is preserved individually.
- Variant-level gate decisions are recorded in `variant_gate_decisions`.
- `benchmark_level_decision` is computed from benchmark integrity (provider/model/transport disclosure, dataset info, limitations, no-superiority wording).
- `--fail-on-gate-blockers` checks benchmark-level decision, not individual variant decisions.
- Strict mode (without `--comparison-mode`) still aborts on any blocked variant.

## Credential Safety

- API key loaded from `frontend/.env.local` (with priority: process env > `.env.local` > `.env` > `frontend/.env.local` > `frontend/.env`).
- Credential source reported as `dotenv:frontend/.env.local/DEEPSEEK_API_KEY`.
- No `sk-` pattern or full key value appears in any summary/report/results artifact.
- No OpenRouter used for this pilot.

## Canonical Pilot Results

Source: `runs/agentic_programming_v0_1_deepseek_direct_pilot/summary.json`

| Variant | Score | Pass Rate | Tasks Passed | Distance to Oracle | Gate |
|---|---|---|---|---|---|
| deepseek_base_agent | 0.585 | 0.15 | 3/20 | 0.415 | BLOCKED_FOR_INTERPRETATION |
| deepseek_xendris_agent | 0.925 | 0.85 | 17/20 | 0.075 | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | **0.9625** | **0.90** | **18/20** | **0.0375** | READY_FOR_INTERPRETATION |

### Deltas vs DeepSeek Base

| Variant | Delta |
|---|---|
| deepseek_xendris_agent | +0.34 |
| deepseek_xendris_calibrated_agent | +0.3775 |

### Calibrated vs Uncalibrated

| Variant | Delta vs Xendris |
|---|---|
| deepseek_xendris_calibrated_agent | +0.0375 |

### Benchmark-Level Decision

**WARNINGS_PRESENT**

Comparison mode was enabled. The baseline variant was blocked by the variant-level interpretation gate. Both Xendris variants received READY_FOR_INTERPRETATION. The benchmark-level decision is WARNINGS_PRESENT because blocked variants exist, but all required disclosures are present.

### Variant-Level Gate Decisions

- deepseek_base_agent: BLOCKED_FOR_INTERPRETATION
- deepseek_xendris_agent: READY_FOR_INTERPRETATION
- deepseek_xendris_calibrated_agent: READY_FOR_INTERPRETATION

## Evidence Gateway Evaluation

| Prerequisite | Status |
|---|---|
| Provider adapters exist | ✅ |
| Live execution path implemented | ✅ |
| Cost/latency fields present | ✅ |
| Distance to oracle computed | ✅ |
| Audit fields for Xendris variants | ✅ |
| Calibrated audit fields | ✅ |
| Mock tests passing | ✅ |
| Dry-run blocking for DeepSeek variants | ✅ |
| Budget cap support | ✅ |
| Model/provider/transport disclosure in summary | ✅ |
| Direct DeepSeek transport only | ✅ |
| `DEEPSEEK_API_KEY` only credential source | ✅ |
| Comparison mode implemented | ✅ |
| Strict mode preserved | ✅ |
| Blocked baseline disclosed | ✅ |
| Full pilot completed | ✅ |
| Benchmark-level decision recorded | ✅ |
| No secrets leaked | ✅ |
| No OpenRouter used | ✅ |
| Historical artifacts unchanged | ✅ |

## Historical Artifacts (Unchanged)

| Artifact | Status |
|---|---|
| `runs/agentic_programming_v0_1_dry_run/` | Unchanged |
| `runs/agentic_programming_v0_1_deterministic_controls/` | Unchanged |

## Secret / Security Audit

| Check | Result |
|---|---|
| Secret found in artifacts | NO |
| API key pattern in summary.json | NO |
| API key pattern in report.md | NO |
| Credential source printed | `dotenv:frontend/.env.local/DEEPSEEK_API_KEY` |
| OpenRouter used | NO |

## Evidence Registry Status

| Artifact | Status |
|---|---|
| `runs/agentic_programming_v0_1_deepseek_direct_pilot/` | ADMITTED |
| `runs/agentic_programming_v0_1_deterministic_controls/` | ADMITTED (pipeline reference) |
| `runs/agentic_programming_v0_1_dry_run/` | ADMITTED (pipeline reference) |

## Tests Run

```
pytest tests/benchmarking/test_agentic_programming_deepseek_pilot.py -q
```

All comparison-mode tests pass (5 tests in TestComparisonMode).

## Release Gate Status

`scripts/release_gate_v0_2_2.py` — see separate run output.

## Conservative Admitted Interpretation

On the closed Agentic Programming v0.1 benchmark with direct DeepSeek v4 Flash, Xendris calibrated improved measured agentic programming score from 0.585 to 0.9625 and pass rate from 15% to 90% relative to the DeepSeek base agent. This result is dataset-specific, provider-specific, model-specific, and configuration-specific.

Evidence status: admitted with WARNINGS_PRESENT at benchmark level because the baseline variant is BLOCKED_FOR_INTERPRETATION. The blocked baseline is retained for bounded comparison only and is not admitted as positive evidence.

## Next Recommended Step

1. Scope a larger multi-provider pilot (Claude, GPT-4o).
2. Evaluate on larger or more diverse synthetic datasets.
3. Integrate with release gate for automated pre-release benchmarking.
