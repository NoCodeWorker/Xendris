# Phygn v4.6 — Experiment Requirement & Next Candidate Matrix

## 0. Purpose

This document defines when PHI_GRADIENT requires new experiment and how to select the next candidate family.

---

## 1. Experiment requirement

Create:

```txt
data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json
```

Schema:

```python
class ExperimentRequirement(BaseModel):
    candidate_id: str
    requirement_status: str
    required_observables: list[str]
    minimum_measurements: int
    required_sensitivity: str | None
    required_apparatus: list[str]
    feasibility_risk: str
    cost_risk: str
    timeline_risk: str
    reason: str
    recommended_action: str
```

Allowed requirement statuses:

```txt
NOT_REQUIRED_IF_ARCHIVED
REQUIRED_TO_UNFREEZE
REQUIRED_BUT_NOT_CURRENTLY_FEASIBLE
REQUIRED_AND_FEASIBILITY_STUDY_RECOMMENDED
```

---

## 2. Next candidate family selection matrix

Create:

```txt
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
```

Candidate families to consider:

```txt
PHI_CURVATURE
PHI_LOCALIZED_WINDOW
PHI_BANDPASS
PHI_GRADIENT
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
```

Selection criteria:

```txt
synthetic survivability
negative-control resistance
source-support availability
y_true accessibility
public dataset availability
observable clarity
SLOT_4 independence
experimental feasibility
claim-risk level
```

Schema:

```python
class CandidateFamilySelectionRecord(BaseModel):
    family_id: str
    previous_status: str
    synthetic_survivability_score: float | None
    negative_control_resistance_score: float | None
    source_support_availability: str
    y_true_accessibility: str
    public_dataset_availability: str
    observable_clarity: str
    slot4_independence: str
    experimental_feasibility: str
    claim_risk_level: str
    selection_score: float
    recommended_action: str
    notes: list[str]
```

---

## 3. Recommended actions

```txt
SELECT_FOR_SOURCE_AND_YTRUE_SCREENING
KEEP_AS_METHOD_ONLY
ARCHIVE
REQUIRES_EXPERIMENT_DESIGN
REJECT_AS_ARTIFACT
```

---

## 4. Selection rule

Do not select a next candidate by synthetic score alone.

Required:

```txt
y_true accessibility must be HIGH or MEDIUM
or experimental feasibility must be HIGH or MEDIUM
or public dataset availability must be plausible
```

If no family qualifies:

```txt
NO_CANDIDATE_READY_FOR_PREDICTIVE_PIPELINE
```

---

## 5. Final principle

```txt
The next candidate must be selected for contact with reality, not beauty in simulation.
```
