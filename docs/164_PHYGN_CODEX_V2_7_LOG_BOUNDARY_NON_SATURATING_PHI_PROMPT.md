# Codex Prompt — Phygn v2.7 LOG_BOUNDARY Non-Saturating Phi Search & Control-Resistant Candidate Design

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
```

Therefore v2.7 starts at:

```txt
160
```

---

# 1. Read first

Read these v2.7 specs:

```txt
docs/160_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_docs/status/GOAL.md
docs/161_PHYGN_NON_SATURATING_PHI_CANDIDATE_FAMILIES.md
docs/162_PHYGN_PHI_CONTROL_RESISTANCE_EVALUATION_PROTOCOL.md
docs/163_PHYGN_PHI_SEARCH_LOOP_FEEDBACK_AND_REPORT_CONTRACT.md
```

Also read:

```txt
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/synthetic_benchmark_design/
phyng/closed_loop/
phyng/core/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
553 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.7:

```txt
Non-Saturating Phi Candidate Search
Control-Resistant Phi Design
Candidate Phi Family Generator
Phi Evaluation Suite
Control Resistance Metrics
Phi Candidate Ranking
Loop Feedback
Canonical Reports
Campaign Runner
Tests
```

Do not authorize physical claims.

---

# 4. Extend package

Extend:

```txt
phyng/synthetic_benchmark_design/
```

Add:

```txt
phi_candidates.py
phi_evaluation.py
phi_search.py
phi_report.py
```

Create campaign:

```txt
phyng/campaigns/log_boundary_non_saturating_phi_search.py
```

---

# 5. Schemas

Implement or extend:

```txt
PhiCandidateSpec
PhiCandidateEvaluationResult
PhiControlResistanceMetrics
PhiCandidateRankingResult
PhiSearchLoopFeedbackResult
PhiSearchCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. Phi candidate families

Implement at minimum:

```txt
PHI_CENTERED
PHI_GRADIENT
PHI_BANDPASS
PHI_CURVATURE
PHI_RELATIVE_BOUNDARY
PHI_NON_SATURATING_RATIO
PHI_COORDINATE_CONTRAST
PHI_LOCALIZED_WINDOW
```

Each candidate must declare:

```txt
formula
parameters
boundedness claim
dimensionless inputs
known risks
control expectations
```

---

# 7. Evaluation

For each phi candidate:

```txt
execute synthetic delta computation
compare constant phi=1 control
compare mean phi control
run remove-u control
run remove-w control
run no-log-coordinates control
run threshold robustness where applicable
compute alpha=1 sensitivity
compute saturation ratio
classify candidate
```

---

# 8. Classifications

Possible classifications:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
PHI_CANDIDATE_FAILS_CONSTANT_CONTROL
PHI_CANDIDATE_SATURATES
PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION
PHI_CANDIDATE_REQUIRES_THRESHOLD_TUNING
PHI_CANDIDATE_NUMERICALLY_UNSTABLE
PHI_SEARCH_NO_SURVIVOR
```

Decision priority:

```txt
numerically unstable
saturates
fails constant control
fails coordinate contribution
requires threshold tuning
survives controls
no survivor
```

---

# 9. Canonical mapping

Add v2.7 statuses to compatibility map if needed.

Survival:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

Failure:

```txt
CanonicalPermission: CLAIM_BLOCKED or REVIEW_REQUIRED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: UNPHYSICAL_PARAMETER, HUMAN_REVIEW_REQUIRED, MISSING_EXPERIMENTAL_DATA
```

No physical claim may be authorized.

---

# 10. Ranking

Rank candidates by:

```txt
non_saturation_score
coordinate_contribution_score
threshold_robustness_score
alpha_1_survival_score
numerical_stability_score
control_resistance_score
```

Ranking is not evidence.

---

# 11. Loop feedback

Implement:

```python
generate_phi_search_loop_feedback(...)
```

Allowed:

```txt
increase source-search priority only for survivors
increase benchmark-pressure priority only for survivors
reject/down-rank saturating or constant-control formulations
select next heuristic family if no survivor
```

Forbidden:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic changes
```

---

# 12. Reports

Generate:

```txt
reports/synthetic_benchmark_execution/phi_candidate_families_v2_7.md
reports/synthetic_benchmark_execution/phi_control_resistance_v2_7.md
reports/synthetic_benchmark_execution/phi_candidate_ranking_v2_7.md
reports/synthetic_benchmark_execution/phi_search_loop_feedback_v2_7.md
reports/campaigns/LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7.md
```

Reports must include:

```txt
canonical status section
candidate formulas
control comparisons
ranking
allowed uses
blocked uses
loop feedback
discipline note
```

---

# 13. Tests

Create:

```txt
tests/test_phi_candidate_families_v2_7.py
tests/test_phi_control_resistance_v2_7.py
tests/test_phi_candidate_ranking_v2_7.py
tests/test_phi_search_loop_feedback_v2_7.py
tests/test_phi_search_reports_v2_7.py
tests/test_log_boundary_non_saturating_phi_campaign_v2_7.py
```

Minimum tests:

```txt
test_phi_candidate_families_exist
test_phi_candidates_are_bounded_or_flagged
test_phi_candidates_use_dimensionless_inputs
test_saturating_candidate_is_rejected
test_constant_control_match_blocks_candidate
test_coordinate_contribution_required
test_surviving_candidate_keeps_physical_claim_blocked
test_ranking_is_not_evidence
test_loop_feedback_blocks_physical_claim
test_no_survivor_downranks_log_boundary
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v2_6_behavior_preserved
```

---

# 14. Behavior preservation

Do not alter:

```txt
existing v2.6 ablation results
existing v2.5 synthetic execution outputs
existing v2.4 closed loop outputs
existing v2.3 benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing business/candidate/copilot gates
historical reports
```

---

# 15. Do not overclaim

Do not write:

```txt
A surviving phi validates LOG_BOUNDARY.
A non-saturating phi proves Frontera C.
Synthetic control resistance proves a physical effect.
```

Allowed:

```txt
A phi candidate survived or failed synthetic control resistance.
A surviving phi may receive source/benchmark pressure.
Physical claims remain blocked.
```

---

# 16. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
phi candidate families exist
control resistance evaluation works
ranking works
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
553 + new v2.7 tests
```

---

# 17. Final discipline

```txt
A surviving phi earns pressure.
A failing phi earns memory.
Neither earns truth.
```
