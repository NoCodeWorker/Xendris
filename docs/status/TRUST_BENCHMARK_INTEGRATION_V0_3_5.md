# Xendris v0.3.5 Trust Benchmark Integration

## Purpose

Integrate the deterministic Trust Kernel benchmark controls into the
`false_formality` benchmark summary path.

The goal is to prevent benchmark wins from being counted when Xendris output is
produced by degraded runtime paths or excluded by the benchmark gate. This makes
benchmark conclusions more defensible and prevents fallback text from inflating
reported performance.

## Scope

Updated:

```txt
xendris/benchmarks/false_formality/core/types.py
xendris/benchmarks/false_formality/scorer.py
tests/test_xendris_false_formality.py
```

## Integrated trust objects

```txt
gate_benchmark_output
diagnose_benchmark_suite
BenchmarkSuiteReadiness
```

## Summary fields added

```txt
xendris_excluded_outputs
xendris_limited_outputs
xendris_inclusion_rate
xendris_average_quality_score
xendris_suite_readiness
```

## Deterministic behavior

The benchmark scorer now:

- gates model responses before scoring when runtime metadata exists;
- excludes timeout, runtime-error, and fallback outputs from scoring;
- computes effective score delta after gate exclusions;
- fails the summary if any Xendris outputs are excluded;
- computes suite-level readiness from gated Xendris outputs;
- exposes inclusion rate and average gated quality score.

## Why this helps model benchmarks

This integration does not claim that Xendris improves all benchmarks. It makes
benchmark claims harder to fake:

- fallback text cannot win by looking cautious;
- runtime failures cannot count as competence;
- suite-level readiness is visible;
- pass/fail is tied to both wins and gate integrity;
- benchmark conclusions remain conservative.

This is necessary before any honest claim of benchmark lift can be made.

## Non-goals

This integration does not:

- call providers;
- add new model logic;
- alter prompts;
- compute universal performance claims;
- validate scientific truth;
- replace external benchmark review.

## Validation

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_xendris_false_formality.py -q
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py tests/core/test_trust_evidence.py tests/core/test_trust_quality_plan.py tests/core/test_trust_benchmark_gate.py tests/core/test_trust_benchmark_diagnostics.py tests/test_xendris_response_contract.py -q
```

Result:

```txt
9 passed
49 passed
```

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.5 development milestone. It does not declare a release, tag,
benchmark result, or model-performance claim.
