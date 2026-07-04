# Xendris v0.3.6 Trust Reasoning Ledger

## Purpose

Add a deterministic transversal reasoning layer for benchmark hygiene and
answer-audit control.

This layer catches false proxies of correctness before outputs enter benchmark
scoring. It separates origin from support, detects unsupported universal claims,
preserves response language in fallback paths, and routes unsupported scoring
rules into deterministic exclusion.

## Scope

Added:

```txt
xendris/core/trust/reasoning.py
tests/core/test_trust_reasoning.py
tests/core/test_trust_scoring_ledger.py
```

Updated:

```txt
xendris/core/trust/__init__.py
xendris/core/trust/benchmark_gate.py
xendris/benchmarks/false_formality/core/base_model_client.py
xendris/benchmarks/false_formality/core/xendris_pipeline.py
```

## New public trust objects

```txt
detect_language
evaluate_reasoning_transversally
```

## Deterministic behavior

The reasoning ledger checks:

- output language preservation for Spanish and English prompts;
- user-provided origin is not equivalent to verified support;
- unsupported scoring rules exclude outputs from scoring;
- unsupported claim premises exclude outputs from scoring;
- citation presence is not treated as correctness;
- low latency is not treated as correctness;
- universal superiority or absolute guarantee claims require evidence;
- deterministic exclusions take precedence over human review;
- genuine evidence conflicts can still require human review.

## Benchmark gate extensions

The benchmark gate now supports these exclusion reasons:

```txt
UNSUPPORTED_SCORING_RULE
UNSUPPORTED_CLAIM_PREMISE
LATENCY_PROXIED_WITHOUT_POLICY
USER_RULE_WITHOUT_EVIDENCE
```

## Why this helps model benchmarks

This layer does not raise benchmark scores directly. It prevents invalid scoring
paths from being counted as model quality:

- fallbacks cannot win by sounding safe;
- citations cannot act as proof by themselves;
- latency cannot act as correctness;
- user-provided benchmark rules require evidence;
- unsupported universal claims are excluded before scoring.

This makes benchmark lift claims more defensible when they are eventually made.

## Non-goals

This layer does not:

- call language models;
- retrieve sources;
- validate factual truth;
- compute benchmark metrics;
- replace domain review;
- prove universal model superiority.

## Validation

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py tests/core/test_trust_evidence.py tests/core/test_trust_quality_plan.py tests/core/test_trust_benchmark_gate.py tests/core/test_trust_benchmark_diagnostics.py tests/core/test_trust_reasoning.py tests/core/test_trust_scoring_ledger.py tests/test_xendris_response_contract.py tests/test_xendris_false_formality.py -q
```

Result:

```txt
78 passed
```

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.6 development milestone. It does not declare a release, tag,
benchmark result, or model-performance claim.
