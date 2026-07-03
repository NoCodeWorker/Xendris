# Phygn Railways, Gates and Terminal States

## 0. Purpose

This document defines the mandatory rails for autonomous execution.

---

## 1. Global hard constraints

The AI must never:

```txt
fabricate sources
fabricate PDFs
fabricate hashes
fabricate page numbers
fabricate figure/table IDs
fabricate numerical values
fabricate units
fabricate y_true
compute PredictiveGain without accepted y_true
claim validation before controls
claim physical support from curve fit
reactivate archived candidates without explicit reopen criteria
hide limitations
skip negative controls
skip C-structure ablation
```

---

## 2. Gate order

The order is mandatory:

```txt
source identity
source availability
observable location
accepted y_true
dataset threshold
benchmark readiness
prediction alignment
PredictiveGain
negative controls
C-structure ablation
scientific debt review
claim permission
validation candidate report
```

No later gate may run before the previous gate passes.

---

## 3. Permission logic

## y_true permission

```txt
source identity + source availability + observable location + numeric value + unit + condition mapping + QC = y_true permission
```

## benchmark permission

```txt
accepted_ytrue_count >= 10 and independent_source_count >= 2
```

## PredictiveGain permission

```txt
benchmark_ready + baseline_predictions + candidate_predictions + accepted_ytrue
```

## validation permission

```txt
PredictiveGain positive + negative controls survived + C-structure ablation survived + scientific debt cleared
```

---

## 4. Terminal states

Success:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
```

Blocks:

```txt
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_NO_PREDICTIVE_GAIN
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
NO_CANDIDATE_WITH_REALITY_CONTACT
```

Falsification/domain failure:

```txt
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
```

Use this only if:

```txt
sufficient benchmark exists
candidate predictions consistently fail
controls do not rescue the claim
alternative baselines dominate
C-structure gives no advantage
```

---

## 5. Reopen criteria for failed candidate families

A failed candidate may only be reopened if:

```txt
new independent sources are added
accepted_ytrue_count increases materially
controls are rerun
simple controls no longer explain gain
out-of-source predictive advantage appears
```

For LOG_BOUNDARY specifically:

```txt
at least 2 independent sources
at least 10 accepted y_true
out-of-source evaluation
negative controls survive
simple controls no longer explain gain
```

Until then:

```txt
LOG_BOUNDARY remains archived as validation candidate
```

---

## 6. Claim vocabulary

Allowed:

```txt
candidate selected for test
benchmark-ready dataset
PredictiveGain smoke test
PredictiveGain positive under constraints
negative controls survived
C-structure ablation survived
validation candidate ready
```

Blocked unless all gates pass:

```txt
Frontera C validated
physical mechanism confirmed
invariant confirmed
general theory validated
```

---

## 7. Final principle

```txt
A railway is not a cage.
It is the structure that lets acceleration remain scientific.
```
