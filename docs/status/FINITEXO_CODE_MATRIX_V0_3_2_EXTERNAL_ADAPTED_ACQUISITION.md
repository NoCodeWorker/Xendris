# Finitexo Code Matrix v0.3.2 - External Adapted Candidate Acquisition

## Why This Exists

v0.3.1 installed the intake layer, but the candidate pool still had no
`EXTERNAL_ADAPTED` candidates.

v0.3.2 adds better candidate origins by adapting public technical ideas into
local fixtures without copying external code or promoting candidates into the
frozen benchmark dataset.

## Previous State

v0.3.1:

```txt
candidate_count: 5
accepted_count: 5
warnings_count: 0
rejected_count: 0
MUTATED_FIXTURE: 2
SEMI_EXTERNAL_SYNTHETIC: 3
EXTERNAL_ADAPTED: 0
EXTERNAL_VERIFIED: 0
mean_externality_score: 0.468
providers_executed: false
claims_authorized: none
decision: IMPLEMENTED_SEMI_EXTERNAL_INTAKE_ONLY
```

## New Sources

Added sources:

```txt
src_006: EXTERNAL_ADAPTED - URL join safety warning adapted to local redirect validation
src_007: EXTERNAL_ADAPTED - timeout tuple behavior adapted to local configuration normalization
src_008: EXTERNAL_ADAPTED - semantic version precedence adapted to local comparator
src_009: EXTERNAL_ADAPTED - Retry-After behavior adapted to local parser
src_010: MUTATED_FIXTURE - query parameter duplicate handling
```

## New Candidates

Added candidates:

```txt
candidate_task_006: EXTERNAL_ADAPTED
candidate_task_007: EXTERNAL_ADAPTED
candidate_task_008: EXTERNAL_ADAPTED
candidate_task_009: EXTERNAL_ADAPTED
candidate_task_010: MUTATED_FIXTURE
```

## Current Candidate Pool

```txt
candidate_count_total: 10
new_candidate_count: 5
accepted_count: 10
warnings_count: 0
rejected_count: 0
```

Origin distribution:

```txt
EXTERNAL_ADAPTED: 4
MUTATED_FIXTURE: 3
SEMI_EXTERNAL_SYNTHETIC: 3
EXTERNAL_VERIFIED: 0
```

Externality scores:

```txt
mean_externality_score_new_candidates: 0.732
mean_externality_score_all_candidates: 0.600
target_mean_externality_score: 0.600
target_met: true
```

## Limitations

The new candidates are `EXTERNAL_ADAPTED`, not `EXTERNAL_VERIFIED`.

They use public technical ideas as inspiration, but fixtures, prompts, tests,
names, and behavior are local. No third-party implementation code is bundled.

## Provider Execution

```txt
providers_executed: false
```

No providers were executed. No `.env` file was read. No network access was used
by the intake command or tests.

## Dataset Promotion

No dataset promotion occurred.

```txt
candidate_pool != frozen_benchmark_dataset
```

Promotion would require a future explicit phase.

## Claims

```txt
claims_authorized: []
```

Externality score is diagnostic only. It does not authorize performance,
superiority, provider, or production-readiness claims.

## Tests

Executed:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_3_2_external_adapted.py -q
```

Result:

```txt
12 passed
```

Additional validation should include v0.3.1 + v0.3.2 together before commit.

## Artifacts

Generated:

```txt
runs/finitexo_code_matrix_v0_3_2_external_adapted/intake_summary.json
runs/finitexo_code_matrix_v0_3_2_external_adapted/intake_report.md
runs/finitexo_code_matrix_v0_3_2_external_adapted/external_adapted_summary.json
```

## Final Decision

```txt
EXTERNAL_ADAPTED_TARGET_MET
```

The candidate pool now contains honestly documented external-adapted tasks and
meets the v0.3.2 externality target. This is still dataset-origin improvement,
not benchmark performance evidence.

