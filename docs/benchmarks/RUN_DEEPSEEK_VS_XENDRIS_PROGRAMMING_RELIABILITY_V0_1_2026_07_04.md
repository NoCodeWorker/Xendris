# DeepSeek Base vs Xendris+DeepSeek - Programming Reliability v0.1

Date: 2026-07-04

## Purpose

Measure programming reliability under a closed dataset with executable tests,
contract preservation, basic security checks, and production-overclaim control.

## Configuration

| Field | Value |
|---|---|
| Execution mode | `dry-run` |
| Provider | `mock` |
| Model | `deepseek-chat` |
| Temperature | `0.0` |
| Top p | `1` |
| Max tokens | `2048` |
| Sample timeout | `2.0 s` |
| Started UTC | `2026-07-06T10:33:03.424807+00:00` |
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
| DeepSeek average score | 0.700 |
| Xendris average score | 1.000 |
| Average delta | 0.300 |
| Xendris wins | 30 |
| DeepSeek wins | 0 |
| Ties | 70 |

## Category Results

| Category | DeepSeek score | Xendris score | Delta |
|---|---:|---:|---:|
| `api_contracts` | 1.000 | 1.000 | 0.000 |
| `bug_fixing` | 0.000 | 1.000 | 1.000 |
| `edge_cases` | 1.000 | 1.000 | 0.000 |
| `normal_control` | 1.000 | 1.000 | 0.000 |
| `performance` | 1.000 | 1.000 | 0.000 |
| `refactor_safety` | 1.000 | 1.000 | 0.000 |
| `security_basics` | 0.000 | 1.000 | 1.000 |
| `unit_tests` | 1.000 | 1.000 | 0.000 |

## System Diagnostics

| Metric | DeepSeek Base | Xendris+DeepSeek |
|---|---:|---:|
| Tests passed | 70 | 100 |
| Contract preserved | 100 | 100 |
| Runtime errors | 20 | 0 |
| Security risks | 10 | 0 |
| Performance regressions | 0 | 0 |
| Production overclaim rate | 0.000 | 0.000 |
| Cost per correct solution | 0.00014286 | 0.00012 |
| Average latency ms | 100.00 | 110.00 |

## Main Xendris Wins

- `PR-BUG-FIXING-001` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-002` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-003` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-004` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-005` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-006` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-007` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-008` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-009` `bug_fixing` delta `1.0`
- `PR-BUG-FIXING-010` `bug_fixing` delta `1.0`

## Main Xendris Losses

- None recorded.

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
