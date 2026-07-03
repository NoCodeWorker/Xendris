# Phygn v2.2 - Heuristic Discovery Layer & Candidate Prioritization Results

Date: 2026-06-30

Source prompt:

```txt
docs/134_PHYGN_CODEX_V2_2_HEURISTIC_DISCOVERY_PROMPT.md
```

Supporting specs:

```txt
docs/130_PHYGN_V2_2_HEURISTIC_DISCOVERY_LAYER_docs/status/GOAL.md
docs/131_PHYGN_HEURISTIC_OUTPUT_PERMISSION_PROTOCOL.md
docs/132_PHYGN_CANDIDATE_GENERATION_AND_PRIORITIZATION.md
docs/133_PHYGN_HEURISTIC_TO_TESTABLE_HYPOTHESIS_PIPELINE.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.2 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.2 implemented a controlled heuristic discovery layer:

```txt
heuristic candidate schemas
heuristic permission gate
candidate generation
candidate prioritization
heuristic scorecard
heuristic-to-testable pipeline
v2.1 canonical grammar integration
reports
campaign runner
meta-tests
```

No destructive refactor was performed.

No existing canonical mapping behavior was broken.

No existing business gate outputs were changed.

No existing copilot truth-boundary outputs were changed.

No existing candidate benchmark outputs were changed.

Final validation:

```txt
pytest -q
497 passed in 19.40s
```

Baseline before v2.2:

```txt
pytest -q
484 passed in 18.31s
```

Net result:

```txt
484 baseline tests + 13 v2.2 tests = 497 passing tests
```

---

## 2. New Package and Campaign

Created:

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

Created campaign:

```txt
phyng/campaigns/heuristic_discovery_layer.py
```

Campaign entrypoint:

```python
run_heuristic_discovery_layer_campaign(root: str | Path = ".")
```

Campaign status:

```txt
HEURISTIC_TEST_DESIGN_READY
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/heuristic_discovery/schemas.py
```

Schemas:

```txt
HeuristicCandidate
HeuristicScorecard
HeuristicRankingResult
HeuristicPermissionGateResult
HeuristicPipelineResult
HeuristicDiscoveryCampaignResult
```

Every `HeuristicCandidate` carries:

```txt
canonical_status: CanonicalStatusRecord
```

This integrates v2.2 outputs with the v2.1 canonical grammar.

---

## 4. Heuristic Statuses and Canonical Mapping

Added to the v2.1 compatibility map:

```txt
HEURISTIC_SEED
HEURISTIC_PRIORITIZED
HEURISTIC_TEST_DESIGN_READY
HEURISTIC_REVIEW_REQUIRED
HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY
HEURISTIC_REJECTED_AD_HOC
HEURISTIC_REJECTED_NO_OBSERVABLE
```

Canonical interpretation:

| Status | Permission | Evidence | Support | Meaning |
|---|---|---|---|---|
| `HEURISTIC_SEED` | `EXPLORE_ALLOWED` | `HEURISTIC_ONLY` | `HEURISTIC` | Candidate may be explored, not claimed |
| `HEURISTIC_PRIORITIZED` | `EXPLORE_ALLOWED` | `HEURISTIC_ONLY` | `HEURISTIC` | Candidate was ranked for search priority |
| `HEURISTIC_TEST_DESIGN_READY` | `TEST_DESIGN_ALLOWED` | `HEURISTIC_ONLY` | `HEURISTIC` | Candidate can move to test design only |
| `HEURISTIC_REVIEW_REQUIRED` | `REVIEW_REQUIRED` | `HEURISTIC_ONLY` | `HEURISTIC` | Human review required |
| `HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY` | `CLAIM_BLOCKED` | `HEURISTIC_ONLY` | `HEURISTIC` | Dimensional issue blocks claim readiness |
| `HEURISTIC_REJECTED_AD_HOC` | `REVIEW_REQUIRED` | `HEURISTIC_ONLY` | `HEURISTIC` | Ad-hoc structure blocks automated promotion |
| `HEURISTIC_REJECTED_NO_OBSERVABLE` | `REVIEW_REQUIRED` | `HEURISTIC_ONLY` | `HEURISTIC` | Missing observable blocks test design |

Hard rule preserved:

```txt
Heuristic statuses never grant CLAIM_LIMITED_ALLOWED, ACTION_LIMITED_ALLOWED, EXECUTION_ALLOWED, SCALE_ALLOWED, BENCHMARK_SUPPORTED, or EXPERIMENTAL_DATA_SUPPORTED.
```

---

## 5. Permission Gate

Implemented in:

```txt
phyng/heuristic_discovery/permissions.py
```

Function:

```python
evaluate_heuristic_permission(candidate: HeuristicCandidate) -> HeuristicPermissionGateResult
```

Rules enforced:

```txt
heuristic-only output cannot authorize truth
heuristic-only output cannot authorize claims
missing observable blocks test design
missing failure condition blocks test design
dimensional inconsistency blocks claim readiness
ad-hoc candidate requires review or rejection
```

Important invariant:

```txt
is_claim_authorized is always False for heuristic-only candidates.
```

---

## 6. Candidate Generation

Implemented in:

```txt
phyng/heuristic_discovery/generator.py
```

Function:

```python
generate_heuristic_candidates(raw_problem: str, domain: str) -> list[HeuristicCandidate]
```

Supported physical candidate families:

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

Supported business candidate families:

```txt
CUSTOMER_HYPOTHESIS
PROBLEM_HYPOTHESIS
WTP_HYPOTHESIS
CHANNEL_HYPOTHESIS
UNIT_ECONOMICS_HYPOTHESIS
```

Supported copilot/question candidate families:

```txt
CLARIFY_TERM
DEFINE_OBSERVABLE
DEFINE_FAILURE_CONDITION
CHOOSE_BENCHMARK
REQUEST_SOURCE
```

Default campaign generation:

```txt
domain: physical_candidate
candidates_generated: 8
```

---

## 7. Candidate Prioritization

Implemented in:

```txt
phyng/heuristic_discovery/prioritizer.py
```

Function:

```python
rank_heuristic_candidates(candidates: list[HeuristicCandidate]) -> HeuristicRankingResult
```

Declared weights:

| Score | Weight |
|---|---:|
| `detectability_potential` | 0.20 |
| `non_ad_hoc_score` | 0.15 |
| `dimensional_consistency` | 0.15 |
| `falsifiability` | 0.15 |
| `benchmarkability` | 0.10 |
| `source_searchability` | 0.10 |
| `simplicity` | 0.05 |
| `novelty` | 0.05 |
| `cost_to_test_inverse` | 0.05 |
| `risk_penalty` | -0.10 |

Campaign ranking result:

| Rank | Candidate ID | Family | Priority Score |
|---:|---|---|---:|
| 1 | `HEUR-PHY-003` | `LOG_BOUNDARY` | 0.7000 |
| 2 | `HEUR-PHY-002` | `QB_STRUCTURAL` | 0.6550 |
| 3 | `HEUR-PHY-004` | `THRESHOLD_SATURATION` | 0.6550 |
| 4 | `HEUR-PHY-005` | `OBSERVABLE_DEPENDENT_BOUNDARY` | 0.6550 |
| 5 | `HEUR-PHY-006` | `DIMENSIONLESS_INVARIANT` | 0.6550 |
| 6 | `HEUR-PHY-007` | `REGIME_TRANSITION` | 0.6550 |
| 7 | `HEUR-PHY-008` | `NOISE_COUPLING_MODULATION` | 0.6550 |
| 8 | `HEUR-PHY-001` | `B_SUPPRESSED` | 0.5500 |

Negative-control learning:

```txt
B_SUPPRESSED remains useful as a control, but is down-ranked for positive prediction after v1.5 negative-control evidence.
```

Safety invariant:

```txt
Priority score is not evidence.
```

---

## 8. Pipeline

Implemented in:

```txt
phyng/heuristic_discovery/pipeline.py
```

Function:

```python
run_heuristic_to_testable_pipeline(raw_problem: str, domain: str) -> HeuristicPipelineResult
```

Pipeline actions:

```txt
generate candidates
rank candidates
evaluate permission gate
identify missing fields
propose next best question
return canonical status
```

Campaign top candidate:

```txt
HEUR-PHY-003 / LOG_BOUNDARY
```

Pipeline canonical status:

```txt
HEURISTIC_TEST_DESIGN_READY
```

Canonical permission:

```txt
TEST_DESIGN_ALLOWED
```

Evidence/support:

```txt
HEURISTIC_ONLY / HEURISTIC
```

---

## 9. Reports Generated

Generated:

```txt
reports/heuristic_discovery/heuristic_discovery_layer_v2_2.md
reports/heuristic_discovery/candidate_generation_v2_2.md
reports/heuristic_discovery/candidate_prioritization_v2_2.md
reports/heuristic_discovery/heuristic_permission_gate_v2_2.md
reports/heuristic_discovery/heuristic_to_testable_pipeline_v2_2.md
reports/campaigns/HEURISTIC-DISCOVERY-LAYER-v2_2.md
```

Report safety:

```txt
All v2.2 reports include a canonical status section using the v2.1 CanonicalReportContract helpers.
```

The campaign report explicitly blocks:

```txt
Heuristic priority does not validate candidates.
Heuristic support is not source, benchmark, or experimental evidence.
```

---

## 10. Tests

Created:

```txt
tests/test_heuristic_candidate_schema_v2_2.py
tests/test_heuristic_permission_gate_v2_2.py
tests/test_heuristic_candidate_generation_v2_2.py
tests/test_heuristic_prioritization_v2_2.py
tests/test_heuristic_pipeline_v2_2.py
tests/test_heuristic_discovery_campaign_v2_2.py
```

New v2.2 tests:

| Test | Purpose |
|---|---|
| `test_heuristic_candidate_has_canonical_status` | Confirms candidates carry `CanonicalStatusRecord` |
| `test_heuristic_seed_maps_to_explore_allowed` | Confirms heuristic seed maps to `EXPLORE_ALLOWED` |
| `test_heuristic_output_cannot_authorize_claim` | Confirms heuristic gate cannot authorize claims |
| `test_missing_observable_blocks_test_design` | Confirms missing observable blocks promotion |
| `test_missing_failure_condition_blocks_test_design` | Confirms missing failure condition blocks promotion |
| `test_physical_generator_includes_log_boundary_candidate` | Confirms physical generator includes `LOG_BOUNDARY` |
| `test_business_generator_includes_wtp_candidate` | Confirms business generator includes WTP hypothesis |
| `test_b_suppressed_downranked_after_negative_control` | Confirms negative-control downranking |
| `test_priority_score_is_not_evidence` | Confirms priority score remains heuristic-only |
| `test_pipeline_returns_next_best_question` | Confirms pipeline next-best-question behavior |
| `test_existing_canonical_mapping_still_passes` | Confirms v2.1 canonical mappings still work |
| `test_reports_include_canonical_section` | Confirms report canonical section rendering |
| `test_campaign_generates_reports` | Confirms campaign report generation |

Focused v2.2 verification:

```txt
pytest -q tests/test_heuristic_candidate_schema_v2_2.py tests/test_heuristic_permission_gate_v2_2.py tests/test_heuristic_candidate_generation_v2_2.py tests/test_heuristic_prioritization_v2_2.py tests/test_heuristic_pipeline_v2_2.py tests/test_heuristic_discovery_campaign_v2_2.py
13 passed in 0.72s
```

Final full-suite verification:

```txt
pytest -q
497 passed in 19.40s
```

---

## 11. Behavior Preservation

v2.2 explicitly avoided changing:

```txt
existing canonical mapping behavior
existing business gate outputs
existing copilot truth-boundary outputs
existing candidate benchmark outputs
existing historical reports
```

Behavior preservation check:

```txt
test_existing_canonical_mapping_still_passes
```

Result:

```txt
passed
```

Meaning:

```txt
v2.2 extends the status grammar for heuristic outputs without breaking representative v2.1 canonical mappings.
```

---

## 12. Final Assessment

v2.2 adds discovery acceleration without weakening claim discipline.

The system can now:

```txt
generate candidate hypotheses
rank them for testing
identify missing testability fields
propose the next best question
attach canonical status interpretation
block heuristic outputs from authorizing truth
```

The safe next step is:

```txt
Use the heuristic pipeline to feed explicit synthetic benchmark design tasks,
while keeping every generated candidate HEURISTIC_ONLY until sources, benchmarks,
or data independently support it.
```

Final discipline note:

```txt
The heuristic layer opens doors.
The gates decide which doors lead anywhere.
```
