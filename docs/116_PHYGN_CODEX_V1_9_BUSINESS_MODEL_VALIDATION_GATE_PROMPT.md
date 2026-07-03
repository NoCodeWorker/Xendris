# Codex Prompt — Phygn v1.9 Business Model Validation Gate

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/111_PHYGN_V1_8_COPILOT_TRUTH_BOUNDARY_UI_RESULTS.md
```

Therefore v1.9 starts at:

```txt
112
```

---

# 1. Read first

Read these v1.9 specs:

```txt
docs/112_PHYGN_V1_9_BUSINESS_MODEL_VALIDATION_GATE_docs/status/GOAL.md
docs/113_PHYGN_BUSINESS_HYPOTHESIS_CANVAS.md
docs/114_PHYGN_WILLINGNESS_TO_PAY_AND_CHANNEL_TEST_PROTOCOL.md
docs/115_PHYGN_UNIT_ECONOMICS_RISK_AND_KILL_CRITERIA_GATE.md
```

Also read the latest v1.8 result:

```txt
docs/111_PHYGN_V1_8_COPILOT_TRUTH_BOUNDARY_UI_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
422 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v1.9:

```txt
Business Model Validation Gate
Business Hypothesis Canvas
Business Claim Decomposition
Willingness-to-Pay Test Protocol
Channel Test Protocol
Unit Economics Gate
Risk Gate
Kill Criteria Gate
Business Post-Mortem
Reports
Campaign Runner
Tests
```

---

# 4. New package

Create:

```txt
phyng/business_validation/
  __init__.py
  schemas.py
  canvas.py
  decomposition.py
  wtp.py
  channel.py
  unit_economics.py
  risk.py
  kill_criteria.py
  post_mortem.py
  gatekeeper.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/business_model_validation_gate.py
```

---

# 5. Schemas

Implement Pydantic models:

```txt
BusinessIdeaInput
BusinessHypothesis
BusinessHypothesisCanvas
WillingnessToPayTest
ChannelTest
UnitEconomicsProfile
BusinessRiskAssessment
KillCriteria
BusinessValidationGateResult
BusinessPostMortem
```

Important enums:

```txt
BusinessHypothesisType
BusinessValidationStatus
WillingnessToPayLevel
ChannelValidationLevel
UnitEconomicsStatus
BusinessRiskStatus
BusinessPermissionLevel
```

---

# 6. Business idea decomposition

Implement:

```python
decompose_business_idea(input: BusinessIdeaInput) -> BusinessHypothesisCanvas
```

It must extract or mark missing:

```txt
target_customer
problem
urgency
current_alternative
value_proposition
WTP assumption
pricing
channel
unit economics
risk
kill criteria
```

Do not invent evidence.

Unknowns must be explicit.

---

# 7. Next Best Business Question

Implement:

```python
generate_next_best_business_question(canvas: BusinessHypothesisCanvas) -> NextBestQuestion
```

Priority:

```txt
1. target customer
2. painful problem
3. current alternative
4. willingness to pay
5. price
6. channel
7. unit economics
8. risks
9. kill criteria
```

Ask only one question.

---

# 8. WTP protocol

Implement:

```python
evaluate_willingness_to_pay(test: WillingnessToPayTest) -> WTPGateResult
```

Rules:

```txt
opinions and likes are not payment evidence
verbal interest is weak
deposits/preorders are stronger
paid pilots are strongest for B2B services
BUSINESS_VALIDATED_LIMITED requires WTP_6 or WTP_7 depending on model
```

---

# 9. Channel protocol

Implement:

```python
evaluate_channel_test(test: ChannelTest) -> ChannelGateResult
```

Rules:

```txt
traffic without qualified response is weak
meetings without offers are weak
offers without payment do not validate WTP
repeatable qualified acquisition upgrades channel status
```

---

# 10. Unit economics gate

Implement:

