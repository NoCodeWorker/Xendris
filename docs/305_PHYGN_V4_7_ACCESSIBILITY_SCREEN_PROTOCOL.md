# Phygn v4.7 — Accessibility Screen Protocol

## 0. Purpose

This document defines the screening protocol for PHI_CURVATURE.

---

## 1. Source accessibility screen

Create:

```txt
data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json
```

Schema:

```python
class SourceAccessibilityScreen(BaseModel):
    candidate_family: str
    likely_source_domains: list[str]
    known_source_refs: list[str]
    local_source_refs: list[str]
    source_location_quality: str
    source_accessibility_score: float
    blockers: list[str]
    recommended_next_action: str
```

Source location quality:

```txt
HIGH
MEDIUM
LOW
UNKNOWN
NONE
```

---

## 2. Observable accessibility screen

Create:

```txt
data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json
```

Schema:

```python
class ObservableAccessibilityScreen(BaseModel):
    candidate_family: str
    proposed_observables: list[str]
    observable_classes: list[str]
    directly_measurable: list[str]
    proxy_observables: list[str]
    blocked_observables: list[str]
    observable_clarity: str
    observable_accessibility_score: float
    notes: list[str]
```

Potential observable classes:

```txt
VISIBILITY
CONTRAST_DECAY
DECOHERENCE_RATE
CURVATURE_PROXY
BOUNDARY_RESPONSE
PARAMETER_SHIFT
PHASE_SHIFT
NOISE_SPECTRUM
```

---

## 3. y_true accessibility screen

Create:

```txt
data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json
```

Schema:

```python
class YTrueAccessibilityScreen(BaseModel):
    candidate_family: str
    target_observables: list[str]
    plausible_ytrue_sources: list[str]
    manual_extraction_likelihood: str
    public_dataset_likelihood: str
    experiment_required: bool
    minimum_ytrue_feasibility: str
    ytrue_accessibility_score: float
    blockers: list[str]
```

Feasibility levels:

```txt
HIGH
MEDIUM
LOW
UNKNOWN
NONE
```

---

## 4. Public dataset screen

Create:

```txt
data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json
```

Schema:

```python
class PublicDatasetScreen(BaseModel):
    candidate_family: str
    plausible_repository_types: list[str]
    known_dataset_refs: list[str]
    local_dataset_refs: list[str]
    dataset_availability: str
    dataset_accessibility_score: float
    required_search_queries: list[str]
    notes: list[str]
```

Repository types:

```txt
SUPPLEMENTARY_MATERIAL
ZENODO
FIGSHARE
OSF
ARXIV_ANCILLARY
JOURNAL_DATA_REPOSITORY
LOCAL_DATASET
AUTHOR_REQUEST
```

---

## 5. Experimental feasibility screen

Create:

```txt
data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json
```

Schema:

```python
class ExperimentalFeasibilityScreen(BaseModel):
    candidate_family: str
    required_observables: list[str]
    possible_experiment_classes: list[str]
    required_apparatus: list[str]
    required_sensitivity: str | None
    feasibility_level: str
    cost_risk: str
    timeline_risk: str
    experiment_accessibility_score: float
    notes: list[str]
```

---

## 6. Claim risk screen

Create:

```txt
data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json
```

Schema:

```python
class ClaimRiskScreen(BaseModel):
    candidate_family: str
    physical_claim_risk: str
    source_overclaim_risk: str
    benchmark_laundering_risk: str
    slot4_dependency_risk: str
    predictive_gain_misuse_risk: str
    mitigation_rules: list[str]
    claim_risk_score: float
```

Risk levels:

```txt
LOW
MEDIUM
HIGH
CRITICAL
```

---

## 7. Final screening decision

Create:

```txt
data/candidate_screening/phi_curvature_screening_decision_v4_7.json
```

Schema:

```python
class CandidateScreeningDecision(BaseModel):
    candidate_family: str
    final_status: str
    source_score: float
    observable_score: float
    ytrue_score: float
    public_dataset_score: float
    experimental_feasibility_score: float
    claim_risk_score: float
    aggregate_accessibility_score: float
    pass_criteria_met: list[str]
    fail_criteria_met: list[str]
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
    required_guardrails: list[str]
    notes: list[str]
```

---

## 8. Final principle

```txt
Screen before building.
Measure before believing.
```
