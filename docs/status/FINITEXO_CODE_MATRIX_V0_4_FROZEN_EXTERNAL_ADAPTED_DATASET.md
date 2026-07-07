# Finitexo Code Matrix v0.4 - Frozen External/Adapted Dataset

## Purpose

Finitexo Code Matrix v0.4 creates the first frozen external/adapted candidate
dataset after the v0.3.x trust infrastructure block.

The purpose is to freeze a small, provenance-linked, hash-protected dataset
without executing providers, comparing models, or authorizing external
superiority claims.

## Scope

Implemented:

- frozen dataset package at `benchmarks/finitexo_code_matrix_v0_4/`;
- frozen dataset manifest;
- frozen task records;
- provenance records;
- deterministic hash registry;
- frozen dataset policy;
- validation helpers;
- generated freeze summary and report.

## Relation To v0.3.x

v0.4 depends on:

- v0.3 adversarial benchmark infrastructure;
- v0.3.1 external dataset intake;
- v0.3.2 external source acquisition gate;
- v0.3.3 external adaptation and contamination audit;
- v0.3.x trust infrastructure closure.

The v0.3.x closure declared:

```txt
V0_3_X_TRUST_INFRASTRUCTURE_COMPLETE
READY_FOR_V0_4_EXTERNAL_DATASET_FREEZE
NO_EXTERNAL_SUPERIORITY_CLAIM_AUTHORIZED
```

## Dataset Boundary

```txt
candidate_pool != frozen_benchmark_dataset
acquisition_record != benchmark_task
adapted_candidate != frozen_benchmark_task
audit_pass != dataset_promotion
frozen_dataset_created != provider_performance_validated
```

## Frozen Task Count

```txt
frozen_task_count: 2
minimum_task_target: 3
minimum_task_target_met: false
```

Only two v0.3.3 records were eligible for future freeze or human-review freeze.
The third-task target is intentionally not met because weaker, blocked,
mutated, synthetic, network-dependent, or secret-dependent records were not
promoted to inflate the dataset.

## Provenance Guarantees

Every frozen task has a linked provenance record containing:

- source id;
- source URL;
- source license;
- source hash;
- adapted candidate hash;
- frozen task hash;
- acquisition record path;
- adaptation record path;
- promotion gate result;
- human review status;
- limitations;
- non-claims.

## Hash Guarantees

The frozen dataset includes:

- dataset hash;
- manifest hash;
- task hashes;
- provenance hashes;
- SHA-256 algorithm declaration.

The validator recomputes the hashes and blocks interpretation if the current
content no longer matches `frozen_dataset_hashes.json`.

## Validation Results

Expected validation command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_4_frozen_dataset.py -q
```

Expected broader regression command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_3.py tests\benchmarking\test_finitexo_code_matrix_v0_3_1_intake.py tests\benchmarking\test_finitexo_code_matrix_v0_3_2_source_acquisition.py tests\benchmarking\test_finitexo_code_matrix_v0_3_3_adaptation_audit.py tests\benchmarking\test_finitexo_code_matrix_v0_4_frozen_dataset.py -q
```

## Generated Artifacts

```txt
runs/finitexo_code_matrix_v0_4_freeze/frozen_dataset_summary.json
runs/finitexo_code_matrix_v0_4_freeze/frozen_dataset_report.md
```

## Authorized Claim

```txt
Finitexo Code Matrix v0.4 contains a frozen external/adapted candidate dataset with provenance and hash controls.
```

## Blocked Claims

- provider superiority demonstrated;
- Xendris superiority demonstrated;
- external benchmark performance validated;
- statistical significance established;
- production-readiness proven;
- verified third-party external benchmark, because not all tasks are truly
  `EXTERNAL_VERIFIED` with strong provenance.

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
FROZEN_EXTERNAL_ADAPTED_DATASET_CREATED_NO_PROVIDER_EXECUTION
```
