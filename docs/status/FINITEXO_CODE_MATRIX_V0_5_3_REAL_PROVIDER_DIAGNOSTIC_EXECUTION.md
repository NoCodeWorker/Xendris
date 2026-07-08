# Finitexo Code Matrix v0.5.3 - Real Provider Diagnostic Execution

## Purpose

v0.5.3 defines explicit real-provider diagnostic execution over the frozen
v0.4.3 n=10 dataset after the v0.5.2 release gate approves the infrastructure.

This phase is diagnostic-only.

No statistical claim is authorized.
No provider superiority claim is authorized.
No Xendris superiority claim is authorized.

## Preconditions

Execution requires:

- release gate decision `APPROVED_FOR_EXPLICIT_REAL_PROVIDER_DIAGNOSTIC_EXECUTION`;
- process environment `FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM=true`;
- process environment `OPENAI_API_KEY`;
- process environment `DEEPSEEK_API_KEY`;
- budget cap configured;
- frozen dataset hash and manifest hash verified.

The implementation does not read `.env` files and does not print secret values.

## Frozen Dataset Contract

```txt
dataset_hash: a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4
manifest_hash: 6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e
frozen_task_count: 10
```

## Current Artifact State

The repository-generated artifact state is blocked because explicit process
environment confirmation and provider keys were not supplied during validation.

```txt
final_decision: REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING
expected_provider_task_attempts: 20
providers_attempted: none
total_estimated_cost_usd: 0
```

## Generated Artifacts

```txt
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_diagnostic_summary.json
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_diagnostic_report.md
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_responses.jsonl
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_scores.jsonl
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_costs.json
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_errors.jsonl
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/real_provider_gate.json
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/provider_request_metadata.jsonl
runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution/provider_preflight.json
```

## Final Decision

```txt
REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING
```
