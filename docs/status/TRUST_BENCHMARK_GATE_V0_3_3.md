# Xendris v0.3.3 Trust Benchmark Gate

## Purpose

Add a deterministic benchmark-readiness gate for audited model outputs.

The gate protects evaluation suites from scoring outputs that are structurally
unsafe, review-blocked, limited without caveats, or produced by degraded runtime
paths such as timeouts, provider errors, and fallback responses.

## Scope

Added:

```txt
xendris/core/trust/benchmark_gate.py
tests/core/test_trust_benchmark_gate.py
```

Updated:

```txt
xendris/core/trust/__init__.py
xendris/benchmarks/false_formality/core/types.py
xendris/benchmarks/false_formality/scorer.py
tests/test_xendris_false_formality.py
```

## New public trust objects

```txt
BenchmarkGateDecision
BenchmarkExclusionReason
BenchmarkGateResult
gate_benchmark_output
```

## Deterministic behavior

The gate applies conservative rules:

- timeout outputs are excluded from scoring;
- runtime error outputs are excluded from scoring;
- fallback outputs are excluded from scoring;
- not-ready trust quality plans are excluded from scoring;
- ready-with-limitations plans may be included only with limitation notes;
- ready plans may be included without limitation notes.

Runtime degradation takes precedence over textual readiness.

## False-formality benchmark integration

The false-formality scorer now records optional benchmark gate metadata:

```txt
base_gate_decision
xendris_gate_decision
base_gate_reason
xendris_gate_reason
base_include_in_scoring
xendris_include_in_scoring
```

When a response is excluded by the gate, its effective score for winner
selection is treated as `0.0`, while the original rubric score remains recorded
for auditability. This prevents fallback text or degraded runtime paths from
winning a benchmark case.

The benchmark summary also refuses a passing decision when any Xendris output
is excluded by the gate.

## Why this helps model benchmarks

This layer does not improve scores directly. It improves benchmark integrity by
ensuring that only structurally eligible outputs enter scoring. This prevents
degraded runtime paths, unsupported high-confidence answers, and review-blocked
answers from polluting benchmark measurements.

It is a benchmark potency layer because it gives orchestration code a
deterministic, reproducible decision before scoring an answer.

## Non-goals

This layer does not:

- compute benchmark metrics;
- compare model providers;
- call language models;
- retrieve sources;
- validate factual truth;
- rewrite answers;
- claim that Xendris improves every benchmark;
- replace human review.

## Validation

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_xendris_false_formality.py tests/core/test_trust_benchmark_gate.py tests/core/test_trust_quality_plan.py -q
```

Result:

```txt
23 passed
```

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.3 development milestone. It does not declare a release, tag,
benchmark result, or model-performance claim.
