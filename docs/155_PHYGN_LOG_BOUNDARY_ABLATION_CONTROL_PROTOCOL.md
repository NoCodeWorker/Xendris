# Phygn v2.6 — LOG_BOUNDARY Ablation Control Protocol

## 0. Purpose

This document defines the ablation controls required before LOG_BOUNDARY may receive stronger source/benchmark pressure.

The goal is to determine whether the detectable synthetic delta found in v2.5 is genuinely caused by log-boundary structure.

---

## 1. Candidate model under test

```txt
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
```

with:

```txt
phi_log = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

---

## 2. Primary control: constant phi

Control:

```txt
DeltaGamma_constant = alpha * Gamma_env
```

Equivalent to:

```txt
phi = 1
```

Purpose:

```txt
Detect whether LOG_BOUNDARY adds anything beyond full saturation.
```

If LOG_BOUNDARY matches this control whenever it is detectable:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

---

## 3. Mean phi control

Control:

```txt
DeltaGamma_mean = alpha * Gamma_env * mean(phi_log over sweep)
```

Purpose:

```txt
Detect whether the signal depends on structured coordinates or merely average modulation.
```

---

## 4. Coordinate removal controls

Controls:

```txt
CONTROL_REMOVE_U:
  phi = sigmoid(k * constant_or_mean_u_shift) * tanh(k2 * (w - w0))^2

CONTROL_REMOVE_W:
  phi = sigmoid(k * (u - u0)) * constant_or_mean_w_term

CONTROL_NO_LOG_COORDINATES:
  phi = fixed or random toy modulation independent of q,b,u,w
```

Purpose:

```txt
Determine whether u and w contribute meaningful structure.
```

---

## 5. Threshold randomization

Control:

```txt
CONTROL_RANDOM_U0_W0
```

Randomly sample u0/w0 from declared ranges or fixed seed values.

Purpose:

```txt
Detect whether the result depends on threshold placement.
```

---

## 6. Alpha sensitivity

Required alpha runs:

```txt
alpha = 0.1
alpha = 1.0
alpha = 3.0
alpha = 10.0
```

Additional non-promotional optional stress runs:

```txt
alpha = 0.01
alpha = 30.0
```

These optional stress runs must be flagged as outside declared v2.5 benchmark range if they were not pre-registered.

---

## 7. Steepness sensitivity

Test:

```txt
k, k2 = 0.5, 1.0, 2.0, 5.0
```

Purpose:

```txt
Detect whether the signal appears only for steep switching behavior.
```

---

## 8. Decision rules

LOG_BOUNDARY may survive ablation only if:

```txt
it differs meaningfully from constant phi controls
detectability is not solely due to phi ≈ 1
alpha = 1 or moderate alpha retains meaningful signal
u/w coordinate removal reduces or changes the result
threshold randomization does not erase the effect entirely
```

If not:

```txt
source-pressure priority must not be increased
candidate remains synthetic toy or is down-ranked
```

---

## 9. Final principle

```txt
If removing the boundary does not change the signal, the boundary did no work.
```
