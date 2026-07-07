# Finitexo Code Matrix v0.3.2 - External Source Acquisition Gate

## Purpose

This phase adds a conservative acquisition gate for external source material.

It does not create an external benchmark dataset. It only defines how external
or adapted source material can be recorded, snapshotted, normalized, evaluated,
and rejected before any future dataset-promotion phase.

## Scope

Implemented:

- source acquisition record model;
- source type and contamination risk enums;
- deterministic promotion-eligibility gate;
- local snapshot hash utility;
- contamination text helper;
- local fixture acquisition records;
- summary/report artifact builder;
- manifest acquisition policy.

## Boundary

```txt
acquisition_record != benchmark_task
eligible_for_future_promotion != promoted_to_dataset
```

The frozen v0.3 seed dataset was not modified.

## Provider Execution

```txt
providers_executed: false
```

No provider calls were made. No `.env` file was read. No network access is
required for this phase.

## Example Records

Four local fixture records were added:

- one valid `EXTERNAL_VERIFIED`-style record with `LOW` contamination risk;
- one valid `EXTERNAL_ADAPTED`-style record with `MEDIUM` contamination risk;
- one rejected record due to missing/unknown license;
- one blocked record due to `BLOCKED` contamination risk.

These examples are not benchmark tasks.

## Policy

A record may only become eligible for future promotion when:

- origin candidate is `EXTERNAL_VERIFIED` or `EXTERNAL_ADAPTED`;
- source URL is present;
- source hash is present;
- license is present and not `UNKNOWN`;
- contamination risk is `LOW` or `MEDIUM`;
- raw snapshot path is present;
- adaptation notes exist when adaptation is required;
- rejection reasons are empty.

## Claims

No external superiority claim is authorized.

Acquisition eligibility is operational metadata only. It does not measure model
performance and does not authorize externality or benchmark claims.

## Artifacts

Expected generated artifacts:

```txt
runs/finitexo_code_matrix_v0_3_2_source_acquisition/source_acquisition_summary.json
runs/finitexo_code_matrix_v0_3_2_source_acquisition/source_acquisition_report.md
```

## Final Decision

```txt
SOURCE_ACQUISITION_GATE_IMPLEMENTED_NO_DATASET_PROMOTION
```

