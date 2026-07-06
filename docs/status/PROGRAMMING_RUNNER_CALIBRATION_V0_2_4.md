# Programming Runner Calibration v0.2.4

## Objective

Integrate the experimental benchmark-aware intervention calibration policy into
the Programming Reliability runner without changing stable runtime behavior or
rewriting historical benchmark results.

Core principle:

```txt
No intervention without domain-calibrated benefit.
```

## Motivation

Programming Reliability v0.1 real-provider results were mixed:

| Metric | DeepSeek Base | Xendris+DeepSeek |
|---|---:|---:|
| Global score | 0.77 | 0.72 |
| `edge_cases` | 0.47 | 1.00 |
| `api_contracts` | 1.00 | 0.20 |
| `unit_tests` | 0.67 | 0.33 |

The result suggests that Xendris helped on edge cases but over-intervened in
restricted programming benchmark contexts. The common failure modes were
import-heavy answers, runtime wrappers, framework-specific test imports, and
production-grade checks inside a narrow sandbox.

## What Was Integrated

The Programming Reliability runner now accepts an experimental calibration flag
through config:

```python
{"experimental_calibration": True}
```

The A/B script also exposes:

```powershell
.\.venv\Scripts\python.exe scripts\run_deepseek_vs_xendris_programming_reliability.py --dry-run --experimental-calibration
```

When enabled, the Xendris path uses:

```txt
xendris.core.calibration.ProgrammingInterventionPolicy
```

The default execution mode is:

```txt
CODE_SANDBOX
```

## Default-Off Behavior

Calibration is disabled by default.

When disabled:

- no calibration audit block is emitted;
- no calibration summary metrics are required;
- existing result payload shape remains unchanged;
- historical benchmark scores are not rewritten;
- no provider calls are introduced.

## Audit Fields

When enabled, each calibrated result can include:

- `calibration_enabled`
- `domain`
- `category`
- `execution_mode`
- `intervention_level`
- `preserve_signature`
- `allow_extra_imports`
- `allow_runtime_type_checks`
- `allow_test_framework_imports`
- `prefer_minimal_patch`
- `require_security_scan`
- `rationale`
- `warnings`

## Summary Metrics

When enabled, summaries can include:

- `calibrated_samples`
- `minimal_intervention_samples`
- `moderate_intervention_samples`
- `strong_intervention_samples`
- `import_restricted_samples`
- `signature_preservation_required_samples`
- `test_framework_import_restricted_samples`
- `security_false_positive_warning_samples`

These are structural policy metrics only. They are not improvement metrics
unless computed against actual benchmark outcomes.

## Policy Effects

### API Contracts

In benchmark/sandbox mode:

- minimal intervention;
- preserve exact function signature;
- no extra imports;
- no runtime type-checking wrappers;
- no test-framework imports;
- prefer minimal patch.

### Unit Tests

In code sandbox mode:

- prefer plain `assert`;
- avoid `pytest` imports and framework fixtures by default.

### Edge Cases

- moderate intervention;
- preserve signature;
- avoid imports by default;
- allow simple boundary handling.

### Security Basics

- keep security scan;
- record false-positive warning for coarse pattern-based detection.

## Validation Commands

Required:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_programming_runner_calibration_integration.py -q
.\.venv\Scripts\python.exe -m pytest tests\core\test_intervention_calibration_policy.py -q
git diff --check
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_2.py
```

Recommended:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Observed Results

Focused integration validation:

```txt
10 passed
```

Existing calibration policy validation:

```txt
10 passed
```

Full Python suite:

```txt
1508 passed, 5 warnings
```

Release gate v0.2.2 before commit:

```txt
BLOCKED only because working tree was dirty with this implementation.
All release subchecks passed.
```

## Limitations

- This is experimental.
- It does not change benchmark scores by itself.
- It does not rewrite historical artifacts.
- It does not run real providers.
- It does not prove global programming improvement.
- It does not promote calibration to stable public API.
- It only controls category-aware intervention policy in the runner.

## Non-Claims

This work does not show that Xendris is better at programming globally.

It does not hide the negative Programming Reliability result.

It does not imply universal superiority over DeepSeek or any frontier model.

It only makes the future Xendris programming path more aware that intervention
can help in one category and harm in another.

## Next Recommended Step

Run an experimental dry-run comparison with calibration enabled and compare:

- overengineering failures;
- sandbox import failures;
- edge-case preservation;
- API contract preservation;
- unit-test category behavior.

Only after a dry-run improvement is measured should real-provider execution be
considered.
