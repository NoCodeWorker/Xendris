# Phygn v2.8 — PHI_GRADIENT Source Slot Registry

## 0. Purpose

This document defines the evidence slots required to evaluate PHI_GRADIENT beyond synthetic survival.

Each slot is designed to prevent vague literature decoration.

---

## 1. Source slot model

```python
class SourceEvidenceSlot(BaseModel):
    slot_id: str
    slot_name: str
    required_component: str
    acceptable_support_types: list[str]
    unacceptable_support_types: list[str]
    minimum_extract_fields: list[str]
    status: str
```

---

## 2. Slot 1 — Decoherence baseline models

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
```

Purpose:

```txt
Constrain V_base(t), Gamma_env, visibility decay and baseline observables.
```

Acceptable support:

```txt
explicit visibility decay model
decoherence rate equation
interferometric contrast loss model
environmental decoherence baseline
```

Unacceptable support:

```txt
generic mention of decoherence
popular science description
non-equation qualitative analogy only
```

---

## 3. Slot 2 — Gravitational decoherence models

```txt
SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS
```

Purpose:

```txt
Identify whether gravitational or mass/scale-related decoherence models offer comparable or conflicting structures.
```

Acceptable support:

```txt
explicit gravitational decoherence model
mass-dependent decoherence rate
length-scale-dependent decoherence proposal
experimental constraint on gravitational decoherence
```

Unacceptable support:

```txt
mere mention of gravity and quantum mechanics
speculative analogy without observable
```

---

## 4. Slot 3 — Log or scale-space formulations

```txt
SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS
```

Purpose:

```txt
Evaluate whether log coordinates or scale-space transformations are meaningful in comparable physical modeling contexts.
```

Acceptable support:

```txt
explicit dimensionless log variables
scale transformation used in model derivation
renormalization/scale-space analogy with mathematical constraint
```

Unacceptable support:

```txt
generic statement that logarithms are useful
log plot without model significance
```

---

## 5. Slot 4 — Gradient/transition operators

```txt
SLOT_4_GRADIENT_TRANSITION_OPERATORS
```

Purpose:

```txt
Evaluate whether transition gradients or boundary derivatives appear as meaningful operators in comparable effective models.
```

Acceptable support:

```txt
explicit gradient term
transition-region operator
derivative of boundary/order parameter
rate contribution from gradient structure
```

Unacceptable support:

```txt
word 'gradient' used metaphorically
optimization gradient unrelated to physical observable
```

---

## 6. Slot 5 — Mesoscopic interferometry benchmarks

```txt
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
```

Purpose:

```txt
Find benchmark systems where visibility decay or decoherence can be compared numerically.
```

Acceptable support:

```txt
experimental interferometry data
visibility decay dataset
published benchmark parameter ranges
mesoscopic mass/length/time ranges
```

Unacceptable support:

```txt
proposal without observable
experiment unrelated to visibility/decoherence
```

---

## 7. Slot 6 — Alpha-like parameter constraints

```txt
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
```

Purpose:

```txt
Constrain alpha-like coupling strength.
```

Acceptable support:

```txt
parameter bound
fitted coupling
upper/lower constraint
dimensionless rate ratio constraint
```

Unacceptable support:

```txt
arbitrary alpha choice
toy parameter with no external bound
```

---

## 8. Slot 7 — Negative or conflicting sources

```txt
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
```

Purpose:

```txt
Record sources that contradict, constrain or make PHI_GRADIENT implausible.
```

Acceptable support:

```txt
experimental exclusion
model incompatibility
known decoherence dominance that overwhelms candidate
parameter bound that kills effect
```

---

## 9. Slot 8 — Observable visibility decay support

```txt
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

Purpose:

```txt
Ensure the observable under discussion is not vague.
```

Acceptable support:

```txt
visibility contrast definition
fringe visibility equation
measured contrast decay
observable linked to Gamma_env or decoherence rate
```

---

## 10. Final principle

```txt
A slot is not filled by a theme.
It is filled by a constraint.
```
