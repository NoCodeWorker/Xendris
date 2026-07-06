# Programming Calibration Ablation v0.2.5

## Purpose

Measure whether experimental benchmark-aware calibration reduces Xendris
overengineering harm in Programming Reliability v0.1 while preserving useful
edge-case behavior.

## Configuration

| Field | Value |
|---|---|
| Dataset | `Programming Reliability v0.1` |
| Dataset version | `0.1` |
| Dataset hash | `b882cc5558c284ccb16dcc9bf9e39ea76aedab6bdcbe47185ea55de53e78776c` |
| Execution mode | `dry-run` |
| Provider mode | `mock` |
| Variants | `deepseek_base, xendris_uncalibrated, xendris_calibrated` |
| Historical artifacts overwritten | `False` |

## No Universal Superiority Warning

This dry-run ablation does not imply universal superiority and does not show
global programming improvement.

## No External Provider Warning

This run uses deterministic local mock behavior only. It does not measure
external provider behavior.

## Global Scores

| Variant | Score |
|---|---:|
| `deepseek_base` | 0.900 |
| `xendris_uncalibrated` | 0.650 |
| `xendris_calibrated` | 1.000 |

## Score Deltas

| Delta | Value |
|---|---:|
| calibrated vs uncalibrated | 0.350 |
| calibrated vs base | 0.100 |
| uncalibrated vs base | -0.250 |

## Category Breakdown

| Category | Base | Uncalibrated | Calibrated | Calibrated vs uncalibrated |
|---|---:|---:|---:|---:|
| `api_contracts` | 1.000 | 0.000 | 1.000 | 1.000 |
| `bug_fixing` | 1.000 | 1.000 | 1.000 | 0.000 |
| `edge_cases` | 1.000 | 1.000 | 1.000 | 0.000 |
| `normal_control` | 1.000 | 1.000 | 1.000 | 0.000 |
| `performance` | 1.000 | 1.000 | 1.000 | 0.000 |
| `refactor_safety` | 1.000 | 1.000 | 1.000 | 0.000 |
| `security_basics` | 0.000 | 0.000 | 1.000 | 1.000 |
| `unit_tests` | 1.000 | 0.000 | 1.000 | 1.000 |

## Direct Questions

| Question | Computed answer |
|---|---|
| Did calibration improve api_contracts vs uncalibrated? | `True` |
| Did calibration improve unit_tests vs uncalibrated? | `True` |
| Did calibration preserve edge_cases? | `True` |
| Did calibration reduce import-related failures? | `True` |
| Did calibration reduce overengineering-style failures? | `True` |

## Limitations

- Dry-run only.
- Mock behavior is deterministic and cannot prove external provider behavior.
- Closed Programming Reliability v0.1 dataset only.
- Experimental calibration evidence is not stable public API evidence.
- Results must not be used as proof of broad programming superiority.

## Interpretation

This artifact is experimental analysis. It measures the net effect of Xendris
intervention policy under a closed dry-run benchmark, not model quality in the
general case.
