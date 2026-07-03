# Phygn v5.6 — LOG_BOUNDARY Control Failure Review & Candidate Disposition Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
```

Therefore, v5.6 starts at:

```txt
327
```

v5.5 produced:

```txt
LOG_BOUNDARY_GAIN_EXPLAINED_BY_SIMPLE_CONTROL
v5.6_permitted = false for C-structure ablation
```

The v5.4 positive smoke-test gain was explained by simpler controls:

```txt
CONTROL_MONOTONIC_INTERPOLATION RMSE = 0.000000
CONTROL_LINEAR_POWER LOO RMSE = 0.080857
M_C_LOG_BOUNDARY LOO RMSE = 0.107647
```

Therefore:

```txt
LOG_BOUNDARY did not survive negative controls.
LOG_BOUNDARY cannot proceed to C-structure ablation.
LOG_BOUNDARY cannot validate Frontera C.
```

---

## 1. Core thesis

```txt
A candidate explained by simpler controls cannot validate Frontera C.
```

---

## 2. Hard rule

```txt
Do not rescue a failed candidate with more architecture.
```

This means:

```txt
No v5.6 C-structure ablation for LOG_BOUNDARY.
No Frontera C validation candidate from LOG_BOUNDARY.
No physical claim.
No invariant confirmation.
No additional benchmark-only expansion designed to save LOG_BOUNDARY.
```

---

## 3. Mission

Implement:

```txt
v5.6 — LOG_BOUNDARY Control Failure Review & Candidate Disposition
```

The mission is to formally decide what happens to LOG_BOUNDARY after negative-control failure.

---

## 4. Required disposition options

The final disposition must be exactly one of:

```txt
ARCHIVE_AS_VALIDATION_CANDIDATE
RETAIN_AS_BENCHMARK_FIXTURE
RETAIN_AS_NEGATIVE_CONTROL_FIXTURE
EXPAND_VISIBILITY_DATASET_BEFORE_RECONSIDERATION
REPRIORITIZE_CANDIDATE_FAMILIES
DESIGN_NEW_EXPERIMENT
```

Multiple secondary roles may be allowed, but the primary disposition must be one.

Recommended conservative disposition:

```txt
ARCHIVE_AS_VALIDATION_CANDIDATE
```

with secondary allowed roles:

```txt
RETAIN_AS_BENCHMARK_FIXTURE
RETAIN_AS_NEGATIVE_CONTROL_FIXTURE
```

---

## 5. Inputs

Load:

```txt
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
data/frontera_c/controls/log_boundary_negative_control_models_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_predictions_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_error_metrics_v5_5.json
data/frontera_c/controls/log_boundary_leakage_tests_v5_5.json
data/frontera_c/controls/log_boundary_leave_one_out_results_v5_5.json
data/frontera_c/controls/log_boundary_control_decision_v5_5.json
data/frontera_c/controls/log_boundary_v5_5_next_gate_decision.json
data/frontera_c/benchmark/log_boundary_predictive_gain_smoke_test_v5_4.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
```

If v5.5 result is missing:

```txt
LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS
```

---

## 6. Required outputs

Create:

```txt
data/frontera_c/disposition/log_boundary_control_failure_review_v5_6.json
data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json
data/frontera_c/disposition/log_boundary_allowed_future_roles_v5_6.json
data/frontera_c/disposition/log_boundary_blocked_claims_v5_6.json
data/frontera_c/disposition/frontera_c_roadmap_update_after_log_boundary_v5_6.json
data/frontera_c/disposition/v5_6_next_research_direction.json
```

---

## 7. Statuses

Add:

```txt
LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_COMPLETED
LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS
LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE
LOG_BOUNDARY_RETAINED_AS_BENCHMARK_FIXTURE
LOG_BOUNDARY_RETAINED_AS_NEGATIVE_CONTROL_FIXTURE
FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE
FRONTERA_C_REQUIRES_CANDIDATE_REPRIORITIZATION
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

Expected final status:

```txt
LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE
```

or:

```txt
FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE
```

---

## 8. Acceptance criteria

v5.6 is complete when:

```txt
v5.5 control results loaded
control failure reason summarized
LOG_BOUNDARY disposition generated
allowed future roles generated
blocked claims generated
Frontera C roadmap updated
next research direction selected
reports generated
tests pass
no PredictiveGain recomputed
no C-structure ablation executed
no physical claim created
no Frontera C validation created
```

---

## 9. Final principle

```txt
Killing a candidate after controls is not failure.
It is the system protecting the theory from itself.
```
