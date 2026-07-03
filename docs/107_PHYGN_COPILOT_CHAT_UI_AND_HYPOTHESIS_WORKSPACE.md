# Phygn v1.8 — Copilot Chat UI & Hypothesis Workspace

## 0. Purpose

This document defines the product interface for Phygn as a chat-based epistemic copilot.

The interface must be understandable by non-technical users while retaining the rigor of the internal Phygn engine.

## 1. Recommended layout

```txt
┌───────────────────────────────────────────────────────────────┐
│ Signphy / Phygn Copilot                                       │
│ Mode · Risk · Ladder Level · Truth Boundary                   │
├───────────────────────────────┬───────────────────────────────┤
│ Chat Copilot                  │ Truth Boundary Panel          │
│                               │                               │
│ User ideas                    │ Current Level                 │
│ Copilot answers               │ Allowed Uses                  │
│ Next questions                │ Blocked Uses                  │
│                               │ Missing Fields                │
│                               │ Next Best Action              │
├───────────────────────────────┴───────────────────────────────┤
│ Hypothesis Workspace                                           │
│ Cards · Variables · Proxies · Observables · Test Plans         │
└───────────────────────────────────────────────────────────────┘
```

## 2. Chat Copilot responsibilities

The chat must accept raw intuition, business ideas, scientific hypotheses, technical claims, financial intuitions, product claims, text excerpts and document summaries.

The chat must return:

```txt
what was understood
current epistemic level
what is allowed now
what is blocked now
one next-best question
```

## 3. Truth Boundary Panel

The panel displays:

```txt
Epistemic Mode
Risk Level
Friction Level
Dream-to-Claim Ladder Level
Truth Boundary Status
Allowed Uses
Blocked Uses
Missing Requirements
Next Best Question
```

Example:

```txt
Mode: HYPOTHESIS_MODE
Level: HYPOTHESIS_SEED
Truth Boundary: INSIDE_HYPOTHESIS_BOUNDARY / OUTSIDE_CLAIM_BOUNDARY
Allowed: explore, refine, design test
Blocked: publish as fact, use for action
Next: define observable
```

## 4. Hypothesis Workspace

Each idea produces a living card:

```txt
Hypothesis Card
```

Required card fields:

```txt
raw_idea
clean_hypothesis
domain
suspected_relation
variables
observables
proxies
baseline_candidates
benchmark_candidates
evidence_needed
failure_condition
time_horizon
risk_level
current_ladder_level
allowed_uses
blocked_uses
history
```

## 5. Workspace state transitions

```txt
EMPTY_WORKSPACE
IDEA_CAPTURED
HYPOTHESIS_SEED_CREATED
QUESTION_PENDING
ANSWER_RECEIVED
CARD_UPDATED
TESTABLE_DRAFT_READY
SOURCE_REQUIRED
BENCHMARK_REQUIRED
CLAIM_LIMITED_ALLOWED
ACTION_BLOCKED
```

## 6. User-facing tone

Avoid:

```txt
Blocked.
Not valid.
Wrong.
```

Prefer:

```txt
Allowed as an idea.
Not yet allowed as a claim.
Here is the shortest path to make it testable.
```

## 7. Required UX buttons

```txt
Ask next question
Suggest observable
Suggest proxy
Draft test plan
Request sources
Audit as claim
Log prediction
Run post-mortem
```

High-risk buttons must be disabled unless gates pass:

```txt
Publish claim
Use for financial decision
Automate execution
```

## 8. Final principle

```txt
The user should experience rigor as guidance, not punishment.
```
