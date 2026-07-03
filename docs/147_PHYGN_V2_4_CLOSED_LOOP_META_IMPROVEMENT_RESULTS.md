# Phygn v2.4 - Closed Loop Learning & Meta-Improvement Engine Results

Date: 2026-06-30

Source prompt:

```txt
docs/146_PHYGN_CODEX_V2_4_CLOSED_LOOP_META_IMPROVEMENT_PROMPT.md
```

Supporting specs:

```txt
docs/142_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_docs/status/GOAL.md
docs/143_PHYGN_CANDIDATE_LEARNING_LOOP_STATE_MACHINE.md
docs/144_PHYGN_META_IMPROVEMENT_LOOP_AND_SHADOW_MODE.md
docs/145_PHYGN_LOOP_GUARDS_AGAINST_SELF_CONFIRMATION.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.4 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.4 implemented:

```txt
Candidate Learning Loop
Meta-Improvement Loop
Post-Mortem-to-Update Proposal Pipeline
Shadow Mode
Meta-Change Risk Classification
Regression/Behavior Preservation Guards
Self-Confirmation Guards
Versioned Update Records
Reports
Campaign Runner
Tests
```

No critical gates were mutated.

No existing v2.3 synthetic benchmark design outputs were changed.

No existing v2.2 heuristic discovery outputs were changed.

No existing v2.1 canonical mapping behavior was broken.

No existing business/candidate/copilot gates were changed.

Final validation:

```txt
pytest -q
523 passed in 21.65s
```

Baseline before v2.4:

```txt
pytest -q
510 passed in 19.61s
```

Net result:

```txt
510 baseline tests + 13 v2.4 tests = 523 passing tests
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/closed_loop/
  __init__.py
  schemas.py
  candidate_loop.py
  meta_loop.py
  shadow_mode.py
  guards.py
  update_proposals.py
  versioning.py
  report.py
