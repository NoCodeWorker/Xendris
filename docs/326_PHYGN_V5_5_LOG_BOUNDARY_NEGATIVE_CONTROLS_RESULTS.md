# Phygn v5.5 - LOG_BOUNDARY Negative Controls Results

Date: 2026-07-02

## Completion Status

Final campaign status:

```txt
LOG_BOUNDARY_GAIN_EXPLAINED_BY_SIMPLE_CONTROL
```

Interpretation:

```txt
Negative controls were run against the v5.4 LOG_BOUNDARY smoke-test gain.
The result remains single-source N=4 and PASS_WITH_LIMITATIONS.
No LOG_BOUNDARY validation was created.
No Frontera C validation was created.
No physical claim was created.
```

## Required Limitation Flags

`SINGLE_SOURCE`, `N_SMALL_4`, `PASS_WITH_LIMITATIONS_YTRUE`, `SMOKE_TEST_ONLY`, `FITTED_SMOKE_TEST`, `NOT_VALIDATION`, `NOT_PHYSICAL_CLAIM`, `CONTROL_GATE`

## Control Metrics

| model_id | params | RMSE | MAE | MAPE | max_abs_error | leakage_risk |
|---|---:|---:|---:|---:|---:|---|
| `CONTROL_MONOTONIC_INTERPOLATION` | 4 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | `HIGH` |
| `M_C_LOG_BOUNDARY` | 2 | 0.042277 | 0.035580 | 0.279848 | 0.071159 | `MEDIUM` |
| `CONTROL_LINEAR_POWER` | 2 | 0.047289 | 0.032150 | 0.441141 | 0.085981 | `MEDIUM` |
| `CONTROL_EXPONENTIAL_POWER` | 2 | 0.056850 | 0.047240 | 0.202425 | 0.079580 | `MEDIUM` |
| `CONTROL_MEAN_BASELINE` | 1 | 0.185523 | 0.172500 | 0.935760 | 0.262500 | `MEDIUM` |
| `CONTROL_NULL_RANDOM` | 1 | 0.213767 | 0.172500 | 0.627445 | 0.368696 | `LOW` |
| `CONTROL_LOG_SHUFFLED` | 2 | 0.228818 | 0.208847 | 1.104376 | 0.332418 | `LOW_FOR_REAL_ALIGNMENT_HIGH_IF_GOOD` |

## Leave-One-Out Results

| model_id | LOO complete | LOO RMSE | instability |
|---|---|---:|---|
| `M_C_LOG_BOUNDARY` | `True` | 0.107647 | `False` |
| `CONTROL_LINEAR_POWER` | `True` | 0.080857 | `False` |
| `CONTROL_EXPONENTIAL_POWER` | `True` | 0.276111 | `True` |
| `CONTROL_MONOTONIC_INTERPOLATION` | `True` | 0.110132 | `False` |

## Decision

```txt
Generic monotonic interpolation matched the four training y_true points exactly (RMSE=0.0), and linear leave-one-out RMSE was lower than M_C; the positive gain is not distinguishable from simple curve-fitting under N=4.
```

## Created Artifacts

```txt
data/frontera_c/controls/log_boundary_negative_control_models_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_predictions_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_error_metrics_v5_5.json
data/frontera_c/controls/log_boundary_leakage_tests_v5_5.json
data/frontera_c/controls/log_boundary_leave_one_out_results_v5_5.json
data/frontera_c/controls/log_boundary_control_decision_v5_5.json
data/frontera_c/controls/log_boundary_v5_5_next_gate_decision.json
reports/frontera_c/controls/log_boundary_negative_control_models_v5_5.md
reports/frontera_c/controls/log_boundary_negative_control_predictions_v5_5.md
reports/frontera_c/controls/log_boundary_negative_control_error_metrics_v5_5.md
reports/frontera_c/controls/log_boundary_leakage_tests_v5_5.md
reports/frontera_c/controls/log_boundary_leave_one_out_results_v5_5.md
reports/frontera_c/controls/log_boundary_control_decision_v5_5.md
reports/frontera_c/controls/log_boundary_v5_5_next_gate_decision.md
reports/campaigns/FRONTERA-C-LOG-BOUNDARY-NEGATIVE-CONTROLS-v5_5.md
```

## Next Gate

```txt
None
```

v5.6 permitted: `False`

## Blocked Claims

- LOG_BOUNDARY is validated.
- Frontera C is validated.
- The invariant is empirically confirmed.
- Negative-control survival equals validation.
- Single-source N=4 generalizes.
- Curve fitting equals physical theory.

## Allowed Claims

- Negative controls were run against the LOG_BOUNDARY smoke-test gain.
- The gain survived, failed, or remained inconclusive according to control rules.
- v5.6 is permitted only if negative controls survive.

Final discipline:

```txt
A positive smoke test is a suspect, not a proof.
Controls decide whether it remains alive.
```
