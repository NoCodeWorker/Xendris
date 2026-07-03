# Phygn v5.4 - LOG_BOUNDARY Prediction Alignment Results

Date: 2026-07-02

## Completion Status

Final campaign status:

```txt
LOG_BOUNDARY_PREDICTIVE_GAIN_SMOKE_TEST_POSITIVE
```

Interpretation:

```txt
Prediction alignment was performed against the four accepted Hackermueller 2004 FIG. 2 y_true records.
M_base and M_C_LOG_BOUNDARY produced complete predictions for all four heating_power_W conditions.
PredictiveGain was computed only as PREDICTIVE_GAIN_SMOKE_TEST_SINGLE_SOURCE.
No physical claim was created.
LOG_BOUNDARY is not validated.
Frontera C is not validated.
The invariant is not empirically confirmed.
```

## Required Limitation Flags

`SINGLE_SOURCE`, `N_SMALL_4`, `PASS_WITH_LIMITATIONS_YTRUE`, `SMOKE_TEST_ONLY`, `NOT_VALIDATION`, `NOT_PHYSICAL_CLAIM`

PredictiveGain labels: `SMOKE_TEST_ONLY`, `SINGLE_SOURCE`, `N_SMALL_4`, `PASS_WITH_LIMITATIONS_YTRUE`, `NOT_FRONTERA_C_VALIDATION`, `NOT_PHYSICAL_VALIDATION`

## Dataset

| heating_power_W | y_true visibility_fraction |
|---:|---:|
| 0.0 | 0.4700 |
| 3.0 | 0.2900 |
| 6.0 | 0.0700 |
| 10.5 | 0.0000 |

## Model Definitions

| model_id | role | formula | status |
|---|---|---|---|
| `M_base` | baseline | `visibility_fraction_hat = mean(y_true.visibility_fraction)` | `FITTED_SMOKE_TEST_BASELINE` |
| `M_C_LOG_BOUNDARY` | candidate | `clip(alpha + beta * log(1 + heating_power_W), 0, 1)` | `FITTED_SMOKE_TEST` |

`M_C_LOG_BOUNDARY` is a fitted smoke-test curve, not a physical model validation.

## Error Metrics

| model_id | MAE | RMSE | MAPE | max_abs_error |
|---|---:|---:|---:|---:|
| `M_base` | 0.172500 | 0.185523 | 0.935760 | 0.262500 |
| `M_C_LOG_BOUNDARY` | 0.035580 | 0.042277 | 0.279848 | 0.071159 |

## PredictiveGain Smoke Test

```txt
PredictiveGain = (RMSE(M_base) - RMSE(M_C_LOG_BOUNDARY)) / RMSE(M_base)
```

| Metric | Value |
|---|---:|
| RMSE(M_base) | 0.185523 |
| RMSE(M_C_LOG_BOUNDARY) | 0.042277 |
| PredictiveGain | 0.772121 |

## Created Artifacts

```txt
data/frontera_c/benchmark/log_boundary_prediction_alignment_v5_4.json
data/frontera_c/benchmark/log_boundary_minimal_models_v5_4.json
data/frontera_c/benchmark/log_boundary_model_predictions_v5_4.json
data/frontera_c/benchmark/log_boundary_error_metrics_v5_4.json
data/frontera_c/benchmark/log_boundary_predictive_gain_smoke_test_v5_4.json
data/frontera_c/benchmark/log_boundary_v5_4_next_gate_decision.json
reports/frontera_c/benchmark/log_boundary_prediction_alignment_v5_4.md
reports/frontera_c/benchmark/log_boundary_minimal_models_v5_4.md
reports/frontera_c/benchmark/log_boundary_model_predictions_v5_4.md
reports/frontera_c/benchmark/log_boundary_error_metrics_v5_4.md
reports/frontera_c/benchmark/log_boundary_predictive_gain_smoke_test_v5_4.md
reports/frontera_c/benchmark/log_boundary_v5_4_next_gate_decision.md
reports/campaigns/FRONTERA-C-LOG-BOUNDARY-PREDICTION-ALIGNMENT-v5_4.md
```

## Next Gate

```txt
v5.5 - Negative Controls & Leakage Tests
```

v5.5 permitted: `True`

## Blocked Claims

- LOG_BOUNDARY is validated.
- Frontera C is validated.
- The invariant is empirically confirmed.
- PredictiveGain smoke test equals validation.
- Single-source N=4 result generalizes.
- Curve fit equals physical theory.

## Allowed Claims

- Prediction alignment was performed against four accepted y_true records.
- A minimal benchmark smoke test was computed because predictions were complete.
- PredictiveGain is a smoke-test metric only.
- v5.5 is permitted because smoke-test PredictiveGain is positive.

Final discipline:

```txt
First y_true enables a benchmark.
A benchmark enables a smoke test.
A smoke test is not validation.
```
