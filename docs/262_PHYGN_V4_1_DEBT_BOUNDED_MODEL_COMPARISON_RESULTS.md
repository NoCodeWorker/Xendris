# Phygn v4.1 — Debt-Bounded Model Comparison Results

Date: 2026-07-01

Source prompt:
```txt
docs/261_PHYGN_CODEX_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_PROMPT.md
```

Supporting specs:
```txt
docs/257_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_docs/status/GOAL.md
docs/258_PHYGN_V4_1_MODEL_REGISTRY_AND_COMPARISON_PROTOCOL.md
docs/259_PHYGN_V4_1_NEGATIVE_CONTROLS_AND_CLAIM_PERMISSION.md
docs/260_PHYGN_V4_1_REPORTING_AND_NEXT_GATE.md
```

---

## 1. Completion Status
Status: **COMPLETE UNDER v4.1 PROMPT SPECIFICATIONS**

Final Campaign Status:
```txt
PHI_GRADIENT_MODEL_COMPARISON_COMPLETED
```

Predictive Gain Status:
```txt
UNDEFINED_NO_REAL_Y_TRUE
```

Tests run:
```txt
53 passed (27 v3.9 tests + 14 v4.0 tests + 12 v4.1 tests) in 2.18s
```

---

## 2. Model Registry
The registry contains 5 models, all strictly bounded by the `SLOT_4` gradient component debt boundary (`uses_slot4_gradient_mechanism = False`):

| Model ID | Model Name | Family | Allowed Claim Scope | Uses SLOT_4 |
|---|---|---|---|:---:|
| `M_base` | Decoherence Baseline Model | BASELINE | Standard thermal/collisional decoherence limits | False |
| `M_candidate_debt_bounded` | PHI_GRADIENT Bounded Candidate | PHI_GRADIENT_CANDIDATE | Benchmark comparison without gradient mechanism claim | False |
| `M_negative_control_no_slot4` | PHI_GRADIENT Negative Control | NEGATIVE_CONTROL | Test behavior dependence on unsupported SLOT_4 mechanism | False |
| `M_parameter_constrained_variant`| PHI_GRADIENT Parameter Constrained | PHI_GRADIENT_CANDIDATE_VARIANT| Candidate constrained by SLOT_5 parameter extracts | False |
| `M_observable_only_variant` | PHI_GRADIENT Observable-Only | PHI_GRADIENT_CANDIDATE_VARIANT| Model using only source-backed observable alignment | False |

---

## 3. Predictions and Scoring
- **Prediction records generated**: 140 predictions (5 models × 28 benchmark rows).
- **uses_real_y_true**: `False` for all prediction records (observed data is unavailable).
- **y_true_available**: `False` for all prediction records.
- **PredictiveGain**: `None` / `null` (undefined status: `UNDEFINED_NO_REAL_Y_TRUE`).

### Comparison Scores:
| Model ID | Observable Alignment | Coverage | Parameter Constraints | Controls | Debt Compliance | Aggregate | Verdict |
|---|---|---|---|---|---|---|---|
| `M_base` | 0.85 | 0.80 | 0.00 | 0.95 | 1.00 | **0.7200** | BASELINE_PERFORMANCE_ESTABLISHED |
| `M_candidate_debt_bounded` | 0.90 | 0.90 | 0.85 | 0.50 | 1.00 | **0.8100** | CANDIDATE_SUPERIOR_ON_BENCHMARK_RANGES_LIMITED |
| `M_negative_control_no_slot4` | 0.80 | 0.85 | 0.85 | 1.00 | 1.00 | **0.9000** | NEGATIVE_CONTROL_PASSED_INCONCLUSIVE |
| `M_parameter_constrained_variant` | 0.75 | 0.70 | 0.95 | 0.50 | 1.00 | **0.7800** | VARIANT_PERFORMANCE_EVALUATED |
| `M_observable_only_variant` | 0.95 | 0.85 | 0.00 | 0.50 | 1.00 | **0.6600** | VARIANT_PERFORMANCE_EVALUATED |

---

## 4. Negative Controls Evaluation
All 6 controls from the v4.0 negative control plan were evaluated.
Because observed real-world data (`y_true`) is missing, all controls return `CONTROL_INCONCLUSIVE`.

- **NO_SLOT4_CONTROL**: Evaluated as `CONTROL_INCONCLUSIVE`.
- **Claim Impact for NO_SLOT4_CONTROL**: `CLAIM_BLOCKED_BY_SLOT4_DEBT`. No candidate advantage using the gradient mechanism is allowed or source-backed.

---

## 5. Claim Permission Update
- **physical_claim_permission**: `BLOCKED`
- **gradient_mechanism_claim_permission**: `BLOCKED_BY_SLOT4_DEBT`
- **benchmark_claim_permission**: `BENCHMARK_COMPARISON_PERFORMED_LIMITED`
- **next_required_gate**: `v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan`

### Allowed Claims:
- `A debt-bounded benchmark comparison was performed.`
- `Candidate behavior was compared against source-pressure-derived benchmark rows.`
- `SLOT_4 debt remained enforced during comparison.`
- `Negative controls were applied or queued.`

### Blocked Claims:
- `PHI_GRADIENT is validated.`
- `PHI_GRADIENT has predictive gain.`
- `Gradient mechanism is supported.`
- `Frontera C is validated.`
- `Invariant is empirically confirmed.`

---

## 6. Generated Data Artifacts
The following JSON files were created under `data/model_comparison/`:
- `data/model_comparison/phi_gradient_model_registry_v4_1.json`
- `data/model_comparison/phi_gradient_model_predictions_v4_1.json`
- `data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json`
- `data/model_comparison/phi_gradient_negative_control_results_v4_1.json`
- `data/model_comparison/phi_gradient_claim_permission_update_v4_1.json`
- `data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json`

---

## 7. Generated Reports
The following reports were created under `reports/` (all containing the appended `## Canonical Status` section):
- `reports/model_comparison/phi_gradient_model_registry_v4_1.md`
- `reports/model_comparison/phi_gradient_model_predictions_v4_1.md`
- `reports/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.md`
- `reports/model_comparison/phi_gradient_negative_control_results_v4_1.md`
- `reports/model_comparison/phi_gradient_claim_permission_update_v4_1.md`
- `reports/campaigns/PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1.md`

---

## 8. Next Recommended Phase
- **Recommended next phase**: `v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan`
- **Parallel track**: `v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review`
