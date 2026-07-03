# Phygn Candidate Strategy and Frontera C Validation Criteria

## 0. Purpose

This document defines how candidates are selected, tested, archived and possibly promoted toward a Frontera C validation candidate.

---

## 1. Candidate status inventory

## LOG_BOUNDARY

Current:

```txt
ARCHIVED_AS_VALIDATION_CANDIDATE
```

Allowed roles:

```txt
benchmark fixture
negative-control fixture
pipeline regression
```

Blocked roles:

```txt
active validation candidate
physical claim
PredictiveGain evidence claim
Frontera C validation claim
```

## PHI_GRADIENT

Current:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

Blocked by:

```txt
SLOT_4 debt
no robust empirical support
```

Allowed roles:

```txt
method fixture
negative-control generator
pipeline stress test
```

## PHI_CURVATURE / PHI_LOCALIZED_WINDOW / PHI_BANDPASS

May be reconsidered only after:

```txt
source identity
source availability
observable alignment
prediction definition without leakage
```

---

## 2. Candidate selection criteria

A candidate can enter predictive testing only if:

```txt
it maps to accepted y_true observables
it can generate predictions without seeing y_true
it has a defined feature set
it has a baseline comparator
it has control tests
it has ablation plan
```

---

## 3. Candidate rejection criteria

Reject or archive if:

```txt
gain explained by simple controls
leakage risk high
out-of-source failure
C-structure ablation failure
model only fits same-source curves
candidate cannot predict accepted y_true
candidate depends on unresolved scientific debt
```

---

## 4. Validation criteria

Frontera C validation candidate readiness requires:

```txt
multi-source accepted y_true dataset
benchmark readiness
positive PredictiveGain
negative controls survived
leakage tests survived
C-structure ablation survived
scientific debt does not block scoped claim
claim permission is explicit and limited
```

---

## 5. Validation scope

Any validation must be scoped by:

```txt
domain
observable class
sources
dataset version
candidate family
baseline model
error metric
control set
ablation set
limitations
```

A valid claim may look like:

```txt
Frontera C validation candidate is ready for the visibility/decoherence domain under dataset vX, candidate Y, baseline Z, and control set W.
```

It must not say:

```txt
Frontera C is universally validated.
```

---

## 6. Falsification logic

If a sufficiently strong benchmark exists and all candidate families fail:

```txt
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
```

This is a domain-level falsification, not global metaphysical disproof.

---

## 7. Final principle

```txt
Candidates are disposable.
The epistemic machine is not.
```