```

Created campaign:

```txt
phyng/campaigns/closed_loop_meta_improvement.py
```

Campaign entrypoint:

```python
run_closed_loop_meta_improvement_campaign(root: str | Path = ".")
```

Campaign status:

```txt
META_CHANGE_APPROVED_LOW_RISK
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/closed_loop/schemas.py
```

Schemas:

```txt
CandidateLoopInput
CandidateLoopResult
CandidateUpdateProposal
MetaObservation
MetaChangeProposal
ShadowModeResult
MetaImprovementResult
LoopGuardResult
VersionedUpdateRecord
ClosedLoopCampaignResult
```

v2.1 integration:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

## 4. Canonical Mapping Added

Added to the canonical compatibility layer:

```txt
LOOP_UPDATE_PROPOSED
LOOP_BLOCKED_REQUIRES_REVIEW
META_CHANGE_PROPOSED
META_CHANGE_APPROVED_LOW_RISK
META_CHANGE_REQUIRES_HUMAN_REVIEW
META_CHANGE_BLOCKED_REGRESSION
```

Interpretation:

| Status | Permission | Meaning |
|---|---|---|
| `LOOP_UPDATE_PROPOSED` | `TEST_DESIGN_ALLOWED` | Loop can propose search/process updates, not truth updates |
| `LOOP_BLOCKED_REQUIRES_REVIEW` | `REVIEW_REQUIRED` | Loop cannot proceed automatically |
| `META_CHANGE_PROPOSED` | `REVIEW_REQUIRED` | Meta-change is recorded but not authoritative |
| `META_CHANGE_APPROVED_LOW_RISK` | `ACTION_LIMITED_ALLOWED` | Low-risk process update can be versioned |
| `META_CHANGE_REQUIRES_HUMAN_REVIEW` | `REVIEW_REQUIRED` | Human review required |
| `META_CHANGE_BLOCKED_REGRESSION` | `ACTION_BLOCKED` | Regression or permission drift blocks change |

---

## 5. Candidate Learning Loop

Implemented in:

```txt
phyng/closed_loop/candidate_loop.py
```

Function:

```python
run_candidate_learning_loop(input: CandidateLoopInput) -> CandidateLoopResult
```

Campaign input:

```txt
input_type: SYNTHETIC_BENCHMARK_RESULT
domain: physical_candidate
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
previous_status: HEURISTIC_TEST_DESIGN_READY
result_status: SYNTHETIC_BENCHMARK_DESIGNED
```

Candidate loop output:

```txt
new_status: LOOP_UPDATE_PROPOSED
ledger_event_id: LOOP-V2-4-LOG-BOUNDARY-LEDGER-001
post_mortem_skip_reason: No synthetic execution outcome exists yet; post-mortem deferred.
audit_event_id: LOOP-V2-4-LOG-BOUNDARY-AUDIT-001
```

Allowed proposals:

```txt
execute synthetic benchmark
source search pressure
benchmark data search
priority update proposal
```

Blocked claims:

```txt
authorize physical claim
validate Frontera C
experimental confirmation
```

---

## 6. Meta-Improvement Loop

Implemented in:

```txt
phyng/closed_loop/meta_loop.py
```

Functions:

```python
propose_meta_improvement(observation: MetaObservation) -> MetaChangeProposal
classify_meta_change_risk(proposal: MetaChangeProposal) -> MetaChangeProposal
```

Risk policy:

| Risk | Change types |
|---|---|
| Low | report wording/templates, warning templates, question priority, bounded heuristic weights |
| Medium | canonical mapping additions, low-risk model routing, benchmark design heuristic change |
| High | gate changes, permission changes, source/benchmark requirement changes, financial/execution gate changes |

High-risk result:

```txt
requires_shadow_mode: true
requires_human_review: true
```

Campaign proposal:

```txt
change_type: REPORT_TEMPLATE_CHANGE
risk_level: LOW
requires_shadow_mode: false
requires_human_review: false
```

---

## 7. Shadow Mode

Implemented in:

```txt
phyng/closed_loop/shadow_mode.py
```

Function:

```python
run_shadow_mode(proposal: MetaChangeProposal, sample_cases: list[dict]) -> ShadowModeResult
```

Records:

```txt
current_outputs
shadow_outputs
differences
permission_differences
blocked_reason_differences
regression_warnings
recommendation
```

Campaign shadow result:

```txt
recommendation: SHADOW_APPROVED_NO_MUTATION
permission_differences: 0
```

Guarantee:

```txt
Shadow mode does not mutate authoritative outputs.
```

---

## 8. Self-Confirmation Guards

Implemented in:

```txt
phyng/closed_loop/guards.py
```

Guards:

```txt
NO_SELF_AUTHORIZATION
NO_PERMISSION_ELEVATION_FROM_HEURISTIC_ONLY
NO_HIDDEN_PARAMETER_OPTIMIZATION
NO_POST_HOC_SCALE_SELECTION
NO_CLAIM_WITHOUT_SOURCE_OR_BENCHMARK
NO_SYNTHETIC_TO_PHYSICAL_PROMOTION
NO_CRITICAL_CHANGE_WITHOUT_SHADOW_MODE
NO_GATE_RELAXATION_WITHOUT_HUMAN_REVIEW
NO_REPORT_WITHOUT_BLOCKED_CLAIMS_SECTION
NO_LOOP_ITERATION_WITHOUT_AUDIT_EVENT
```

Campaign guard result:

```txt
All guards passed.
```

Critical guard tests verify blocks for:

```txt
permission elevation from HEURISTIC_ONLY
synthetic-to-physical promotion
```

---

## 9. Versioned Update Records

Implemented in:

```txt
phyng/closed_loop/versioning.py
```

Function:

```python
create_versioned_update_record(...)
```

Record fields:

```txt
version_id
proposal_id
previous_config
new_config
reason
tests_required
rollback_path
impact_summary
canonical_status
```

Campaign rollback path:

```txt
Revert to previous report template config.
```

---

## 10. Reports Generated

Generated:

```txt
reports/closed_loop/candidate_learning_loop_v2_4.md
reports/closed_loop/meta_improvement_loop_v2_4.md
reports/closed_loop/shadow_mode_v2_4.md
reports/closed_loop/self_confirmation_guards_v2_4.md
reports/closed_loop/versioned_update_records_v2_4.md
reports/campaigns/CLOSED-LOOP-META-IMPROVEMENT-v2_4.md
```

Report safety:

```txt
All reports include canonical status sections.
Reports include blocked claims or blocked actions.
```

Campaign blocked claims:

```txt
Phygn improves its truth automatically.
The loop validates hypotheses.
Self-improvement can relax evidence gates.
```

---

## 11. Tests

Created:

```txt
tests/test_candidate_learning_loop_v2_4.py
tests/test_meta_improvement_loop_v2_4.py
tests/test_shadow_mode_v2_4.py
tests/test_loop_guards_v2_4.py
tests/test_versioned_update_records_v2_4.py
tests/test_closed_loop_meta_improvement_campaign_v2_4.py
```

New v2.4 tests:

| Test | Purpose |
|---|---|
| `test_candidate_loop_accepts_synthetic_benchmark_designed` | Confirms loop accepts v2.3 synthetic design result |
| `test_candidate_loop_never_authorizes_physical_claim` | Confirms physical claim remains blocked |
| `test_candidate_loop_proposes_next_actions` | Confirms structured next actions |
| `test_meta_change_risk_classifies_gate_change_as_high_risk` | Confirms gate changes are high risk |
| `test_high_risk_meta_change_requires_human_review` | Confirms high-risk review requirement |
| `test_shadow_mode_does_not_mutate_authoritative_outputs` | Confirms shadow mode is non-mutating |
| `test_guard_blocks_permission_elevation_from_heuristic_only` | Confirms heuristic-only permission elevation is blocked |
| `test_guard_blocks_synthetic_to_physical_promotion` | Confirms synthetic-to-physical promotion is blocked |
| `test_versioned_update_record_has_rollback_path` | Confirms rollback path is mandatory |
| `test_reports_include_canonical_section` | Confirms canonical report sections |
| `test_reports_include_blocked_claims_or_actions` | Confirms blocked claims/actions reporting |
| `test_campaign_generates_reports` | Confirms campaign output files |
| `test_existing_v2_3_behavior_preserved` | Confirms v2.3 benchmark design behavior remains intact |

Focused v2.4 verification:

```txt
pytest -q tests/test_candidate_learning_loop_v2_4.py tests/test_meta_improvement_loop_v2_4.py tests/test_shadow_mode_v2_4.py tests/test_loop_guards_v2_4.py tests/test_versioned_update_records_v2_4.py tests/test_closed_loop_meta_improvement_campaign_v2_4.py
13 passed in 0.87s
```

Final full-suite verification:

```txt
pytest -q
523 passed in 21.65s
```

---

## 12. Behavior Preservation

v2.4 explicitly avoided changing:

```txt
existing v2.3 synthetic benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing v1.5 candidate benchmark outputs
existing business/candidate/copilot gates
historical reports
```

Meaning:

```txt
v2.4 adds a closed-loop process layer.
It does not relax evidence gates or mutate critical permission behavior.
```

---

## 13. Final Assessment

v2.4 gives Phygn a closed-loop learning structure while preserving epistemic authority boundaries.

The system can now:

```txt
turn candidate outcomes into update proposals
classify meta-change risk
run shadow-mode comparisons
block self-confirming promotions
create rollbackable versioned records
generate canonical loop reports
```

The system still cannot:

```txt
self-authorize physical truth
relax evidence requirements automatically
promote synthetic results to physical validation
change critical gates without review
```

Safe next step:

```txt
Use this loop to execute the LOG_BOUNDARY synthetic benchmark, classify the result,
and feed the outcome back into candidate priority/source-pressure proposals while
keeping all claim permissions gated by source, benchmark, and evidence requirements.
```

Final discipline note:

```txt
Phygn can improve itself.
It cannot give itself permission to be right.
```
