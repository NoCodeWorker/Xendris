# Phygn v1.8 — Socratic Question Engine & Next Best Question Protocol

## 0. Purpose

Phygn should not merely list what is missing.

It must ask the question that obtains the missing information with minimum cognitive friction.

```txt
The right question is the bridge between intuition and testability.
```

## 1. Pipeline

```txt
Raw idea
→ Parse suspected relation
→ Detect missing fields
→ Rank missing fields by epistemic leverage
→ Generate one next-best question
→ Offer answer options if useful
→ Update hypothesis card
→ Recalculate truth boundary
```

## 2. Missing field taxonomy

```txt
UNKNOWN_DOMAIN
UNCLEAR_TERM
UNCLEAR_CAUSE
UNCLEAR_EFFECT
MISSING_VARIABLE
MISSING_OBSERVABLE
MISSING_PROXY
MISSING_TIME_HORIZON
MISSING_BASELINE
MISSING_BENCHMARK
MISSING_FAILURE_CONDITION
MISSING_SOURCE
MISSING_METRIC
MISSING_RISK_DEFINITION
```

## 3. Question types

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

## 4. Default priority

For general hypothesis formation:

```txt
1. clarify the relation
2. define the observable
3. define the failure condition
4. define the time horizon
5. define the baseline
6. choose proxy/measurement
7. choose metric
8. request source/benchmark
```

For financial or real-world action contexts, risk, invalidation and position/action constraints move upward.

## 5. NextBestQuestion schema

```python
class NextBestQuestion(BaseModel):
    question_id: str
    question_type: str
    question_text: str
    why_needed: str
    answer_options: list[str]
    free_text_allowed: bool
    updates_fields: list[str]
    blocks_until_answered: list[str]
```

## 6. Example: business hypothesis

Input:

```txt
I think companies will pay for claim audits before raising investment.
```

Next question:

```txt
Who exactly would pay first?

A) startup founder
B) investor / fund
C) consultant
D) corporate innovation team
E) technical due diligence firm
F) other
```

Why:

```txt
Without buyer definition, willingness-to-pay cannot be tested.
```

## 7. Example: finance intuition

Input:

```txt
BTC feels ready to rise this week.
```

Next question:

```txt
What would make you accept that this intuition was wrong?

A) price closes below a defined level
B) invalidating news/event
C) underperformance versus benchmark
D) failure to move within the time horizon
E) other
```

Why:

```txt
Financial intuition cannot move toward action without invalidation.
```

## 8. Example: scientific hypothesis

Input:

```txt
Frontera C may create a decoherence signature.
```

Next question:

```txt
What observable would change if this were true?

A) visibility decay curve
B) coherence time
C) interference contrast
D) environmental decoherence rate
E) other
```

Why:

```txt
A physical hypothesis needs an observable before it can become testable.
```

## 9. Final rule

Ask only one question at a time unless the user explicitly requests full diagnosis.

## 10. Final principle

```txt
Phygn does not require users to know how to formulate hypotheses.
It interviews them until the hypothesis appears.
```
