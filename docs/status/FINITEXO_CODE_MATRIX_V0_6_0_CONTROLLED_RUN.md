# Finitexo Code Matrix v0.6.0 — Real Provider Controlled Run n=30

## Status

This is a **controlled diagnostic real-provider run** extending the v0.5.4–v0.5.7 diagnostic chain.

## Purpose

- Validate n=30 diagnostic stability, provider reliability, and scoring consistency.
- Provide a larger sample (n=30) than the v0.5.4 diagnostic n=10 while remaining diagnostic-only.
- Confirm the v0.5.7 gate's `ready_for_v0_6_0_controlled_run: true` recommendation.

## Authorization

- This phase is **diagnostic only**.
- It does **not** prove model superiority.
- It does **not** authorize production-readiness, statistical significance, or universal benchmark claims.
- Any future superiority claim requires a larger, paired, externally stronger benchmark with explicit variant comparison.

## Dataset

- 30 tasks generated deterministically from the v0.4.3 frozen 10-task set (3 variants per base task).
- Provenance documented in `benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30/provenance.json`.
- Dataset hashes and manifest hashes are reproducible.

## Provider Coverage

| Provider | Model | Max Tokens | Temperature |
|---|---|---|---|
| DeepSeek | deepseek-v4-flash | 1024 | 0.0 |
| OpenAI | gpt-4.1-nano | 1024 | 0.0 |

## Budget

- Budget cap: $0.50
- Soft target: $0.20
- Execution stops before exceeding the cap.

## Preflight Requirements

1. v0.5.7 report admissibility gate approved with `ready_for_v0_6_0_controlled_run: true`.
2. `FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM=true` in process environment.
3. `DEEPSEEK_API_KEY` present.
4. `OPENAI_API_KEY` present.
5. Dataset exists with ≥30 tasks.
6. Output directory is empty (or `allow_overwrite=true`).

## Output Directory

`runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30/`

## Implementation

Module: `benchmarks/finitexo_code_matrix_v0_6/real_provider_controlled_run/`

| File | Purpose |
|---|---|
| `controlled_run_config.py` | `ControlledRunConfig`, `ControlledProviderSpec` |
| `controlled_run_gate.py` | Preflight gate (`evaluate_controlled_run_preflight`) |
| `controlled_run_scoring.py` | Diagnostic scorer with 9+4 components, provider aggregation |
| `controlled_run_report.py` | Markdown report builder |
| `controlled_run_runner.py` | Main runner + `main()` entry point + artifact writer |
| `__init__.py` | Public exports |

## Authorized Claims

- Real providers executed under controlled conditions.
- Budget was respected or not respected.
- Provider failures were observed or not observed.
- Diagnostic scores computed according to the documented scorer.
- No broad superiority claim is authorized.

## Prohibited Claims

- Universal model superiority
- Production readiness
- Statistically significant superiority
- Provider quality ranking (unless diagnostic-only labeled)
- Xendris improvement without paired variant comparison
- General coding ability
- External benchmark performance

## Tests

Test file: `tests/benchmarking/test_finitexo_code_matrix_v0_6_controlled_run.py`

Covers:
- Config defaults
- Preflight blocks (missing readiness, missing confirmation, missing keys, dataset count mismatch, output dir not empty, mode not real)
- Preflight passes with all conditions
- Scorer range validation (0..1)
- Scorer empty/full/secret exposure/false success
- Scorer provider-independence (symmetry)
- Provider aggregation and overall mean
- Verified count tracking
- Report contains prohibited-claim guardrails
- Summary contains authorized_claims and prohibited_claims
- Budget block behavior
- Artifact path creation (9 files)
- Full runner path with real dataset (60 completions)

## Relation to v0.5.x Chain

```
v0.5.3 Diagnostic Execution  →  BLOCKED (precondition)
v0.5.4 Authorized Diagnostic  →  COMPLETED_DIAGNOSTIC_ONLY
v0.5.5 Evidence Integrity     →  APPROVED
v0.5.6 Scoring Consistency    →  APPROVED
v0.5.7 Report Admissibility   →  APPROVED (ready_for_v0_6_0: true)
v0.6.0 Controlled Run n=30    →  [this phase]
```

## Current Status

- Implementation: complete
- Dataset: generated (30 tasks from v0.4.3 with provenance)
- Tests: implemented
- Execution: not yet run (requires live API keys and preflight approval)
