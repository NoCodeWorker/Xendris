# Phygn v5.9 — Reality-Contact Candidate Family Construction Goal

## 0. Context

The current master result reports:

```txt
Final terminal status: NO_CANDIDATE_WITH_REALITY_CONTACT
Last completed gate: v5.8 - dataset threshold / benchmark readiness preflight
First failed gate: candidate_family_selection
Blocker type: MODEL_BLOCKER
accepted_ytrue_count = 10
independent_source_count = 5
benchmark_readiness = READY_FOR_MULTI_SOURCE_BENCHMARK
```

The current package index is:

```txt
docs/368_PHYGN_SELF_IMPROVEMENT_MASTER_PACKAGE_INDEX.md
```

Therefore v5.9 starts at:

```txt
369
```

---

## 1. Core problem

The project now has enough observed truth to build a multi-source benchmark.

But it does not yet have a valid candidate family with a leak-free prediction rule over the expanded visibility/decoherence dataset.

Current blocker:

```txt
MODEL_BLOCKER
NO_CANDIDATE_WITH_REALITY_CONTACT
```

---

## 2. Core rule

```txt
Now that the dataset can judge,
the candidate must earn the right to be judged.
```

---

## 3. Mission

Implement:

```txt
v5.9 — Reality-Contact Candidate Family Construction
```

The mission is to define, screen and select at least one candidate family that can generate predictions over the expanded visibility/decoherence y_true dataset without target leakage.

This phase does not compute PredictiveGain.

This phase does not run negative controls.

This phase does not run C-structure ablation.

This phase only decides whether a candidate family has the right to enter v6.0 prediction alignment.

---

## 4. Primary objective

Create a candidate family registry and selection gate that can decide whether any candidate has:

```txt
reality contact
feature availability
target alignment
prediction rule
baseline comparability
leakage resistance
control-testability
C-structure ablation possibility
```

---

## 5. Required inputs

Load:

```txt
docs/PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
docs/368_PHYGN_SELF_IMPROVEMENT_MASTER_PACKAGE_INDEX.md

data/frontera_c/master_goal/dataset_v5_7_4_master.json
data/frontera_c/master_goal/quality_v5_7_4_master.json
data/frontera_c/master_goal/benchmark_readiness_v5_7_4_master.json
data/frontera_c/master_goal/candidate_gate_v5_7_4_master.json
data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json
```

If the master-goal dataset exists, prefer it as canonical because it reached:

```txt
accepted_ytrue_count = 10
independent_source_count = 5
```

---

## 6. Candidate families to consider

At minimum evaluate:

```txt
PHI_CURVATURE
PHI_LOCALIZED_WINDOW
PHI_BANDPASS
PHI_GRADIENT_METHOD_ONLY
B_SUPPRESSED
QB_STRUCTURAL
THRESHOLD_SATURATION
DATA_DRIVEN_PHYSICS_BASELINE
C_COORDINATE_RESPONSE
SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE
```

LOG_BOUNDARY remains archived as validation candidate.

It may only be used as:

```txt
benchmark fixture
negative-control fixture
pipeline regression fixture
```

It must not be selected as active validation candidate.

---

## 7. Reality-contact requirements

A candidate has reality contact only if it can define all of:

```txt
input_feature_schema
observable_target
prediction_rule
required_parameters
parameter_fitting_policy
out_of_source_evaluation_policy
baseline_comparison_policy
leakage_screen
negative_control_plan
C_structure_ablation_plan
```

A candidate must be rejected if it:

```txt
uses y_true directly as input
uses source_id as target proxy
uses location labels as target proxy
interpolates exact y_true values
requires unavailable physical variables
requires arbitrary ad hoc scale L
requires unresolved scientific debt
cannot produce predictions for all benchmark records
cannot be compared to a baseline
cannot be ablated for C-structure
```

---

## 8. Strict no-leakage rule

Forbidden features:

```txt
visibility_fraction
target value
original_value_text
qc_status as predictive feature
source_id if it functions as direct lookup
page_number if it functions as direct lookup
figure_id if it functions as direct lookup
any value derived from y_true
```

Allowed features only if present and not target-derived:

```txt
heating_power_W
temperature_K
pressure_mbar or pressure_Pa
time_s
mass_amu or mass_kg
path_separation_m
velocity_m_s
molecule_class
decoherence_mechanism_class
regime labels if not target-derived
source-independent normalized condition variables
C-coordinates Q, B, u, w if all required physical quantities and scales are justified
```

---

## 9. Output artifacts

Create:

```txt
data/frontera_c/candidates/candidate_family_registry_v5_9.json
data/frontera_c/candidates/candidate_feature_schema_v5_9.json
data/frontera_c/candidates/candidate_prediction_rules_v5_9.json
data/frontera_c/candidates/candidate_reality_contact_screen_v5_9.json
data/frontera_c/candidates/candidate_leakage_screen_v5_9.json
data/frontera_c/candidates/candidate_selection_decision_v5_9.json
data/frontera_c/candidates/v5_9_next_gate_decision.json
```

---

## 10. Final statuses

Emit exactly one:

```txt
CANDIDATE_FAMILY_SELECTED_FOR_PREDICTIVE_GATE
NO_CANDIDATE_WITH_REALITY_CONTACT
CANDIDATE_SELECTION_REQUIRES_THEORY_REFORMULATION
CANDIDATE_SELECTION_REQUIRES_NEW_OBSERVABLES
CANDIDATE_SELECTION_REQUIRES_NEW_EXPERIMENT
CANDIDATE_SELECTION_BLOCKED_BY_LEAKAGE
CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES
CANDIDATE_SELECTION_BLOCKED_BY_SCIENTIFIC_DEBT
```

---

## 11. Next gate

If one or more candidate families pass:

```txt
permit v6.0 — Candidate Prediction Alignment & PredictiveGain Gate
```

If none pass:

```txt
stop with exact blocker
```

---

## 12. Final principle

```txt
A candidate is not a name.
A candidate is a leak-free rule that can be wrong.
```
