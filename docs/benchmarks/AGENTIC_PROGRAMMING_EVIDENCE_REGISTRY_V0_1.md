# Xendris — Agentic Programming Evidence Registry v0.1

## Purpose

This registry tracks all benchmark artifacts for the Agentic Programming v0.1 benchmark and their evidence admissibility status. Only admitted artifacts may support public benchmark claims.

## Registry Entry: DeepSeek Direct Pilot

| Field | Value |
|---|---|
| Artifact Path | `runs/agentic_programming_v0_1_deepseek_direct_pilot/` |
| Summary | `runs/agentic_programming_v0_1_deepseek_direct_pilot/summary.json` |
| Report | `runs/agentic_programming_v0_1_deepseek_direct_pilot/report.md` |
| Results | `runs/agentic_programming_v0_1_deepseek_direct_pilot/results.jsonl` |
| Status | ADMITTED |
| Decision | WARNINGS_PRESENT |
| Benchmark-level Decision | WARNINGS_PRESENT |
| Provider | deepseek |
| Model | deepseek-v4-flash |
| Transport | direct |
| Samples | 20 |
| Comparison Mode | enabled |
| Date Admitted | 2026-07-07 |

### Admission Note

This artifact is admitted with warnings because the benchmark-level decision is
WARNINGS_PRESENT. The baseline variant is blocked at variant level and is
retained only for bounded comparison, not as positive evidence.

### Allowed Usage

- Benchmark-local real-provider comparison of DeepSeek base vs DeepSeek+Xendris variants.
- Agentic programming behavior analysis under this closed dataset, provider, model, and configuration.
- Evidence that Xendris scaffolding can improve measured agentic programming reliability on this specific benchmark.

### Forbidden Usage

- Universal superiority over any other model or agent framework.
- General coding superiority.
- Production readiness.
- Transfer to OpenRouter, other DeepSeek models, Claude, GPT, Codex, Kimi, or GLM.
- Treating blocked variant (deepseek_base_agent) as admitted positive evidence.

## Registry Entry: Deterministic Controls

| Field | Value |
|---|---|
| Artifact Path | `runs/agentic_programming_v0_1_deterministic_controls/` |
| Status | ADMITTED (pipeline reference only) |
| Decision | Not applicable (pipeline validation only) |
| Usage | Pipeline validation, scoring verification, reference baselines |

## Registry Entry: Dry Run

| Field | Value |
|---|---|
| Artifact Path | `runs/agentic_programming_v0_1_dry_run/` |
| Status | ADMITTED (pipeline reference only) |
| Decision | Not applicable (pipeline validation only) |
| Usage | Dry-run pipeline validation only. Not admissible as real-provider evidence. |

## Evidence Policy

- Only artifacts with ADMITTED status and READY_FOR_INTERPRETATION or WARNINGS_PRESENT decision may support benchmark-local claims.
- BLOCKED_FOR_INTERPRETATION variants within an admitted artifact are retained for comparison only and must not be treated as positive evidence.
- Benchmark-local evidence must not be generalized beyond its dataset, provider, model, and configuration.
- No claim of universal or general superiority is supported by any artifact in this registry.
