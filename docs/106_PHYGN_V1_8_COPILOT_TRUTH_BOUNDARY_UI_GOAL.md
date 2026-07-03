# Phygn v1.8 — Copilot Truth-Boundary UI Goal

## 0. Context

The latest confirmed document is:

```txt
105_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_ACCURACY_RUNTIME_RESULTS.md
```

Therefore, v1.8 starts at:

```txt
106
```

v1.7 established Idea Intake, Hypothesis Seed Cards, Math Translator, Prediction Accuracy Ledger, Calibration, Filter Lift, Post-Mortem Loop, Model-Agnostic Runtime and Open-source Model Mode.

v1.8 turns these subsystems into the first real product interface:

```txt
a chat copilot that receives any idea,
asks the perfect next question,
updates a hypothesis workspace,
and shows the user's truth-boundary status.
```

## 1. Product thesis

```txt
Cheap model + strong Phygn logic > expensive model without epistemic control.
```

The AI model is not the final authority.

The model handles conversation, paraphrasing, question phrasing, candidate suggestions and hypothesis drafting.

Phygn handles epistemic status, truth-boundary evaluation, mode classification, risk classification, claim permission, action permission, missing-field detection, audit trail and prediction logging.

## 2. What "truth-boundary" means

Phygn should not claim:

```txt
This is true.
```

unless the necessary epistemic requirements exist.

Instead it should say:

```txt
This is still an idea.
This is a hypothesis seed.
This is testable.
This has synthetic support.
This has source-backed limited support.
This is benchmark-supported.
This is actionable under constraints.
This has crossed a falsehood/overclaim/action boundary.
```

## 3. Core UX promise

```txt
Tell Phygn any idea.
Phygn will interview the idea until it becomes testable,
or reveal exactly why it cannot yet become a claim.
```

## 4. Main user-facing loop

```txt
User writes idea
→ Copilot summarizes what it understood
→ Phygn detects current mode and ladder level
→ Phygn identifies the missing field with highest leverage
→ Copilot asks one perfect next question
→ User answers
→ Hypothesis Card updates
→ Truth Boundary Panel updates
→ Repeat until testable or blocked by explicit boundary
```

## 5. Required UI components

```txt
Chat Copilot
Truth Boundary Panel
Hypothesis Workspace
Next Best Question Card
Allowed / Blocked Uses
Evidence Ladder
Prediction Ledger Preview
Audit Trail Preview
```

## 6. Non-negotiable epistemic discipline

Do not allow unsupported public claims, financial action from intuition, automated execution without full authorization, source hallucination, or claim elevation from tone/confidence alone.

Do allow private dreams, early intuitions, hypothesis incubation, test design, synthetic exploration and limited source-backed claims.

## 7. v1.8 acceptance criteria

v1.8 is complete when the implementation provides:

```txt
Socratic Question Engine
Truth Boundary Status
Copilot Response Contract
Hypothesis Workspace State
Cheap/Open-source Model Orchestration Hooks
Mode-aware UI State
Reports
Tests
Campaign Runner
```

## 8. Final principle

```txt
Phygn does not tell users they own the truth.
It tells them where they stand in relation to testable truth.
```
