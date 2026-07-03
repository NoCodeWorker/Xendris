# Phygn v1.9 — Unit Economics, Risk & Kill Criteria Gate

## 0. Purpose

A business may have demand and still fail if economics, risks or operations are broken.

This document defines the gate that prevents enthusiasm from bypassing economics.

---

## 1. Unit economics fields

```txt
price
gross_revenue_per_customer
cost_to_deliver
gross_margin
customer_acquisition_cost
sales_cycle_length
refund_rate
support_cost
retention_rate
repeat_purchase_rate
payback_period
contribution_margin
```

---

## 2. Unit economics status

```txt
UNIT_ECONOMICS_UNKNOWN
UNIT_ECONOMICS_NEGATIVE
UNIT_ECONOMICS_FRAGILE
UNIT_ECONOMICS_PLAUSIBLE
UNIT_ECONOMICS_STRONG
```

---

## 3. Minimum unit economics gate

A business cannot be `BUSINESS_OPERATIONALLY_ACTIONABLE` unless it has:

```txt
defined price
estimated delivery cost
estimated CAC or acquisition effort
gross margin estimate
sales cycle estimate
failure threshold
```

---

## 4. Risk gate

Risk categories:

```txt
LEGAL
REGULATORY
FINANCIAL
REPUTATIONAL
OPERATIONAL
TECHNICAL
DATA_PRIVACY
SAFETY
DEPENDENCY
```

Risk status:

```txt
RISK_UNASSESSED
RISK_LOW
RISK_MEDIUM
RISK_HIGH_REQUIRES_REVIEW
RISK_BLOCKING
```

---

## 5. Kill criteria

Every business validation attempt must define:

```txt
what result kills the hypothesis
what result requires pivot
what result justifies another test
what result justifies investment
```

Example kill criteria:

```txt
If 30 qualified prospects produce 0 payment signals, the WTP hypothesis fails.
If CAC exceeds gross margin after three channel tests, the channel hypothesis fails.
If paid pilots require custom work exceeding margin, delivery model fails.
```

---

## 6. Business Post-Mortem

For each failed or completed validation experiment, Phygn records:

```txt
hypothesis
test
expected result
actual result
gate decision
was gate too strict
was gate too loose
next decision
```

---

## 7. Business permission levels

```txt
EXPLORE_ONLY
INTERVIEW_ALLOWED
TEST_OFFER_ALLOWED
PAID_PILOT_ALLOWED
LIMITED_LAUNCH_ALLOWED
SCALE_BLOCKED
SCALE_ALLOWED
```

---

## 8. Final principle

```txt
A good business test is designed so that failure teaches faster than hope burns money.
```
