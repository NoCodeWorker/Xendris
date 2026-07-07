# Xendris — Agentic Programming DeepSeek Pilot v0.1

## Dataset Scope

| Field | Value |
|---|---|
| Benchmark | Agentic Programming Reliability |
| Version | v0.1 |
| Samples | 20 closed synthetic tasks |
| Categories | bug_fixing, security_basics, unit_tests, edge_cases, api_contracts, feature_addition, multi_file_reasoning, performance, refactor_safety, dependency_discipline |

## Provider / Model

| Field | Value |
|---|---|
| Provider | DeepSeek |
| Model | deepseek-v4-flash |
| Transport | Direct DeepSeek API (not OpenRouter) |
| API Format | OpenAI-compatible chat completions |

## Variants

| Variant | Description |
|---|---|
| `deepseek_base_agent` | Raw DeepSeek call with issue description and source files. No Xendris enforcement. |
| `deepseek_xendris_agent` | DeepSeek + Xendris boundary enforcement: allowed/forbidden files, test evidence, API preservation. |
| `deepseek_xendris_calibrated_agent` | DeepSeek + Xendris + ProgrammingInterventionPolicy with CODE_SANDBOX mode, calibration audit. |

## Deterministic Control References

| Control | Score | Pass Rate | Role |
|---|---|---|---|
| `oracle_agent` | 1.0 | 1.0 | Perfect upper bound |
| `partial_agent` | 0.7875 | 0.55 | Partial baseline |
| `bad_agent` | 0.0 | 0.1 | Lower bound |

Deterministic controls are NOT evidence of real-provider performance. They are reference baselines for pipeline validation only.

## Run Parameters

| Parameter | Value |
|---|---|
| Execution mode | live |
| Max iterations per sample | 2 |
| Max samples | 20 |
| Budget | $1.00 |
| Comparison mode | enabled (blocked variants do not abort) |

## Result Tables

| Variant | Score | Pass Rate | Distance to Oracle | Gate |
|---|---|---|---|---|
| `deepseek_base_agent` | 0.5850 | 0.15 | 0.4150 | BLOCKED_FOR_INTERPRETATION |
| `deepseek_xendris_agent` | 0.9250 | 0.85 | 0.0750 | READY_FOR_INTERPRETATION |
| `deepseek_xendris_calibrated_agent` | **0.9625** | **0.90** | **0.0375** | READY_FOR_INTERPRETATION |

## Deltas vs DeepSeek Base

| Variant | Delta vs DeepSeek Base |
|---|---|
| `deepseek_xendris_agent` | +0.3400 |
| `deepseek_xendris_calibrated_agent` | **+0.3775** |

## Distance to Oracle

| Variant | Distance to Oracle (1.0) |
|---|---|
| `deepseek_base_agent` | 0.4150 |
| `deepseek_xendris_agent` | 0.0750 |
| `deepseek_xendris_calibrated_agent` | **0.0375** |

## Cost / Latency

| Variant | Avg Latency (ms) | Est. Cost Total |
|---|---|---|
| `deepseek_base_agent` | 301.30 | $0.003798 |
| `deepseek_xendris_agent` | 303.55 | $0.005722 |
| `deepseek_xendris_calibrated_agent` | 309.42 | $0.005738 |

## Benchmark-Level Decision

**WARNINGS_PRESENT**

The baseline variant (`deepseek_base_agent`) received BLOCKED_FOR_INTERPRETATION. Both Xendris variants received READY_FOR_INTERPRETATION. Under comparison mode, the benchmark-level gate is WARNINGS_PRESENT because all required disclosures are present, but the blocked baseline must remain comparison-only evidence.

## Conservative Interpretation

- On the closed Agentic Programming v0.1 benchmark with direct DeepSeek v4 Flash, Xendris calibrated improved measured agentic programming score from 0.585 to 0.9625 and pass rate from 15% to 90% relative to the DeepSeek base agent. This result is dataset-specific, provider-specific, model-specific, and configuration-specific.
- Results apply only to the Agentic Programming v0.1 dataset (20 closed synthetic tasks).
- Results do NOT generalize to open-ended programming, production codebases, or other domains.
- Results are not evidence of general coding superiority.
- Cost/latency estimates depend on API conditions and are not guaranteed reproducible.
- Deterministic controls are pipeline references only, not real-provider evidence.
- Xendris improvements are measured only on this specific task distribution.
- The blocked baseline is included for comparison only and is not admitted as positive evidence.

## Forbidden Interpretations

The following interpretations are NOT supported by this pilot:

- Universal superiority over any other model or agent framework.
- General coding ability improvement.
- Production-readiness of any variant.
- Comparison against Claude, GPT, Codex, or any model not measured in this pilot.
- Generalization beyond the 20-task closed synthetic dataset.
- Treating blocked variants as admitted positive evidence.

## Limitations

- 20 samples is small; variance is high.
- Synthetic tasks may not reflect real-world bug distributions.
- Single provider and transport: direct DeepSeek API only.
- Results do not transfer to OpenRouter or any other transport.
- Cost estimates are approximate (based on token counts × published pricing).
- Latency does not include sandbox test execution time.
- Pre-existing fitz import error in `test_master_goal_frontera_c_decision.py` is unrelated.

## Next Steps

1. Scope a larger multi-provider pilot (e.g. Claude, GPT-4o).
2. Evaluate on larger or more diverse synthetic datasets.
3. Consider open-ended programming task evaluation.
