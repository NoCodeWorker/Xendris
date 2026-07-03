# Codex Prompt — Phygn v2.4 Closed Loop Learning & Meta-Improvement Engine

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
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
```

Therefore v2.4 starts at:

```txt
142
```

---

# 1. Read first

Read these v2.4 specs:

```txt
docs/142_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_docs/status/GOAL.md
docs/143_PHYGN_CANDIDATE_LEARNING_LOOP_STATE_MACHINE.md
docs/144_PHYGN_META_IMPROVEMENT_LOOP_AND_SHADOW_MODE.md
docs/145_PHYGN_LOOP_GUARDS_AGAINST_SELF_CONFIRMATION.md
```

Also read:

```txt
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect these packages:

```txt
phyng/heuristic_discovery/
phyng/synthetic_benchmark_design/
phyng/prediction_accuracy/
phyng/core/
phyng/copilot/
phyng/business_validation/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
510 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.4:

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

Do not introduce debt from the older loop.

Do not mutate critical gates.

---

# 4. New package

Create:

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

Create campaign:

```txt
phyng/campaigns/closed_loop_meta_improvement.py
```

---

# 5. Schemas

Implement:

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

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

from v2.1.

---

# 6. Candidate Learning Loop

Implement:

```python
run_candidate_learning_loop(input: CandidateLoopInput) -> CandidateLoopResult
```

It must:

```txt
accept result/input
classify domain and input type
attach canonical status
produce post-mortem reference or skip reason
generate update proposals
propose next actions
never authorize physical claims
```

For LOG_BOUNDARY benchmark design result:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
```

It may propose:

```txt
execute synthetic benchmark
source search pressure
benchmark data search
priority update proposal
```

It may not propose:

```txt
authorize physical claim
validate Frontera C
experimental confirmation
```

---

# 7. Meta-Improvement Loop

Implement:

```python
propose_meta_improvement(observation: MetaObservation) -> MetaChangeProposal
classify_meta_change_risk(proposal: MetaChangeProposal) -> MetaChangeProposal
```

Risk policy:

```txt
low risk: report wording, warning templates, bounded question priority
medium risk: mapping addition, low-risk model routing
high risk: gate changes, permission changes, source/benchmark requirement changes
```

High-risk proposals require human review.

---

# 8. Shadow Mode

Implement:

```python
run_shadow_mode(proposal: MetaChangeProposal, sample_cases: list[dict]) -> ShadowModeResult
```

Must record:

```txt
current_outputs
shadow_outputs
differences
permission_differences
blocked_reason_differences
regression_warnings
recommendation
```

Shadow mode must not mutate authoritative behavior.

---

# 9. Guards

Implement:

```python
run_loop_guards(...)
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

If any critical guard fails:

```txt
META_CHANGE_BLOCKED_REGRESSION
```

or:

```txt
LOOP_BLOCKED_REQUIRES_REVIEW
```

---

# 10. Versioned updates

Implement:

```python
create_versioned_update_record(...)
```

Record:

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

Do not apply high-risk updates automatically.

---

# 11. Reports

Generate:

```txt
reports/closed_loop/candidate_learning_loop_v2_4.md
reports/closed_loop/meta_improvement_loop_v2_4.md
reports/closed_loop/shadow_mode_v2_4.md
reports/closed_loop/self_confirmation_guards_v2_4.md
reports/closed_loop/versioned_update_records_v2_4.md
reports/campaigns/CLOSED-LOOP-META-IMPROVEMENT-v2_4.md
```

Reports must include canonical status sections and blocked claims/blocked actions.

---

# 12. Tests

Create:

```txt
tests/test_candidate_learning_loop_v2_4.py
tests/test_meta_improvement_loop_v2_4.py
tests/test_shadow_mode_v2_4.py
tests/test_loop_guards_v2_4.py
tests/test_versioned_update_records_v2_4.py
tests/test_closed_loop_meta_improvement_campaign_v2_4.py
```

Minimum tests:

```txt
test_candidate_loop_accepts_synthetic_benchmark_designed
test_candidate_loop_never_authorizes_physical_claim
test_candidate_loop_proposes_next_actions
test_meta_change_risk_classifies_gate_change_as_high_risk
test_high_risk_meta_change_requires_human_review
test_shadow_mode_does_not_mutate_authoritative_outputs
test_guard_blocks_permission_elevation_from_heuristic_only
test_guard_blocks_synthetic_to_physical_promotion
test_versioned_update_record_has_rollback_path
test_reports_include_canonical_section
test_reports_include_blocked_claims_or_actions
test_campaign_generates_reports
test_existing_v2_3_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v2.3 synthetic benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing v1.5 candidate benchmark outputs
existing business/candidate/copilot gates
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Phygn improves its truth automatically.
The loop validates hypotheses.
Self-improvement can relax evidence gates.
```

Allowed:

```txt
The loop improves candidate prioritization.
The meta-loop proposes process improvements.
Critical changes require shadow mode and review.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
candidate loop works
meta-loop works
shadow mode works
guards work
versioned records work
reports generated
no critical gate behavior changes
loop debt is resolved
```

Expected test count:

```txt
510 + new v2.4 tests
```

---

# 16. Final discipline

```txt
Phygn can improve itself.
It cannot give itself permission to be right.
```
