# Codex Prompt — Phygn v2.2 Heuristic Discovery Layer & Candidate Prioritization

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
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Therefore v2.2 starts at:

```txt
130
```

---

# 1. Read first

Read these v2.2 specs:

```txt
docs/130_PHYGN_V2_2_HEURISTIC_DISCOVERY_LAYER_docs/status/GOAL.md
docs/131_PHYGN_HEURISTIC_OUTPUT_PERMISSION_PROTOCOL.md
docs/132_PHYGN_CANDIDATE_GENERATION_AND_PRIORITIZATION.md
docs/133_PHYGN_HEURISTIC_TO_TESTABLE_HYPOTHESIS_PIPELINE.md
```

Also read the latest v2.1 result:

```txt
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Also inspect the v2.1 core package:

```txt
phyng/core/
  permissions.py
  blocked_reasons.py
  evidence_levels.py
  risk_levels.py
  support_levels.py
  status_mapping.py
  compatibility.py
  report_contract.py
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
484 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.2:

```txt
Heuristic Discovery Layer
Heuristic Candidate Schemas
Heuristic Permission Gate
Candidate Generation
Candidate Prioritization
Heuristic Scorecard
Heuristic-to-Testable Pipeline
Canonical v2.1 Mapping Integration
Reports
Campaign Runner
Tests
```

Hard rule:

```txt
Heuristics may guide search.
They may not grant truth.
```

---

# 4. New package

Create:

```txt
phyng/heuristic_discovery/
  __init__.py
  schemas.py
  permissions.py
  generator.py
  prioritizer.py
  pipeline.py
  scorecard.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/heuristic_discovery_layer.py
```

---

# 5. Schemas

Implement:

```txt
HeuristicCandidate
HeuristicScorecard
HeuristicRankingResult
HeuristicPermissionGateResult
HeuristicPipelineResult
HeuristicDiscoveryCampaignResult
```

Candidate fields:

```txt
candidate_id
domain
raw_idea
proposed_hypothesis
candidate_family
suggested_observables
suggested_proxies
required_sources
required_benchmarks
failure_conditions
assumptions
heuristic_scores
canonical_status
```

Use v2.1 `CanonicalStatusRecord`.

---

# 6. Heuristic statuses

Define domain statuses:

```txt
HEURISTIC_SEED
HEURISTIC_PRIORITIZED
HEURISTIC_TEST_DESIGN_READY
HEURISTIC_REVIEW_REQUIRED
HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY
HEURISTIC_REJECTED_AD_HOC
HEURISTIC_REJECTED_NO_OBSERVABLE
```

Map them using v2.1 canonical grammar.

Add these statuses to the compatibility layer if appropriate, or provide module-local mapping that returns `CanonicalStatusRecord`.

---

# 7. Permission gate

Implement:

```python
evaluate_heuristic_permission(candidate: HeuristicCandidate) -> HeuristicPermissionGateResult
```

Rules:

```txt
heuristic-only output cannot authorize truth
heuristic-only output cannot authorize claims
missing observable blocks test design
missing failure condition blocks test design
dimensional inconsistency blocks claim readiness
ad-hoc candidate requires review or rejection
```

Canonical defaults:

```txt
HEURISTIC_SEED:
  permission = EXPLORE_ALLOWED
  evidence = HEURISTIC_ONLY
  support = HEURISTIC

HEURISTIC_TEST_DESIGN_READY:
  permission = TEST_DESIGN_ALLOWED
  evidence = HEURISTIC_ONLY
  support = HEURISTIC

HEURISTIC_REVIEW_REQUIRED:
  permission = REVIEW_REQUIRED
  blocked_reason = HUMAN_REVIEW_REQUIRED
```

---

# 8. Candidate generator

Implement:

```python
generate_heuristic_candidates(raw_problem: str, domain: str) -> list[HeuristicCandidate]
```

For physical domain, generate candidate families:

