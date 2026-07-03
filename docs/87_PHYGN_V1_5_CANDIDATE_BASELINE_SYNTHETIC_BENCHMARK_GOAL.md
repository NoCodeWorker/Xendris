# Phygn v1.5 — Candidate vs Baseline Synthetic Benchmark Goal

## 0. Purpose

Phygn v1.4 operationalized a Frontera C candidate:

```txt
CAND-FC-B-NEGCTRL-001
family = B_SUPPRESSED
candidate term = DeltaGamma_C = alpha * B
observable = visibility_loss
```

The positive prediction gate moved from:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

to:

```txt
POSITIVE_PREDICTION_REQUIRES_EVIDENCE
```

v1.5 now creates the first quantitative confrontation:

```txt
V_base(t) vs V_C(t)
```

under a synthetic benchmark.

This does not unlock physical prediction.

It answers:

```txt
Does the candidate produce a detectable numerical difference under declared parameters?
```

---

## 1. Current state

Previous result:

```txt
85_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_RESULTS.md
```

Current candidate status:

```txt
candidate_id = CAND-FC-B-NEGCTRL-001
candidate_family = B_SUPPRESSED
candidate_readiness = requires evidence / benchmark
physical_prediction = BLOCKED
```

---

## 2. Shared observable

```txt
observable = visibility_loss
```

Baseline:

\[
V_{base}(t)=e^{-\Gamma_{env}t}
\]

Candidate:

\[
V_C(t)=e^{-(\Gamma_{env}+\alpha B)t}
\]

where:

```txt
B = r_g / L
alpha = pre-registered coupling-rate scale
```

---

## 3. v1.5 mission

Implement a synthetic benchmark engine for the candidate:

```txt
time grid
baseline visibility curve
candidate visibility curve
delta curve
max_abs_delta
detectability assessment
SyntheticGain
failure condition evaluation
report generation
```

---

## 4. Synthetic benchmark is not physical prediction

Synthetic benchmark may compute:

```txt
SyntheticDelta
SyntheticGain
DetectabilityToyStatus
```

It may not compute:

```txt
PredictiveGain
```

unless:

```txt
y_true exists
benchmark provenance is experimental or literature-extracted
baseline is source-backed
candidate is admissible for physical interpretation
```

---

## 5. Required benchmark inputs

```txt
candidate_id
system_id
m_kg
L_value_m
L_type
B
Gamma_env
alpha
t_grid
epsilon_exp
y_true optional
error_metric
benchmark_provenance = SYNTHETIC
```

---

## 6. Required outputs

```txt
V_base
V_candidate
delta
max_abs_delta
detectability_status
synthetic_gain_status
triggered_failure_conditions
allowed_claims
blocked_claims
```

---

## 7. Detectability statuses

```txt
DETECTABLE_SYNTHETIC_DELTA
UNDETECTABLE_SYNTHETIC_DELTA
NO_THRESHOLD_DECLARED
```

Rule:

```txt
max_abs_delta > epsilon_exp
→ DETECTABLE_SYNTHETIC_DELTA

max_abs_delta <= epsilon_exp
→ UNDETECTABLE_SYNTHETIC_DELTA
```

---

## 8. Expected default outcome

For mesoscopic CAMPAIGN-002:

```txt
B ~ 7.43e-38
```

Therefore, unless alpha is enormous:

```txt
alpha * B is negligible
max_abs_delta likely undetectable
```

This is not failure of Phygn. It is numerical information.

---

## 9. Alpha sweep

v1.5 must include an alpha sweep:

```txt
alpha_values = [1e0, 1e10, 1e20, 1e30, 1e35, 1e38, 1e40]
```

Purpose:

```txt
find approximate alpha required for detectability
```

If detectable only for absurd alpha:

```txt
FAIL_PARAMETER_UNDERIDENTIFIED
or
REQUIRES_UNPHYSICAL_ALPHA
```

---

## 10. What v1.5 may unlock

Allowed:

```txt
The candidate has been synthetically benchmarked.
The candidate delta is detectable/undetectable under declared toy parameters.
The required alpha scale has been estimated.
Failure conditions were evaluated.
```

Not allowed:

```txt
Phygn predicts decoherence.
Frontera C is validated.
The candidate has physical PredictiveGain.
SyntheticGain proves physical gain.
```

---

## 11. Acceptance criteria

v1.5 is complete when:

```txt
synthetic benchmark schemas exist
candidate vs baseline benchmark runs
delta and detectability are computed
alpha sweep exists
failure conditions update
reports generated
tests pass
physical claims remain blocked
```

---

## 12. Final principle

```txt
A toy benchmark cannot prove a theory.
But it can reveal whether the first candidate is numerically alive.
```
