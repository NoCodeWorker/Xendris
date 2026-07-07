# Xendris — Agentic Programming Benchmark Report

**Date:** 2026-07-07
**Benchmark:** Agentic Programming Reliability v0.1
**Execution Mode:** live
**Provider Mode:** real

## Summary

- Total tasks: 5
- Total results: 15
- Agents evaluated: 3
- Execution mode: live
- Provider mode: real
- Benchmark-level decision: READY_FOR_INTERPRETATION
- Comparison mode: enabled

## Scores by Agent Variant

| Variant | Total Score | Tasks Passed | Total Tasks | Pass Rate |
|---------|-------------|--------------|-------------|-----------|
| deepseek_base_agent | 0.74 | 2 | 5 | 0.4 |
| deepseek_xendris_agent | 0.93 | 4 | 5 | 0.8 |
| deepseek_xendris_calibrated_agent | 0.85 | 3 | 5 | 0.6 |

## Excellence Gate Decisions

| Variant | Decision |
|---------|----------|
| deepseek_base_agent | WARNINGS_PRESENT |
| deepseek_xendris_agent | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | READY_FOR_INTERPRETATION |

## Conservative Comparison Interpretation

Blocked variants are included for comparison only and are not admitted as positive evidence.

## Forbidden Interpretations

- Universal superiority over any other model or agent framework.
- General coding superiority.
- Production readiness.
- Treating blocked variants as admitted positive evidence.

## Limitations

- Execution mode is live: direct provider APIs were used (deepseek). Not OpenRouter.
- Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.
- Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized.
- Results do not transfer to OpenRouter or any other transport.
- Deterministic controls (oracle_agent, partial_agent, bad_agent) are reference baselines only, not evidence of real-provider performance.
- Cost/latency estimates depend on API response conditions and may not be reproducible.
- No comparison against Claude, Codex, Kimi, GLM, or any non-measured model is included. No superior generalization is claimed.
- Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.

## Warning: No Superiority Claim

This benchmark evaluates Xendris variants against provider base models on specific closed dataset. No claim of universal superiority over any other model or agent framework is made or implied.

## Warning: No General Coding Superiority Claim

This benchmark is not evidence of general coding superiority. Results are limited to the closed Agentic Programming v0.1 dataset, providers, models, and configuration.

## Commercial Metrics

| Metric | Value |
|--------|-------|
| task_success_rate | 0.6 |
| verified_successful_count | 9 |
| visible_test_pass_rate | 0.9333 |
| hidden_test_pass_rate | 0.6 |
| api_preservation_rate | 1.0 |
| forbidden_file_touch_rate | 0.0 |
| false_success_claim_rate | 0.0 |
| unauthorized_dependency_rate | 0.0 |
| minimal_patch_rate | 1.0 |
| security_clean_rate | 0.8667 |
| average_latency_ms | 303.98 |
| estimated_cost_total | 0.005737 |
| cost_per_verified_successful_task | 0.000637 |

## Legend

- **Total Score:** Weighted composite (0-1 scale)
- **Tasks Passed:** Visible + hidden tests both green
- **Excellence Gate:** READY_FOR_INTERPRETATION | WARNINGS_PRESENT | BLOCKED_FOR_INTERPRETATION
