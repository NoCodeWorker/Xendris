# Xendris v0.3.2 Trust Quality Plan

## Purpose

Add a deterministic quality planning layer to the Xendris Trust Kernel.

The layer converts a structural reasoning audit into a conservative operational
plan that can be used before model outputs enter benchmark or evaluation flows.
It is designed to improve benchmark hygiene and answer quality without gaming
benchmarks, calling models, rewriting answers, or claiming factual validation.

## Scope

Added:

```txt
xendris/core/trust/quality.py
tests/core/test_trust_quality_plan.py
```

Updated:

```txt
xendris/core/trust/__init__.py
```

## New public trust objects

```txt
QualityAction
QualityPriority
BenchmarkReadiness
QualityDimension
QualityImprovementPlan
build_quality_improvement_plan
validate_quality_improvement_plan
```

## Deterministic behavior

The planner applies conservative rules:

- blocked or critical audits are not benchmark-ready;
- high-risk audits require human review or stronger evidence;
- non-conservative Response Contract assessments downgrade readiness;
- answers with unsupported claims are usable only with limitations;
- low-risk approved audits are structurally benchmark-ready;
- structural readiness is not factual validation.

The module also exposes `validate_quality_improvement_plan`, a deterministic
contract check that rejects internally incoherent plans and prevents blocked or
human-review-required audits from being treated as benchmark-ready.

## Why this helps model benchmarks

This layer does not directly optimize model scores. Instead, it improves the
quality control path around model outputs:

- unsafe or contradicted outputs are blocked before evaluation;
- high-confidence unsupported outputs require review;
- limited outputs carry explicit caveats;
- structurally clean outputs can be routed into benchmark use;
- benchmark readiness becomes inspectable and reproducible.
- response-contract overclaim signals can prevent premature full readiness.

This is a potency layer because it gives orchestration code a deterministic way
to decide what must happen next before an answer is used, compared, or scored.

## Non-goals

This layer does not:

- call language models;
- extract claims automatically;
- retrieve sources;
- validate truth;
- rewrite responses;
- compute benchmark metrics;
- claim that Xendris improves every benchmark;
- replace human review.

## Validation

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py tests/core/test_trust_evidence.py tests/core/test_trust_quality_plan.py tests/test_xendris_response_contract.py -q
```

Result:

```txt
36 passed
```

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.2 development milestone. It does not declare a release, tag,
benchmark result, or model-performance claim.
