# Codex Prompt — Phygn v1.6 Epistemic Modes & Friction Gradient

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v1.5 intended: candidate vs baseline synthetic benchmark.
Core concern: Phygn may become too blocking if every idea is treated as a high-risk claim.
Need: epistemic modes, friction gradient, and hypothesis incubation.
```

Important numbering:

```txt
v1.6 docs:
91_PHYGN_V1_6_EPISTEMIC_MODES_AND_FRICTION_GRADIENT_docs/status/GOAL.md
92_PHYGN_DREAM_TO_CLAIM_LADDER.md
93_PHYGN_RISK_WEIGHTED_GATEKEEPING_PROTOCOL.md
94_PHYGN_HYPOTHESIS_INCUBATION_MODE.md
95_PHYGN_CODEX_V1_6_EPISTEMIC_MODES_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/91_PHYGN_V1_6_EPISTEMIC_MODES_AND_FRICTION_GRADIENT_docs/status/GOAL.md
docs/92_PHYGN_DREAM_TO_CLAIM_LADDER.md
docs/93_PHYGN_RISK_WEIGHTED_GATEKEEPING_PROTOCOL.md
docs/94_PHYGN_HYPOTHESIS_INCUBATION_MODE.md
```

Also read recent v1.3-v1.5 reports if available.

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement v1.6 support for:

```txt
epistemic modes
dream-to-claim ladder
risk-weighted friction gradient
hypothesis incubation
mode-aware claim/action gating
reports
tests
```

The purpose is not to weaken Phygn.

The purpose is to prevent Phygn from using publication/execution-level friction on early-stage intuition.

---

# 4. New modules

Create:

```txt
phyng/epistemic_modes/
  __init__.py
  schemas.py
  modes.py
  ladder.py
  friction.py
  incubation.py
  gatekeeper.py
  report.py

phyng/campaigns/epistemic_modes_friction_gradient.py
```

---

# 5. Schemas

Implement:

```python
EpistemicMode
RiskLevel
FrictionLevel
LadderLevel
ModeGateResult
HypothesisSeed
IncubationResult
```

Recommended enums:

```txt
DREAM_MODE
EXPLORATION_MODE
HYPOTHESIS_MODE
TEST_DESIGN_MODE
CLAIM_MODE
PUBLICATION_MODE
FINANCIAL_ACTION_MODE
AUTOMATED_EXECUTION_MODE
```

Risk:

```txt
RISK_0_PRIVATE_THOUGHT
RISK_1_INTERNAL_NOTE
RISK_2_INTERNAL_RESEARCH
RISK_3_PUBLIC_CONTENT
RISK_4_CLIENT_DELIVERABLE
RISK_5_FINANCIAL_RECOMMENDATION
RISK_6_REAL_WORLD_ACTION
RISK_7_AUTOMATED_EXECUTION
```

Friction:

```txt
FRICTION_0_FREE
FRICTION_1_LABEL
FRICTION_2_STRUCTURE
FRICTION_3_REQUIRE_OBSERVABLE
FRICTION_4_REQUIRE_SOURCE
FRICTION_5_REQUIRE_BENCHMARK
FRICTION_6_REQUIRE_RISK_ENGINE
FRICTION_7_REQUIRE_HUMAN_APPROVAL
FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED
```

---

# 6. Dream-to-claim ladder

Implement:

```python
classify_ladder_level(input_text, requested_use, available_evidence) -> LadderClassification
```

Levels:

```txt
DREAM
HYPOTHESIS_SEED
FORMALIZING_HYPOTHESIS
TESTABLE_HYPOTHESIS
SYNTHETIC_SUPPORT
SOURCE_BACKED_LIMITED
BENCHMARK_SUPPORTED
OPERATIONALLY_ACTIONABLE
AUTOMATED_EXECUTION_ALLOWED
```

---

# 7. Friction gradient

Implement:

```python
evaluate_friction(risk_level: RiskLevel, mode: EpistemicMode) -> FrictionDecision
```

Rule:

```txt
low risk -> allow/label/structure
high risk -> require evidence/risk/human approval/block
```

---

# 8. Mode-aware gatekeeper

Implement:

```python
evaluate_mode_gate(...)
```

It must distinguish:

```txt
idea permission
hypothesis permission
claim permission
action permission
execution permission
```

Example:

```txt
Idea: allowed
Claim: blocked
Action: blocked
```

---

# 9. Hypothesis incubation

Implement:

```python
incubate_hypothesis(seed: HypothesisSeed) -> IncubationResult
```

It should return:

```txt
allowed_use
blocked_use
next_formalization_steps
required_evidence_for_next_level
```

---

# 10. Financial action specific gate

Implement:

```python
evaluate_financial_action_gate(...)
```

Required fields:

```txt
asset
time_horizon
source_freshness
entry_condition
exit_condition
invalidation
risk_per_trade
position_sizing
benchmark
post_mortem_plan
```

If missing:

```txt
ACTION_BLOCKED
```

But the initial intuition may remain:

```txt
INTUITION_LOGGED
```

---

# 11. Reports

Generate:

```txt
reports/epistemic_modes/dream_to_claim_ladder_v1_6.md
reports/epistemic_modes/friction_gradient_v1_6.md
reports/epistemic_modes/hypothesis_incubation_v1_6.md
reports/epistemic_modes/risk_weighted_gatekeeping_v1_6.md
reports/campaigns/EPISTEMIC-MODES-FRICTION-GRADIENT-v1_6.md
```

---

# 12. Tests

Add:

```txt
tests/test_epistemic_modes_v1_6.py
tests/test_dream_to_claim_ladder_v1_6.py
tests/test_friction_gradient_v1_6.py
tests/test_hypothesis_incubation_v1_6.py
tests/test_risk_weighted_gatekeeper_v1_6.py
tests/test_epistemic_modes_campaign_v1_6.py
```

Minimum tests:

```txt
test_dream_mode_allows_intuition
test_dream_mode_blocks_public_claim
test_hypothesis_seed_allowed_not_claim
test_claim_mode_requires_source
test_financial_action_requires_risk_fields
test_automated_execution_blocks_without_full_authorization
test_low_risk_low_friction
test_high_risk_high_friction
test_incubation_returns_next_steps
test_reports_generated
```

---

# 13. Do not overclaim

Do not write:

```txt
Phygn eliminates hallucinations completely.
Phygn guarantees correct financial action.
Phygn validates intuition.
```

Allowed:

```txt
Phygn preserves intuition as seed while blocking unsupported claims/actions.
Friction scales with risk.
High-risk execution remains tightly gated.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
modes exist
ladder classification works
friction gradient works
hypothesis incubation works
financial action gate works
reports generated
early ideas allowed
high-risk claims/actions blocked
```

---

# 15. Final discipline

```txt
Phygn should be a ladder, not a guillotine.
```
