# Finitexo Code Matrix v0.5.5 - Real Provider Evidence Integrity Gate

## Purpose

v0.5.5 validates the integrity of the v0.5.4 diagnostic real-provider
artifacts.

This gate does not execute providers, does not read `.env`, does not print
secrets, does not recalculate scores with models and does not authorize
statistical, provider-superiority or Xendris-superiority claims.

## Input Evidence

```txt
runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/
```

## Required Dataset Contract

```txt
dataset_hash: a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4
manifest_hash: 6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e
frozen_task_count: 10
```

## Checks

- summary/gate/report/artifact presence;
- dataset and manifest hash consistency;
- provider and task count arithmetic;
- response, score and metadata traceability by `(provider_name, task_id)`;
- provider cost breakdown consistency;
- no mock fallback;
- no mock/stub/fake/simulated/dry-run text in execution artifacts;
- no unauthorized statistical, provider-superiority or Xendris-superiority
  claims.

## Final Decision

Expected when all checks pass:

```txt
REAL_PROVIDER_EVIDENCE_INTEGRITY_APPROVED_DIAGNOSTIC_ONLY
```

This approval means only that the v0.5.4 evidence artifacts are internally
consistent and diagnostic-only. It does not authorize a benchmark-performance
claim or any superiority claim.
