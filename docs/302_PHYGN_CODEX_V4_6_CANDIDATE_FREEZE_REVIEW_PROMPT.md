# Codex Prompt — Phygn v4.6 Candidate Freeze Review & Pivot Decision

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current latest result document:

```txt
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
```

Therefore v4.6 starts at:

```txt
298
```

---

# 1. Read first

Read these v4.6 specs:

```txt
docs/298_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_docs/status/GOAL.md
docs/299_PHYGN_V4_6_FINAL_CLAIM_PERMISSION_AND_METHOD_REDEFINITION.md
docs/300_PHYGN_V4_6_EXPERIMENT_REQUIREMENT_AND_NEXT_CANDIDATE_MATRIX.md
docs/301_PHYGN_V4_6_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
docs/285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
```

---

# 2. First action

Run focused v4.5 validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_external_evidence_loader_v4_5.py tests/test_external_table_review_v4_5.py tests/test_external_supplementary_search_v4_5.py tests/test_external_public_dataset_search_v4_5.py tests/test_external_ytrue_candidates_v4_5.py tests/test_external_dataset_update_v4_5.py tests/test_external_freeze_decision_v4_5.py tests/test_phi_gradient_external_evidence_campaign_v4_5.py
```

Expected recent result:

```txt
v4.5 tests pass.
```

---

# 3. Mission

Implement:

```txt
v4.6 — Candidate Freeze Review & Pivot Decision
```

Do not compute PredictiveGain.

Do not attempt to rescue PHI_GRADIENT through new benchmark abstractions.

Do not close SLOT_4 debt.

---

# 4. Required inputs

Load:

```txt
data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json
data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json
data/external_evidence/phi_gradient_table_review_results_v4_5.json
data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json
data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json
data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json
data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json
data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json
data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
```

Optional historical candidate artifacts:

```txt
data/closed_loop/
data/synthetic_benchmark_design/
data/source_pressure/
data/benchmarks/
```

If freeze decision is missing:

```txt
PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION
```

---

# 5. Create package

Create:

```txt
phyng/candidate_decision/
  __init__.py
  schemas.py
  loader.py
  freeze_review.py
  claim_permissions.py
  method_redefinition.py
  experiment_requirement.py
  next_candidate_matrix.py
  pivot_decision.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_candidate_freeze_review.py
```

Entrypoint:

```python
run_phi_gradient_candidate_freeze_review_campaign(root: str | Path = ".")
```

---

# 6. Decision logic

Given:

```txt
accepted_y_true_count = 0
freeze_status = FROZEN_NO_YTRUE_AVAILABLE
PredictiveGain = UNDEFINED_INSUFFICIENT_YTRUE
SLOT_4 = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Default decision:

```txt
REDEFINE_AS_METHOD_ONLY
```

and optionally:

```txt
PIVOT_TO_NEXT_CANDIDATE_FAMILY
```

Do not choose active predictive continuation for PHI_GRADIENT.

---

# 7. Method-only redefinition

Create a method-only object with required label:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

Allowed roles:

```txt
negative-control generator
benchmark-shaping heuristic
candidate-stress-test fixture
source-pressure pipeline test case
claim-gating regression fixture
```

Prohibited roles:

```txt
physical model
validated mechanism
predictive model
Frontera C evidence
invariant confirmation
```

---

# 8. Next candidate matrix

Evaluate candidate families:

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

Do not select by synthetic score alone.

Prioritize:

```txt
y_true accessibility
public dataset availability
observable clarity
SLOT_4 independence
experimental feasibility
```

---

# 9. Output files

Create:

```txt
data/candidate_decisions/phi_gradient_freeze_review_v4_6.json
data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json
```

---

# 10. Reports

Generate:

```txt
reports/candidate_decisions/phi_gradient_freeze_review_v4_6.md
reports/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.md
reports/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.md
reports/candidate_decisions/phi_gradient_experiment_requirement_v4_6.md
reports/candidate_decisions/next_candidate_family_selection_matrix_v4_6.md
reports/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.md
reports/campaigns/PHI-GRADIENT-CANDIDATE-FREEZE-REVIEW-v4_6.md
```

---

# 11. Statuses

Add mappings:

```txt
PHI_GRADIENT_FREEZE_REVIEW_COMPLETED
PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION
PHI_GRADIENT_ARCHIVED_EMPIRICALLY_UNGROUNDED
PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY
PHI_GRADIENT_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_PIVOT_TO_NEXT_CANDIDATE
```

---

# 12. Tests

Create:

```txt
tests/test_candidate_decision_loader_v4_6.py
tests/test_phi_gradient_freeze_review_v4_6.py
tests/test_phi_gradient_final_claim_permissions_v4_6.py
tests/test_phi_gradient_method_redefinition_v4_6.py
tests/test_phi_gradient_experiment_requirement_v4_6.py
tests/test_next_candidate_matrix_v4_6.py
tests/test_phi_gradient_pivot_decision_v4_6.py
tests/test_phi_gradient_candidate_freeze_review_campaign_v4_6.py
```

Minimum tests:

```txt
test_missing_freeze_decision_blocks_review
test_zero_ytrue_blocks_predictive_continuation
test_phi_gradient_redefined_method_only
test_method_only_prohibits_physical_model_role
test_final_claim_permissions_block_predictive_gain
test_final_claim_permissions_block_physical_claim
test_slot4_debt_remains_open
test_next_candidate_not_selected_by_synthetic_score_alone
test_pivot_decision_created
test_no_predictive_gain_created
test_no_ytrue_created
test_reports_include_canonical_status
```

---

# 13. Behavior preservation

Do not alter:

```txt
v4.5 external evidence results
v4.4.2 audit remediation
v4.4 manual extraction
v4.3 y_true extraction
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
PHI_GRADIENT is validated.
PHI_GRADIENT has PredictiveGain.
PHI_GRADIENT is empirically supported.
Method-only means physical.
Pivot means success.
Archive means failure.
```

Allowed:

```txt
PHI_GRADIENT was frozen as empirically ungrounded under current artifacts.
PHI_GRADIENT was redefined as method-only if the gate says so.
A pivot candidate family was recommended if selection criteria support it.
```

---

# 15. Acceptance criteria

Complete when:

```txt
v4.5 freeze decision loaded
v4.6 tests pass
freeze review generated
final claim permissions generated
method-only redefinition generated
experiment requirement generated
next candidate matrix generated
pivot decision generated
reports generated
no PredictiveGain created
no y_true created
no physical claim upgraded
SLOT_4 debt remains open
```

---

# 16. Final discipline

```txt
A frozen candidate is not dead knowledge.
It is protected knowledge.
```
