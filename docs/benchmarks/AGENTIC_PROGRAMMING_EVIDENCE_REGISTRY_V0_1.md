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

## Registry Entry: DeepSeek/OpenAI Direct Comparison

| Field | Value |
|---|---|
| Artifact Path | `runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/` |
| Summary | `runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/summary.json` |
| Report | `runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/report.md` |
| Results | `runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/results.jsonl` |
| Status | ADMITTED |
| Decision | WARNINGS_PRESENT |
| Benchmark-level Decision | WARNINGS_PRESENT |
| Providers | deepseek, openai |
| Models | deepseek-v4-flash, gpt-4.1-mini |
| Transport | direct |
| Samples | 20 |
| Variants | 6 |
| Comparison Mode | enabled |
| Date Admitted | 2026-07-07 |

### Admission Note

This artifact is admitted with warnings because the benchmark-level decision is WARNINGS_PRESENT. The deepseek_base_agent variant is blocked at variant level and is retained only for bounded comparison, not as positive evidence.

### Allowed Usage

- Benchmark-local comparison of DeepSeek direct vs OpenAI direct under Agentic Programming v0.1.
- Benchmark-local comparison of base vs Xendris variants for each provider.
- Benchmark-local cost/performance comparison under this dataset and configuration.
- Evidence that Xendris scaffolding can improve measured agentic programming reliability for both providers on this specific benchmark.

### Forbidden Usage

- Universal superiority over any other model, provider, or agent framework.
- General coding superiority.
- Production readiness.
- Transfer to OpenRouter, other providers, other models, other datasets, or other transports.
- Claims about Claude, Codex, Kimi, GLM, or any unmeasured model.
- Treating blocked/warning variants as admitted positive evidence.
- Cross-provider deltas as evidence of general provider superiority.

## Registry Entry: Real-World v0.2 (Repository-Local Tasks)

| Field | Value |
|---|---|
| Artifact Path | `runs/agentic_programming_real_world_v0_2/` |
| Summary | `runs/agentic_programming_real_world_v0_2/summary.json` |
| Report | `runs/agentic_programming_real_world_v0_2/report.md` |
| Results | `runs/agentic_programming_real_world_v0_2/results.jsonl` |
| Status | ADMITTED |
| Decision | WARNINGS_PRESENT |
| Benchmark-level Decision | WARNINGS_PRESENT |
| Providers | deepseek, openai |
| Models | deepseek-v4-flash, gpt-4.1-mini |
| Transport | direct |
| Task Suite | real_world_v0_2 |
| Samples | 10 |
| Variants | 6 |
| Comparison Mode | enabled |
| Date Admitted | 2026-07-07 |

### Admission Note

This artifact is admitted with warnings because the benchmark-level decision is WARNINGS_PRESENT. Both base agent variants are blocked at variant level and are retained only for bounded comparison, not as positive evidence. All Xendris variants are at WARNINGS_PRESENT, which preserves their comparative utility.

### Allowed Usage

- Benchmark-local comparison of DeepSeek direct vs OpenAI direct on 10 repository-local tasks.
- Benchmark-local comparison of base vs Xendris variants for each provider.
- Evidence that Xendris scaffolding can improve measured agentic programming reliability for both providers on small real-world tasks.
- Cost/performance comparison under this dataset and configuration.

### Forbidden Usage

- Universal superiority over any other model, provider, or agent framework.
- General coding superiority.
- Production readiness.
- Transfer to OpenRouter, other providers, other models, other datasets, or other transports.
- Claims about Claude, Codex, Kimi, GLM, or any unmeasured model.
- Treating blocked/warning variants as admitted positive evidence.

## Evidence Policy

- Only artifacts with ADMITTED status and READY_FOR_INTERPRETATION or WARNINGS_PRESENT decision may support benchmark-local claims.
- BLOCKED_FOR_INTERPRETATION variants within an admitted artifact are retained for comparison only and must not be treated as positive evidence.
- Benchmark-local evidence must not be generalized beyond its dataset, provider, model, and configuration.
- No claim of universal or general superiority is supported by any artifact in this registry.
