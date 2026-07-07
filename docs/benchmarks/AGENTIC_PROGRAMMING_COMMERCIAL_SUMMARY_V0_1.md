# Agentic Programming v0.1 — Commercial Summary

## Benchmark

Closed synthetic mini-repo benchmark: 20 tasks across 10 categories (bug fixing, unit tests, security, edge cases, API contracts, feature addition, multi-file reasoning, performance, refactor safety, dependency discipline). The benchmark measures whether an agent produces a correct, minimal, safe patch without breaking existing contracts.

## Provider

DeepSeek v4 Flash via direct API (not OpenRouter). 2 iterations per task.

## Results

| Variant | Score | Pass Rate | Tasks Passed | Est. Cost |
|---|---|---|---|---|
| DeepSeek base | 0.585 | 15% | 3/20 | $0.0038 |
| DeepSeek + Xendris | 0.925 | 85% | 17/20 | $0.0057 |
| DeepSeek + Xendris calibrated | **0.9625** | **90%** | **18/20** | $0.0057 |

Cost per verified successful task: **$0.000401**

## What This Measures

- Whether the agent applies a correct patch within allowed files
- Whether the patch passes visible + hidden tests
- Whether the patch preserves API contracts
- Whether the patch avoids forbidden files and false success claims
- Whether the patch is minimal and security-clean

## What This Does Not Prove

- General coding ability
- Production readiness
- Performance on open-ended programming tasks
- Performance with other providers, models, or datasets

## Why This Matters

- **Fewer failed agent tasks:** Pass rate improved from 15% → 90% (calibrated), meaning the agent failed 17/20 without Xendris but only 2/20 with Xendris calibrated.
- **Closer to oracle behavior:** Distance to oracle dropped from 0.415 to 0.0375 — near-perfect replication of the correct patch on this benchmark.
- **Better evidence discipline:** Every Xendris result includes audit fields (allowed files enforced, forbidden files checked, test evidence, API preservation).
- **Measurable cost per verified task:** $0.000401 per verified success across all variants — economically negligible for this task size.

## Note

The DeepSeek base variant was blocked by the interpretation gate (BLOCKED_FOR_INTERPRETATION) and is included for comparison only. Results are scoped to this dataset, provider, model, and configuration. No universal or general coding superiority is claimed.
