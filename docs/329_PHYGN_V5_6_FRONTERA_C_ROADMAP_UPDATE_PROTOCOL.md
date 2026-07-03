# Phygn v5.6 — Frontera C Roadmap Update Protocol

## 0. Purpose

This document defines how the Frontera C roadmap changes after LOG_BOUNDARY negative-control failure.

---

## 1. Roadmap update

Create:

```txt
data/frontera_c/disposition/frontera_c_roadmap_update_after_log_boundary_v5_6.json
```

Schema:

```python
class FronteraCRoadmapUpdate(BaseModel):
    previous_active_candidate: str
    previous_blocker: str
    new_blocker: str
    candidates_archived: list[str]
    candidates_retained_as_fixtures: list[str]
    current_validation_status: str
    next_viable_paths: list[str]
    recommended_path: str
    rationale: str
    forbidden_paths: list[str]
```

Required values:

```txt
previous_active_candidate = LOG_BOUNDARY
new_blocker = FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE
current_validation_status = NOT_VALIDATED
```

---

## 2. Next viable paths

The roadmap may select one of:

```txt
EXPAND_VISIBILITY_DATASET
REPRIORITIZE_CANDIDATE_FAMILIES
NEW_EXPERIMENT_DESIGN
HUMAN_SOURCE_LOOKUP_FOR_NEXT_CANDIDATE
PAUSE_VALIDATION_AND_HARDEN_BENCHMARKS
```

Decision guidance:

### EXPAND_VISIBILITY_DATASET

Choose if:

```txt
visibility/decoherence y_true extraction appears scalable from resolved sources
```

### REPRIORITIZE_CANDIDATE_FAMILIES

Choose if:

```txt
LOG_BOUNDARY failed but other candidates may have better control resistance
```

### NEW_EXPERIMENT_DESIGN

Choose if:

```txt
existing literature cannot produce enough independent y_true
```

### HUMAN_SOURCE_LOOKUP_FOR_NEXT_CANDIDATE

Choose if:

```txt
candidate families remain blocked by source identity
```

### PAUSE_VALIDATION_AND_HARDEN_BENCHMARKS

Choose if:

```txt
test/data leakage risk remains too high
```

---

## 3. Recommended path

Default recommendation:

```txt
EXPAND_VISIBILITY_DATASET
```

but only as a data expansion path, not LOG_BOUNDARY rescue.

Rationale:

```txt
The pipeline has successfully extracted accepted y_true from Hackermueller 2004.
The immediate scientific bottleneck is N=4 single-source fragility.
Expanding visibility/decoherence y_true may create a stronger benchmark domain independent of LOG_BOUNDARY.
```

---

## 4. Forbidden paths

Do not allow:

```txt
C-structure ablation for LOG_BOUNDARY
Frontera C validation report from LOG_BOUNDARY
physical claim from v5.4 or v5.5
new benchmark-only score inflation
architecture-only continuation
```

---

## 5. Final principle

```txt
After a control failure, the next step is not rescue.
It is either more independent data or a better candidate.
```
