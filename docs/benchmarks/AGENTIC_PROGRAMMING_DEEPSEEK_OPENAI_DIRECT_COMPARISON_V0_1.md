# Xendris - Agentic Programming DeepSeek/OpenAI Direct Comparison v0.1

## Purpose

Benchmark-local comparison of DeepSeek direct and OpenAI direct variants under Agentic Programming v0.1. Limited to the closed 20-task synthetic benchmark, the same scorer, the same sandbox, comparison-mode gate semantics, and direct provider APIs only. Does not support universal superiority, general coding superiority, production readiness, or transfer claims.

## Provider And Model Scope

| Provider | Transport | Model | Status |
|---|---|---|---|
| DeepSeek | direct | deepseek-v4-flash | Preflight credential detected |
| OpenAI | direct | gpt-4.1-mini | Preflight credential detected |

OpenRouter was not used. No OpenRouter API calls were made.

## Variant Definitions

| Variant | Definition |
|---|---|
| deepseek_base_agent | Raw DeepSeek call with issue description and source files; no Xendris enforcement. |
| openai_base_agent | Raw OpenAI call with issue description and source files; no Xendris enforcement. |
| deepseek_xendris_agent | DeepSeek call wrapped with Xendris boundary enforcement. |
| openai_xendris_agent | OpenAI call wrapped with Xendris boundary enforcement. |
| deepseek_xendris_calibrated_agent | DeepSeek + Xendris + ProgrammingInterventionPolicy in CODE_SANDBOX mode. |
| openai_xendris_calibrated_agent | OpenAI + Xendris + ProgrammingInterventionPolicy in CODE_SANDBOX mode. |

## Deterministic Control References

| Control | Artifact |
|---|---|
| oracle_agent | `runs/agentic_programming_v0_1_deterministic_controls/` |
| partial_agent | `runs/agentic_programming_v0_1_deterministic_controls/` |
| bad_agent | `runs/agentic_programming_v0_1_deterministic_controls/` |

Controls are reference baselines only, not evidence of real-provider performance.

## Run Parameters

| Field | Smoke | Full Comparison |
|---|---|---:|---:|
| execution_mode | live | live |
| comparison_mode | true | true |
| max_samples | 3 | 20 |
| max_iterations | 1 | 2 |
| fail_on_gate_blockers | true | true |
| budget_usd | 0.25 | 1.50 |
| total tasks | 18 | 120 |

## Result Table

| Variant | Score | Pass Rate | Tasks Passed | Distance To Oracle | Gate Decision |
|---|---|---|---:|---:|---:|---|
| deepseek_base_agent | 0.5000 | 0.15 | 3/20 | 0.5000 | BLOCKED_FOR_INTERPRETATION |
| openai_base_agent | 0.6000 | 0.20 | 4/20 | 0.4000 | WARNINGS_PRESENT |
| deepseek_xendris_agent | 0.9525 | 0.90 | 18/20 | 0.0475 | READY_FOR_INTERPRETATION |
| openai_xendris_agent | 0.8375 | 0.65 | 13/20 | 0.1625 | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | 0.9175 | 0.80 | 16/20 | 0.0825 | READY_FOR_INTERPRETATION |
| openai_xendris_calibrated_agent | 0.8375 | 0.65 | 13/20 | 0.1625 | READY_FOR_INTERPRETATION |

## Deltas — Within Provider

### DeepSeek

| Comparison | Delta |
|---|---|
| deepseek_xendris_agent vs deepseek_base_agent | +0.4525 |
| deepseek_xendris_calibrated_agent vs deepseek_base_agent | +0.4175 |
| deepseek_xendris_calibrated_agent vs deepseek_xendris_agent | -0.0350 |

### OpenAI

| Comparison | Delta |
|---|---|
| openai_xendris_agent vs openai_base_agent | +0.2375 |
| openai_xendris_calibrated_agent vs openai_base_agent | +0.2375 |
| openai_xendris_calibrated_agent vs openai_xendris_agent | +0.0000 |

## Deltas — Cross-Provider (Benchmark-Local Observed Differences Only)

| Comparison | Observed Difference | Status |
|---|---|---|
| openai_base_agent vs deepseek_base_agent | +0.1000 | Benchmark-local only. Not evidence of general superiority. |
| openai_xendris_calibrated_agent vs deepseek_xendris_calibrated_agent | -0.0800 | Benchmark-local only. Not evidence of general superiority. |

