# Phygn v2.7 - LOG_BOUNDARY Non-Saturating Phi Search Results

Date: 2026-06-30

Source prompt:

```txt
docs/164_PHYGN_CODEX_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_PROMPT.md
```

Supporting specs:

```txt
docs/160_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_docs/status/GOAL.md
docs/161_PHYGN_NON_SATURATING_PHI_CANDIDATE_FAMILIES.md
docs/162_PHYGN_PHI_CONTROL_RESISTANCE_EVALUATION_PROTOCOL.md
docs/163_PHYGN_PHI_SEARCH_LOOP_FEEDBACK_AND_REPORT_CONTRACT.md
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.7 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.7 searched for non-saturating LOG_BOUNDARY phi formulations after v2.6 classified the original phi as:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

Final campaign status:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
```

Important boundary:

```txt
Surviving synthetic controls permits source/benchmark pressure only.
It does not authorize physical claims, Frontera C validation, or experimental confirmation.
```

Final validation:

```txt
pytest -q
566 passed in 38.25s
```

Baseline before v2.7 implementation:

```txt
pytest -q
553 passed in 25.69s
```

Net result:

```txt
553 baseline tests + 13 v2.7 tests = 566 passing tests
```

---

## 2. New Phi Search Layer

Extended:

```txt
phyng/synthetic_benchmark_design/
  phi_candidates.py
  phi_evaluation.py
  phi_search.py
  phi_report.py
```

Created campaign:

```txt
phyng/campaigns/log_boundary_non_saturating_phi_search.py
```

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `phi_candidates.py` | Declares candidate phi families, formulas, risks and control expectations |
| `phi_evaluation.py` | Executes control-resistance metrics and per-candidate classification |
| `phi_search.py` | Ranks candidates and generates closed-loop feedback |
| `phi_report.py` | Writes v2.7 canonical reports |
| `log_boundary_non_saturating_phi_search.py` | Campaign runner |

Campaign entrypoint:

```python
run_log_boundary_non_saturating_phi_search_campaign(root: str | Path = ".")
```

---

## 3. Schemas Added

Extended:

```txt
phyng/synthetic_benchmark_design/schemas.py
```

New schemas:

```txt
PhiCandidateSpec
PhiCandidateEvaluationResult
PhiControlResistanceMetrics
PhiCandidateRankingResult
PhiSearchLoopFeedbackResult
PhiSearchCampaignResult
```

---

## 4. Candidate Families

Generated report:

```txt
reports/synthetic_benchmark_execution/phi_candidate_families_v2_7.md
```

Implemented families:

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

Each family declares:

```txt
formula
parameters
boundedness claim
dimensionless inputs
known risks
control expectations
```

---

## 5. Control-Resistance Results

Generated report:

```txt
reports/synthetic_benchmark_execution/phi_control_resistance_v2_7.md
```

Classification summary:

| Family | Classification | Score | Saturation Ratio | Coordinate Contribution |
|---|---|---:|---:|---:|
| `PHI_COORDINATE_CONTRAST` | `PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION` | `0.6` | `0.0` | `-0.0077917511099330206` |
| `PHI_RELATIVE_BOUNDARY` | `PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION` | `0.48686140869264183` | `0.49126757952465927` | `-0.13391396622922724` |
| `PHI_GRADIENT` | `PHI_CANDIDATE_SURVIVES_CONTROLS` | `0.4744746218666944` | `0.13379011334485147` | `0.011007867472232202` |
| `PHI_CURVATURE` | `PHI_CANDIDATE_SURVIVES_CONTROLS` | `0.46677329875608475` | `0.17883891575224017` | `0.0039645199373199436` |
| `PHI_LOCALIZED_WINDOW` | `PHI_CANDIDATE_SURVIVES_CONTROLS` | `0.4565513505276825` | `0.6952069395028331` | `0.37740690991725223` |
| `PHI_CENTERED` | `PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION` | `0.4529413132176645` | `0.6191750426941809` | `0.0` |
| `PHI_NON_SATURATING_RATIO` | `PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION` | `0.42743232012523313` | `0.6323139375438936` | `-0.020403800487581725` |
| `PHI_BANDPASS` | `PHI_CANDIDATE_SURVIVES_CONTROLS` | `0.37742335229333634` | `0.9085874125476677` | `0.20124191847909967` |

Important ranking note:

```txt
The score is a synthetic heuristic.
The best candidate family reported by the campaign is the best surviving candidate, not the highest raw score if that candidate failed controls.
```

Best surviving candidate:

