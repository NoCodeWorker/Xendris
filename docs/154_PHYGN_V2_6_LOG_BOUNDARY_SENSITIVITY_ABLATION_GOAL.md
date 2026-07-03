# Phygn v2.6 — LOG_BOUNDARY Sensitivity & Ablation Analysis Goal

## 0. Context

The latest confirmed document is:

```txt
153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
```

Therefore, v2.6 starts at:

```txt
154
```

v2.5 executed the LOG_BOUNDARY synthetic benchmark and found:

```txt
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
status: LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
best_max_abs_delta: 0.7152665915101674
epsilon_exp: 1e-06
best_alpha: 10.0
best_phi_log: 1.0
best_DeltaGamma_log: 0.5
Gamma_env: 0.05
```

This is a strong synthetic signal, but it is not yet clear whether the signal belongs to the log-boundary structure or to saturation and parameter amplitude.

---

## 1. Core thesis

```txt
A synthetic signal must survive ablation before it earns source pressure.
```

v2.6 asks:

```txt
Does LOG_BOUNDARY do real synthetic work,
or did the toy model simply saturate into DeltaGamma ≈ alpha * Gamma_env?
```

---

## 2. Hard rule

```txt
Synthetic detectability is not enough.
The candidate must beat its controls.
```

A candidate that is detectable only because:

```txt
alpha is high
phi_log saturates to 1
u0/w0 are conveniently placed
the log variables do not affect the result
```

must not receive increased source-pressure priority.

---

## 3. Main ablations

v2.6 must test:

```txt
alpha sensitivity
phi saturation sensitivity
u0/w0 threshold sensitivity
k/k2 steepness sensitivity
m/L regime sensitivity
constant phi control
randomized threshold control
coordinate removal control
log-coordinate contribution
```

---

## 4. Required controls

At minimum:

```txt
CONTROL_CONSTANT_PHI_ONE
CONTROL_CONSTANT_PHI_MEAN
CONTROL_RANDOM_U0_W0
CONTROL_REMOVE_U
CONTROL_REMOVE_W
CONTROL_ALPHA_ONE
CONTROL_LOW_STEEPNESS
CONTROL_NO_LOG_COORDINATES
```

---

## 5. Key question

The most important comparison is:

```txt
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
```

against:

```txt
DeltaGamma_control = alpha * Gamma_env
```

If the candidate does not beat or meaningfully differ from the constant control, then the log-boundary component is not doing useful work in the toy benchmark.

---

## 6. Possible outcomes

```txt
LOG_BOUNDARY_SURVIVES_ABLATION
LOG_BOUNDARY_FAILS_CONSTANT_CONTROL
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME
LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING
LOG_BOUNDARY_SENSITIVITY_INCONCLUSIVE
LOG_BOUNDARY_ABLATION_BLOCKED
```

---

## 7. Canonical interpretation

Even if LOG_BOUNDARY survives ablation:

```txt
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Blocked Reasons:
  MISSING_SOURCE_SUPPORT
  MISSING_BENCHMARK
  MISSING_EXPERIMENTAL_DATA
```

No physical claim may be authorized.

---

## 8. Acceptance criteria

v2.6 is complete when:

```txt
ablation schemas exist
constant phi control exists
alpha sensitivity exists
threshold sensitivity exists
coordinate contribution tests exist
saturation artifact detection exists
comparison report exists
loop feedback exists
tests pass
physical claims remain blocked
```

---

## 9. Final principle

```txt
A number is not yet a signal until it survives its simplest explanation.
```