Cross-provider deltas are reported as observed differences on this specific dataset. They must not be used as universal superiority claims.

## Cost And Latency

| Variant | Avg Latency (ms) | Total Cost (USD) | Cost Per Passed Task (USD) |
|---|---|---|---:|---:|---:|
| deepseek_base_agent | 309.54 | 0.004204 | 0.001401 |
| openai_base_agent | 2060.39 | 0.004223 | 0.001056 |
| deepseek_xendris_agent | 314.23 | 0.005833 | 0.000324 |
| openai_xendris_agent | 2539.84 | 0.005898 | 0.000454 |
| deepseek_xendris_calibrated_agent | 301.89 | 0.005657 | 0.000354 |
| openai_xendris_calibrated_agent | 2623.58 | 0.005892 | 0.000453 |

## Quality Metrics

| Variant | Visible Pass Rate | Hidden Pass Rate | API Preservation | Minimal Patch | False Success Claims |
|---|---|---|---:|---:|---:|---:|---:|
| deepseek_base_agent | 0.40 | 0.15 | 0.95 | 0.90 | 0.00 |
| openai_base_agent | 0.45 | 0.20 | 1.00 | 0.95 | 0.00 |
| deepseek_xendris_agent | 0.95 | 0.90 | 1.00 | 1.00 | 0.00 |
| openai_xendris_agent | 0.85 | 0.65 | 0.95 | 1.00 | 0.00 |
| deepseek_xendris_calibrated_agent | 0.95 | 0.80 | 1.00 | 1.00 | 0.00 |
| openai_xendris_calibrated_agent | 0.85 | 0.65 | 0.95 | 1.00 | 0.00 |

## Variant-Level Gate Decisions

| Variant | Decision |
|---|---|
| deepseek_base_agent | BLOCKED_FOR_INTERPRETATION |
| openai_base_agent | WARNINGS_PRESENT |
| deepseek_xendris_agent | READY_FOR_INTERPRETATION |
| openai_xendris_agent | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | READY_FOR_INTERPRETATION |
| openai_xendris_calibrated_agent | READY_FOR_INTERPRETATION |

Blocked/warning variants are retained for comparison only and must not be treated as positive evidence.

## Benchmark-Level Decision

WARNINGS_PRESENT

Reason: baseline variants are blocked/warning at variant level, but comparison mode is enabled. Benchmark integrity and disclosure requirements are met.

## Secret Scan Result

SECRET_OR_HEADER_PATTERN_FOUND=False

No actual API keys, Authorization headers, Bearer tokens, or secret values were found in any artifact. Variable names `DEEPSEEK_API_KEY` and `OPENAI_API_KEY` appear only in safe `credential_sources_by_provider` dotenv paths. No `sk-` prefix detected.

## Conservative Admitted Interpretation

Xendris scaffolding (Xendris agent or calibrated agent) improves measured agentic programming reliability for both DeepSeek-v4-flash and gpt-4.1-mini on this specific closed 20-task benchmark under comparison-mode evidence rules. The improvement is observed for both providers but is larger for DeepSeek on this dataset. The evidence is admitted only for this specific benchmark, provider pair, transport, and configuration.

## Forbidden Interpretations

- Universal superiority over any other model, provider, or agent framework.
- General coding superiority.
- Production readiness.
- Transfer to OpenRouter, other providers, other models, other datasets, or other transports.
- Claims about Claude, Codex, Kimi, GLM, or any unmeasured model.
- Treating blocked or warning variants as admitted positive evidence.
- Cross-provider deltas as evidence of general provider superiority.

## Limitations

- Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.
- Results are specific to the Agentic Programming v0.1 benchmark.
- OpenAI is gpt-4.1-mini; DeepSeek is deepseek-v4-flash. Different model sizes and capabilities.
- Cost/latency estimates depend on API response conditions and may not be reproducible.
- Deterministic controls are reference baselines only.
- Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.

## Next Steps

1. Update evidence registry with this artifact as ADMITTED.
2. Consider expanding to real-world programming tasks.
3. Consider adding more providers or models (Claude, Codex, Gemini).
4. Consider larger sample sizes for stronger statistical confidence.
