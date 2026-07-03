# Codex Prompt — Phygn v5.6 LOG_BOUNDARY Control Failure Review & Candidate Disposition

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
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
```

Therefore v5.6 starts at:

```txt
327
```

---

# 1. Read first

Read these v5.6 specs:

```txt
docs/327_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_docs/status/GOAL.md
docs/328_PHYGN_V5_6_CANDIDATE_DISPOSITION_PROTOCOL.md
docs/329_PHYGN_V5_6_FRONTERA_C_ROADMAP_UPDATE_PROTOCOL.md
docs/330_PHYGN_V5_6_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
docs/325_PHYGN_V5_4_LOG_BOUNDARY_PREDICTION_ALIGNMENT_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
docs/323_PHYGN_V5_2_1_LOG_BOUNDARY_OBSERVABLE_LOCATION_REVIEW_RESULTS.md
docs/322_PHYGN_V5_0_TO_V5_3_SOURCE_TO_YTRUE_ROADMAP_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v5.6 — LOG_BOUNDARY Control Failure Review & Candidate Disposition
```

Do not rescue LOG_BOUNDARY.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not create physical claims.

---

# 3. Required inputs

Load:

```txt
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
data/frontera_c/controls/log_boundary_negative_control_models_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_predictions_v5_5.json
data/frontera_c/controls/log_boundary_negative_control_error_metrics_v5_5.json
data/frontera_c/controls/log_boundary_leakage_tests_v5_5.json
data/frontera_c/controls/log_boundary_leave_one_out_results_v5_5.json
data/frontera_c/controls/log_boundary_control_decision_v5_5.json
data/frontera_c/controls/log_boundary_v5_5_next_gate_decision.json
data/frontera_c/benchmark/log_boundary_predictive_gain_smoke_test_v5_4.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
```

If missing:

```txt
LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS
```

---

# 4. Create package

Create:

```txt
phyng/frontera_c_disposition/
  __init__.py
  schemas.py
  loader.py
  control_failure_review.py
  candidate_disposition.py
  allowed_future_roles.py
  blocked_claims.py
  roadmap_update.py
  next_research_direction.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_log_boundary_control_failure_review.py
```

Entrypoint:

```python
run_frontera_c_log_boundary_control_failure_review_campaign(root: str | Path = ".")
```

---

# 5. Decision rules

Given v5.5 status:

```txt
LOG_BOUNDARY_GAIN_EXPLAINED_BY_SIMPLE_CONTROL
```

the campaign must set:

```txt
can_proceed_to_c_structure_ablation = false
can_support_frontera_c_validation = false
```

The primary disposition should be:

```txt
ARCHIVE_AS_VALIDATION_CANDIDATE
```

Secondary roles may include:

```txt
BENCHMARK_FIXTURE
NEGATIVE_CONTROL_FIXTURE
YTRUE_PIPELINE_REGRESSION_FIXTURE
SOURCE_IDENTITY_REGRESSION_FIXTURE
```

---

# 6. Reopen criteria

LOG_BOUNDARY may only be reopened as active candidate if future work provides:

```txt
at least 2 independent sources
at least 10 accepted y_true records
out-of-sample or leave-one-source-out evaluation
negative controls survive
simple controls no longer explain gain
```

---

# 7. Output files

Create:

```txt
data/frontera_c/disposition/log_boundary_control_failure_review_v5_6.json
data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json
data/frontera_c/disposition/log_boundary_allowed_future_roles_v5_6.json
data/frontera_c/disposition/log_boundary_blocked_claims_v5_6.json
data/frontera_c/disposition/frontera_c_roadmap_update_after_log_boundary_v5_6.json
data/frontera_c/disposition/v5_6_next_research_direction.json
```

---

# 8. Reports

Generate:

```txt
reports/frontera_c/disposition/log_boundary_control_failure_review_v5_6.md
reports/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.md
reports/frontera_c/disposition/log_boundary_allowed_future_roles_v5_6.md
reports/frontera_c/disposition/log_boundary_blocked_claims_v5_6.md
reports/frontera_c/disposition/frontera_c_roadmap_update_after_log_boundary_v5_6.md
reports/frontera_c/disposition/v5_6_next_research_direction.md
reports/campaigns/FRONTERA-C-LOG-BOUNDARY-CONTROL-FAILURE-REVIEW-v5_6.md
```

---

# 9. Statuses

Add mappings:

```txt
LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_COMPLETED
LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS
LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE
LOG_BOUNDARY_RETAINED_AS_BENCHMARK_FIXTURE
LOG_BOUNDARY_RETAINED_AS_NEGATIVE_CONTROL_FIXTURE
FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE
FRONTERA_C_REQUIRES_CANDIDATE_REPRIORITIZATION
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

---

# 10. Tests

Create:

```txt
tests/test_log_boundary_control_failure_loader_v5_6.py
tests/test_log_boundary_control_failure_review_v5_6.py
tests/test_log_boundary_candidate_disposition_v5_6.py
tests/test_log_boundary_allowed_future_roles_v5_6.py
tests/test_log_boundary_blocked_claims_v5_6.py
tests/test_frontera_c_roadmap_update_v5_6.py
tests/test_v5_6_next_research_direction.py
tests/test_frontera_c_log_boundary_control_failure_campaign_v5_6.py
```

Minimum tests:

```txt
test_missing_control_results_blocks_disposition
test_gain_explained_by_simple_control_blocks_c_ablation
test_log_boundary_archived_as_validation_candidate
test_log_boundary_retained_only_as_fixture
test_reopen_requires_independent_sources_and_more_ytrue
test_physical_claims_remain_blocked
test_frontera_c_remains_unvalidated
test_next_direction_generated
test_no_predictive_gain_recomputed
test_reports_include_canonical_status
```

---

# 11. Behavior preservation

Do not alter:

```txt
v5.5 negative controls
v5.4 prediction alignment
v5.3 accepted y_true
v5.2.1 observable location
v5.0-v5.2 source pipeline
v4.x historical artifacts
```

---

# 12. Do not overclaim

Do not write:

```txt
LOG_BOUNDARY validates anything.
LOG_BOUNDARY has robust PredictiveGain.
Control failure can be bypassed.
Frontera C is validated.
Invariant is empirically confirmed.
```

Allowed:

```txt
LOG_BOUNDARY failed the negative-control gate.
LOG_BOUNDARY was archived as a validation candidate if disposition says so.
LOG_BOUNDARY may be retained as a benchmark/control fixture.
The roadmap now requires dataset expansion, candidate reprioritization, or experiment design.
```

---

# 13. Acceptance criteria

Complete when:

```txt
v5.5 inputs loaded
v5.6 tests pass
control failure review generated
candidate disposition generated
allowed future roles generated
blocked claims generated
roadmap update generated
next research direction generated
reports generated
no PredictiveGain recomputed
no C-structure ablation executed
no physical claim created
no Frontera C validation created
```

---

# 14. Final discipline

```txt
A positive smoke test is a suspect, not a proof.
A control failure is a verdict.
```
