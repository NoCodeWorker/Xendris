# Phygn v1.6 — Epistemic Modes & Friction Gradient Results

Date: 2026-06-30

Source prompt:

```txt
docs/98_PHYGN_CODEX_V1_6_EPISTEMIC_MODES_PROMPT.md
```

Supporting specs:

```txt
docs/94_PHYGN_V1_6_EPISTEMIC_MODES_AND_FRICTION_GRADIENT_docs/status/GOAL.md
docs/95_PHYGN_DREAM_TO_CLAIM_LADDER.md
docs/96_PHYGN_RISK_WEIGHTED_GATEKEEPING_PROTOCOL.md
docs/97_PHYGN_HYPOTHESIS_INCUBATION_MODE.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.6 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All acceptance criteria from §14 of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **390 passed, 0 failed** (339 baseline + 51 new) |
| Modes exist | ✅ 8 epistemic modes defined |
| Ladder classification works | ✅ 9 rungs, advances with evidence |
| Friction gradient works | ✅ 8 risk levels × mode floor |
| Hypothesis incubation works | ✅ Seed incubated with next steps |
| Financial action gate works | ✅ 10 required fields, blocks incomplete actions |
| Reports generated | ✅ 5 reports written |
| Early ideas allowed | ✅ `IDEA_ALLOWED` in DREAM_MODE |
| High-risk claims/actions blocked | ✅ `CLAIM_BLOCKED`, `ACTION_BLOCKED` enforced |

---

## 2. New Package: `phyng/epistemic_modes/`

### Modules

| Module | Responsibility |
|---|---|
| [schemas.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/schemas.py) | All Pydantic models: `ModeGateResult`, `HypothesisSeed`, `IncubationResult`, `LadderClassification`, `FrictionDecision`, `FinancialActionGateResult` |
| [modes.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/modes.py) | Mode→risk mappings, `is_high_risk_mode()`, `is_low_risk_mode()` |
| [ladder.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/ladder.py) | `classify_ladder_level()` — 9-rung dream-to-claim ladder |
| [friction.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/friction.py) | `evaluate_friction()` — scales friction with risk + mode floor |
| [incubation.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/incubation.py) | `incubate_hypothesis()` — preserves seeds without premature claims |
| [gatekeeper.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/gatekeeper.py) | `evaluate_mode_gate()`, `evaluate_financial_action_gate()` |
| [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/epistemic_modes/report.py) | Report writer for all 5 v1.6 reports |

### Campaign

- [epistemic_modes_friction_gradient.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/epistemic_modes_friction_gradient.py)
  — Full orchestrator: runs all components, generates all reports.

---

## 3. Epistemic Modes

```txt
DREAM_MODE               → RISK_0_PRIVATE_THOUGHT
EXPLORATION_MODE         → RISK_1_INTERNAL_NOTE
HYPOTHESIS_MODE          → RISK_2_INTERNAL_RESEARCH
TEST_DESIGN_MODE         → RISK_2_INTERNAL_RESEARCH
CLAIM_MODE               → RISK_3_PUBLIC_CONTENT
PUBLICATION_MODE         → RISK_4_CLIENT_DELIVERABLE
FINANCIAL_ACTION_MODE    → RISK_5_FINANCIAL_RECOMMENDATION
AUTOMATED_EXECUTION_MODE → RISK_7_AUTOMATED_EXECUTION
```

---

## 4. Dream-to-Claim Ladder (9 rungs)

| # | Level | Claim | Action |
|---|---|---|---|
| 0 | DREAM | ❌ | ❌ |
| 1 | HYPOTHESIS_SEED | ❌ | ❌ |
| 2 | FORMALIZING_HYPOTHESIS | ❌ | ❌ |
| 3 | TESTABLE_HYPOTHESIS | ❌ | ❌ |
| 4 | SYNTHETIC_SUPPORT | ❌ | ❌ |
| 5 | SOURCE_BACKED_LIMITED | ✅ limited | ❌ |
| 6 | BENCHMARK_SUPPORTED | ✅ limited | ❌ |
| 7 | OPERATIONALLY_ACTIONABLE | ✅ | ✅ limited |
| 8 | AUTOMATED_EXECUTION_ALLOWED | ✅ | ✅ |

Example (Frontera C default seed): **Level 1 — HYPOTHESIS_SEED**.
- Idea: `IDEA_ALLOWED`
- Claim: `CLAIM_BLOCKED`
- Action: `ACTION_BLOCKED`

---

## 5. Friction Gradient

| Risk Level | Default Friction | Blocked |
|---|---|---|
| RISK_0_PRIVATE_THOUGHT | FRICTION_0_FREE | — |
| RISK_1_INTERNAL_NOTE | FRICTION_1_LABEL | — |
| RISK_2_INTERNAL_RESEARCH | FRICTION_3_REQUIRE_OBSERVABLE | — |
| RISK_3_PUBLIC_CONTENT | FRICTION_4_REQUIRE_SOURCE | — |
| RISK_4_CLIENT_DELIVERABLE | FRICTION_5_REQUIRE_BENCHMARK | — |
| RISK_5_FINANCIAL_RECOMMENDATION | FRICTION_6_REQUIRE_RISK_ENGINE | — |
| RISK_6_REAL_WORLD_ACTION | FRICTION_7_REQUIRE_HUMAN_APPROVAL | — |
| RISK_7_AUTOMATED_EXECUTION | FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED | ✅ |

**Mode floor**: `AUTOMATED_EXECUTION_MODE` is always friction 8 regardless of risk.

---

## 6. Financial Action Gate

Required fields (all 10 must be present):

```txt
asset, time_horizon, source_freshness, entry_condition,
exit_condition, invalidation, risk_per_trade, position_sizing,
benchmark, post_mortem_plan
```

If any missing → `ACTION_BLOCKED`.
Intuition always → `INTUITION_LOGGED`.

Campaign example: `{"asset": "BTC", "time_horizon": "1w"}` → `ACTION_BLOCKED`, 8 missing fields.

---

## 7. Reports Generated (5 total)

```txt
reports/epistemic_modes/dream_to_claim_ladder_v1_6.md
reports/epistemic_modes/friction_gradient_v1_6.md
reports/epistemic_modes/hypothesis_incubation_v1_6.md
reports/epistemic_modes/risk_weighted_gatekeeping_v1_6.md
reports/campaigns/EPISTEMIC-MODES-FRICTION-GRADIENT-v1_6.md
```

---

## 8. Test Verification Summary

```
======================== 390 passed in 2.01s ========================
```

Previous baseline (v1.5): 339 passed → **+51 new tests added**.

### New test files (v1.6)

| File | Tests | All Pass |
|---|---|---|
| [test_epistemic_modes_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_epistemic_modes_v1_6.py) | 8 | ✅ |
| [test_dream_to_claim_ladder_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_dream_to_claim_ladder_v1_6.py) | 9 | ✅ |
| [test_friction_gradient_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_friction_gradient_v1_6.py) | 9 | ✅ |
| [test_hypothesis_incubation_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_hypothesis_incubation_v1_6.py) | 8 | ✅ |
| [test_risk_weighted_gatekeeper_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_risk_weighted_gatekeeper_v1_6.py) | 9 | ✅ |
| [test_epistemic_modes_campaign_v1_6.py](file:///d:/BIOCULTOR/PHYNG/tests/test_epistemic_modes_campaign_v1_6.py) | 8 | ✅ |

---

## 9. What v1.6 Does NOT Do

- Does not weaken rigor for public claims.
- Does not weaken rigor for financial execution.
- Does not call intuition evidence.
- Does not allow unsupported claims as truth.

## 10. What v1.6 DOES Do

- Preserves intuition as a seed while blocking unsupported claims/actions.
- Scales friction with risk, not with imagination.
- Keeps high-risk execution tightly gated.
- Allows early ideas to breathe without premature authority.

---

## 11. Scientific Discipline Note

> Phygn must not kill hope.
> It must stop hope from signing contracts as evidence.

> Phygn should be a ladder, not a guillotine.
