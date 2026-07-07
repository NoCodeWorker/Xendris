# Finitexo Code Matrix v0.3.3 - External Adaptation + Contamination Audit

## Purpose

v0.3.3 adds a conservative audit layer for adapted source material.

The goal is to decide whether an acquired source can become a safe adapted
candidate in a future version, without promoting anything into the frozen
benchmark dataset.

## Scope

Implemented:

- adaptation record model;
- adaptation type, validity, fit, leakage, difficulty and recommendation enums;
- deterministic adaptation diff heuristics;
- contamination audit;
- leakage controls;
- task validity review;
- difficulty estimator;
- adaptation recommendation gate;
- local fixture adaptation examples;
- JSON and Markdown report generation.

## Boundary

```txt
acquisition_record != benchmark_task
adapted_candidate != frozen_benchmark_task
audit_pass != dataset_promotion
```

## Example Records

Five local fixture records were added:

- clean `EXTERNAL_VERIFIED` direct port recommended for future freeze;
- `EXTERNAL_ADAPTED` API normalization requiring human review;
- rejected synthetic expansion with weak source preservation;
- blocked mutated internal fixture;
- invalid task depending on live network state or secrets.

The examples are not benchmark tasks.

## Decision Logic

A candidate may receive `RECOMMEND_FOR_FUTURE_FREEZE` only if:

- source origin is `EXTERNAL_VERIFIED` or `EXTERNAL_ADAPTED`;
- adaptation type is not `SYNTHETIC_EXPANSION` or `MUTATED_INTERNAL_FIXTURE`;
- contamination risk is `LOW`;
- leakage risk is `LOW` or `MEDIUM`;
- task validity is `VALID` or `VALID_WITH_WARNINGS`;
- benchmark fit is `FIT_FOR_AGENTIC_PROGRAMMING` or `FIT_WITH_LIMITATIONS`;
- semantic preservation is at least `0.70`;
- structural change is at most `0.65`;
- difficulty shift is at most `0.50`;
- source and adapted hashes are present;
- adaptation summary is present;
- rejection reasons are empty.

Recommendation metadata does not promote the dataset.

## Generated Artifacts

```txt
runs/finitexo_code_matrix_v0_3_3_adaptation_audit/adaptation_audit_summary.json
runs/finitexo_code_matrix_v0_3_3_adaptation_audit/adaptation_audit_report.md
```

## Non-Claims

This phase does not:

- execute providers;
- require network access;
- read `.env`;
- print secrets;
- modify the frozen v0.3 dataset;
- authorize external superiority claims;
- validate external benchmark performance.

## Final Decision

```txt
EXTERNAL_ADAPTATION_AUDIT_IMPLEMENTED_NO_FROZEN_DATASET_CHANGE
```

