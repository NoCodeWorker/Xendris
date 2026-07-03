# Phygn v1.9 — Business Hypothesis Canvas

## 0. Purpose

This document defines the canvas used by Phygn to convert a business model into testable hypotheses.

A business model is not treated as a single idea.

It is treated as a network of claims.

---

## 1. Business Hypothesis Canvas fields

```txt
business_idea
target_customer
customer_segment
problem
problem_urgency
current_alternative
value_proposition
pain_intensity
willingness_to_pay_assumption
pricing_assumption
channel_assumption
sales_cycle_assumption
conversion_assumption
retention_assumption
gross_margin_assumption
delivery_cost_assumption
regulatory_risk
operational_risk
differentiation_claim
kill_criteria
next_test
validation_status
```

---

## 2. Claim decomposition

Example input:

```txt
Signphy will help startups and investors audit AI/deeptech claims.
```

Decomposition:

```txt
Claim 1: startups have a painful credibility problem
Claim 2: investors want technical claim audits
Claim 3: both groups are willing to pay
Claim 4: the audit can be delivered at acceptable cost
Claim 5: the output creates enough trust/value
Claim 6: the market can be reached through a repeatable channel
```

Each claim must become a hypothesis.

---

## 3. Business hypothesis format

```python
class BusinessHypothesis(BaseModel):
    hypothesis_id: str
    claim_text: str
    hypothesis_type: str
    target_customer: str | None
    observable: str | None
    metric: str | None
    test_method: str | None
    success_threshold: str | None
    failure_threshold: str | None
    evidence_level: str
    status: str
```

---

## 4. Hypothesis types

```txt
CUSTOMER
PROBLEM
URGENCY
VALUE_PROPOSITION
WILLINGNESS_TO_PAY
CHANNEL
CONVERSION
RETENTION
UNIT_ECONOMICS
DIFFERENTIATION
REGULATORY
OPERATIONAL
```

---

## 5. Required minimum for testability

A business hypothesis is not testable until it has:

```txt
target customer
observable behavior
metric
test method
success threshold
failure threshold
time window
```

---

## 6. Next Best Business Question examples

If no customer:

```txt
Who exactly has the problem strongly enough to pay first?
```

If no problem:

```txt
What painful situation does this customer experience today?
```

If no willingness-to-pay:

```txt
What real offer could you put in front of them to test payment intent?
```

If no channel:

```txt
How will you reach 20 qualified prospects this week?
```

If no unit economics:

```txt
How much does it cost you to deliver one successful outcome?
```

---

## 7. Evidence levels

```txt
NO_EVIDENCE
ANECDOTAL
INTERVIEW_SIGNAL
COMMITMENT_SIGNAL
PAYMENT_SIGNAL
REPEAT_PAYMENT_SIGNAL
RETENTION_SIGNAL
SCALABLE_CHANNEL_SIGNAL
UNIT_ECONOMICS_SIGNAL
```

---

## 8. Final principle

```txt
Every business claim must know what customer behavior would prove it wrong.
```
