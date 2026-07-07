# Xendris — Agentic Programming v0.1 DeepSeek Direct Pilot

## Benchmark Scope

| Field | Value |
|---|---|
| Benchmark | Agentic Programming Reliability |
| Version | v0.1 |
| Samples | 20 closed synthetic tasks |
| Categories | bug_fixing, security_basics, unit_tests, edge_cases, api_contracts, feature_addition, multi_file_reasoning, performance, refactor_safety, dependency_discipline |
| Provider | DeepSeek |
| Model | deepseek-v4-flash |
| Transport | Direct DeepSeek API (not OpenRouter) |
| Output Path | `runs/agentic_programming_v0_1_deepseek_direct_pilot/` |

## Deterministic Controls

| Control | Score | Pass Rate | Role |
|---|---|---|---|
| oracle_agent | 1.0 | 1.0 | Perfect upper bound |
| partial_agent | 0.7875 | 0.55 | Partial baseline |
| bad_agent | 0.0 | 0.1 | Lower bound |

Deterministic controls are pipeline references only, not real-provider evidence.

## Live Pilot Results

| Variant | Score | Tasks Passed | Pass Rate | Distance to Oracle | Gate |
|---|---|---|---|---|---|
| deepseek_base_agent | 0.585 | 3 | 0.15 | 0.415 | BLOCKED_FOR_INTERPRETATION |
| deepseek_xendris_agent | 0.925 | 17 | 0.85 | 0.075 | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | **0.9625** | **18** | **0.90** | **0.0375** | READY_FOR_INTERPRETATION |

## Deltas vs DeepSeek Base

| Variant | Delta vs DeepSeek Base |
|---|---|
| deepseek_xendris_agent | +0.34 |
| deepseek_xendris_calibrated_agent | **+0.3775** |

## Distance to Oracle

| Variant | Distance to Oracle (1.0) |
|---|---|
| deepseek_base_agent | 0.415 |
| deepseek_xendris_agent | 0.075 |
| deepseek_xendris_calibrated_agent | **0.0375** |

## Comparison-Mode Handling

The baseline variant (deepseek_base_agent) was blocked by the variant-level interpretation gate (BLOCKED_FOR_INTERPRETATION). It is retained for comparison only and is not admitted as positive evidence.

- Benchmark-level decision: **WARNINGS_PRESENT**
- Variant-level decisions: deepseek_base_agent=BLOCKED_FOR_INTERPRETATION, deepseek_xendris_agent=READY_FOR_INTERPRETATION, deepseek_xendris_calibrated_agent=READY_FOR_INTERPRETATION

## Cost / Latency

| Variant | Avg Latency (ms) | Estimated Cost Total |
|---|---|---|
| deepseek_base_agent | 301.30 | $0.003798 |
| deepseek_xendris_agent | 303.55 | $0.005722 |
| deepseek_xendris_calibrated_agent | 309.42 | $0.005738 |
| **All variants** | 304.76 | $0.015257 |

Cost per verified successful task: **$0.000401**

## Admitted Interpretation

On the closed Agentic Programming v0.1 benchmark with direct DeepSeek v4 Flash, Xendris calibrated improved measured agentic programming score from 0.585 to 0.9625 and pass rate from 15% to 90% relative to the DeepSeek base agent. This result is dataset-specific, provider-specific, model-specific, and configuration-specific.

## Secret / Security Audit

| Check | Result |
|---|---|
| Secret pattern found in artifacts | False |
| OpenRouter used | No |

## Forbidden Interpretations

- Universal superiority over any other model or agent framework.
- General coding superiority.
- Production readiness.
- Treating blocked variants as admitted positive evidence.
- Transfer to OpenRouter, other DeepSeek models, Claude, GPT, Codex, Kimi, or GLM.

## Limitations

- Execution mode is live: the direct DeepSeek API was called, not OpenRouter.
- Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.
- Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized.
- Results do not transfer to OpenRouter or any other transport.
- Deterministic controls (oracle_agent, partial_agent, bad_agent) are reference baselines only, not evidence of real-provider performance.
- Cost/latency estimates depend on API response conditions and may not be reproducible.
- No comparison against Claude, GPT, Codex, or any other model is included. No superior generalization is claimed.
- Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.

## Next Steps

1. Scope a larger multi-provider pilot (Claude, GPT-4o).
2. Evaluate on larger or more diverse synthetic datasets.
3. Integrate with release gate for automated pre-release benchmarking.