```python
evaluate_unit_economics(profile: UnitEconomicsProfile) -> UnitEconomicsGateResult
```

Rules:

```txt
unknown economics -> UNIT_ECONOMICS_UNKNOWN
negative margin -> UNIT_ECONOMICS_NEGATIVE
low margin/high delivery cost -> UNIT_ECONOMICS_FRAGILE
defined price + delivery cost + plausible margin -> UNIT_ECONOMICS_PLAUSIBLE
repeatable acquisition + healthy margin -> UNIT_ECONOMICS_STRONG
```

---

# 11. Risk and kill criteria

Implement:

```python
evaluate_business_risk(...)
evaluate_kill_criteria(...)
```

Block scale if:

```txt
RISK_BLOCKING
no kill criteria
no failure threshold
no customer definition
no WTP evidence
negative unit economics
```

---

# 12. Business gatekeeper

Implement:

```python
evaluate_business_validation_gate(canvas, wtp, channel, economics, risk, kill) -> BusinessValidationGateResult
```

Statuses:

```txt
BUSINESS_IDEA_ALLOWED
BUSINESS_HYPOTHESIS_SEED
BUSINESS_TESTABLE
BUSINESS_EVIDENCE_LIGHT
BUSINESS_VALIDATED_LIMITED
BUSINESS_BLOCKED_NO_CUSTOMER
BUSINESS_BLOCKED_NO_PROBLEM
BUSINESS_BLOCKED_NO_WTP
BUSINESS_BLOCKED_NO_CHANNEL
BUSINESS_BLOCKED_UNIT_ECONOMICS
BUSINESS_BLOCKED_REGULATORY_RISK
BUSINESS_BLOCKED_OVERCLAIM
```

Permissions:

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

# 13. Reports

Generate:

```txt
reports/business_validation/business_hypothesis_canvas_v1_9.md
reports/business_validation/willingness_to_pay_test_v1_9.md
reports/business_validation/channel_test_v1_9.md
reports/business_validation/unit_economics_risk_gate_v1_9.md
reports/business_validation/business_validation_gate_v1_9.md
reports/campaigns/BUSINESS-MODEL-VALIDATION-GATE-v1_9.md
```

---

# 14. Tests

Create:

```txt
tests/test_business_hypothesis_canvas_v1_9.py
tests/test_business_next_best_question_v1_9.py
tests/test_willingness_to_pay_v1_9.py
tests/test_channel_validation_v1_9.py
tests/test_unit_economics_risk_v1_9.py
tests/test_business_validation_gate_v1_9.py
tests/test_business_model_validation_campaign_v1_9.py
```

Minimum tests:

```txt
test_business_idea_decomposes_into_hypotheses
test_unknown_customer_blocks_validation
test_next_question_prioritizes_customer_first
test_wtp_opinion_not_payment_signal
test_paid_pilot_upgrades_wtp
test_channel_traffic_without_response_is_weak
test_negative_unit_economics_blocks_scale
test_missing_kill_criteria_blocks_scale
test_blocking_risk_blocks_scale
test_validated_limited_requires_wtp_and_channel
test_reports_generated
test_campaign_runs_end_to_end
```

---

# 15. Do not overclaim

Do not write:

```txt
Phygn guarantees business success.
Phygn validates a startup as profitable.
A positive gate means the business will work.
```

Allowed:

```txt
Phygn validates limited evidence for specific business hypotheses.
Phygn identifies missing evidence and risky assumptions.
Phygn defines the next cheapest test.
```

---

# 16. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
business canvas works
business decomposition works
next best business question works
WTP gate works
channel gate works
unit economics gate works
risk/kill criteria work
business gatekeeper works
reports generated
campaign runner works
```

Expected test count:

```txt
422 + new v1.9 tests
```

---

# 17. Final discipline

```txt
No customer, no business.
No payment signal, no validation.
No margin, no scale.
No kill criteria, no rigor.
```
