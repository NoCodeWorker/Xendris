# Phygn v5.9 — Candidate Reality-Contact Protocol

## 0. Purpose

This document defines how candidate families are screened for reality contact.

---

## 1. Candidate registry

Create:

```txt
data/frontera_c/candidates/candidate_family_registry_v5_9.json
```

Schema:

```python
class CandidateFamilyRecord(BaseModel):
    candidate_family_id: str
    display_name: str
    status_before_v5_9: str
    candidate_type: str
    allowed_role: str
    blocked_roles: list[str]
    theoretical_basis: str
    target_observable_classes: list[str]
    required_features: list[str]
    optional_features: list[str]
    prediction_rule_summary: str | None
    can_predict_without_ytrue: bool
    can_run_out_of_source: bool
    can_compare_to_baseline: bool
    can_run_negative_controls: bool
    can_run_c_structure_ablation: bool
    scientific_debt_blockers: list[str]
    notes: list[str]
```

Candidate types:

```txt
C_STRUCTURE_CANDIDATE
METHOD_ONLY
DATA_BASELINE
NEGATIVE_CONTROL
ARCHIVED_FIXTURE
```

---

## 2. Feature schema

Create:

```txt
data/frontera_c/candidates/candidate_feature_schema_v5_9.json
```

Schema:

```python
class CandidateFeatureSchema(BaseModel):
    dataset_id: str
    target_variable: str
    forbidden_feature_columns: list[str]
    allowed_feature_columns: list[str]
    missing_required_features_by_candidate: dict
    derived_feature_rules: list[dict]
    leakage_notes: list[str]
```

Target variable examples:

```txt
visibility_fraction
decoherence_rate
contrast_fraction
coherence_loss_fraction
```

Forbidden:

```txt
target variable itself
original value text
QC-only fields
source-local identifiers used as lookup keys
```

---

## 3. Prediction rules

Create:

```txt
data/frontera_c/candidates/candidate_prediction_rules_v5_9.json
```

Schema:

```python
class CandidatePredictionRule(BaseModel):
    candidate_family_id: str
    rule_id: str
    rule_status: str
    input_features: list[str]
    target_variable: str
    formula_or_algorithm: str
    parameter_policy: str
    training_policy: str
    prediction_domain: str
    constraints: list[str]
    leakage_risk: str
    ablation_plan_available: bool
    notes: list[str]
```

Rule statuses:

```txt
READY_FOR_ALIGNMENT
BLOCKED_MISSING_FEATURES
BLOCKED_LEAKAGE
BLOCKED_AD_HOC_SCALE
BLOCKED_SCIENTIFIC_DEBT
METHOD_ONLY_NOT_CANDIDATE
ARCHIVED_NOT_ACTIVE
```

---

## 4. Reality-contact screen

Create:

```txt
data/frontera_c/candidates/candidate_reality_contact_screen_v5_9.json
```

Fields:

```txt
candidate_family_id
has_target_alignment
has_required_features
has_prediction_rule
has_no_leakage
has_baseline_comparator
has_control_plan
has_ablation_plan
has_no_blocking_debt
reality_contact_passed
failure_reasons
```

Passing requires all booleans true.

---

## 5. Leakage screen

Create:

```txt
data/frontera_c/candidates/candidate_leakage_screen_v5_9.json
```

Leakage checks:

```txt
target_column_not_used
original_value_text_not_used
source_lookup_not_used
page_figure_lookup_not_used
condition_value_not_derived_from_target
duplicate_target_not_used
posthoc_fit_flagged
ad_hoc_scale_flagged
```

Leakage statuses:

```txt
LOW
MEDIUM
HIGH
BLOCKING
```

Any BLOCKING leakage rejects candidate.

---

## 6. Selection decision

Create:

```txt
data/frontera_c/candidates/candidate_selection_decision_v5_9.json
```

Schema:

```python
class CandidateSelectionDecision(BaseModel):
    final_status: str
    selected_candidate_family: str | None
    selected_rule_id: str | None
    candidate_count: int
    passed_candidate_count: int
    rejected_candidate_count: int
    blocked_by_leakage_count: int
    blocked_by_missing_features_count: int
    blocked_by_scientific_debt_count: int
    rationale: str
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
```

---

## 7. Final principle

```txt
Reality contact is the right to be tested, not the right to be believed.
```
