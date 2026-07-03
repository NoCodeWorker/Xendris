# Codex Prompt — Phygn v1.8 Copilot Truth-Boundary UI & Socratic Question Engine

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current confirmed latest document:

```txt
docs/105_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_ACCURACY_RUNTIME_RESULTS.md
```

Therefore v1.8 starts at:

```txt
106
```

# 1. Read first

Read these v1.8 specs:

```txt
docs/106_PHYGN_V1_8_COPILOT_TRUTH_BOUNDARY_UI_docs/status/GOAL.md
docs/107_PHYGN_COPILOT_CHAT_UI_AND_HYPOTHESIS_WORKSPACE.md
docs/108_PHYGN_SOCRATIC_QUESTION_ENGINE_AND_NEXT_BEST_QUESTION_PROTOCOL.md
docs/109_PHYGN_TRUTH_BOUNDARY_STATUS_AND_CHEAP_MODEL_ORCHESTRATION.md
```

Also read the latest v1.7 result:

```txt
docs/105_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_ACCURACY_RUNTIME_RESULTS.md
```

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
408 passed, 0 failed
```

If tests fail, fix baseline first.

# 3. Mission

Implement v1.8:

```txt
Copilot Truth-Boundary UI contracts
Socratic Question Engine
Next Best Question protocol
Truth Boundary Status evaluator
Hypothesis Workspace state
Cheap/Open-source model orchestration hooks
Copilot Response Contract
Reports
Campaign Runner
Tests
```

This is backend/API/state-contract work. Do not build a full frontend unless the repository already has frontend architecture prepared.

# 4. New package

Create:

```txt
phyng/copilot/
  __init__.py
  schemas.py
  question_engine.py
  truth_boundary.py
  workspace.py
  response_contract.py
  orchestration.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/copilot_truth_boundary_ui.py
```

Optional frontend contract files if appropriate:

```txt
frontend/contracts/copilot_response_contract.schema.json
frontend/contracts/hypothesis_workspace.schema.json
frontend/contracts/next_best_question.schema.json
```

# 5. Schemas

Implement Pydantic models:

```txt
CopilotInput
NextBestQuestion
TruthBoundaryEvaluation
CopilotResponseContract
HypothesisWorkspaceState
HypothesisCardState
AllowedBlockedUses
ModelOrchestrationResult
```

Required contract:

```python
class CopilotResponseContract(BaseModel):
    user_facing_message: str
    epistemic_mode: str
    ladder_level: str
    risk_level: str
    friction_level: str
    truth_boundary_status: str
    allowed_uses: list[str]
    blocked_uses: list[str]
    next_best_question: NextBestQuestion | None
    hypothesis_card: dict | None
    audit_log_event: dict
