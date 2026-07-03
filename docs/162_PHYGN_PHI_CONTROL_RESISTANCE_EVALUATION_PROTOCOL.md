# Phygn v2.7 — Phi Control-Resistance Evaluation Protocol

## 0. Purpose

This document defines how candidate phi functions are evaluated against controls.

The purpose is to prevent replacing one saturating artifact with another.

---

## 1. Required comparisons

Every phi candidate must be compared against:

```txt
CONTROL_CONSTANT_PHI_ONE
CONTROL_CONSTANT_PHI_MEAN
CONTROL_REMOVE_U
CONTROL_REMOVE_W
CONTROL_NO_LOG_COORDINATES
CONTROL_RANDOM_THRESHOLDS
CONTROL_ALPHA_ONE
```

---

## 2. Core metrics

```txt
candidate_delta
constant_phi_delta
mean_phi_delta
remove_u_delta
remove_w_delta
no_log_delta
alpha_1_delta
saturation_ratio
control_gain
coordinate_contribution_score
threshold_robustness_score
alpha_sensitivity_score
non_saturation_score
```

---

## 3. Saturation test

If:

```txt
max(phi_values) >= 0.99
```

and:

```txt
candidate_delta ≈ constant_phi_delta
```

then:

```txt
PHI_CANDIDATE_SATURATES
```

---

## 4. Constant control test

```txt
control_gain = (candidate_delta - constant_phi_delta) / max(constant_phi_delta, eps)
```

If:

```txt
abs(control_gain) < tolerance
```

then:

```txt
PHI_CANDIDATE_FAILS_CONSTANT_CONTROL
```

unless the candidate is intentionally lower amplitude but wins on coordinate contribution or robustness.

---

## 5. Coordinate contribution test

```txt
coordinate_contribution_score =
  candidate_delta - max(remove_u_delta, remove_w_delta, no_log_delta)
```

If:

```txt
coordinate_contribution_score <= threshold
```

then:

```txt
PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION
```

---

## 6. Threshold robustness test

For candidates with u0/w0 or sigma parameters:

```txt
rerun over perturbed thresholds
compute variance of detectability
detect threshold collapse
```

If the candidate only works for a narrow tuned window:

```txt
PHI_CANDIDATE_REQUIRES_THRESHOLD_TUNING
```

---

## 7. Ranking score

Recommended:

```txt
control_resistance_score =
  0.30 * non_saturation_score
+ 0.25 * coordinate_contribution_score_normalized
+ 0.20 * threshold_robustness_score
+ 0.15 * alpha_1_survival_score
+ 0.10 * numerical_stability_score
```

This ranking is heuristic and synthetic-only.

---

## 8. Promotion rule

Only candidates classified as:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
```

may receive:

```txt
source-search priority proposal
benchmark-pressure priority proposal
```

No candidate may receive physical claim authorization.

---

## 9. Final principle

```txt
Controls are not obstacles to discovery.
They are how discovery survives itself.
```
