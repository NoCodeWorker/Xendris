# Phygn v3.0 — Real Source Query Plan & Candidate Manifest

## 0. Purpose

This document defines the real source acquisition query plan for PHI_GRADIENT.

The campaign must not rely on vague search terms alone.

It must search by slot and by component.

---

## 1. Query plan schema

```python
class RealSourceQueryPlan(BaseModel):
    campaign_id: str
    target_candidate: str
    slot_queries: list[SlotQuery]
    negative_queries: list[SlotQuery]
    benchmark_queries: list[SlotQuery]
    acquisition_limits: dict[str, int]
    inclusion_rules: list[str]
    exclusion_rules: list[str]
```

```python
class SlotQuery(BaseModel):
    query_id: str
    slot_id: str
    query_text: str
    expected_components: list[str]
    priority: int
    source_types: list[str]
```

---

## 2. Slot query groups

### SLOT 1 — Decoherence baseline / visibility decay

Search for:

```txt
visibility decay decoherence rate interferometry Gamma_env
fringe visibility decoherence exponential decay contrast loss
environmental decoherence rate mesoscopic interferometry visibility
```

Expected components:

```txt
visibility_decay_observable
Gamma_env_rate
baseline_model
contrast_loss_equation
```

---

### SLOT 2 — Mesoscopic interferometry benchmarks

Search for:

```txt
mesoscopic interferometry visibility decoherence benchmark mass separation time
matter wave interferometry macromolecule decoherence visibility data
nanoparticle interferometry decoherence contrast experimental parameters
```

Expected components:

```txt
mass_range
length_or_separation_range
time_range
visibility_measure
environmental_baseline
```

---

### SLOT 3 — Gravitational decoherence models

Search for:

```txt
gravitational decoherence model mass dependent decoherence rate
Diosi Penrose decoherence rate experimental constraints
gravity related collapse model interferometry constraints
```

Expected components:

```txt
mass_dependent_rate
length_scale_dependence
parameter_constraints
negative_constraints
```

---

### SLOT 4 — Gradient / transition operators

Search for:

```txt
gradient term effective decoherence model transition region operator
boundary gradient effective rate contribution
order parameter gradient transition boundary effective action decoherence
```

Expected components:

```txt
gradient_operator
transition_region
rate_contribution
effective_model_component
```

---

### SLOT 5 — Log or scale-space formulations

Search for:

```txt
log scale coordinates decoherence model dimensionless variables
renormalization scale decoherence effective model
scale-space formulation quantum decoherence mesoscopic
```

Expected components:

```txt
dimensionless_log_variables
scale_transformation
model_constraint
```

---

### SLOT 6 — Alpha-like parameter constraints

Search for:

```txt
dimensionless coupling decoherence rate constraint interferometry
collapse model parameter bounds interferometry
decoherence coupling upper bound mesoscopic experiment
```

Expected components:

```txt
alpha_like_constraint
coupling_bound
rate_ratio_constraint
experimental_exclusion
```

---

### SLOT 7 — Negative / conflicting sources

Search for:

```txt
environmental decoherence dominates gravitational decoherence interferometry
experimental bounds exclude gravitational decoherence mesoscopic
decoherence models ruled out interferometry constraints
```

Expected components:

```txt
contradiction
exclusion
dominant_background
parameter_bound_that_kills_effect
```

---

## 3. Inclusion rules

Include source candidates only if they likely contain at least one of:

```txt
equation
observable
parameter range
benchmark data
experimental bound
rate model
explicit negative constraint
```

---

## 4. Exclusion rules

Exclude or mark analogy-only if source contains only:

```txt
broad conceptual discussion
generic gradient language
generic scale language
no observable
no equation
no parameter range
no benchmark
```

---

## 5. Candidate manifest fields

Every candidate source must record:

```txt
source_id
title
authors
year
source_type
url/doi/arxiv/local path
targeted slots
expected components
acquisition status
reason for inclusion
risk of analogy-only
```

---

## 6. Final principle

```txt
A query is good when it knows what would count against the candidate.
```
