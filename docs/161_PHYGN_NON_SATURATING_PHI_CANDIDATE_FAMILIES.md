# Phygn v2.7 — Non-Saturating Phi Candidate Families

## 0. Purpose

This document defines candidate phi families for LOG_BOUNDARY after v2.6 showed that the previous phi saturated and matched the constant phi=1 control.

All phi functions must be:

```txt
dimensionless
bounded
finite
non-trivially dependent on u and/or w
resistant to constant controls
resistant to coordinate removal
```

---

## 1. Inputs

Use log-boundary coordinates:

```txt
q = log(Q)
b = log(B)
u = (q + b) / 2
w = (b - q) / 2
```

All arguments to logarithms must remain dimensionless.

---

## 2. Candidate: PHI_CENTERED

Raw:

```txt
phi_raw = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

Centered:

```txt
phi_centered = phi_raw - mean(phi_raw over declared sweep)
```

Bounded positive version:

```txt
phi_centered_pos = abs(phi_centered)
```

Purpose:

```txt
Remove constant background contribution.
```

Risk:

```txt
May still inherit threshold tuning.
```

---

## 3. Candidate: PHI_GRADIENT

```txt
phi_gradient = |d phi_raw / du| + |d phi_raw / dw|
```

Purpose:

```txt
Detect boundary transition regions rather than saturated plateaus.
```

Expected behavior:

```txt
Low in saturated regions.
High near boundary gradients.
```

---

## 4. Candidate: PHI_BANDPASS

```txt
phi_bandpass = exp(-((u-u0)^2 / sigma_u^2 + (w-w0)^2 / sigma_w^2))
```

Normalized variant:

```txt
phi_bandpass_norm = phi_bandpass / max(phi_bandpass over declared grid)
```

Purpose:

```txt
Localize signal near a declared region without global saturation.
```

Risk:

```txt
Threshold/center tuning.
```

---

## 5. Candidate: PHI_CURVATURE

```txt
phi_curvature = |d2 phi_raw / du2| + |d2 phi_raw / dw2|
```

Purpose:

```txt
Detect curvature of transition zones rather than amplitude.
```

Risk:

```txt
Numerical instability if implemented by finite differences without smoothing.
```

---

## 6. Candidate: PHI_RELATIVE_BOUNDARY

```txt
phi_relative = |u - w| / (1 + |u| + |w|)
```

Purpose:

```txt
Use relative log-boundary separation without threshold centers.
```

Advantage:

```txt
No u0/w0 threshold tuning.
```

---

## 7. Candidate: PHI_NON_SATURATING_RATIO

```txt
phi_ratio = log(1 + |u-u0|) / (1 + log(1 + |u-u0|) + log(1 + |w-w0|))
```

Purpose:

```txt
Bounded smooth ratio with slower saturation than sigmoid/tanh gates.
```

Risk:

```txt
Still contains u0/w0 centers.
```

---

## 8. Candidate: PHI_COORDINATE_CONTRAST

```txt
phi_contrast = abs(zscore(u) - zscore(w)) / (1 + abs(zscore(u)) + abs(zscore(w)))
```

Purpose:

```txt
Force dependence on relative coordinate structure.
```

---

## 9. Candidate: PHI_LOCALIZED_WINDOW

```txt
phi_window = sech((u-u0)/sigma_u)^2 * sech((w-w0)/sigma_w)^2
```

Purpose:

```txt
Localized non-plateau response.
```

Risk:

```txt
Center and width tuning.
```

---

## 10. Family selection rule

A phi family is eligible for ranking only if it passes:

```txt
finite values
bounded values
no saturation_ratio >= 0.99
constant_control_gain != 0 within tolerance
coordinate contribution > threshold
physical claims blocked
```

---

## 11. Final principle

```txt
The new phi must be a boundary diagnostic, not an amplitude knob.
```
