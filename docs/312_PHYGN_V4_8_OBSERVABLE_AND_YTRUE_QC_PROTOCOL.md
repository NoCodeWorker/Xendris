# Phygn v4.8 — Observable & y_true QC Protocol

## 0. Purpose

This document defines candidate observables and strict y_true acceptance for PHI_CURVATURE.

---

## 1. Candidate observables

Create:

```txt
data/phi_curvature/evidence/phi_curvature_candidate_observables_v4_8.json
```

Schema:

```python
class PhiCurvatureCandidateObservable(BaseModel):
    observable_id: str
    candidate_family: str
    source_id: str
    observable_class: str
    variable_name: str
    expected_unit: str | None
    source_location_type: str | None
    source_location_value: str | None
    candidate_text: str | None
    numeric_candidate_present: bool
    extraction_status: str
    blockers: list[str]
```

Allowed observable classes:

```txt
CURVATURE_PROXY
DECOHERENCE_RATE
PHASE_DECAY_RATE
VISIBILITY
CONTRAST_DECAY
PHASE_SHIFT
NOISE_SPECTRUM
BOUNDARY_RESPONSE
```

---

## 2. y_true candidates

Create:

```txt
data/phi_curvature/evidence/phi_curvature_ytrue_candidates_v4_8.json
```

Schema:

```python
class PhiCurvatureYTrueCandidate(BaseModel):
    candidate_id: str
    observable_id: str
    source_id: str
    source_hash: str | None
    observable_class: str
    variable_name: str
    value: float | None
    unit: str | None
    uncertainty: float | None
    source_location_type: str | None
    source_location_value: str | None
    extraction_method: str
    provenance_status: str
    qc_status: str
    matched_prediction_placeholder: bool
    can_enter_dataset: bool
    rejection_reason: str | None
```

---

## 3. y_true acceptance rule

Accept only if:

```txt
value is numeric
unit exists unless explicitly dimensionless
source_hash exists
source location exists
source identity resolved
provenance_status = PROVENANCE_COMPLETE
qc_status in PASS, PASS_WITH_LIMITATIONS
```

For v4.8, matched prediction may be placeholder:

```txt
matched_prediction_placeholder = true
```

because the minimal campaign precedes full benchmark construction.

However:

```txt
matched_prediction_placeholder does not allow PredictiveGain.
```

---

## 4. Accepted y_true

Create:

```txt
data/phi_curvature/evidence/phi_curvature_accepted_ytrue_v4_8.json
```

Accepted record schema:

```python
class PhiCurvatureAcceptedYTrue(BaseModel):
    y_true_id: str
    candidate_id: str
    observable_id: str
    source_id: str
    source_hash: str
    observable_class: str
    variable_name: str
    value: float
    unit: str
    uncertainty: float | None
    source_location_type: str
    source_location_value: str
    extraction_method: str
    limitations: list[str]
```

---

## 5. Rejected y_true

Create:

```txt
data/phi_curvature/evidence/phi_curvature_rejected_ytrue_v4_8.json
```

Rejection reasons:

```txt
SOURCE_UNRESOLVED
SOURCE_NOT_AVAILABLE
NO_NUMERIC_VALUE
MISSING_UNIT
MISSING_LOCATION
MISSING_HASH
PROVENANCE_INCOMPLETE
AMBIGUOUS_OBSERVABLE
CONSTRAINT_NOT_YTRUE
LIMITATION_NOT_YTRUE
```

---

## 6. Minimal dataset

Create:

```txt
data/phi_curvature/datasets/phi_curvature_minimal_ytrue_dataset_v4_8.json
```

Fields:

```txt
dataset_id
candidate_family
accepted_ytrue_count
minimum_threshold
threshold_reached
records
predictive_gain_status
physical_claim_permission
notes
```

Required values:

```txt
predictive_gain_status = UNDEFINED_NOT_COMPUTED_IN_MINIMAL_CAMPAIGN
physical_claim_permission = BLOCKED
```

---

## 7. Final principle

```txt
A number without provenance is not truth.
It is temptation.
```
