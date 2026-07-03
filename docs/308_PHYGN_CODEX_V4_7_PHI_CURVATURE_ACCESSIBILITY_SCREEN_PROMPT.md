# Codex Prompt — Phygn v4.7 PHI_CURVATURE Source/y_true Accessibility Screen

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
docs/303_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_RESULTS.md
```

Therefore v4.7 starts at:

```txt
304
```

---

# 1. Read first

Read these v4.7 specs:

```txt
docs/304_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_docs/status/GOAL.md
docs/305_PHYGN_V4_7_ACCESSIBILITY_SCREEN_PROTOCOL.md
docs/306_PHYGN_V4_7_DECISION_GATE_AND_GUARDRAILS.md
docs/307_PHYGN_V4_7_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/303_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_RESULTS.md
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
docs/285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
```

---

# 2. First action

Run focused v4.6 validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_candidate_decision_loader_v4_6.py tests/test_phi_gradient_freeze_review_v4_6.py tests/test_phi_gradient_final_claim_permissions_v4_6.py tests/test_phi_gradient_method_redefinition_v4_6.py tests/test_phi_gradient_experiment_requirement_v4_6.py tests/test_next_candidate_matrix_v4_6.py tests/test_phi_gradient_pivot_decision_v4_6.py tests/test_phi_gradient_candidate_freeze_review_campaign_v4_6.py
```

Expected recent result:

```txt
v4.6 tests pass.
```

---

# 3. Mission

Implement:

```txt
v4.7 — PHI_CURVATURE Source/y_true Accessibility Screen
```

Do not build a full PHI_CURVATURE pipeline.

Only screen accessibility.

---

# 4. Required inputs

Load:

```txt
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json
data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Optional historical PHI_CURVATURE artifacts:

```txt
data/synthetic_benchmark_design/
data/closed_loop/
data/source_pressure/
data/benchmarks/
reports/
docs/
```

If pivot decision missing:

```txt
PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION
```

---

# 5. Create package

Create:

```txt
phyng/candidate_screening/
  __init__.py
  schemas.py
  loader.py
  source_accessibility.py
  observable_accessibility.py
  ytrue_accessibility.py
  public_dataset_screen.py
  experimental_feasibility.py
  claim_risk.py
  decision.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_curvature_accessibility_screen.py
```

Entrypoint:

```python
run_phi_curvature_accessibility_screen_campaign(root: str | Path = ".")
```

---

# 6. Screening requirements

Evaluate:

```txt
source accessibility
observable clarity
y_true accessibility
public dataset availability
supplementary plausibility
experimental feasibility
SLOT_4 independence
claim risk
```

Do not invent public datasets or source references.

If unknown:

```txt
UNKNOWN
```

not optimistic.

---

# 7. Decision rule

PHI_CURVATURE may pass only if at least two are true:

```txt
source_accessibility >= MEDIUM
observable_clarity >= MEDIUM
y_true_accessibility >= MEDIUM
public_dataset_availability >= PLAUSIBLE
experimental_feasibility >= MEDIUM
slot4_independence = TRUE
```

If not:

```txt
PARTIAL
FAILED
REQUIRES_EXPERIMENT
REJECTED_NO_REALITY_CONTACT
```

---

# 8. Output files

Create:

```txt
data/candidate_screening/phi_curvature_screening_inputs_v4_7.json
data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json
data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json
data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json
data/candidate_screening/phi_curvature_screening_decision_v4_7.json
```

---

# 9. Reports

Generate:

```txt
reports/candidate_screening/phi_curvature_screening_inputs_v4_7.md
reports/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_public_dataset_screen_v4_7.md
reports/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_claim_risk_screen_v4_7.md
reports/candidate_screening/phi_curvature_screening_decision_v4_7.md
reports/campaigns/PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7.md
```

---

# 10. Statuses

Add mappings:

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED
PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL
PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED
PHI_CURVATURE_REQUIRES_EXPERIMENT_BEFORE_PIPELINE
PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT
```

---

# 11. Tests

Create:

```txt
tests/test_phi_curvature_screen_loader_v4_7.py
tests/test_phi_curvature_source_accessibility_v4_7.py
tests/test_phi_curvature_observable_accessibility_v4_7.py
tests/test_phi_curvature_ytrue_accessibility_v4_7.py
tests/test_phi_curvature_public_dataset_screen_v4_7.py
tests/test_phi_curvature_experimental_feasibility_v4_7.py
tests/test_phi_curvature_claim_risk_v4_7.py
tests/test_phi_curvature_screening_decision_v4_7.py
tests/test_phi_curvature_accessibility_campaign_v4_7.py
```

Minimum tests:

```txt
test_missing_pivot_decision_blocks_screen
test_screen_does_not_create_ytrue
test_screen_does_not_create_predictive_gain
test_unknown_sources_do_not_pass_as_medium
test_unknown_public_datasets_do_not_pass_as_plausible
test_pass_requires_at_least_two_accessibility_criteria
test_high_claim_risk_blocks_pass
test_slot4_dependency_blocks_physical_candidate
test_phi_gradient_remains_method_only
test_decision_blocks_full_pipeline_if_screen_failed
test_partial_screen_allows_only_targeted_source_discovery
test_reports_include_canonical_status
```

---

# 12. Behavior preservation

Do not alter:

```txt
v4.6 candidate freeze review
v4.5 external evidence
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

# 13. Do not overclaim

Do not write:

```txt
PHI_CURVATURE is validated.
PHI_CURVATURE has PredictiveGain.
PHI_CURVATURE is empirically supported.
Accessibility screen proves evidence.
Pivot means success.
```

Allowed:

```txt
PHI_CURVATURE was screened for source/y_true accessibility.
The screen result allows or blocks a minimal next phase.
Accessibility is permission to look for evidence, not evidence.
```

---

# 14. Acceptance criteria

Complete when:

```txt
v4.6 pivot decision loaded
v4.7 tests pass
all screen artifacts generated
all reports generated
screening decision generated
no y_true created
no PredictiveGain created
no physical claim upgraded
PHI_GRADIENT remains method-only
SLOT_4 debt remains open and scoped
```

---

# 15. Final discipline

```txt
Accessibility is not evidence.
It is permission to look for evidence.
```
