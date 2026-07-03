# Phygn v1.3 — Positive Prediction Pressure & Kill Criteria

## 0. Purpose

This document answers a serious risk:

```txt
What if Frontera C only produces negative bounds forever?
```

If so, it may be a useful negative framework, but not a positive predictive theory. Phygn must be able to say that.

## 1. Problem

Current achievements:

```txt
structural invariant
negative bound
toy model comparison
synthetic benchmark protocol
source ingestion pipeline
baseline preparation
```

Current missing element:

```txt
positive physical prediction
```

A theory cannot claim high predictive status unless it produces:

```txt
a difference that could be right or wrong.
```

## 2. Positive Prediction Gate

A candidate must define:

```txt
observable
baseline model
candidate model
candidate term
free parameters
data target
error metric
expected sign/pattern
detectability threshold
failure condition
```

If not:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

## 3. Candidate model requirement

A Frontera C candidate cannot be generic boundary language.

It must be:

```txt
M_C(t; theta)
```

or equivalent.

It must output the same observable as the baseline.

Example structure:

```txt
V_base(t) = exp(-Gamma_env t)

V_C(t) = exp(-(Gamma_env + DeltaGamma_C)t)

DeltaGamma_C = explicit function of Q, B, L and parameters
```

But the function cannot be chosen arbitrarily to fit data.

## 4. Failure condition

Every candidate must declare:

```txt
If Gain_C <= 0 on admissible benchmark, candidate fails for this campaign.
If delta <= epsilon_exp, candidate is not detectable in this setup.
If parameters are unconstrained, candidate is underidentified.
If source support is absent, physical interpretation is blocked.
```

## 5. Kill / pivot criteria

After a defined number of campaigns, if Phygn only produces:

```txt
negative bounds
undetectable toy deltas
no source-backed candidate
no benchmark gain
no experimental observable
```

then Frontera C must be classified as one of:

```txt
NEGATIVE_FILTER_ONLY
STRUCTURAL_FRAMEWORK_ONLY
CLAIM_GATING_ARCHITECTURE
NOT_PREDICTIVE_CURRENTLY
```

Allowed conclusion:

```txt
Frontera C is currently not a predictive physical theory.
```

## 6. Survival criteria

Frontera C may remain in predictive track only if it produces at least one:

```txt
SOURCE_BACKED_CANDIDATE
BENCHMARK_GAIN_CANDIDATE
DETECTABLE_DELTA_CANDIDATE
EXPERIMENTAL_PROPOSAL_CANDIDATE
```

## 7. Positive prediction roadmap

Next after v1.3:

```txt
v1.4 — Source Pack Ingestion Attempt
v1.5 — Candidate Model Definition
v1.6 — Candidate vs Baseline Benchmark
v1.7 — Detectability & Failure Report
```

## 8. Red team statement

```txt
If Frontera C cannot generate a candidate model that improves or differs detectably from a source-backed baseline, then it should be demoted from predictive theory to structural/epistemic framework.
```

This demotion is not failure of Phygn. It is success of Phygn.

## 9. Final principle

```txt
A theory that cannot risk losing cannot earn the right to win.
```
