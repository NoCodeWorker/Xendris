# Forensic Note — Finitexo v0.6.0 Blocked Preflight

## Blocked Run Directory

`runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30/`

## Final Decision

`REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_INSUFFICIENT_TASKS`

## Summary

| Field | Value |
|---|---|
| Providers attempted | [] |
| Providers completed | [] |
| Actual cost | $0.00 |
| Responses | 0 |
| Scores | 0 |
| Metadata rows | 0 |
| Task count loaded | 10 |
| Expected task count | 30 |
| Expected attempts | 60 |
| Dataset loaded | v0.4.3 (10 tasks) |
| Dataset hash | `a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4` |

## Preflight Blockers

```
missing_explicit_execution_confirmation
missing_provider_key:deepseek
missing_provider_key:openai
insufficient_tasks
```

## Root Cause

This blocked run was produced by the **old v0.6.0 runner** at `benchmarks/finitexo_code_matrix_v0_6_0/real_provider_controlled_run/controlled_run.py`. That runner loads `benchmarks/finitexo_code_matrix_v0_4_3` (n=10) but expects `expected_task_count=30`. The preflight correctly blocked execution.

The **new v0.6.0 implementation** at `benchmarks/finitexo_code_matrix_v0_6/real_provider_controlled_run/` already defaults to the correct 30-task dataset at `benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30/` with the correct hashes.

## Remediation Applied

- `ControlledRunConfig.expected_dataset_hash` default set to the v0.6.0 n30 dataset hash.
- `ControlledRunConfig.expected_manifest_hash` default set to the v0.6.0 n30 manifest hash.
- `main()` entry point now loads API keys and confirmation from `frontend/.env.local` if not in process environment.
- Regression tests added for: config path, task count 10 rejection, dataset hash mismatch detection.

## Status

- Live execution has not been performed.
- v0.6.0 is ready for live execution after this fix.
- The blocked run artifacts are preserved as evidence of a safe preflight block.
