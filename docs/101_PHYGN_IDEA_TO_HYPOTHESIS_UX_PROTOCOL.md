# Phygn v1.7 — Idea-to-Hypothesis UX Protocol

## 0. Purpose

This document defines the UX flow for users who have only an intuition.

Phygn must not require mathematical sophistication at entry.

It must transform:

```txt
intuition -> hypothesis seed -> variables -> observables -> proxies -> test plan
```

---

## 1. Primary UX entry points

The interface should offer:

```txt
I have an intuition
I saw a pattern
I want to test an idea
I want to audit a claim
I want to design a benchmark
I want to know if this can be acted on
```

The default entry for non-technical users:

```txt
I have an intuition
```

---

## 2. Idea Intake schema

```python
class IdeaIntake(BaseModel):
    idea_id: str
    raw_intuition: str
    domain: str | None
    suspected_relation: str | None
    possible_cause: str | None
    possible_effect: str | None
    context: str | None
    user_confidence: float | None
    intended_use: str
    risk_level: str
```

---

## 3. Hypothesis Seed Card

```python
class HypothesisSeedCard(BaseModel):
    seed_id: str
    title: str
    raw_intuition: str
    cleaned_hypothesis: str
    current_ladder_level: str
    allowed_uses: list[str]
    blocked_uses: list[str]
    candidate_variables: list[str]
    candidate_observables: list[str]
    candidate_proxies: list[str]
    missing_information: list[str]
    next_best_questions: list[str]
    minimum_test_plan: list[str]
```

---

## 4. Guided questioning

Phygn should ask or infer:

```txt
What do you think influences what?
What would you expect to observe?
When should it happen?
What would prove you wrong?
What data could represent the idea?
What is the baseline?
What is the cost of being wrong?
Is this private exploration, public claim, or action?
```

---

## 5. Math Translator

The Math Translator converts natural language into candidate structures.

Example:

```txt
Input:
"I think attention without volume means a stock move is fake."

Candidate variables:
attention = news count / social mentions / search trend
volume confirmation = relative volume / OBV / VWAP behavior
fake move = reversal within N days / failure to hold breakout

Candidate hypothesis:
If attention rises but volume confirmation remains below threshold,
then breakout continuation probability is lower than baseline.
```

The user does not need to provide the formula.

Phygn proposes:

```txt
observable
proxy
baseline
failure condition
test plan
```

---

## 6. Output style

Avoid:

```txt
BLOCKED. No model.
```

Prefer:

```txt
IDEA_ALLOWED.
Not yet a claim.
Here is the shortest path to make it testable.
```

---

## 7. UX states

```txt
IDEA_CAPTURED
HYPOTHESIS_SEED_CREATED
VARIABLES_SUGGESTED
OBSERVABLES_SUGGESTED
PROXIES_SUGGESTED
TEST_PLAN_DRAFTED
READY_FOR_USER_REVIEW
READY_FOR_BENCHMARK_DESIGN
```

---

## 8. Claim permission display

The UI must show use-specific permission:

```txt
Explore privately: Allowed
Save as hypothesis: Allowed
Publish as fact: Blocked
Use for client decision: Blocked
Use for automated execution: Blocked
```

This is more human than a single red/green result.

---

## 9. Reports

Generate:

```txt
reports/ux/idea_to_hypothesis_flow_v1_7.md
reports/ux/hypothesis_seed_cards_v1_7.md
```

---

## 10. Final principle

```txt
A user should be able to start with a feeling and leave with a testable question.
```
