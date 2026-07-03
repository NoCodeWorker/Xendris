# Phygn v1.4 — Frontera C Candidate Term Design

## 0. Purpose

This document defines candidate term families for Frontera C.

These are not validated physical terms.

They are structured hypotheses designed to be tested, rejected, constrained, or demoted.

---

## 1. Shared model form

Baseline:

\[
V_{base}(t)=e^{-\Gamma_{env}t}
\]

Candidate:

\[
V_C(t)=e^{-(\Gamma_{env}+\Delta\Gamma_C)t}
\]

Candidate term:

\[
\Delta\Gamma_C = \alpha \cdot F_C(Q,B,L,\mathcal{E})
\]

where:

```txt
alpha = coupling scale / calibration factor
Q = lambda_C / L
B = r_g / L
QB = (l_P / L)^2
L = operational scale
E = experimental context
```

---

## 2. Dimensional rule

If \(\Delta\Gamma_C\) is a rate:

```txt
units = 1/time
```

Therefore:

```txt
alpha must carry units if F_C is dimensionless.
```

Every candidate term must declare:

```txt
term_units
alpha_units
dimensionless_core
```

If units are missing:

```txt
BLOCKED_DIMENSIONAL_INCOMPLETE
```

---

## 3. Candidate Family A — B-suppressed boundary term

\[
F_A(Q,B,L)=B
\]

\[
\Delta\Gamma_C=\alpha B
\]

Interpretation:

```txt
direct gravitational boundary suppression
```

Expected behavior:

```txt
for mesoscopic CAMPAIGN-001, B ≈ 7.43e-38
therefore delta is essentially negligible unless alpha is huge
```

Risk:

```txt
requires enormous alpha to become detectable
may become ad hoc
```

Default classification:

```txt
HYPOTHETICAL_NEGATIVE_CONTROL_CANDIDATE
```

Usefulness:

```txt
good as sanity check
bad as positive prediction unless alpha is independently constrained
```

---

## 4. Candidate Family B — QB structural coupling term

\[
F_B(Q,B,L)=QB=\left(\frac{\ell_P}{L}\right)^2
\]

\[
\Delta\Gamma_C=\alpha QB
\]

Interpretation:

```txt
structural Planck-scale coupling at operational scale L
```

Expected behavior:

```txt
independent of mass at fixed L
extremely small for laboratory L
```

Risk:

```txt
likely even less predictive for mesoscopic systems
may only reinforce negative bounds
```

Default classification:

```txt
STRUCTURAL_NEGATIVE_CONTROL_CANDIDATE
```

---

## 5. Candidate Family C — log-boundary coordinate term

Using:

\[
u=\frac{\log Q+\log B}{2}
\]

\[
w=\frac{\log B-\log Q}{2}
\]

A bounded candidate can use:

\[
F_C(u,w)=\sigma(a u + b w + c)
\]

where \(\sigma\) is bounded, e.g.:

\[
\sigma(x)=\frac{1}{1+e^{-x}}
\]

Interpretation:

```txt
boundary coordinate response in log Q/B space
```

Risk:

```txt
too flexible
parameters a,b,c may overfit
```

Required constraints:

```txt
a,b,c must be fixed before benchmark
no fitting without penalty
regularization or prior required
```

Default classification:

```txt
UNDERCONSTRAINED_UNLESS_PRIOR_DEFINED
```

---

## 6. Candidate Family D — threshold/saturation term

\[
F_D(Q,B,L)=\frac{B}{B+B_*}
\]

or:

\[
F_D(Q,B,L)=\frac{QB}{QB+(QB)_*}
\]

Interpretation:

```txt
saturating boundary effect near chosen threshold
```

Risk:

```txt
threshold B_* or (QB)_* can be arbitrary
```

Required:

```txt
threshold must be source-backed, physically motivated, or pre-registered
```

Default classification:

```txt
BLOCKED_IF_THRESHOLD_AD_HOC
```

---

## 7. Candidate admissibility statuses

```txt
ADMISSIBLE_TOY_CANDIDATE
ADMISSIBLE_NEGATIVE_CONTROL
UNDERIDENTIFIED_CANDIDATE
BLOCKED_AS_AD_HOC_CANDIDATE
BLOCKED_DIMENSIONAL_INCOMPLETE
REQUIRES_PARAMETER_PRIOR
REQUIRES_SOURCE_BACKING
```

---

## 8. Initial recommendation

The first operational candidate should not be the most flexible.

Recommended order:

```txt
1. Family A as negative control.
2. Family B as structural control.
3. Family D only if threshold can be motivated.
4. Family C only after priors/regularization.
```

---

## 9. Final principle

```txt
A candidate term is not valuable because it can fit.
It is valuable because it can fail.
```
