# Phygn v3.9 - Source Pressure Decision Gate Results

Date: 2026-07-01

Source prompt:

```txt
docs/249_PHYGN_CODEX_V3_9_SOURCE_PRESSURE_DECISION_PROMPT.md
```

Supporting specs:

```txt
docs/245_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_docs/status/GOAL.md
docs/246_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_RULES.md
docs/247_PHYGN_V3_9_SOURCE_PRESSURE_OUTPUT_SCHEMAS.md
docs/248_PHYGN_V3_9_REPORTING_AND_POST_DECISION_GATE.md
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.9 PROMPT SPECIFICATIONS**

Final campaign status:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
```

Interpretation:

```txt
The 29 validation-ready extracts were classified and judged.
Source pressure decision was performed.
Baseline decoherence framing has limited source backing.
Visibility/coherence as observable has limited source backing.
Benchmark ranges relevant for model comparison were found.
No SLOT_4 validation-ready extract exists.
gradient_component_support = false
PHI_GRADIENT cannot be source-backed as a physical gradient mechanism.
Physical claims remain blocked.
```

Validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py tests/test_semantic_triage_loader_v3_8_2.py tests/test_semantic_triage_slot_rules_v3_8_2.py tests/test_semantic_triage_scoring_v3_8_2.py tests/test_semantic_triage_packet_builder_v3_8_2.py tests/test_semantic_triage_reports_v3_8_2.py tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py tests/test_priority_packet_review_loader_v3_8_3.py tests/test_priority_packet_review_promotion_rules_v3_8_3.py tests/test_priority_packet_review_pedernales_expander_v3_8_3.py tests/test_priority_packet_review_pack_v3_8_3.py tests/test_priority_packet_review_reports_v3_8_3.py tests/test_phi_gradient_priority_packet_review_campaign_v3_8_3.py tests/test_source_pressure_loader_v3_9.py tests/test_source_pressure_classifier_v3_9.py tests/test_source_pressure_slot_summary_v3_9.py tests/test_source_pressure_benchmark_alignment_v3_9.py tests/test_source_pressure_decision_engine_v3_9.py tests/test_source_pressure_reports_v3_9.py tests/test_phi_gradient_source_pressure_campaign_v3_9.py
83 passed in 3.14s
```

Focused v3.9 validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_source_pressure_loader_v3_9.py tests/test_source_pressure_classifier_v3_9.py tests/test_source_pressure_slot_summary_v3_9.py tests/test_source_pressure_benchmark_alignment_v3_9.py tests/test_source_pressure_decision_engine_v3_9.py tests/test_source_pressure_reports_v3_9.py tests/test_phi_gradient_source_pressure_campaign_v3_9.py
27 passed in 1.07s
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/source_pressure_decision/
  __init__.py
  schemas.py
  loader.py
  pressure_classifier.py
  slot_pressure.py
  benchmark_alignment.py
  contradiction_map.py
  decision_engine.py
  recommendations.py
  reports.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_source_pressure_decision.py
```

Entrypoint:

```python
run_phi_gradient_source_pressure_decision_campaign(root: str | Path = ".")
```

Campaign command:

```txt
.\.venv\Scripts\python.exe -m phyng.campaigns.phi_gradient_source_pressure_decision
```

Campaign output:

```txt
status = PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
primary_decision = PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
confidence = LOW
gradient_component_support = false
validation_ready_count = 29
physical_claim_permission = BLOCKED
global_decisions = [PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND, PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED]
```

---

## 3. Input Artifacts

Loaded:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json
data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json
data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json
data/real_sources/source_hashes_v3_6.json
```

---

## 4. Source Pressure Decision

Primary decision:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

Global decisions:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

Gradient component support:

```txt
gradient_component_support = false
```

Reason:

```txt
No SLOT_4 validation-ready extract exists.
PHI_GRADIENT cannot be source-backed as a physical gradient mechanism.
```

Confidence:

```txt
LOW
```

---

## 5. Slot Pressure Summary

| Slot | Extracts | Support | Contradiction | Limitation | Status |
|---|---:|---:|---:|---:|---|
| `SLOT_1_DECOHERENCE_BASELINE` | 2 | 2 | 0 | 0 | `SLOT_SOURCE_BACKED_LIMITED` |
| `SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE` | 5 | 5 | 0 | 0 | `SLOT_SOURCE_BACKED_LIMITED` |
| `SLOT_3_BENCHMARK_RANGES` | 12 | 12 | 0 | 0 | `SLOT_BENCHMARK_RELEVANT` |
| `SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS` | 0 | 0 | 0 | 0 | `SLOT_NO_VALID_EXTRACTS` |
| `SLOT_5_PARAMETER_CONSTRAINTS` | 6 | 6 | 0 | 0 | `SLOT_SOURCE_BACKED_LIMITED` |
| `SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS` | 3 | 0 | 0 | 3 | `SLOT_LIMITED` |
| `SLOT_7_EXPERIMENTAL_CONTEXT` | 1 | 0 | 0 | 0 | `SLOT_INCONCLUSIVE` |

Critical observation:

```txt
SLOT_4 has zero validation-ready extracts.
This blocks gradient-component support.
SLOT_6 contains 3 limitation extracts with net negative pressure score (-1.45).
```

---

## 6. Benchmark Alignment

```txt
benchmark_decision = BENCHMARK_WITH_OBSERVABLE_AND_RANGE
benchmark_extracts = 12
observable_alignment = 5
```

Missing benchmark fields:

```txt
visibility (as literal term in SLOT_3 extracts)
```

Limitations:

```txt
Benchmark relevance does not validate physics.
Benchmark alignment is necessary but not sufficient for model comparison.
```

---

## 7. Contradiction and Limitation Map

```txt
contradictions = 0
limitations = 3
```

The 3 limitation extracts are from SLOT_6 (negative constraints/limitations).

Dominant risks:

```txt
Source-backed limitations constrain candidate viability.
```

Required model changes:

```txt
Assess whether limitations narrow the candidate to a viable regime.
```

---

## 8. Generated Data Artifacts

Created:

```txt
data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json
data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json
data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json
data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json
```

---

## 9. Generated Reports

Created:

```txt
reports/source_pressure/phi_gradient_source_pressure_decision_v3_9.md
reports/source_pressure/phi_gradient_extract_pressure_map_v3_9.md
reports/source_pressure/phi_gradient_slot_pressure_summary_v3_9.md
reports/source_pressure/phi_gradient_benchmark_alignment_v3_9.md
reports/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.md
reports/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.md
reports/campaigns/PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9.md
```

All generated reports include the canonical status section.

---

## 10. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
phyng/core/risk_levels.py (SCIENTIFIC_RISK added)
```

