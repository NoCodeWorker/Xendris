# Phygn v1.9 — Willingness-to-Pay & Channel Test Protocol

## 0. Purpose

This document defines how Phygn tests whether a business model has real demand.

Interest is not demand.

Praise is not demand.

Engagement is not payment.

---

## 1. Willingness-to-Pay ladder

```txt
WTP_0_OPINION
WTP_1_INTEREST
WTP_2_MEETING_ACCEPTED
WTP_3_PROBLEM_CONFIRMED
WTP_4_PRICE_ACCEPTED_VERBALLY
WTP_5_PURCHASE_INTENT_WITH_DEADLINE
WTP_6_DEPOSIT_OR_PREORDER
WTP_7_PAID_PILOT
WTP_8_REPEAT_PAYMENT
```

---

## 2. WTP gate

A business cannot reach `BUSINESS_VALIDATED_LIMITED` without at least:

```txt
WTP_6_DEPOSIT_OR_PREORDER
```

or, for B2B service validation:

```txt
WTP_7_PAID_PILOT
```

---

## 3. WTP test definition

Each WTP test must define:

```txt
offer
target customer
price
delivery promise
time window
minimum outreach count
minimum qualified conversations
success threshold
failure threshold
```

Example:

```txt
Offer: Technical Claim Audit Report
Target: AI/deeptech startups preparing fundraising
Price: 1,500 EUR
Outreach: 30 qualified founders
Success: 2 paid pilots or 3 deposits
Failure: 0 payment signals after 30 qualified contacts
Time window: 14 days
```

---

## 4. Channel test

A channel test must define:

```txt
channel
target segment
message
outreach volume
qualified response threshold
conversion threshold
cost
time window
```

Channel types:

```txt
cold email
LinkedIn outbound
warm referrals
content/SEO
communities
partners
paid ads
marketplaces
events
direct sales
```

---

## 5. Channel validation levels

```txt
CHANNEL_0_UNTESTED
CHANNEL_1_REACHABLE
CHANNEL_2_RESPONSES
CHANNEL_3_QUALIFIED_CONVERSATIONS
CHANNEL_4_OFFERS_SENT
CHANNEL_5_PAYMENTS
CHANNEL_6_REPEATABLE
CHANNEL_7_SCALABLE
```

---

## 6. False positives

Phygn must flag:

```txt
vanity metrics
likes without payment
traffic without conversion
meetings without problem urgency
interest without price
pilot without decision-maker
discounted payment that destroys margins
```

---

## 7. Next Best Business Question examples

If WTP is weak:

```txt
What paid offer can you test within 14 days?
```

If channel is unknown:

```txt
Which channel can reach 30 qualified prospects fastest?
```

If price is vague:

```txt
What exact price will you ask for in the first test?
```

---

## 8. Final principle

```txt
The customer validates the business by risking money, time, reputation or operational change.
```
