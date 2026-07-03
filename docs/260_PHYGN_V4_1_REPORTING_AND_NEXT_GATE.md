# Phygn v4.1 — Reporting & Next Gate

## 0. Purpose

This document defines reports and next gates after model comparison.

---

## 1. Required reports

Generate:

```txt
reports/model_comparison/phi_gradient_model_registry_v4_1.md
reports/model_comparison/phi_gradient_model_predictions_v4_1.md
reports/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.md
reports/model_comparison/phi_gradient_negative_control_results_v4_1.md
reports/model_comparison/phi_gradient_claim_permission_update_v4_1.md
reports/campaigns/PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1.md
```

---

## 2. Report requirements

Reports must include:

```txt
benchmark row count
model count
prediction record count
comparison score table
negative-control results
SLOT_4 debt status
PredictiveGain status
claim permission update
allowed claims
blocked claims
next recommended phase
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_MODEL_COMPARISON_COMPLETED
PHI_GRADIENT_MODEL_COMPARISON_PARTIAL
PHI_GRADIENT_MODEL_COMPARISON_BASELINE_WINS
PHI_GRADIENT_MODEL_COMPARISON_CANDIDATE_WINS_LIMITED
PHI_GRADIENT_MODEL_COMPARISON_NEGATIVE_CONTROL_FAIL
PHI_GRADIENT_MODEL_COMPARISON_INCONCLUSIVE
PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK
PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_BY_SLOT4_DEBT
```

Suggested mapping if comparison completes without y_true:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

If negative control fails:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Possible next phases

If comparison is benchmark-actionable but no y_true:

```txt
v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan
```

If negative controls fail:

```txt
v4.2 — Candidate Revision / Kill-Pivot Gate
```

If candidate wins limited but y_true unavailable:

```txt
v4.2 — Experimental/Benchmark Data Acquisition Gate
```

Parallel:

```txt
v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review
```

---

## 5. Final principle

```txt
The next frontier is not a better score.
It is observed truth.
```
