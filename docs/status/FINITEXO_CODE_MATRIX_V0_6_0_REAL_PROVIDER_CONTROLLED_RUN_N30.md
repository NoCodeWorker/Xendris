# Finitexo Code Matrix v0.6.0 - Real Provider Controlled Run n=30

## Purpose

v0.6.0 defines the first controlled real-provider diagnostic run target for
Finitexo Code Matrix with:

- 30 frozen/admissible tasks;
- two providers: DeepSeek and OpenAI;
- expected 60 real provider responses;
- full traceability, costs, metadata and deterministic diagnostic scoring.

## Safety Boundary

This phase does not authorize:

- statistical significance claims;
- provider superiority claims;
- Xendris superiority claims;
- production-readiness claims;
- universal programming benchmark claims;
- commercial superiority claims.

## Preconditions

Execution requires:

- `provider_mode = real`;
- `execution_mode = live`;
- expected providers exactly `deepseek` and `openai`;
- explicit execution confirmation;
- process-environment provider keys;
- budget cap;
- v0.5.7 report admissibility readiness;
- dataset and manifest hash verification;
- at least 30 frozen/admissible tasks.

## Current Repository Status

The currently configured frozen dataset path is:

```txt
benchmarks/finitexo_code_matrix_v0_4_3
```

That dataset contains 10 frozen tasks. Therefore, a v0.6.0 n=30 execution must
block with:

```txt
REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_INSUFFICIENT_TASKS
```

until a later frozen/admissible dataset contains at least 30 tasks.

## Artifacts

The runner writes to:

```txt
runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30/
```

Expected files:

- `controlled_run_summary.json`
- `controlled_run_report.md`
- `responses.jsonl`
- `scores.jsonl`
- `metadata.jsonl`
- `real_provider_costs.json`
- `provider_attempts.json`
- `provider_failures.json`
- `run_manifest.json`

## Final Decision

Expected in the current repository state:

```txt
REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_INSUFFICIENT_TASKS
```

This is the correct conservative outcome because v0.6.0 must not synthesize new
tasks or mutate the frozen v0.4.3 dataset.
