# Finitexo Code Matrix v0.4.3 - Explicit Expanded Freeze n=10

## Purpose

Finitexo Code Matrix v0.4.3 creates an explicitly versioned expanded frozen
external/adapted candidate dataset with `n=10` tasks.

This phase does not execute providers, compare models, require network access,
read `.env`, print secrets, or authorize superiority/statistical claims.

## Relation To v0.4, v0.4.1 and v0.4.2

- v0.4 created the first frozen external/adapted candidate dataset with two
  tasks.
- v0.4.1 created the expansion intake layer.
- v0.4.2 completed the expansion candidate pool and passed the mixed
  conservative readiness condition.
- v0.4.3 performs the explicit freeze expansion into a new dataset directory:
  `benchmarks/finitexo_code_matrix_v0_4_3/`.

The original v0.4 dataset is not modified in place.

## Selection Logic

The expanded freeze contains:

- 2 inherited v0.4 frozen tasks;
- 7 `READY_FOR_FUTURE_FREEZE` expansion candidates;
- 1 `READY_WITH_HUMAN_REVIEW` candidate with explicit local human-review
  authorization.

Blocked, rejected, missing-provenance, missing-hash, network-required,
secret-required, provider-required, mutated-fixture, and synthetic-local
candidates were excluded.

## Human Review Handling

One human-review candidate was promoted:

```txt
candidate_id: fcm_v0_4_1_candidate_004
reviewer: LOCAL_HUMAN_REVIEW
review_status: APPROVED_FOR_FREEZE
```

The approval is scoped only to freeze inclusion. It does not authorize provider
claims, superiority claims, statistical claims, or production-readiness claims.

## Frozen Task Count

```txt
frozen_task_count: 10
inherited_v0_4_tasks_count: 2
expansion_candidates_promoted_count: 8
human_review_promoted_count: 1
excluded_candidate_count: 6
```

## Provenance Guarantees

Every frozen task has a linked provenance record containing:

- source id;
- source origin;
- source URL;
- source license;
- raw source hash;
- adapted candidate hash;
- frozen task hash;
- base task reference or expansion candidate reference;
- acquisition/adaptation record references;
- human-review reference when applicable;
- known limitations;
- non-claims.

## Hash Guarantees

```txt
dataset_hash: a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4
manifest_hash: 6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e
hash_algorithm: sha256
```

The validator recomputes manifest, task, provenance, human-review and dataset
hashes. A silent content change produces a hash mismatch.

## Validation Results

Expected focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_4_3_expanded_freeze.py -q
```

Expected regression validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_3.py tests\benchmarking\test_finitexo_code_matrix_v0_3_1_intake.py tests\benchmarking\test_finitexo_code_matrix_v0_3_2_source_acquisition.py tests\benchmarking\test_finitexo_code_matrix_v0_3_3_adaptation_audit.py tests\benchmarking\test_finitexo_code_matrix_v0_4_frozen_dataset.py tests\benchmarking\test_finitexo_code_matrix_v0_4_1_expansion_intake.py tests\benchmarking\test_finitexo_code_matrix_v0_4_2_expansion_completion.py tests\benchmarking\test_finitexo_code_matrix_v0_4_3_expanded_freeze.py -q
```

## Artifacts

```txt
runs/finitexo_code_matrix_v0_4_3_expanded_freeze/expanded_freeze_summary.json
runs/finitexo_code_matrix_v0_4_3_expanded_freeze/expanded_freeze_report.md
```

## Authorized Claim

```txt
Finitexo Code Matrix v0.4.3 contains an explicitly versioned expanded frozen external/adapted candidate dataset with n=10 tasks, provenance records, and reproducible hashes.
```

## Blocked Claims

- provider superiority demonstrated;
- Xendris superiority demonstrated;
- external benchmark performance validated;
- statistical significance established;
- production-readiness proven;
- verified third-party external benchmark established unless all tasks meet that
  stricter standard.

## Safety Guarantees

```txt
providers_executed: false
model_comparison_run: false
network_required: false
env_read: false
secrets_printed: false
external_superiority_claim_authorized: false
```

## Final Decision

```txt
EXPLICIT_EXPANDED_FREEZE_N10_CREATED_NO_PROVIDER_EXECUTION
```
