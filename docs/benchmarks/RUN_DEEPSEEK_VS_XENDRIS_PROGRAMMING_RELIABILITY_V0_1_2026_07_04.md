# DeepSeek Base vs Xendris+DeepSeek - Programming Reliability v0.1

Date: 2026-07-04

## Purpose

Measure programming reliability under a closed dataset with executable tests,
contract preservation, basic security checks, and production-overclaim control.

## Configuration

| Field | Value |
|---|---|
| Execution mode | `real-provider` |
| Provider | `deepseek` |
| Model | `deepseek-chat` |
| Temperature | `0.0` |
| Top p | `1` |
| Max tokens | `2048` |
| Sample timeout | `2.0 s` |
| Started UTC | `2026-07-06T15:18:57.084700+00:00` |
| Dataset hash | `b882cc5558c284ccb16dcc9bf9e39ea76aedab6bdcbe47185ea55de53e78776c` |
| Xendris version | `0.2.0` |
| Python version | `3.11.9` |

## No Universal Superiority Warning

This run is valid only for Programming Reliability v0.1 under the listed
configuration. It does not imply universal programming superiority over DeepSeek
or any frontier model.

## Programming Reliability vs Production Claims

Passing benchmark-owned tests means the output satisfied this local dataset and
sandbox. It does not prove production readiness, security completeness,
operational robustness, or real-world performance.

## Global Results

| Metric | Value |
|---|---:|
| Total samples | 100 |
| DeepSeek average score | 0.770 |
| Xendris average score | 0.720 |
| Average delta | -0.050 |
| Xendris wins | 11 |
| DeepSeek wins | 16 |
| Ties | 73 |

## Category Results

| Category | DeepSeek score | Xendris score | Delta |
|---|---:|---:|---:|
| `api_contracts` | 1.000 | 0.200 | -0.800 |
| `bug_fixing` | 1.000 | 1.000 | 0.000 |
| `edge_cases` | 0.467 | 1.000 | 0.533 |
| `normal_control` | 1.000 | 1.000 | 0.000 |
| `performance` | 1.000 | 1.000 | 0.000 |
| `refactor_safety` | 1.000 | 1.000 | 0.000 |
| `security_basics` | 0.000 | 0.000 | 0.000 |
| `unit_tests` | 0.667 | 0.333 | -0.333 |

## System Diagnostics

| Metric | DeepSeek Base | Xendris+DeepSeek |
|---|---:|---:|
| Tests passed | 77 | 72 |
| Contract preserved | 100 | 100 |
| Runtime errors | 15 | 16 |
| Security risks | 8 | 12 |
| Performance regressions | 0 | 0 |
| Production overclaim rate | 0.000 | 0.000 |
| Cost per correct solution | 7.361e-05 | 0.0001055 |
| Average latency ms | 2052.39 | 2487.98 |

## Main Xendris Wins

- `PR-UNIT-TESTS-003` `unit_tests` delta `1.0`
- `PR-UNIT-TESTS-004` `unit_tests` delta `1.0`
- `PR-UNIT-TESTS-015` `unit_tests` delta `1.0`
- `PR-EDGE-CASES-001` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-002` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-003` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-004` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-008` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-009` `edge_cases` delta `1.0`
- `PR-EDGE-CASES-012` `edge_cases` delta `1.0`

## Main Xendris Losses

- `PR-UNIT-TESTS-002` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-005` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-006` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-007` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-009` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-010` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-012` `unit_tests` delta `-1.0`
- `PR-UNIT-TESTS-013` `unit_tests` delta `-1.0`
- `PR-API-CONTRACTS-001` `api_contracts` delta `-1.0`
- `PR-API-CONTRACTS-003` `api_contracts` delta `-1.0`

## Costs

Costs are estimated from provider-reported usage where available. Dry-run costs
are deterministic placeholders and not billing records.

## Latency

Latency is measured per sample by the benchmark runner and includes local
post-processing in the Xendris path.

## Limitations

- Dataset is closed and initial.
- Sandbox is intentionally narrow.
- Tests are benchmark-owned and cannot prove full correctness.
- Security detection is basic.
- Real provider results can vary by model version, account state, latency,
  prompts, and API availability.

## Next Steps

- Run real-provider mode after explicit approval to send dataset prompts to the
  external API.
- Add stronger code extraction and language-specific sandboxes.
- Add multi-model comparison against frontier providers.
