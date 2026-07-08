# Finitexo Code Matrix v0.5.1 - Real Provider Smoke on Frozen n=10

## Purpose

Finitexo Code Matrix v0.5.1 defines the first real-provider smoke execution
layer for the explicitly frozen v0.4.3 n=10 dataset.

This phase validates real-provider configuration gates, response capture,
failure handling, cost tracking, diagnostic scoring and conservative reporting.
It does not validate statistical performance.

This phase is diagnostic-only.

No statistical claim is authorized.
No provider superiority claim is authorized.
No Xendris superiority claim is authorized.

## Relation to v0.5

v0.5 implemented provider-smoke dry-run plumbing in mock mode.

v0.5.1 extends that structure for real provider mode while preserving the v0.5
mock smoke path and tests.

## Relation to v0.4.3

Input dataset:

```txt
benchmarks/finitexo_code_matrix_v0_4_3/
```

The frozen v0.4.3 dataset is not modified by this phase.

## Dataset Integrity

```txt
dataset_hash: a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4
manifest_hash: 6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e
frozen_task_count: 10
```

## Provider Mode

```txt
provider_mode: real
mock_fallback_allowed: false
```

The default real-provider configuration targets:

- DeepSeek `deepseek-v4-flash`
- OpenAI `gpt-4.1-nano`

Provider API keys are read only from process environment mappings supplied to
the config. `.env` files are not read by the v0.5.1 gate or tests.

## Real Provider Gate

The gate verifies:

- dataset hash;
- manifest hash;
- frozen task count;
- explicit real-provider confirmation;
- provider key presence by provider name only;
- bounded budget;
- `max_iterations_per_task = 1`;
- `temperature = 0.0`;
- bounded max tokens;
- mock fallback disabled;
- statistical, provider superiority, Xendris superiority and external
  benchmark validation claims disabled.

If configuration is missing, execution is blocked before any provider call.

## Execution Summary

The committed v0.5.1 implementation uses deterministic tests with stub adapters.
No real provider call is executed as part of repository validation.

Expected decisions:

```txt
REAL_PROVIDER_SMOKE_ON_FROZEN_N10_COMPLETED_NO_STATISTICAL_CLAIM
REAL_PROVIDER_SMOKE_READY_CONFIGURATION_MISSING_NO_EXECUTION
REAL_PROVIDER_SMOKE_ATTEMPTED_ALL_PROVIDERS_FAILED_NO_CLAIM
```

## Budget Summary

Default budget cap:

```txt
0.50 USD
```

Recommended target:

```txt
0.05 USD
```

Budget-blocked attempts are recorded as blocked attempts. They are not hidden
and do not trigger mock fallback.

## Scoring Summary

Scoring remains diagnostic only.

The v0.5 scorer does not execute hidden tests and does not authorize hidden-test
validation claims.

## Provider Failures

Provider failures are captured per provider and task with sanitized error text.

Provider failures do not become positive evidence and are not hidden.

## Generated Artifacts

Expected output directory:

```txt
runs/finitexo_code_matrix_v0_5_1_real_provider_smoke/
```

Required artifact names:

```txt
real_provider_smoke_summary.json
real_provider_smoke_report.md
real_provider_responses.jsonl
real_provider_scores.jsonl
real_provider_costs.json
real_provider_errors.jsonl
real_provider_gate.json
```

## Limitations

- n=10 smoke execution is not statistically conclusive.
- Diagnostic scoring is not external benchmark validation.
- Real provider execution is not production-readiness proof.
- Provider errors are execution facts, not benchmark failure by themselves.
- Results must not be generalized beyond this frozen dataset and configuration.

## Authorized Claims

If real provider smoke completes:

```txt
Finitexo Code Matrix v0.5.1 completed a real-provider smoke test on the frozen v0.4.3 n=10 dataset.
```

If configuration is missing:

```txt
Finitexo Code Matrix v0.5.1 is ready for real-provider smoke execution, but real execution was not run because explicit provider configuration was missing.
```

## Blocked Claims

- provider superiority demonstrated;
- Xendris superiority demonstrated;
- statistical significance established;
- external benchmark performance validated;
- production-readiness proven;
- verified third-party benchmark performance proven;
- broad model-quality conclusion established.

## Final Decision

```txt
REAL_PROVIDER_SMOKE_READY_CONFIGURATION_MISSING_NO_EXECUTION
```

This status document records implementation readiness. Actual real-provider
execution requires explicit runtime configuration and must generate fresh
artifacts.