Statuses:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_READY
PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
PHI_GRADIENT_SOURCE_PRESSURE_BENCHMARK_RELEVANT
PHI_GRADIENT_SOURCE_PRESSURE_CONTRADICTED
PHI_GRADIENT_SOURCE_PRESSURE_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK
```

The active status maps to:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

---

## 11. New Tests

Created:

```txt
tests/test_source_pressure_loader_v3_9.py
tests/test_source_pressure_classifier_v3_9.py
tests/test_source_pressure_slot_summary_v3_9.py
tests/test_source_pressure_benchmark_alignment_v3_9.py
tests/test_source_pressure_decision_engine_v3_9.py
tests/test_source_pressure_reports_v3_9.py
tests/test_phi_gradient_source_pressure_campaign_v3_9.py
```

Coverage includes:

```txt
test_missing_validation_ready_pack_blocks_pressure_gate
test_extract_classified_as_baseline_only
test_extract_classified_as_observable_only
test_extract_classified_as_benchmark_alignment
test_extract_classified_as_parameter_constraint
test_no_slot4_extract_blocks_gradient_component_support
test_negative_or_limitation_extract_can_dominate_support
test_analogy_only_extract_does_not_grant_support
test_benchmark_relevant_does_not_validate_physics
test_decision_engine_allows_contradiction
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_8_3_behavior_preserved
```

---

## 12. Allowed Claims

```txt
The literature supports baseline decoherence framing.
The literature supports visibility/coherence as a relevant observable.
The literature contains benchmark ranges relevant for model comparison.
The current extract pack does not support the gradient-component mechanism.
Physical claims remain blocked unless explicitly permitted by later experimental gates.
```

---

## 13. Blocked Claims

```txt
PHI_GRADIENT is physically validated.
Frontera C is validated.
The invariant has empirical confirmation.
Source pressure is experimental proof.
Source pressure validates PHI_GRADIENT.
Benchmark relevance validates physics.
Baseline support validates gradient mechanism.
Parameter constraints prove the model.
```

---

## 14. Next Recommendations

```txt
v4.0 — Benchmark Dataset Construction & Observable Alignment
Seek exact Pedernales manual review for SLOT_4 content.
Design benchmark-only model comparison without gradient-component claim.
Run negative-control source pressure.
```

---

## 15. Acceptance Criteria Check

| Criterion | Result |
|---|---|
| focused prior tests pass | ✓ 56 passed |
| v3.9 tests pass | ✓ 27 passed |
| 29 validation-ready extracts loaded | ✓ 29 loaded |
| extract pressure map generated | ✓ |
| slot pressure summary generated | ✓ |
| benchmark alignment generated | ✓ |
| contradiction/limitation map generated | ✓ |
| global decision produced | ✓ |
| reports generated | ✓ 7 reports |
| physical claims remain blocked | ✓ BLOCKED |

---

## 16. Final Assessment

v3.9 performed the first honest source-pressure decision on 29 validation-ready extracts.

The result:

```txt
Limited source backing exists for baseline framing and observable alignment.
Benchmark-relevant data was found.
No SLOT_4 extract exists — gradient-component support is false.
3 limitation extracts constrain candidate viability.
Physical claims remain blocked.
Confidence is LOW.
```

The gate worked:

```txt
It did not force a positive outcome.
It identified the gradient-component gap.
It recorded limitations from negative-constraint extracts.
It recommended SLOT_4 literature acquisition before any gradient claim.
```

Final discipline note:

```txt
A source-pressure gate that cannot contradict the hypothesis is not a gate.
```
