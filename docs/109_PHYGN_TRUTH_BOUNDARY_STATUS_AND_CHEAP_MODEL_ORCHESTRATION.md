# Phygn v1.8 — Truth Boundary Status & Cheap Model Orchestration

## 0. Purpose

This document defines how Phygn can operate with cheap, efficient or open-source models while preserving epistemic rigor.

The model is not the authority.

Phygn's logic layer is the permission system.

## 1. Architecture

```txt
User
→ Chat UI
→ Cheap/Open-source LLM
→ Structured Output Parser
→ Phygn Logic Layer
→ Truth Boundary Evaluator
→ Response Contract
→ UI Update
```

## 2. Model responsibilities

The model may summarize, paraphrase, suggest candidate variables, suggest candidate proxies, draft user-facing explanations and draft question wording.

The model may not authorize truth, claims, financial action, real-world action, automated execution, invent sources or convert confidence into evidence.

## 3. Phygn responsibilities

Phygn must decide:

```txt
epistemic mode
risk level
friction level
ladder level
truth boundary status
allowed uses
blocked uses
next required field
claim/action permission
audit log event
```

## 4. Truth Boundary Status values

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

## 5. Important distinction

Lack of evidence:

```txt
OUTSIDE_CLAIM_BOUNDARY
```

Contradiction with evidence or internal constraints:

```txt
CROSSED_FALSEHOOD_BOUNDARY
```

Unsupported exaggeration:

```txt
CROSSED_OVERCLAIM_BOUNDARY
```

## 6. Cheap model runtime modes

```txt
CHEAP_MODEL_MODE
OPEN_SOURCE_MODEL_MODE
FRONTIER_MODEL_MODE
RULE_ONLY_MODE
HUMAN_REVIEW_MODE
```

Routing principle:

```txt
cheap/open-source models can assist low-risk ideation
but cannot authorize high-risk claims/actions.
```

## 7. Fallback behavior

If structured output is invalid:

```txt
retry with stricter schema
fallback to rule-based question templates
mark output as MODEL_OUTPUT_UNTRUSTED
do not elevate claims
```

If model invents source support:

```txt
SOURCE_CLAIM_REJECTED
CLAIM_PERMISSION_BLOCKED
```

## 8. Response contract

Every copilot response must internally include:

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
    next_best_question: dict | None
    hypothesis_card: dict | None
    audit_log_event: dict
```

The UI may show a simplified version, but the contract must remain complete.

## 9. Final principle

```txt
A cheap model can be useful if the expensive part is the protocol.
```
