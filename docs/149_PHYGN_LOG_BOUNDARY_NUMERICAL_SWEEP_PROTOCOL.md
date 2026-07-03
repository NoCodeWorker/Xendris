# Phygn v2.5 — LOG_BOUNDARY Numerical Sweep Protocol

## 0. Purpose

This document defines the numerical execution protocol for the LOG_BOUNDARY synthetic benchmark.

v2.3 designed the benchmark.

v2.5 executes it.

---

## 1. Equations

Baseline:

```txt
V_base(t) = exp(-Gamma_env * t)
```

Candidate:

```txt
V_log(t) = exp(-(Gamma_env + DeltaGamma_log) * t)
```

Perturbation:

```txt
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
```

Toy log-boundary modulation:

```txt
phi_log = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

Coordinates:

```txt
Q = lambda_C / L
B = r_g / L
q = log(Q)
b = log(B)
u = (q + b) / 2
w = (b - q) / 2
```

---

## 2. Numerical functions

Implement:

```python
compute_boundary_coordinates(m_kg: float, L_m: float) -> BoundaryCoordinates
```

```python
phi_log(u: float, w: float, k: float, k2: float, u0: float, w0: float) -> float
```

```python
compute_visibility_curves(...) -> VisibilityCurveResult
```

```python
compute_max_abs_delta(V_base, V_log) -> float
```

---

## 3. Declared sweep

Use the declared v2.3 ranges unless the implementation already stores them in the spec:

```txt
alpha_values: [0.1, 1.0, 3.0, 10.0]
k_values: [0.5, 1.0, 2.0, 5.0]
k2_values: [0.5, 1.0, 2.0, 5.0]
u0_values: [-90.0, -70.0, -50.0]
w0_values: [-40.0, -20.0, 0.0]
Gamma_env_values: [0.01, 0.05, 0.1]
```

Also include:

```txt
m_kg = 1e-17
L_m = 1e-7
t_grid = 101 points over [0, 10] seconds
epsilon_exp = 1e-6
```

---

## 4. Detectability classification

```txt
if max_abs_delta > epsilon_exp:
    LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
else:
    LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
```

But if detectability only appears outside declared ranges:

```txt
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
```

If detectability appears only with extreme/unjustified parameters:

```txt
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
```

---

## 5. Parameter reasonableness

Classify each best result:

```txt
PARAMETERS_DECLARED_TOY_RANGE
PARAMETERS_EXTREME_TOY_RANGE
PARAMETERS_POST_HOC
PARAMETERS_UNJUSTIFIED_OR_UNPHYSICAL
```

Rules:

```txt
declared sweep values are toy-declared, not source-backed
values outside sweep are post-hoc
detectability with post-hoc values cannot promote status
detectability with toy values still remains synthetic-only
```

---

## 6. Numerical safety

The implementation must handle:

```txt
overflow-safe sigmoid
finite values only
non-negative DeltaGamma_log
V values in [0, 1] where applicable
empty sweep error
NaN/inf detection
```

---

## 7. Final principle

```txt
A sweep is evidence of behavior inside declared assumptions, not evidence of nature.
```
