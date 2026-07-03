# Codex Prompt — Phygn v1.7 Idea-to-Hypothesis UX, Prediction Accuracy & Model-Agnostic Runtime

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v1.6 complete or in progress.
Epistemic modes and friction gradient are defined.
Concern: users may only have intuition, not mathematical models.
Concern: passing Phygn filters must statistically improve prediction outcomes.
Concern: Phygn should work with open-source/local models, not only frontier models.
```

Important numbering:

```txt
v1.7 docs:
100_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_AND_PREDICTION_ACCURACY_docs/status/GOAL.md
101_PHYGN_IDEA_TO_HYPOTHESIS_UX_PROTOCOL.md
102_PHYGN_PREDICTION_ACCURACY_LEDGER_AND_CALIBRATION.md
103_PHYGN_MODEL_AGNOSTIC_RUNTIME_AND_OPENSOURCE_MODELS.md
104_PHYGN_CODEX_V1_7_IDEA_TO_HYPOTHESIS_ACCURACY_RUNTIME_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/100_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_AND_PREDICTION_ACCURACY_docs/status/GOAL.md
docs/101_PHYGN_IDEA_TO_HYPOTHESIS_UX_PROTOCOL.md
docs/102_PHYGN_PREDICTION_ACCURACY_LEDGER_AND_CALIBRATION.md
docs/103_PHYGN_MODEL_AGNOSTIC_RUNTIME_AND_OPENSOURCE_MODELS.md
```

Also read:

```txt
docs/98_PHYGN_CODEX_V1_6_EPISTEMIC_MODES_PROMPT.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement v1.7 support for:

```txt
Idea Intake
Hypothesis Seed Card
Math Translator
Observable/Proxy Suggestion
Prediction Accuracy Ledger
Calibration Metrics
Post-Mortem Loop
Model Backend Registry
Open-source/local model compatibility
reports
tests
```

This phase must make Phygn usable by people who only have ideas, and accountable when its filters pass predictions.

---

# 4. New modules

Create:

```txt
phyng/ux/
  __init__.py
  idea_intake.py
  hypothesis_builder.py
  math_translator.py
  report.py

phyng/prediction_accuracy/
  __init__.py
  schemas.py
  metrics.py
  calibration.py
  ledger.py
  post_mortem.py
  report.py

phyng/model_runtime/
  __init__.py
  schemas.py
  backends.py
  routing.py
  report.py

phyng/campaigns/idea_to_hypothesis_accuracy_runtime.py
```

---

# 5. Idea Intake

Implement:

```python
process_idea_intake(intake: IdeaIntake) -> HypothesisSeedCard
```

It must output:

```txt
IDEA_ALLOWED
HYPOTHESIS_SEED_CREATED
candidate variables
candidate observables
candidate proxies
missing information
next best questions
minimum test plan
blocked uses
```

---

# 6. Math Translator

Implement:

```python
translate_intuition_to_testable_structure(...)
```

Input:

```txt
natural language intuition
domain
intended use
```

Output:

```txt
possible X variables
possible Y observables
proxy candidates
baseline candidates
failure condition candidates
test plan candidates
```

It must label proposals as:

```txt
SUGGESTED_NOT_VALIDATED
```

---

# 7. Prediction Accuracy Ledger

Implement:

```python
record_prediction(...)
resolve_prediction(...)
compute_prediction_metrics(...)
```

Schemas:

```txt
PredictionRecord
PredictionOutcome
PredictionMetrics
CalibrationReport
FilterLiftReport
```

Metrics:

```txt
hit_rate
base_rate
accuracy_lift
Brier score where probabilities exist
expected calibration error
false positive rate
false negative rate
benchmark-relative performance
```

---

# 8. Filter usefulness

Implement:

```python
evaluate_filter_lift(records, outcomes)
```

Statuses:

```txt
FILTER_NOT_PREDICTIVELY_USEFUL_YET
FILTER_SHOWS_PREDICTIVE_LIFT
INSUFFICIENT_OUTCOMES
LADDER_NOT_PREDICTIVELY_ORDERED
```

---

# 9. Post-mortem

Implement:

```python
generate_prediction_post_mortem(prediction_id)
```

It must answer:

```txt
what was predicted
what happened
was baseline beaten
which evidence mattered
which gate was too strict/too loose
what should change
```

---

# 10. Model-agnostic runtime

Implement:

```python
register_model_backend(...)
route_model_task(...)
evaluate_backend_permission(...)
```

Backend types:

```txt
FRONTIER_API
OPEN_SOURCE_API
LOCAL_LLM
SMALL_CLASSIFIER
EMBEDDING_MODEL
RULE_BASED
HUMAN_REVIEW
```

Rule:

```txt
LLM proposes.
Phygn verifies.
```

Open-source/local models should be allowed for:

```txt
idea intake
hypothesis seed generation
proxy suggestion
draft summarization
low-risk claim extraction
```

They should be blocked or require human review for:

```txt
financial action
automated execution
physical validation
medical/legal high-risk claims
```

---

# 11. Reports

Generate:

```txt
reports/ux/idea_to_hypothesis_flow_v1_7.md
reports/ux/hypothesis_seed_cards_v1_7.md
reports/prediction_accuracy/prediction_ledger_v1_7.md
reports/prediction_accuracy/calibration_report_v1_7.md
reports/prediction_accuracy/filter_lift_report_v1_7.md
reports/prediction_accuracy/post_mortem_report_v1_7.md
reports/model_runtime/model_backend_registry_v1_7.md
reports/model_runtime/opensource_model_mode_v1_7.md
reports/model_runtime/capability_routing_v1_7.md
reports/campaigns/IDEA-TO-HYPOTHESIS-ACCURACY-RUNTIME-v1_7.md
```

---

# 12. Tests

Add:

```txt
tests/test_idea_intake_v1_7.py
tests/test_math_translator_v1_7.py
tests/test_prediction_accuracy_ledger_v1_7.py
tests/test_calibration_metrics_v1_7.py
tests/test_filter_lift_v1_7.py
tests/test_post_mortem_v1_7.py
tests/test_model_runtime_v1_7.py
tests/test_idea_to_hypothesis_accuracy_campaign_v1_7.py
```

Minimum tests:

```txt
test_idea_intake_creates_seed_card
test_seed_card_allows_exploration_blocks_claim
test_math_translator_suggests_observable_and_proxy
test_prediction_record_and_resolution
test_hit_rate_computation
test_brier_score_computation
test_filter_lift_insufficient_outcomes
test_filter_lift_detects_no_predictive_lift
test_post_mortem_generated
test_open_source_model_allowed_for_low_risk
test_open_source_model_blocked_for_financial_execution
test_rule_based_backend_allowed_for_gatekeeping
test_reports_generated
```

---

# 13. Do not overclaim

Do not write:

```txt
Phygn guarantees prediction accuracy.
Phygn eliminates hallucinations.
Open-source models are always safe.
Passing Phygn proves truth.
```

Allowed:

```txt
Phygn tracks whether filtered predictions outperform baselines.
Phygn can work with open-source models under stronger gates.
Intuitions can be converted into testable hypothesis seeds.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
Idea Intake works
Hypothesis Seed Card works
Math Translator works
Prediction Ledger works
Calibration metrics work
Filter Lift report works
Post-Mortem loop works
Model Backend Registry works
open-source mode is supported with risk-aware routing
reports generated
```

---

# 15. Final discipline

```txt
Phygn must help ideas become testable.
Then it must measure whether its own approvals were worth anything.
```
