# Phygn v1.7 — Idea-to-Hypothesis UX, Prediction Accuracy & Model-Agnostic Runtime Results

Date: 2026-06-30

Source prompt:

```txt
docs/104_PHYGN_CODEX_V1_7_IDEA_TO_HYPOTHESIS_ACCURACY_RUNTIME_PROMPT.md
```

Supporting specs:

```txt
docs/100_PHYGN_V1_7_IDEA_TO_HYPOTHESIS_AND_PREDICTION_ACCURACY_docs/status/GOAL.md
docs/101_PHYGN_IDEA_TO_HYPOTHESIS_UX_PROTOCOL.md
docs/102_PHYGN_PREDICTION_ACCURACY_LEDGER_AND_CALIBRATION.md
docs/103_PHYGN_MODEL_AGNOSTIC_RUNTIME_AND_OPENSOURCE_MODELS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.7 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All acceptance criteria from §14 of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **408 passed, 0 failed** (390 baseline + 18 new) |
| Idea Intake works | ✅ Natural language inputs converted without requiring math equations |
| Hypothesis Seed Card works | ✅ Generates draft vars, proxies, missing info, and test plan |
| Math Translator works | ✅ Proposes suggested_not_validated structures based on domain |
| Prediction Ledger works | ✅ Record/Resolve pipeline implemented and verified |
| Calibration metrics work | ✅ Brier Score, ECE, and over/underconfidence classification works |
| Filter Lift report works | ✅ Verifies if passed predictions outperform baseline |
| Post-Mortem loop works | ✅ Falsification review: what happened, which gate was correct/loose/strict |
| Model Backend Registry works | ✅ Abstraction and registration interface works |
| Open-source mode works | ✅ Routing logic routes low-risk to local models, blocks high-risk |
| Reports generated | ✅ 10 markdown reports generated and verified |

---

## 2. New Packages and Modules

### UX Subsystem (`phyng/ux/`)
- [idea_intake.py](file:///d:/BIOCULTOR/PHYNG/phyng/ux/idea_intake.py) — Schemas for `IdeaIntake`, `HypothesisSeedCard`, and `MathTranslatorOutput`
- [hypothesis_builder.py](file:///d:/BIOCULTOR/PHYNG/phyng/ux/hypothesis_builder.py) — Core conversion logic (`process_idea_intake`)
- [math_translator.py](file:///d:/BIOCULTOR/PHYNG/phyng/ux/math_translator.py) — Converts intuition to testable candidate structures (`translate_intuition_to_testable_structure`)
- [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/ux/report.py) — Report writer for flow & seed card reports

### Prediction Accuracy Ledger Subsystem (`phyng/prediction_accuracy/`)
- [schemas.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/schemas.py) — Schemas for `PredictionRecord`, `PredictionOutcome`, etc.
- [metrics.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/metrics.py) — Hits, base rates, lifts, precision, recall, MAE, etc.
- [calibration.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/calibration.py) — Brier score, Expected Calibration Error (ECE)
- [ledger.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/ledger.py) — record/resolve & filter lift usefulness test
- [post_mortem.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/post_mortem.py) — post-mortem falsification/analysis loop
- [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_accuracy/report.py) — Report writer for ledger, calibration, lift, and post-mortem

### Model Runtime Subsystem (`phyng/model_runtime/`)
- [schemas.py](file:///d:/BIOCULTOR/PHYNG/phyng/model_runtime/schemas.py) — Backend registrations and model response types
- [backends.py](file:///d:/BIOCULTOR/PHYNG/phyng/model_runtime/backends.py) — Registry and routing/permissions logic
- [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/model_runtime/report.py) — Report writer for registry, routing, and open-source mode

---

## 3. Core Principles Enforced

### Propose vs Verify
> **LLM proposes. Phygn verifies.**
> The model is never the final authority. Authority comes from deterministic validation, benchmarks, sources, and human audits.

### Accountability
> **A filter that never measures its own predictive lift is just bureaucracy.**
> Phygn must not only judge hypotheses; it must judge the quality of its own judgments by measuring hit rate lift and expected calibration error.

### Hope-Preserving UX
> Avoid: "BLOCKED. No model."
> Prefer: "IDEA_ALLOWED. Not yet a claim. Here is the shortest path to make it testable."

---

## 4. Reports Generated (10 total)

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

## 5. Test Verification Summary

```
======================== 408 passed in 2.21s ========================
```

- Previous baseline (v1.6): 390 passed → **+18 new tests added**.

### New test files (v1.7)

| File | Tests | All Pass |
|---|---|---|
| [test_idea_intake_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_idea_intake_v1_7.py) | 2 | ✅ |
| [test_math_translator_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_math_translator_v1_7.py) | 2 | ✅ |
| [test_prediction_accuracy_ledger_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_prediction_accuracy_ledger_v1_7.py) | 1 | ✅ |
| [test_calibration_metrics_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_calibration_metrics_v1_7.py) | 4 | ✅ |
| [test_filter_lift_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_filter_lift_v1_7.py) | 2 | ✅ |
| [test_post_mortem_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_post_mortem_v1_7.py) | 1 | ✅ |
| [test_model_runtime_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_model_runtime_v1_7.py) | 5 | ✅ |
| [test_idea_to_hypothesis_accuracy_campaign_v1_7.py](file:///d:/BIOCULTOR/PHYNG/tests/test_idea_to_hypothesis_accuracy_campaign_v1_7.py) | 1 | ✅ |

---

## 6. What v1.7 Does NOT Do
- Does not guarantee prediction accuracy.
- Does not claim to eliminate hallucinations.
- Does not state that open-source models are inherently safe or correct.
- Does not equate filter approval with absolute truth.

## 7. What v1.7 DOES Do
- Converts raw natural language intuitions into structured, testable hypothesis seeds.
- Suggests candidate variables, proxies, observables, and test plans using template heuristics.
- Tracks Hit Rate, Base Rate, Accuracy Lift, Brier Score, and Expected Calibration Error (ECE).
- Identifies if the ladder is predictively ordered, issuing warnings if higher rungs fail to outperform lower ones.
- Conducts post-mortem falsification analysis to evaluate if gates were too loose or too strict.
- Implements capability-aware routing, permitting local/open-source models for low-risk ideation while blocking them for high-risk actions.
