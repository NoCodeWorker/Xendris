# Xendris v0.3.4 Trust Benchmark Diagnostics

## Purpose

Add deterministic diagnostics for a complete benchmark run after each output has
passed through the Trust Kernel benchmark gate.

The diagnostics layer converts per-output gate results into a suite-level
readiness decision. It is designed to make benchmark runs more auditable,
cleaner, and easier to improve without pretending that benchmark scores have
already increased.

## Scope

Added:

```txt
xendris/core/trust/benchmark_diagnostics.py
tests/core/test_trust_benchmark_diagnostics.py
```

Updated:

```txt
xendris/core/trust/__init__.py
```

## New public trust objects

```txt
BenchmarkSuiteReadiness
BenchmarkSuiteDiagnostics
diagnose_benchmark_suite
```

## Readiness states

```txt
EXCELLENT
USABLE_WITH_LIMITATIONS
NEEDS_REMEDIATION
BLOCKED
```

## Deterministic behavior

The diagnostics layer computes:

- total outputs;
- included outputs;
- limited outputs;
- excluded outputs;
- inclusion rate;
- average trust quality score;
- suite readiness;
- improvement actions.

Decision rules:

- empty runs are blocked;
- fully excluded runs are blocked;
- runtime degradation or excluded outputs require remediation;
- limited outputs are usable only with limitations;
- all-clean high-quality outputs are marked excellent;
- all-clean lower-quality outputs remain usable with limitations.

## Why this helps model benchmarks

This layer does not directly optimize model behavior. It improves the
benchmark-control loop around model behavior:

- degraded runtime paths become visible;
- unsupported or review-blocked answers cannot silently enter scoring;
- limited outputs carry explicit caveat requirements;
- suite-level readiness becomes reproducible;
- improvement actions are derived from deterministic gate outcomes.

This is a benchmark potency layer because it gives orchestration and evaluation
code a concrete control signal before interpreting benchmark results.

## Non-goals

This layer does not:

- compute benchmark task scores;
- compare providers;
- call language models;
- retrieve external sources;
- rewrite answers;
- claim that Xendris improves every benchmark;
- replace human review;
- validate factual truth.

## Validation

Focused validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py tests/core/test_trust_evidence.py tests/core/test_trust_quality_plan.py tests/core/test_trust_benchmark_gate.py tests/core/test_trust_benchmark_diagnostics.py tests/test_xendris_response_contract.py -q
```

Result:

```txt
49 passed
```

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.4 development milestone. It does not declare a release, tag,
benchmark result, or model-performance claim.
