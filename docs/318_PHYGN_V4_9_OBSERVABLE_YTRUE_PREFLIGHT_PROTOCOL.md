# Phygn v4.9 — Observable/y_true Preflight Protocol

## 0. Purpose

This document defines observable identity and y_true path plausibility before a candidate enters a pipeline.

---

## 1. Observable identity matrix

Create:

```txt
data/preflight/source_identity/observable_identity_matrix_v4_9.json
```

Schema:

```python
class ObservableIdentityRecord(BaseModel):
    family_id: str
    source_id: str | None
    observable_class: str
    observable_name: str
    source_locatable: bool
    expected_location_type: str | None
    expected_unit: str | None
    numeric_value_expected: bool
    observable_status: str
    blockers: list[str]
```

Observable statuses:

```txt
SOURCE_LOCATABLE
SOURCE_NOT_LOCATABLE
THEORETICAL_ONLY
PROXY_ONLY
UNKNOWN
```

Allowed observable classes:

```txt
VISIBILITY
CONTRAST_DECAY
DECOHERENCE_RATE
PHASE_DECAY_RATE
PHASE_SHIFT
CURVATURE_PROXY
LOCALIZATION_WIDTH
BANDPASS_RESPONSE
BOUNDARY_RESPONSE
NOISE_SPECTRUM
PARAMETER_BOUND
```

---

## 2. y_true path plausibility matrix

Create:

```txt
data/preflight/source_identity/ytrue_path_plausibility_matrix_v4_9.json
```

Schema:

```python
class YTruePathPlausibilityRecord(BaseModel):
    family_id: str
    source_id: str | None
    observable_class: str
    possible_ytrue_source: str
    plausibility_level: str
    requires_manual_review: bool
    requires_download: bool
    requires_new_experiment: bool
    blockers: list[str]
```

Plausibility levels:

```txt
HIGH
MEDIUM
LOW
NONE
UNKNOWN
```

---

## 3. Plausibility rules

A y_true path can be HIGH only if:

```txt
source identity complete
observable source-locatable
numeric value expected
local artifact or exact external identity exists
```

A y_true path can be MEDIUM if:

```txt
source identity complete
observable class is plausible
download/manual review is required
```

A y_true path must be LOW/NONE if:

```txt
source identity incomplete
observable theoretical-only
no numeric value expected
source unavailable
```

---

## 4. Candidate preflight decision matrix

Create:

```txt
data/preflight/source_identity/candidate_preflight_decision_matrix_v4_9.json
```

Schema:

```python
class CandidatePreflightDecisionRecord(BaseModel):
    family_id: str
    resolvable_source_count: int
    local_or_exact_source_count: int
    source_locatable_observable_count: int
    plausible_ytrue_path_count: int
    slot4_dependency: str
    claim_risk: str
    preflight_status: str
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
    required_next_action: str
    notes: list[str]
```

Preflight statuses:

```txt
PREFLIGHT_PASSED
PREFLIGHT_PARTIAL_REQUIRES_SOURCE_ACQUISITION
PREFLIGHT_FAILED_NO_RESOLVABLE_SOURCES
PREFLIGHT_FAILED_NO_YTRUE_PATH
PREFLIGHT_BLOCKED_SLOT4_DEPENDENCY
PREFLIGHT_REQUIRES_HUMAN_LOOKUP
```

---

## 5. Final principle

```txt
A candidate does not deserve a pipeline until its evidence path is named.
```
