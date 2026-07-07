# Xendris — Agentic Programming Benchmark Report

**Date:** 2026-07-07
**Benchmark:** Agentic Programming Reliability v0.1
**Execution Mode:** live
**Provider Mode:** real

## Summary

- Total tasks: 20
- Total results: 60
- Agents evaluated: 3
- Execution mode: live
- Provider mode: real
- Benchmark-level decision: WARNINGS_PRESENT
- Comparison mode: enabled

## Scores by Agent Variant

| Variant | Total Score | Tasks Passed | Total Tasks | Pass Rate |
|---------|-------------|--------------|-------------|-----------|
| deepseek_base_agent | 0.585 | 3 | 20 | 0.15 |
| deepseek_xendris_agent | 0.925 | 17 | 20 | 0.85 |
| deepseek_xendris_calibrated_agent | 0.9625 | 18 | 20 | 0.9 |

## Excellence Gate Decisions

| Variant | Decision |
|---------|----------|
| deepseek_base_agent | BLOCKED_FOR_INTERPRETATION |
| deepseek_xendris_agent | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | READY_FOR_INTERPRETATION |

## Blocked Variant Handling

Blocked variants are included for comparison only and are not admitted as positive evidence.

| Variant | Reason |
|---------|--------|
| deepseek_base_agent | Variant-level interpretation gate blocked this result (score=0.585, pass_rate=0.15). It is retained for comparison only and is not admitted as positive evidence. |

On this run, the baseline variant was blocked by the interpretation gate, while Xendris variants may be ready. This permits a bounded comparison of observed benchmark behavior, but the blocked baseline must not be treated as admitted positive evidence.

## Conservative Comparison Interpretation

Blocked variants are included for comparison only and are not admitted as positive evidence.

## Forbidden Interpretations

- Universal superiority over any other model or agent framework.
- General coding superiority.
- Production readiness.
- Treating blocked variants as admitted positive evidence.

## Limitations

- Execution mode is live: the direct DeepSeek API was called, not OpenRouter.
- Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.
- Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized.
- Results do not transfer to OpenRouter or any other transport.
- Deterministic controls (oracle_agent, partial_agent, bad_agent) are reference baselines only, not evidence of real-provider performance.
- Cost/latency estimates depend on API response conditions and may not be reproducible.
- No comparison against Claude, GPT, Codex, or any other model is included. No superior generalization is claimed.
- Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.

## Warning: No Superiority Claim

This benchmark evaluates Xendris variants against a DeepSeek base on a specific closed dataset. No claim of universal superiority over any other model or agent framework is made or implied.

## Commercial Metrics

| Metric | Value |
|--------|-------|
| task_success_rate | 0.6333 |
| verified_successful_count | 38 |
| visible_test_pass_rate | 0.7833 |
| hidden_test_pass_rate | 0.6333 |
| api_preservation_rate | 1.0 |
| forbidden_file_touch_rate | 0.0 |
| false_success_claim_rate | 0.0 |
| unauthorized_dependency_rate | 0.0 |
| minimal_patch_rate | 1.0 |
| security_clean_rate | 0.9167 |
| average_latency_ms | 304.76 |
| estimated_cost_total | 0.015257 |
| cost_per_verified_successful_task | 0.000401 |

## Legend

- **Total Score:** Weighted composite (0-1 scale)
- **Tasks Passed:** Visible + hidden tests both green
- **Excellence Gate:** READY_FOR_INTERPRETATION | WARNINGS_PRESENT | BLOCKED_FOR_INTERPRETATION