```

# 6. Question Engine

Implement:

```python
generate_next_best_question(
    input_text: str,
    hypothesis_card: HypothesisCardState | None,
    mode: str,
    risk_level: str,
) -> NextBestQuestion
```

It must detect missing fields, rank missing fields by leverage, ask one question only, offer answer options when useful, explain why the question matters and declare which fields it updates.

Question types:

```txt
CLARIFY_TERM
DEFINE_VARIABLE
DEFINE_OBSERVABLE
SELECT_PROXY
DEFINE_TIME_HORIZON
CHOOSE_BASELINE
CHOOSE_BENCHMARK
DEFINE_FAILURE_CONDITION
REQUEST_SOURCE
CHOOSE_METRIC
ASSESS_RISK
CONFIRM_SCOPE
```

# 7. Truth Boundary

Implement:

```python
evaluate_truth_boundary(
    ladder_level: str,
    mode: str,
    risk_level: str,
    has_sources: bool = False,
    has_benchmark: bool = False,
    has_contradiction: bool = False,
    has_overclaim: bool = False,
    requests_action: bool = False,
    requests_execution: bool = False,
) -> TruthBoundaryEvaluation
```

Statuses:

```txt
INSIDE_DREAM_BOUNDARY
INSIDE_EXPLORATION_BOUNDARY
INSIDE_HYPOTHESIS_BOUNDARY
INSIDE_TESTABILITY_BOUNDARY
INSIDE_SYNTHETIC_SUPPORT_BOUNDARY
INSIDE_SOURCE_BACKED_LIMITED_BOUNDARY
INSIDE_BENCHMARK_SUPPORTED_BOUNDARY
OUTSIDE_CLAIM_BOUNDARY
OUTSIDE_ACTION_BOUNDARY
OUTSIDE_EXECUTION_BOUNDARY
CROSSED_OVERCLAIM_BOUNDARY
CROSSED_FALSEHOOD_BOUNDARY
```

Rules:

```txt
lack of evidence != falsehood
unsupported public claim -> OUTSIDE_CLAIM_BOUNDARY
claim stronger than evidence -> CROSSED_OVERCLAIM_BOUNDARY
contradiction -> CROSSED_FALSEHOOD_BOUNDARY
action without operational authorization -> OUTSIDE_ACTION_BOUNDARY
execution without full authorization -> OUTSIDE_EXECUTION_BOUNDARY
```

# 8. Workspace

Implement:

```python
create_or_update_workspace(...)
```

It must maintain:

```txt
workspace_id
idea_history
current_hypothesis_card
answered_questions
missing_fields
current_ladder_level
truth_boundary_status
allowed_uses
blocked_uses
next_best_question
audit_trail
```

# 9. Cheap model orchestration

Implement hooks:

```python
compose_copilot_prompt_for_model(...)
validate_model_structured_output(...)
fallback_to_rule_based_question(...)
orchestrate_model_assisted_response(...)
```

Rules:

```txt
model can suggest language
Phygn decides permission
invalid model output cannot elevate claims
source hallucination is rejected
local/open-source models allowed for low-risk ideation
high-risk actions require stronger gates/human review
```

# 10. API endpoints if FastAPI exists

If the project has FastAPI architecture, add:

```txt
POST /copilot/message
GET /copilot/workspace/{workspace_id}
POST /copilot/workspace/{workspace_id}/answer
```

Do not force API if no app structure exists.

# 11. Reports

Generate:

```txt
reports/copilot/copilot_truth_boundary_ui_v1_8.md
reports/copilot/socratic_question_engine_v1_8.md
reports/copilot/hypothesis_workspace_v1_8.md
reports/copilot/cheap_model_orchestration_v1_8.md
reports/campaigns/COPILOT-TRUTH-BOUNDARY-UI-v1_8.md
```

# 12. Tests

Create:

```txt
tests/test_copilot_question_engine_v1_8.py
tests/test_truth_boundary_v1_8.py
tests/test_copilot_response_contract_v1_8.py
tests/test_hypothesis_workspace_v1_8.py
tests/test_cheap_model_orchestration_v1_8.py
tests/test_copilot_truth_boundary_campaign_v1_8.py
```

Minimum tests:

```txt
test_next_best_question_for_raw_business_idea
test_next_best_question_for_scientific_hypothesis
test_question_engine_asks_only_one_question
test_question_engine_offers_options
test_lack_of_evidence_is_outside_claim_not_falsehood
test_overclaim_crosses_overclaim_boundary
test_contradiction_crosses_falsehood_boundary
test_action_without_authorization_blocked
test_execution_without_authorization_blocked
test_response_contract_contains_required_fields
test_workspace_updates_after_answer
test_model_output_never_authorizes_claim
test_rule_based_fallback_generates_question
test_reports_generated
```

# 13. Do not overclaim

Do not write:

```txt
Phygn is the truth.
Phygn guarantees truth.
Cheap models solve epistemology.
Open-source models are safe by default.
```

Allowed:

```txt
Phygn estimates truth-boundary status.
Phygn helps users stay on a path toward testability.
Cheap models can assist conversation when Phygn gates claims/actions.
```

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
question engine works
truth boundary works
workspace updates
response contract works
cheap model hooks exist
reports generated
campaign runner works
claims/actions remain gated
ideas remain allowed
```

Expected test count:

```txt
408 + new v1.8 tests
```

# 15. Final discipline

```txt
The model speaks.
Phygn decides what the speech is allowed to become.
```
