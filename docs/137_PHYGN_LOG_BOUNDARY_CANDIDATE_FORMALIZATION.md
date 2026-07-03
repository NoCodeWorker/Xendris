# Phygn v2.3 — LOG_BOUNDARY Candidate Formalization

## 0. Purpose

This document defines how the heuristic `LOG_BOUNDARY` family becomes a formal synthetic benchmark candidate.

The candidate must be explicit enough to compute.

It must not be allowed to remain poetic.

---

## 1. Background

Frontera C uses dimensionless boundary coordinates:

```txt
Q = lambda_C / L
B = r_g / L
QB = (ell_P / L)^2
```

Log-coordinates:

```txt
q = log(Q)
b = log(B)
u = (q + b) / 2 = log(ell_P / L)
w = (b - q) / 2 = log(m / m_P)
```

The heuristic idea is that boundary behavior may be more naturally expressed in logarithmic coordinates than in raw B-suppressed terms.

---

## 2. Candidate family

```txt
LOG_BOUNDARY
```

Candidate intuition:

```txt
The physical trace may not scale directly as B.
It may arise from a log-boundary modulation over dimensionless variables q, b, u, w.
```

This remains heuristic.

---

## 3. Required formalization

A LOG_BOUNDARY candidate must define:

```txt
observable
baseline model
candidate model
dimensionless input variables
coupling parameters
parameter ranges
detectability metric
failure conditions
```

---

## 4. Candidate model template

Baseline visibility:

```txt
V_base(t) = exp(-Gamma_env * t)
```

Candidate visibility:

```txt
V_log(t) = exp(-(Gamma_env + DeltaGamma_log) * t)
```

Candidate perturbation:

```txt
DeltaGamma_log = alpha * Gamma_env * phi_log(q, b, u, w)
```

This makes `DeltaGamma_log` dimensionally valid because:

```txt
Gamma_env has units s^-1
alpha is dimensionless
phi_log is dimensionless
```

---

## 5. Example admissible phi functions

Allowed toy functions:

```txt
phi_log_1 = sigmoid(k * (u - u0))
phi_log_2 = tanh(k * (w - w0))^2
phi_log_3 = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

These are not physical laws.

They are toy candidate functions for synthetic benchmark design.

---

## 6. Forbidden forms

Forbidden unless explicitly justified:

```txt
DeltaGamma_log = alpha * log(B)
```

Reason:

```txt
log(B) is negative and large in magnitude, can create sign/scale artifacts,
and does not automatically produce a physical positive decoherence rate.
```

Forbidden:

```txt
arbitrary L chosen only to maximize effect
post-hoc u0 chosen after seeing desired detectability
parameter sweep without pre-registered ranges
dimensionful logs
```

---

## 7. Parameter pre-registration

Candidate must declare:

```txt
alpha_range
k_range
u0_range
w0_range
t_grid
epsilon_exp
Gamma_env
m_range
L_range
```

All ranges are toy unless source-backed.

---

## 8. Minimum candidate record

```python
class LogBoundaryCandidateSpec(BaseModel):
    candidate_id: str
    candidate_family: Literal["LOG_BOUNDARY"]
    observable: str
    baseline_equation: str
    candidate_equation: str
    phi_function: str
    dimensionless_variables: list[str]
    parameters: dict[str, float | tuple[float, float]]
    parameter_ranges: dict[str, tuple[float, float]]
    t_grid: list[float]
    epsilon_exp: float
    failure_conditions: list[str]
    canonical_status: CanonicalStatusRecord
```

---

## 9. Final principle

```txt
Logarithms are allowed only when the argument is dimensionless and the output is operationalized.
```
