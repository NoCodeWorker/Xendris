# Phygn v1.6 — Risk-Weighted Gatekeeping Protocol

## 0. Purpose

This document defines how Phygn adjusts its strictness based on the possible harm of an output.

The same idea may be harmless in private brainstorming and dangerous in public execution.

---

## 1. Risk dimensions

Phygn should evaluate:

```txt
financial risk
health/safety risk
legal/compliance risk
reputational risk
scientific overclaim risk
automation risk
scale of impact
reversibility
```

---

## 2. Risk levels

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

---

## 3. Friction levels

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

## 4. Risk-to-friction mapping

| Risk | Default friction |
|---|---|
| `RISK_0_PRIVATE_THOUGHT` | `FRICTION_0_FREE` |
| `RISK_1_INTERNAL_NOTE` | `FRICTION_1_LABEL` |
| `RISK_2_INTERNAL_RESEARCH` | `FRICTION_3_REQUIRE_OBSERVABLE` |
| `RISK_3_PUBLIC_CONTENT` | `FRICTION_4_REQUIRE_SOURCE` |
| `RISK_4_CLIENT_DELIVERABLE` | `FRICTION_5_REQUIRE_BENCHMARK` |
| `RISK_5_FINANCIAL_RECOMMENDATION` | `FRICTION_6_REQUIRE_RISK_ENGINE` |
| `RISK_6_REAL_WORLD_ACTION` | `FRICTION_7_REQUIRE_HUMAN_APPROVAL` |
| `RISK_7_AUTOMATED_EXECUTION` | `FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED` |

---

## 5. Financial action gate

For finance/investment agents, any action-like output requires:

```txt
ticker/asset
time horizon
source freshness
entry condition
exit condition
invalidation
risk per trade
position sizing
max drawdown rule
benchmark comparison
post-mortem logging
```

If missing:

```txt
ACTION_BLOCKED
```

Private intuition may still be:

```txt
INTUITION_LOGGED
```

---

## 6. Scientific public claim gate

For scientific public claims, require:

```txt
source support
observable
baseline
metric
failure condition
scope limitation
claim level
```

If missing:

```txt
CLAIM_BLOCKED
```

---

## 7. Principle of proportionality

```txt
Higher risk does not make ideas illegal.
It makes actions and claims more expensive.
```

---

## 8. Final principle

```txt
Friction must scale with harm, not with imagination.
```
