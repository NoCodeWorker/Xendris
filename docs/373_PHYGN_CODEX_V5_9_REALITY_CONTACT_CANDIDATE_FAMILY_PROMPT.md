# Codex Prompt — Phygn v5.9 Reality-Contact Candidate Family Construction

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current master package index:

```txt
docs/368_PHYGN_SELF_IMPROVEMENT_MASTER_PACKAGE_INDEX.md
```

Current master decision state:

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT
accepted_ytrue_count = 10
independent_source_count = 5
benchmark_readiness = READY_FOR_MULTI_SOURCE_BENCHMARK
first_failed_gate = candidate_family_selection
blocker_type = MODEL_BLOCKER
```

Therefore v5.9 starts at:

```txt
369
```

---

# 1. Read first

Read v5.9 specs:

```txt
docs/369_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_docs/status/GOAL.md
docs/370_PHYGN_V5_9_CANDIDATE_REALITY_CONTACT_PROTOCOL.md
docs/371_PHYGN_V5_9_CANDIDATE_FAMILIES_AND_THEORY_NOTES.md
docs/372_PHYGN_V5_9_REPORTING_AND_NEXT_GATE.md
```

Also read master roadmap and loop docs:

```txt
docs/357_PHYGN_MASTER_GOAL_FRONTERA_C_VALIDATION_OR_BLOCKAGE.md
docs/358_PHYGN_AUTONOMOUS_ROADMAP_V57_4_TO_V64.md
docs/359_PHYGN_RAILWAYS_GATES_AND_TERMINAL_STATES.md
docs/360_PHYGN_TECHNICAL_ARCHITECTURE_AND_LIBRARIES.md
docs/361_PHYGN_CANDIDATE_STRATEGY_AND_VALIDATION_CRITERIA.md
docs/364_PHYGN_EVIDENCE_GATED_SELF_CORRECTION_LOOP.md
docs/365_PHYGN_BLOCKER_TAXONOMY_AND_MINIMAL_IMPROVEMENT_PROTOCOL.md
docs/366_PHYGN_SCIENTIFIC_VIBE_CODING_RUNTIME_ARCHITECTURE.md
```

---

# 2. Mission

Implement:

```txt
v5.9 — Reality-Contact Candidate Family Construction
```

The mission is to define and screen candidate families for leak-free prediction over the expanded visibility/decoherence dataset.

This phase only selects whether a candidate may enter v6.0.

Do not compute PredictiveGain.

Do not run benchmark scoring.

Do not run negative controls.

Do not run C-structure ablation.

Do not validate Frontera C.

---

# 3. Required inputs

Load:

```txt
docs/PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md

data/frontera_c/master_goal/dataset_v5_7_4_master.json
data/frontera_c/master_goal/quality_v5_7_4_master.json
data/frontera_c/master_goal/benchmark_readiness_v5_7_4_master.json
data/frontera_c/master_goal/candidate_gate_v5_7_4_master.json
data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json
```

Prefer the master-goal dataset if it exists because it reached:

```txt
accepted_ytrue_count = 10
independent_source_count = 5
```

---

# 4. Create package

Create:

```txt
phyng/candidates/
  __init__.py
  schemas.py
  dataset_introspection.py
  family_registry.py
  feature_schema.py
  prediction_rules.py
  reality_contact_screen.py
  leakage_screen.py
  selection_decision.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_reality_contact_candidate_family.py
```

Entrypoint:

```python
run_frontera_c_reality_contact_candidate_family_campaign(root: str | Path = ".")
```

---

# 5. Candidate families

Evaluate at minimum:

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

LOG_BOUNDARY remains archived.

Do not select LOG_BOUNDARY as active validation candidate.

---

# 6. Candidate passing requirements

A candidate passes only if it has:

```txt
has_target_alignment = true
has_required_features = true
has_prediction_rule = true
has_no_leakage = true
has_baseline_comparator = true
has_control_plan = true
has_ablation_plan = true
has_no_blocking_debt = true
```

---

# 7. Forbidden leakage

Reject if the candidate uses:

```txt
visibility_fraction
target value
original_value_text
qc_status as feature
source_id as lookup proxy
page_number as lookup proxy
figure_id as lookup proxy
any value derived from y_true
```

---

# 8. Required outputs

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

# 9. Required reports

Create:

```txt
reports/frontera_c/candidates/candidate_family_registry_v5_9.md
reports/frontera_c/candidates/candidate_feature_schema_v5_9.md
reports/frontera_c/candidates/candidate_prediction_rules_v5_9.md
reports/frontera_c/candidates/candidate_reality_contact_screen_v5_9.md
reports/frontera_c/candidates/candidate_leakage_screen_v5_9.md
reports/frontera_c/candidates/candidate_selection_decision_v5_9.md
reports/campaigns/FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9.md
```

Create final result document:

```txt
docs/374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md
```

---

# 10. Final statuses

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

# 11. Next gate logic

If a candidate passes:

```txt
permit v6.0 — Candidate Prediction Alignment & PredictiveGain Gate
```

Otherwise:

```txt
stop with exact blocker
```

---

# 12. Tests

Create:

```txt
tests/test_v5_9_candidate_family_registry.py
tests/test_v5_9_candidate_feature_schema.py
tests/test_v5_9_candidate_prediction_rules.py
tests/test_v5_9_reality_contact_screen.py
tests/test_v5_9_leakage_screen.py
tests/test_v5_9_candidate_selection_decision.py
tests/test_frontera_c_reality_contact_candidate_family_campaign.py
```

Minimum tests:

```txt
test_log_boundary_not_reactivated
test_candidate_requires_prediction_rule
test_candidate_rejects_target_leakage
test_candidate_rejects_missing_features
test_candidate_requires_baseline_comparator
test_candidate_requires_control_plan
test_candidate_requires_ablation_plan
test_selected_candidate_permits_v60
test_no_predictive_gain_computed
test_no_physical_claim_created
```

---

# 13. Hard constraints

Do not compute PredictiveGain.

Do not train/evaluate benchmark.

Do not run negative controls.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not claim physical support.

Do not reactivate LOG_BOUNDARY.

Do not fabricate candidate features.

Do not allow arbitrary scale L.

Do not use y_true-derived values as input features.

---

# 14. Allowed claims

Allowed if true:

```txt
candidate families were screened
feature schema was created
leakage screen was run
candidate selected for predictive gate
or no candidate has reality contact
```

Blocked:

```txt
candidate validated
Frontera C validated
PredictiveGain exists
physical mechanism confirmed
invariant confirmed
```

---

# 15. Final discipline

```txt
A candidate is not a name.
A candidate is a leak-free rule that can be wrong.
```