```txt
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
OBSERVABLE_DEPENDENT_BOUNDARY
DIMENSIONLESS_INVARIANT
REGIME_TRANSITION
NOISE_COUPLING_MODULATION
```

For business domain, generate:

```txt
CUSTOMER_HYPOTHESIS
PROBLEM_HYPOTHESIS
WTP_HYPOTHESIS
CHANNEL_HYPOTHESIS
UNIT_ECONOMICS_HYPOTHESIS
```

For copilot/question domain, generate:

```txt
CLARIFY_TERM
DEFINE_OBSERVABLE
DEFINE_FAILURE_CONDITION
CHOOSE_BENCHMARK
REQUEST_SOURCE
```

---

# 9. Prioritizer

Implement:

```python
rank_heuristic_candidates(candidates: list[HeuristicCandidate]) -> HeuristicRankingResult
```

Use declared weights:

```txt
detectability_potential: 0.20
non_ad_hoc_score: 0.15
dimensional_consistency: 0.15
falsifiability: 0.15
benchmarkability: 0.10
source_searchability: 0.10
simplicity: 0.05
novelty: 0.05
cost_to_test_inverse: 0.05
risk_penalty: -0.10
```

Do not treat priority score as evidence.

---

# 10. Pipeline

Implement:

```python
run_heuristic_to_testable_pipeline(raw_problem: str, domain: str) -> HeuristicPipelineResult
```

It must:

```txt
generate candidates
rank candidates
evaluate permission gate
identify missing fields
propose next best question
return canonical status
```

---

# 11. Reports

Generate:

```txt
reports/heuristic_discovery/heuristic_discovery_layer_v2_2.md
reports/heuristic_discovery/candidate_generation_v2_2.md
reports/heuristic_discovery/candidate_prioritization_v2_2.md
reports/heuristic_discovery/heuristic_permission_gate_v2_2.md
reports/heuristic_discovery/heuristic_to_testable_pipeline_v2_2.md
reports/campaigns/HEURISTIC-DISCOVERY-LAYER-v2_2.md
```

Reports must include canonical section using v2.1 `CanonicalReportContract` or equivalent helper.

---

# 12. Tests

Create:

```txt
tests/test_heuristic_candidate_schema_v2_2.py
tests/test_heuristic_permission_gate_v2_2.py
tests/test_heuristic_candidate_generation_v2_2.py
tests/test_heuristic_prioritization_v2_2.py
tests/test_heuristic_pipeline_v2_2.py
tests/test_heuristic_discovery_campaign_v2_2.py
```

Minimum tests:

```txt
test_heuristic_candidate_has_canonical_status
test_heuristic_seed_maps_to_explore_allowed
test_heuristic_output_cannot_authorize_claim
test_missing_observable_blocks_test_design
test_missing_failure_condition_blocks_test_design
test_physical_generator_includes_log_boundary_candidate
test_b_suppressed_downranked_after_negative_control
test_priority_score_is_not_evidence
test_pipeline_returns_next_best_question
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_canonical_mapping_still_passes
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing canonical mapping behavior
existing business gate outputs
existing copilot truth-boundary outputs
existing candidate benchmark outputs
existing report files except new v2.2 reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Heuristic discovery validates candidates.
High heuristic priority means the candidate is true.
The system discovered a physical law.
Heuristic support is evidence.
```

Allowed:

```txt
Heuristic discovery prioritizes candidates for testing.
High heuristic priority means test this first.
The output remains HEURISTIC_ONLY until sources, benchmarks or data support it.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
heuristic schemas exist
heuristic permission gate works
candidate generation works
prioritizer works
pipeline works
canonical v2.1 grammar is used
reports generated
reports include canonical section
heuristic outputs cannot authorize truth
```

Expected test count:

```txt
484 + new v2.2 tests
```

---

# 16. Final discipline

```txt
The heuristic layer opens doors.
The gates decide which doors lead anywhere.
```
