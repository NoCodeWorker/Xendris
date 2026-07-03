# Phygn v5.9 — Candidate Families & Theory Notes

## 0. Purpose

This document describes candidate families to evaluate without overclaiming.

---

## 1. PHI_CURVATURE

Candidate idea:

```txt
Observable response may correlate with curvature-like changes in normalized experimental condition space.
```

Possible features:

```txt
normalized heating power
normalized pressure
normalized temperature
normalized time
condition-space curvature proxies
```

Risks:

```txt
may become generic nonlinear curve fitting
may lack C-specific structure
```

Requirement:

```txt
must define C-structure or be classified as data baseline
```

---

## 2. PHI_LOCALIZED_WINDOW

Candidate idea:

```txt
Observable degradation may occur in localized windows of experimental regimes.
```

Possible features:

```txt
condition windows
thresholded regime indicators
normalized physical conditions
```

Risks:

```txt
post-hoc window selection
leakage through threshold tuning
```

Requirement:

```txt
window definitions must be predeclared or cross-validated
```

---

## 3. PHI_BANDPASS

Candidate idea:

```txt
Physical response may peak or decay in band-limited regime regions.
```

Possible features:

```txt
pressure band
temperature band
mass band
time band
normalized condition bands
```

Risks:

```txt
can mimic arbitrary smooth curves
```

Requirement:

```txt
must survive simple bandpass and monotonic controls
```

---

## 4. PHI_GRADIENT_METHOD_ONLY

Current status:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

Allowed:

```txt
method fixture
negative-control generator
benchmark stress test
```

Blocked:

```txt
active physical candidate unless SLOT_4 and y_true blockers resolved
```

---

## 5. B_SUPPRESSED

Candidate idea:

```txt
Gravity-scale term B = r_g / L contributes suppressed correction.
```

Risk:

```txt
likely numerically negligible in current regimes
```

Requirement:

```txt
must show detectable predicted variation without extreme parameters
```

---

## 6. QB_STRUCTURAL

Candidate idea:

```txt
Combined invariant structure QB = (l_P/L)^2.
```

Risk:

```txt
may not vary meaningfully across dataset
may require arbitrary L
```

Requirement:

```txt
operational scale L must be justified and not ad hoc
```

---

## 7. THRESHOLD_SATURATION

Candidate idea:

```txt
Responses saturate near regime boundaries.
```

Risk:

```txt
generic saturation model, not C-specific
```

Requirement:

```txt
must beat generic logistic/exponential controls
```

---

## 8. DATA_DRIVEN_PHYSICS_BASELINE

Not a C candidate.

Use as:

```txt
strong baseline
control comparator
```

Examples:

```txt
linear/ridge/lasso
exponential decay
monotonic model
group-aware regression
```

---

## 9. C_COORDINATE_RESPONSE

Candidate idea:

```txt
Use available physical quantities to derive C-coordinate features Q, B, u, w where justified.
```

Definitions:

```txt
Q = lambda_C / L
B = r_g / L
u = (log Q + log B) / 2
w = (log B - log Q) / 2
```

Hard blocker:

```txt
No justified mass m and operational scale L, no C-coordinate feature.
```

No arbitrary L.

If L is ad hoc:

```txt
BLOCKED_AD_HOC_SCALE
```

---

## 10. SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE

Candidate idea:

```txt
Predict y_true from source-independent physical condition variables without source identity leakage.
```

May be candidate only if:

```txt
rule is predeclared
features are physical
source_id is excluded
out-of-source evaluation is possible
```

May otherwise be baseline.

---

## 11. Final principle

```txt
If a candidate cannot be wrong, it is not a candidate.
```
