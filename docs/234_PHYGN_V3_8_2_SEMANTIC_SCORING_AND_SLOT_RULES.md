# Phygn v3.8.2 — Semantic Scoring & Slot Rules

## 0. Purpose

This document defines triage scoring, slot assignment and priority selection.

---

## 1. Candidate scoring

Each candidate receives:

```txt
semantic_score
source_priority_score
slot_relevance_score
cleanliness_score
specificity_score
risk_score
triage_score
```

Recommended formula:

```txt
triage_score =
  0.25 * semantic_score
+ 0.20 * slot_relevance_score
+ 0.20 * source_priority_score
+ 0.15 * specificity_score
+ 0.10 * cleanliness_score
+ 0.10 * risk_score
```

All scores are in:

```txt
0.0 to 1.0
```

---

## 2. Source priority

```txt
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING = 1.00
SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS = 0.95
SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST = 0.90
SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE = 0.85
SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE = 0.85
```

Rationale:

```txt
Pedernales is the SLOT_4 gradient-component bottleneck.
Schrinski and Nimmrichter are key for hypothesis/constraint pressure.
Hornberger and Hackermueller are key for decoherence baseline/observable grounding.
```

---

## 3. Slot assignment rules

### SLOT_1_DECOHERENCE_BASELINE

Keywords:

```txt
decoherence
collisional decoherence
thermal emission
environmental decoherence
scattering
decoherence rate
loss of coherence
```

### SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE

Keywords:

```txt
visibility
fringe visibility
contrast
interference visibility
coherence loss
interferometer signal
```

### SLOT_3_BENCHMARK_RANGES

Keywords:

```txt
mass
amu
molecule
cluster
nanoparticle
time
separation
distance
temperature
pressure
mbar
K
seconds
```

### SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS

Keywords:

```txt
gradient
field gradient
magnetic field gradient
transition
effective dynamics
Hamiltonian
operator
motional dynamical decoupling
spin-motion coupling
motional state
```

### SLOT_5_PARAMETER_CONSTRAINTS

Keywords:

```txt
CSL
collapse
lambda
r_C
parameter
constraint
bound
exclusion
Bayesian
hypothesis test
macrorealistic modification
MMM
```

### SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS

Keywords:

```txt
negligible
dominates
excluded
ruled out
limitation
noise
background
thermal
environmental
incompatible
falsify
```

### SLOT_7_EXPERIMENTAL_CONTEXT

Keywords:

```txt
setup
experiment
interferometer
KDTLI
LUMI
Talbot
Kapitza-Dirac
nanodiamond
matter-wave
```

### SLOT_8_ANALOGY_ONLY_OR_BACKGROUND

Use when the text is relevant but does not directly map to a pressure slot.

---

## 4. Priority class thresholds

```txt
CRITICAL: triage_score >= 0.82 and slot in SLOT_4/SLOT_5/SLOT_6/SLOT_2
HIGH:     triage_score >= 0.68
MEDIUM:   triage_score >= 0.50
LOW:      triage_score >= 0.35
EXCLUDE:  triage_score < 0.35 or garbage/noise
```

Override:

```txt
Pedernales + SLOT_4 = minimum HIGH if text is non-empty and not obvious garbage.
Schrinski + SLOT_5/SLOT_6 = minimum HIGH if text is non-empty and not obvious garbage.
Nimmrichter + SLOT_5 = minimum HIGH if text is non-empty and not obvious garbage.
```

---

## 5. Cleanliness scoring

Clean text:

```txt
contains normal words
has limited broken spacing
contains coherent sentence or equation-like content
```

Noisy text:

```txt
broken encoding dominates
mostly references
mostly symbols without context
repeated headers
page artifacts
```

---

## 6. Specificity scoring

High specificity if candidate contains:

```txt
equation number
explicit parameter
observable
unit
experimental range
named model
named mechanism
```

Low specificity if generic background only.

---

## 7. Risk scoring

Risk is high if the candidate could:

```txt
contradict PHI_GRADIENT
limit applicability
show benchmark mismatch
force analogy-only classification
block a claim
```

Phygn should prioritize damaging evidence as much as supportive-looking evidence.

---

## 8. Final principle

```txt
A good triage system searches for the passages that can hurt the hypothesis.
```
