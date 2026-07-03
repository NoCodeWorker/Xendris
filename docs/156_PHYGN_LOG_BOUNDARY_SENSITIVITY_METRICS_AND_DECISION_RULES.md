# Phygn v2.6 — LOG_BOUNDARY Sensitivity Metrics & Decision Rules

## 0. Purpose

This document defines the metrics and decisions used to classify the LOG_BOUNDARY ablation result.

---

## 1. Required metrics

```txt
best_max_abs_delta
baseline_max_abs_delta
constant_phi_max_abs_delta
mean_phi_max_abs_delta
remove_u_max_abs_delta
remove_w_max_abs_delta
no_log_coordinates_max_abs_delta
alpha_1_max_abs_delta
saturation_ratio
coordinate_contribution_score
control_gain
threshold_sensitivity_score
```

---

## 2. Saturation ratio

```txt
saturation_ratio = max(phi_log over best region)
```

Interpretation:

```txt
saturation_ratio ≈ 1.0 means phi_log saturated.
```

If:

```txt
saturation_ratio >= 0.99
```

then add warning:

```txt
WARN_PHI_SATURATION
```

---

## 3. Control gain

Compare candidate against constant phi control:

```txt
control_gain = (candidate_delta - constant_control_delta) / max(constant_control_delta, eps)
```

If:

```txt
abs(control_gain) < tolerance
```

then:

```txt
LOG_BOUNDARY_FAILS_CONSTANT_CONTROL
```

or:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

depending on phi saturation.

---

## 4. Coordinate contribution score

Estimate:

```txt
coordinate_contribution_score =
  candidate_delta - max(remove_u_delta, remove_w_delta, no_log_coordinates_delta)
```

If coordinate contribution is near zero:

```txt
WARN_LOW_COORDINATE_CONTRIBUTION
```

If removal controls match candidate performance:

```txt
LOG_BOUNDARY_FAILS_COORDINATE_CONTRIBUTION
```

---

## 5. Alpha sensitivity

If detectable only at:

```txt
alpha = 10.0
```

and not at:

```txt
alpha = 1.0
```

then flag:

```txt
WARN_ALPHA_DEPENDENCE
```

If alpha must exceed declared toy range:

```txt
LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME
```

---

## 6. Threshold sensitivity

If small changes or randomization of u0/w0 erase detectability:

```txt
WARN_THRESHOLD_TUNING
```

If threshold placement appears post-hoc or overly precise:

```txt
LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING
```

---

## 7. Survival status

Possible final statuses:

```txt
LOG_BOUNDARY_SURVIVES_ABLATION
LOG_BOUNDARY_FAILS_CONSTANT_CONTROL
LOG_BOUNDARY_FAILS_COORDINATE_CONTRIBUTION
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME
LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING
LOG_BOUNDARY_SENSITIVITY_INCONCLUSIVE
LOG_BOUNDARY_ABLATION_BLOCKED
```

---

## 8. Canonical mapping

For survival:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

For failure/artifact:

```txt
CanonicalPermission: CLAIM_BLOCKED or REVIEW_REQUIRED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: UNPHYSICAL_PARAMETER, HUMAN_REVIEW_REQUIRED, MISSING_EXPERIMENTAL_DATA
```

---

## 9. Final principle

```txt
Sensitivity analysis turns a big number into a diagnostic.
```
