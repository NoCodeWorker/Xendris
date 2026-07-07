# Xendris — Agentic Programming Benchmark Report

**Date:** 2026-07-07
**Benchmark:** Agentic Programming Reliability v0.1
**Execution Mode:** dry-run
**Provider Mode:** mock

## Summary

- Total tasks: 20
- Total results: 60
- Agents evaluated: 3
- Execution mode: dry-run
- Provider mode: mock

## Scores by Agent Variant

| Variant | Total Score | Tasks Passed | Total Tasks | Pass Rate |
|---------|-------------|--------------|-------------|-----------|
| oracle_agent | 1.0 | 20 | 20 | 1.0 |
| partial_agent | 0.7875 | 11 | 20 | 0.55 |
| bad_agent | 0.0 | 2 | 20 | 0.1 |

## Excellence Gate Decisions

| Variant | Decision |
|---------|----------|
| oracle_agent | READY_FOR_INTERPRETATION |
| partial_agent | WARNINGS_PRESENT |
| bad_agent | BLOCKED_FOR_INTERPRETATION |

## Limitations

- Execution mode is dry-run: no real provider was called, no real model output was evaluated.
- Provider mode is mock: patches are generic stubs, not real agent output.
- These results are NOT evidence of real-provider agent programming performance.
- These results are NOT evidence of general programming superiority.
- These results are NOT evidence of production readiness.
- Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.
- Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.

## Warning: No Real Provider Called

No real provider was called. All task results use mock/stub patches. Real-provider performance requires a separate live-mode run with provider credentials and real agent implementations.

## Warning: No Superiority Claim

This dry-run does not compare against any other model or agent framework. No claim of universal superiority is made or implied.

## Commercial Metrics

| Metric | Value |
|--------|-------|
| task_success_rate | 0.55 |
| visible_test_pass_rate | 0.7 |
| hidden_test_pass_rate | 0.5667 |
| api_preservation_rate | 0.9333 |
| forbidden_file_touch_rate | 0.3 |
| false_success_claim_rate | 0.3333 |
| unauthorized_dependency_rate | 0.0 |
| minimal_patch_rate | 1.0 |
| security_clean_rate | 0.8833 |
| cost_per_verified_successful_task | None |

## Legend

- **Total Score:** Weighted composite (0-1 scale)
- **Tasks Passed:** Visible + hidden tests both green
- **Excellence Gate:** READY_FOR_INTERPRETATION | WARNINGS_PRESENT | BLOCKED_FOR_INTERPRETATION
