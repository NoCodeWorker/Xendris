# Phygn v1.7 — Idea-to-Hypothesis UX & Prediction Accuracy Goal

## 0. Purpose

Phygn v1.6 introduced:

```txt
Epistemic Modes
Dream-to-Claim Ladder
Friction Gradient
Hypothesis Incubation
Risk-Weighted Gatekeeping
```

v1.7 addresses two critical concerns:

```txt
1. What happens if the user only has an intuition and no mathematical model?
2. If an idea passes Phygn filters, does that statistically improve prediction quality?
```

This version must ensure Phygn is not merely a blocking machine.

Phygn must become:

```txt
a translator from intuition to testable hypothesis
and
a ledger of whether passing Phygn actually improves prediction outcomes.
```

---

## 1. Core principle

```txt
You do not need to start with a formula.
You need to start with an idea willing to be interrogated.
```

And:

```txt
Passing Phygn is not proof.
Passing Phygn must become statistically accountable.
```

---

## 2. Problem A — user lacks mathematics

Many users have:

```txt
intuition
pattern recognition
domain experience
market feel
scientific suspicion
creative analogy
```

but lack:

```txt
formal variables
equations
observables
baselines
metrics
benchmarks
```

Phygn must not answer:

```txt
Come back when you have a model.
```

It must answer:

```txt
Let us convert your intuition into a hypothesis seed.
```

---

## 3. Problem B — filtered ideas must show better outcomes

If Phygn allows a claim/action after passing filters, then over time the system must measure:

```txt
Did allowed predictions perform better than blocked/rejected/low-level ideas?
Did confidence scores calibrate?
Did benchmark-supported claims outperform intuition-only claims?
Did financial action gates reduce losses?
Did scientific claim gates reduce overclaim?
```

Without this loop, Phygn is only epistemic theater.

---

## 4. v1.7 mission

Implement support for:

```txt
Idea Intake
Guided Questioning
Math Translator
Hypothesis Seed Card
Observable/Proxy Suggestion
Next Best Test
Prediction Accuracy Ledger
Calibration Metrics
Post-Mortem Engine
Model-Agnostic Runtime
Open-source model compatibility
```

---

## 5. User experience goal

The user writes:

```txt
I have a feeling that X affects Y.
```

Phygn returns:

```txt
IDEA_ALLOWED
HYPOTHESIS_SEED_CREATED
possible variables
possible observables
possible proxies
missing information
next best questions
blocked claims
minimum test plan
```

---

## 6. Prediction accountability goal

Every prediction-like output must be logged as:

```txt
PredictionRecord
```

and later evaluated with:

```txt
PredictionOutcome
```

The system must compute:

```txt
hit rate
base rate
Brier score
calibration error
precision/recall where applicable
profit/loss if financial
benchmark-relative performance
false-positive rate
false-negative rate
blocked-claim avoided-loss estimate if available
```

---

## 7. Phygn pass-rate vs accuracy

Phygn must explicitly track:

```txt
pass_rate
accuracy_given_pass
accuracy_given_fail_or_low_level
lift_over_baseline
calibration_by_ladder_level
calibration_by_mode
```

If:

```txt
accuracy_given_pass <= baseline_accuracy
```

then Phygn must report:

```txt
FILTER_NOT_PREDICTIVELY_USEFUL_YET
```

This is allowed and important.

---

## 8. Model-agnostic runtime

Phygn must not depend on frontier models.

It should support:

```txt
frontier LLMs
open-source LLMs
local models
small classifiers
rule-based validators
symbolic/deterministic gates
```

Critical rule:

```txt
LLM proposes.
Phygn verifies.
```

If model quality is low:

```txt
more tasks are routed to deterministic gates or human review
```

---

## 9. What v1.7 may unlock

Allowed:

```txt
intuitions can become hypothesis seeds
hypotheses can receive suggested observables/proxies
predictions can be tracked statistically
model outputs can be audited across model backends
```

Not allowed:

```txt
Phygn guarantees correct predictions
Phygn eliminates hallucinations completely
Open-source model outputs are automatically trustworthy
Passing filters equals truth
```

---

## 10. Acceptance criteria

v1.7 is complete when:

```txt
Idea Intake schema exists
Hypothesis Builder exists
Math Translator exists
PredictionRecord schema exists
PredictionOutcome schema exists
accuracy/calibration metrics exist
post-mortem loop exists
model backend abstraction exists
open-source/local model mode is supported
reports generated
tests pass
```

---

## 11. Final principle

```txt
A filter that never measures its own predictive lift is just bureaucracy.
```
