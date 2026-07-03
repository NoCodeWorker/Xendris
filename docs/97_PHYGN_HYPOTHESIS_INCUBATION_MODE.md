# Phygn v1.6 — Hypothesis Incubation Mode

## 0. Purpose

Hypothesis Incubation Mode allows early ideas to live without being prematurely upgraded to claims.

It is the antidote to Phygn becoming the Grinch of hypothesis generation.

---

## 1. Incubation input

An incubated hypothesis may be incomplete.

Allowed fields:

```txt
intuition
domain
possible observable
analogy
known unknowns
risk level
next formalization step
```

---

## 2. HypothesisSeed schema

```python
class HypothesisSeed(BaseModel):
    seed_id: str
    title: str
    intuition: str
    domain: str
    possible_observable: str | None
    analogy: str | None
    current_level: str
    risk_level: str
    known_unknowns: list[str]
    next_formalization_steps: list[str]
    forbidden_claims: list[str]
```

---

## 3. Incubation statuses

```txt
INCUBATING_AS_INTUITION
NEEDS_OBSERVABLE
NEEDS_VARIABLES
NEEDS_BASELINE
NEEDS_FAILURE_CONDITION
READY_FOR_TESTABLE_HYPOTHESIS
ARCHIVED_AS_POETIC_OR_ANALOGICAL
```

---

## 4. What incubation allows

Allowed:

```txt
recording intuition
linking possible analogies
creating a research backlog
suggesting formalization steps
preserving creative momentum
```

Blocked:

```txt
publication claim
financial action
scientific validation
automated execution
```

---

## 5. Hope-preserving output

Phygn should say:

```txt
This idea is allowed as a seed.
It is not yet allowed as a claim.
Here is what would make it testable.
```

Not:

```txt
Blocked. Invalid.
```

unless the user asks for claim/action permission.

---

## 6. Incubation report

Generate:

```txt
reports/epistemic_modes/hypothesis_incubation_v1_6.md
```

Must include:

```txt
seed
level
allowed use
blocked use
next steps
risk friction
```

---

## 7. Final principle

```txt
Do not bury a seed because it is not yet a tree.
```
