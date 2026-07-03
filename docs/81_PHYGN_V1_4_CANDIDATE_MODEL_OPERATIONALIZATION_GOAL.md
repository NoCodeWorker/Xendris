# Phygn v1.4 — Candidate Model Operationalization Goal

## 0. Purpose

Phygn v1.3 introduced a critical pressure:

```txt
POSITIVE_PREDICTION_GATE
KILL / PIVOT CRITERIA
```

Current status:

```txt
Positive Prediction Gate = POSITIVE_PREDICTION_NOT_OPERATIONALIZED
Kill/Pivot Status = CLAIM_GATING_ARCHITECTURE
```

This is honest but dangerous. If Frontera C never operationalizes a positive candidate, it must stop claiming predictive physical status.

v1.4 therefore has one mission:

```txt
force Frontera C to define a candidate model that can win, lose, or be demoted.
```

---

## 1. Core question

```txt
Can Frontera C define a concrete candidate term that modifies a shared observable relative to a baseline, with explicit failure conditions?
```

Not:

```txt
Can Frontera C sound plausible?
```

Not:

```txt
Can Frontera C block other claims?
```

But:

```txt
Can Frontera C risk being wrong?
```

---

## 2. Required candidate structure

A candidate must define:

```txt
observable
baseline model
candidate model
candidate term
parameters
data target
error metric
expected pattern
detectability threshold
failure condition
```

If not, status remains:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

---

## 3. Candidate model target

For CAMPAIGN-002, the shared observable remains:

```txt
visibility_loss / coherence_decay
```

Baseline:

\[
V_{base}(t)=e^{-\Gamma_{env}t}
\]

Candidate:

\[
V_C(t)=e^{-(\Gamma_{env}+\Delta\Gamma_C)t}
\]

where:

\[
\Delta\Gamma_C = \alpha \cdot F_C(Q,B,L,\mathcal{E})
\]

But this is not allowed to be arbitrary.

---

## 4. Candidate term discipline

The term \(F_C\) must be:

```txt
dimensionally explicit
bounded
scale-aware
non-arbitrary
linked to Q/B/L
declared as hypothetical
tested against baseline
```

If the term is chosen only to fit data:

```txt
BLOCKED_AS_AD_HOC_CANDIDATE
```

If it has unconstrained parameters:

```txt
UNDERIDENTIFIED_CANDIDATE
```

---

## 5. Initial candidate families

v1.4 may define candidate families, but must label them clearly:

```txt
CANDIDATE_FAMILY_A: B-suppressed boundary term
CANDIDATE_FAMILY_B: QB structural coupling term
CANDIDATE_FAMILY_C: log-boundary coordinate term
CANDIDATE_FAMILY_D: threshold/saturation boundary term
```

All are initially:

```txt
HYPOTHETICAL_CANDIDATE
```

not physical prediction.

---

## 6. Positive Prediction Gate update

v1.4 target:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
→ POSITIVE_PREDICTION_REQUIRES_EVIDENCE
```

This is progress.

It means:

```txt
the candidate is now formally defined,
but still lacks evidence/benchmark/source support.
```

---

## 7. What v1.4 may unlock

Allowed:

```txt
Frontera C has an operational candidate family.
The candidate can be benchmarked in future phases.
The candidate has explicit failure conditions.
```

Not allowed:

```txt
Frontera C predicts decoherence.
The candidate is validated.
The candidate has PredictiveGain.
Frontera C is a confirmed physical theory.
```

---

## 8. Failure is allowed

v1.4 may conclude:

```txt
No non-ad-hoc candidate term can currently be defined.
```

If so:

```txt
status = NOT_PREDICTIVE_CURRENTLY
```

This is not failure of Phygn. It is success of the method.

---

## 9. Acceptance criteria

v1.4 is complete when:

```txt
candidate model schemas exist
candidate term registry exists
candidate admissibility classifier exists
positive prediction gate can evaluate the candidate
failure conditions are explicit
reports are generated
tests pass
no physical claim is unlocked
```

---

## 10. Final principle

```txt
Now Frontera C must risk a formula.
```
