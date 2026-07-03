# Phygn v3.8.3 — Promotion Decision Rules

## 0. Purpose

This document defines how priority review items become validation-ready extracts.

---

## 1. Review decisions

Each item must receive one of:

```txt
PROMOTE_VALIDATION_READY
REJECT_GARBAGE
REJECT_TOO_AMBIGUOUS
REJECT_UNSUPPORTED_ROLE
REJECT_DUPLICATE
SEND_TO_MANUAL_REVIEW
CLASSIFY_ANALOGY_ONLY
CLASSIFY_NEGATIVE_OR_LIMITATION
```

---

## 2. Promotion requirements

A priority item can be promoted only if all are true:

```txt
source_id is present
sha256 is present and matches v3.6 hash manifest
page_number or exact location is present
exact_text_or_preview is non-empty
text is legible enough for review
assigned_slot is not SLOT_8 unless explicitly analogy-only
component role is clear
decision_needed can be answered by the extract
limitations are recorded
```

Promotion status:

```txt
PROMOTE_VALIDATION_READY
```

---

## 3. Component roles

Allowed promoted roles:

```txt
DECOHERENCE_BASELINE
VISIBILITY_COHERENCE_OBSERVABLE
BENCHMARK_RANGE
GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
PARAMETER_CONSTRAINT
NEGATIVE_CONSTRAINT_LIMITATION
EXPERIMENTAL_CONTEXT
```

Non-promoted roles:

```txt
ANALOGY_ONLY
BACKGROUND_ONLY
REJECTED_GARBAGE
REQUIRES_MANUAL_REVIEW
```

---

## 4. Slot-specific promotion rules

### SLOT_1_DECOHERENCE_BASELINE

Promote if text cleanly identifies:

```txt
collisional decoherence
thermal emission decoherence
environmental decoherence mechanism
decoherence rate
visibility loss caused by environment
```

### SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE

Promote if text cleanly identifies:

```txt
fringe visibility
interference contrast
coherence loss
observed visibility
observable used to falsify coherence-loss models
```

### SLOT_3_BENCHMARK_RANGES

Promote if text cleanly includes:

```txt
mass range
time range
distance/separation
temperature/pressure
experimental regime
```

with at least one number, unit or named setup.

### SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS

Promote only if text links gradient/transition/effective dynamics to:

```txt
motional state
spin-motion coupling
Hamiltonian/operator
decoherence suppression/protection
interferometry dynamics
observable effect
```

If gradient appears only as experimental apparatus with no pressure on PHI_GRADIENT:

```txt
CLASSIFY_ANALOGY_ONLY
```

### SLOT_5_PARAMETER_CONSTRAINTS

Promote if text cleanly includes:

```txt
CSL/MMM/collapse parameter
bound or exclusion
Bayesian hypothesis test
constraint relation
parameter range
```

### SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS

Promote if text cleanly identifies:

```txt
limitation
dominant background
negligible effect
mismatch
exclusion
failure condition
```

These are important and should be prioritized.

---

## 5. Manual review rules

Send to manual review if:

```txt
equation formatting is damaged
text is promising but broken
page location uncertain
role ambiguous between analogy and support
missing nearby context
candidate references a figure/table not captured
```

---

## 6. Analogy-only rules

Classify as analogy-only if:

```txt
text is scientifically relevant
but does not constrain, support, contradict or benchmark PHI_GRADIENT
```

Analogy-only material is useful context, not pressure.

---

## 7. Negative/limitation rule

Negative or limitation extracts must not be down-ranked.

If clean and relevant:

```txt
PROMOTE_VALIDATION_READY
```

because v3.9 must be able to hurt PHI_GRADIENT.

---

## 8. Final principle

```txt
The most valuable extract may be the one that blocks the claim.
```