```txt
PHI_GRADIENT
```

---

## 6. Ranking Result

Generated report:

```txt
reports/synthetic_benchmark_execution/phi_candidate_ranking_v2_7.md
```

Ranking summary:

| Field | Result |
|---|---|
| status | `PHI_CANDIDATE_SURVIVES_CONTROLS` |
| survivor_count | `4` |
| best_candidate_family | `PHI_GRADIENT` |
| ranking_note | `Ranking is synthetic-only and is not evidence of physical truth.` |

Canonical status:

| Field | Value |
|---|---|
| Domain Status | `PHI_CANDIDATE_SURVIVES_CONTROLS` |
| Canonical Permission | `CLAIM_LIMITED_ALLOWED` |
| Evidence Level | `SYNTHETIC_ONLY` |
| Support Level | `SYNTHETIC` |
| Blocked Reasons | `MISSING_SOURCE_SUPPORT`, `MISSING_BENCHMARK`, `MISSING_EXPERIMENTAL_DATA` |
| Allowed Uses | synthetic control-resistance claim, source-search prioritization, benchmark-pressure prioritization |
| Blocked Uses | physical prediction, Frontera C validation, experimental confirmation |

---

## 7. Loop Feedback

Generated report:

```txt
reports/synthetic_benchmark_execution/phi_search_loop_feedback_v2_7.md
```

Loop feedback summary:

| Field | Result |
|---|---|
| loop_event_id | `LOG-BOUNDARY-PHI-SEARCH-v2_7-AUDIT-001` |
| result_status | `PHI_CANDIDATE_SURVIVES_CONTROLS` |

Allowed updates:

```txt
increase source-search priority for surviving phi formulation
increase benchmark-pressure priority
```

Blocked updates:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic changes
claim gate relaxation
```

Next actions:

```txt
schedule source-support audit
schedule benchmark-data search
keep physical claims blocked
```

---

## 8. Generated Reports

v2.7 generated:

```txt
reports/synthetic_benchmark_execution/phi_candidate_families_v2_7.md
reports/synthetic_benchmark_execution/phi_control_resistance_v2_7.md
reports/synthetic_benchmark_execution/phi_candidate_ranking_v2_7.md
reports/synthetic_benchmark_execution/phi_search_loop_feedback_v2_7.md
reports/campaigns/LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7.md
```

This document consolidates all v2.7 results into:

```txt
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

---

## 9. New Tests

Created:

```txt
tests/test_phi_candidate_families_v2_7.py
tests/test_phi_control_resistance_v2_7.py
tests/test_phi_candidate_ranking_v2_7.py
tests/test_phi_search_loop_feedback_v2_7.py
tests/test_phi_search_reports_v2_7.py
tests/test_log_boundary_non_saturating_phi_campaign_v2_7.py
```

Focused v2.7 verification:

```txt
pytest -q tests/test_phi_candidate_families_v2_7.py tests/test_phi_control_resistance_v2_7.py tests/test_phi_candidate_ranking_v2_7.py tests/test_phi_search_loop_feedback_v2_7.py tests/test_phi_search_reports_v2_7.py tests/test_log_boundary_non_saturating_phi_campaign_v2_7.py
13 passed in 13.95s
```

Full-suite verification:

```txt
pytest -q
566 passed in 38.25s
```

---

## 10. Behavior Preservation

v2.7 preserved v2.6 behavior:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
candidate_delta = 0.7152665915101674
control_gain = 0.0
```

Behavior preservation test:

```txt
test_existing_v2_6_behavior_preserved
```

Result:

```txt
passed
```

---

## 11. Operational Notes

`git status --short` could not be used in this environment.

Observed output:

```txt
fatal: not a git repository (or any of the parent directories): .git
```

The reliable direct runtime remains:

```txt
C:\Users\usuario\AppData\Local\Programs\Python\Python311\python.exe
```

The final validation source remains:

```txt
pytest -q
```

---

## 12. Final Assessment

v2.7 found synthetic phi alternatives that do better than the saturated v2.6 formulation under control-resistance checks.

Best surviving candidate:

```txt
PHI_GRADIENT
```

This means:

```txt
PHI_GRADIENT may receive source/benchmark pressure as a synthetic candidate.
```

This does not mean:

```txt
PHI_GRADIENT validates LOG_BOUNDARY physically.
PHI_GRADIENT proves Frontera C.
Synthetic control resistance proves a real-world effect.
```

Safest next move:

```txt
Run source-support and benchmark-data pressure for PHI_GRADIENT while preserving all physical-claim blocks.
```
