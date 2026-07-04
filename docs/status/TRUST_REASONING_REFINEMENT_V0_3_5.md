# Xendris Trust Reasoning Refinement v0.3.5

Date: 2026-07-04

## Objective

Improve Xendris performance on Trust Traps Dataset v0.1 by refining
deterministic trust reasoning, evidence-conflict classification,
user-provided-origin handling, and code/production claim gating.

This refinement targets the previously weak categories:

- `evidence_conflict`
- `user_provided_without_evidence`
- `code_and_production_claims`

The goal is to improve benchmark-local admission control without changing the
dataset, inflating the rubric, degrading `normal_control`, or claiming universal
superiority.

## Categories Improved

### evidence_conflict

The reasoning layer now distinguishes:

- direct evidence conflict;
- contradicted evidence;
- partial support;
- insufficient evidence;
- claim overreach;
- source-validation gaps;
- unresolved ambiguity.

### user_provided_without_evidence

The reasoning layer now separates user-provided origin from support status:

- `USER_PROVIDED_FACT`
- `USER_PROVIDED_RULE`
- `USER_PROVIDED_POLICY`
- `USER_PROVIDED_CLAIM`
- `USER_PROVIDED_EVIDENCE_REFERENCE`

Rule:

```txt
origin = USER_PROVIDED does not imply support_status = VERIFIED
```

### code_and_production_claims

The reasoning layer now recognizes production and engineering overclaims:

- compilation is not correctness;
- a small local test count is not production readiness;
- no visible warning is not security validation;
- local benchmark behavior is not real-world performance;
- type hints are not proof of safety;
- production readiness requires multiple evidence classes.

## New Reasons And Types

New structural reasons were added where compatible with the current gate:

- `EVIDENCE_CONFLICT`
- `PARTIAL_SUPPORT`
- `CONTRADICTED_EVIDENCE`
- `INSUFFICIENT_EVIDENCE`
- `CLAIM_OVERREACH`
- `NEEDS_SOURCE_VALIDATION`
- `AMBIGUITY_NOT_RESOLVABLE`
- `PRODUCTION_READINESS_NOT_ESTABLISHED`
- `SECURITY_NOT_VALIDATED`
- `TEST_COVERAGE_INSUFFICIENT`
- `PERFORMANCE_NOT_MEASURED`
- `RUNTIME_ENVIRONMENT_MISMATCH`
- `COMPILATION_NOT_CORRECTNESS`
- `TEST_PASS_NOT_PRODUCTION_READY`
- `BENCHMARK_NOT_REAL_WORLD_PERFORMANCE`

New user-provided claim types:

- `USER_PROVIDED_FACT`
- `USER_PROVIDED_RULE`
- `USER_PROVIDED_POLICY`
- `USER_PROVIDED_CLAIM`
- `USER_PROVIDED_EVIDENCE_REFERENCE`

## Integrity Rules

- Do not alter Trust Traps Dataset v0.1.
- Do not alter the scoring rubric to raise scores.
- Do not count excluded responses as valid correct responses.
- Do not convert user-provided material into verified evidence.
- Do not use human review for deterministic exclusions.
- Use `HUMAN_REVIEW_REQUIRED` only for real unresolved conflicts or ambiguity.
- Preserve `normal_control = 1.000`.
- Do not present benchmark-local results as universal model superiority.

## Expected Impact

Expected Trust Traps v0.1 dry-run impact:

- `evidence_conflict`: from `0.500` to `>= 0.700`
- `user_provided_without_evidence`: from `0.800` to `>= 0.900`
- `code_and_production_claims`: from `0.800` to `>= 0.900`
- `normal_control`: remains `1.000`
- global Xendris score: expected `> 0.900`

## Limits

This refinement improves deterministic classification and gate compatibility
for Trust Traps v0.1. It does not prove factual truth, production safety,
general model quality, or universal superiority over any model.

Real provider runs may differ from dry-run behavior due to provider output,
latency, failures, pricing, model version, and token settings.

## Validation Commands

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_evidence_conflict_granularity.py tests/core/test_user_provided_origin_support.py tests/core/test_code_production_claims.py tests/benchmarking/test_trust_traps_regression_targets.py tests/benchmarking/test_ablation_benchmark.py tests/benchmarking/test_trust_traps_dataset.py tests/benchmarking/test_ab_benchmark_runner.py tests/core/test_trust_benchmark_gate.py tests/core/test_trust_scoring_ledger.py tests/test_xendris_response_contract.py -q
```

Full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Diff hygiene:

```powershell
git diff --check
```

## No Universal Superiority Warning

If scores improve, the claim is limited to:

```txt
Under Trust Traps Dataset v0.1 and this deterministic scoring setup, Xendris
improves benchmark-admission behavior relative to DeepSeek Base.
```

Forbidden interpretation:

```txt
Xendris is universally superior to DeepSeek or frontier models.
```
