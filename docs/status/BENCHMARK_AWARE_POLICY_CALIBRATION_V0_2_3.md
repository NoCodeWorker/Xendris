# Benchmark-Aware Policy Calibration v0.2.3

## Objective

Implement a deterministic, non-invasive calibration layer that makes Xendris
aware that intervention can help or harm depending on domain, benchmark
category, and execution mode.

Core principle:

```txt
No intervention without domain-calibrated benefit.
```

## Motivation

Programming Reliability v0.1 real-provider results showed mixed behavior:

| Metric | DeepSeek Base | Xendris+DeepSeek |
|---|---:|---:|
| Average score | 0.77 | 0.72 |
| Tests passed | 77 / 100 | 72 / 100 |
| Runtime errors | 15 | 16 |
| Security risks | 8 | 12 |
| Average latency | 2052 ms | 2488 ms |
| Total cost | $0.0057 | $0.0076 |

Category result:

| Category | DeepSeek Base | Xendris+DeepSeek | Interpretation |
|---|---:|---:|---|
| `api_contracts` | 1.0 | 0.2 | Xendris over-intervened |
| `bug_fixing` | 1.0 | 1.0 | tie |
| `edge_cases` | 0.47 | 1.0 | Xendris helped |
| `normal_control` | 1.0 | 1.0 | tie |
| `performance` | 1.0 | 1.0 | tie |
| `refactor_safety` | 1.0 | 1.0 | tie |
| `security_basics` | 0.0 | 0.0 | tie |
| `unit_tests` | 0.67 | 0.33 | Xendris over-intervened |

## Root Cause

Xendris can harm benchmark performance in restricted programming sandboxes when
it adds:

- exhaustive validations;
- complex imports;
- test-framework dependencies;
- additional tests;
- production-grade checks in benchmark-only contexts.

Observed failure patterns included:

- `ImportError: __import__ not found`
- `NameError: name 'complex' is not defined`
- security-risk false positives from coarse sandbox pattern matching

## Implemented Policy

Created experimental module:

```txt
xendris.core.calibration
```

Files:

- `xendris/core/calibration/__init__.py`
- `xendris/core/calibration/domain.py`
- `xendris/core/calibration/intervention.py`
- `xendris/core/calibration/programming_policy.py`
- `xendris/core/calibration/audit.py`

Implemented primitives:

- `ExecutionMode`
- `InterventionLevel`
- `Domain`
- `ProgrammingCategory`
- `InterventionDecision`
- `CalibrationMetrics`
- `CalibrationAudit`
- `ProgrammingInterventionPolicy`

## Policy Behavior

### API Contracts

For `PROGRAMMING / API_CONTRACTS` in `BENCHMARK_EXECUTION` or `CODE_SANDBOX`:

- intervention level: `MINIMAL`
- preserve signature: `true`
- extra imports: `false`
- runtime type checks: `false`
- test-framework imports: `false`
- prefer minimal patch: `true`

### Edge Cases

For `PROGRAMMING / EDGE_CASES`:

- intervention level: `MODERATE`
- preserve signature: `true`
- extra imports: `false`
- runtime type checks: `true` only when no import is required
- prefer minimal patch: `true`

### Unit Tests

For `PROGRAMMING / UNIT_TESTS` in `CODE_SANDBOX`:

- test-framework imports are disabled by default;
- plain `assert` tests are preferred;
- `pytest` dependency is avoided unless explicitly allowed later.

### Security Basics

For `PROGRAMMING / SECURITY_BASICS`:

- security scan is required;
- false-positive warning is recorded because sandbox pattern matching can be
  coarse.

### Production

For `PRODUCTION` mode:

- stronger checks are allowed than in benchmark mode;
- explicit API contracts remain protected;
- production claims still require deployment/test evidence elsewhere in the
  governance stack.

## Metrics Structures

Defined but not computed without fixture data:

- `intervention_gain_rate`
- `intervention_harm_rate`
- `false_positive_security_rate`
- `sandbox_import_failure_rate`
- `overengineering_failure_rate`
- `minimal_solution_preservation_rate`
- `domain_calibration_score`

## Validation

Added:

```txt
tests/core/test_intervention_calibration_policy.py
```

Required command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_intervention_calibration_policy.py -q
```

Broader recommended command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Limitations

- The module does not rewrite code.
- The module does not change benchmark scores.
- The module does not call providers.
- The module does not run real-provider benchmarks.
- The module is not a stable public API yet.
- The module encodes deterministic policy decisions only.
- Metrics are structural placeholders until measured fixture data is supplied.

## Non-Claims

This work does not show that Xendris improves programming globally.

It does not hide the negative Programming Reliability result.

It does not imply universal model superiority.

It only adds a policy layer that makes future interventions more category-aware
and less likely to overengineer benchmark-constrained programming tasks.

## Next Step

Integrate `ProgrammingInterventionPolicy` into programming benchmark runners in
a dry-run-only pathway first, then measure whether it reduces overengineering
failures without lowering the edge-case gains.
