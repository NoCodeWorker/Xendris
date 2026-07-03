# Codex Prompt — Phygn v3.9 Source Pressure Decision Gate

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
```

Therefore v3.9 starts at:

```txt
245
```

---

# 1. Read first

Read these v3.9 specs:

```txt
docs/245_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_docs/status/GOAL.md
docs/246_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_RULES.md
docs/247_PHYGN_V3_9_SOURCE_PRESSURE_OUTPUT_SCHEMAS.md
docs/248_PHYGN_V3_9_REPORTING_AND_POST_DECISION_GATE.md
```

Also read:

```txt
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
docs/238_PHYGN_V3_8_2_SEMANTIC_TRIAGE_RESULTS.md
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
```

Inspect:

```txt
phyng/priority_packet_review/
phyng/semantic_triage/
phyng/extract_candidate_review/
phyng/pdf_text_extraction/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py tests/test_semantic_triage_loader_v3_8_2.py tests/test_semantic_triage_slot_rules_v3_8_2.py tests/test_semantic_triage_scoring_v3_8_2.py tests/test_semantic_triage_packet_builder_v3_8_2.py tests/test_semantic_triage_reports_v3_8_2.py tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py tests/test_priority_packet_review_loader_v3_8_3.py tests/test_priority_packet_review_promotion_rules_v3_8_3.py tests/test_priority_packet_review_pedernales_expander_v3_8_3.py tests/test_priority_packet_review_pack_v3_8_3.py tests/test_priority_packet_review_reports_v3_8_3.py tests/test_phi_gradient_priority_packet_review_campaign_v3_8_3.py
```

Expected recent focused result:

```txt
56 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v3.9 — Source Pressure Decision Gate
```

Judge the 29 validation-ready extracts.

v3.9 must be allowed to hurt PHI_GRADIENT.

Do not force a positive outcome.

---

# 4. Input files

Load:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json
data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json
data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json
data/real_sources/source_hashes_v3_6.json
```

If missing:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK
```

---

# 5. Create package

Create:

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

Create wrapper:

```txt
phyng/campaigns/phi_gradient_source_pressure_decision.py
```

Entrypoint:

```python
run_phi_gradient_source_pressure_decision_campaign(root: str | Path = ".")
```

---

# 6. Decision logic

For each extract classify:

```txt
SUPPORTS_BASELINE_ONLY
SUPPORTS_OBSERVABLE_ONLY
SUPPORTS_BENCHMARK_ALIGNMENT
SUPPORTS_PARAMETER_CONSTRAINT
SUPPORTS_GRADIENT_COMPONENT
CONTRADICTS_COMPONENT
LIMITS_COMPONENT
ANALOGY_ONLY
INCONCLUSIVE
IRRELEVANT_AFTER_REVIEW
```

Then decide slot pressure.

Then decide global source pressure.

---

# 7. Critical rule

Implement exactly:

```txt
No SLOT_4 validation-ready extract
→ gradient_component_support = false
→ PHI_GRADIENT cannot be source-backed as a physical gradient mechanism.
```

If SLOT_4 is absent but baseline/observable/benchmark extracts exist:

```txt
candidate may be benchmark-relevant or source-pressure-limited,
but not physically gradient-supported.
```

---

# 8. Required outputs

Create:

```txt
data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json
data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json
data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json
data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json
```

---

# 9. Reports

Generate:

```txt
reports/source_pressure/phi_gradient_source_pressure_decision_v3_9.md
reports/source_pressure/phi_gradient_extract_pressure_map_v3_9.md
reports/source_pressure/phi_gradient_slot_pressure_summary_v3_9.md
reports/source_pressure/phi_gradient_benchmark_alignment_v3_9.md
reports/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.md
reports/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.md
reports/campaigns/PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9.md
```

---

# 10. Statuses

Add status mappings:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_READY
PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
PHI_GRADIENT_SOURCE_PRESSURE_BENCHMARK_RELEVANT
PHI_GRADIENT_SOURCE_PRESSURE_CONTRADICTED
PHI_GRADIENT_SOURCE_PRESSURE_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK
```

---

# 11. Tests

Create:

```txt
tests/test_source_pressure_loader_v3_9.py
tests/test_source_pressure_classifier_v3_9.py
tests/test_source_pressure_slot_summary_v3_9.py
tests/test_source_pressure_benchmark_alignment_v3_9.py
tests/test_source_pressure_decision_engine_v3_9.py
tests/test_source_pressure_reports_v3_9.py
tests/test_phi_gradient_source_pressure_campaign_v3_9.py
```

Minimum tests:

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

# 12. Behavior preservation

Do not alter:

```txt
v3.8.3 priority packet review
v3.8.2 semantic triage
v3.8.1 PDF reader integration
v3.8 candidate review
v3.7 PDF extraction
v3.6 source registry
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
Source pressure validates PHI_GRADIENT.
Benchmark relevance validates physics.
Baseline support validates gradient mechanism.
Parameter constraints prove the model.
Frontera C is validated.
```

Allowed:

```txt
Source pressure decision was performed.
The current extract pack supports/limits/contradicts/inconclusively pressures specific components.
Physical claims remain blocked unless explicitly permitted by later experimental gates.
```

---

# 14. Acceptance criteria

Complete when:

```txt
focused prior tests pass
v3.9 tests pass
29 validation-ready extracts loaded
extract pressure map generated
slot pressure summary generated
benchmark alignment generated
contradiction/limitation map generated
global decision produced
reports generated
physical claims remain blocked
```

---

# 15. Final discipline

```txt
A source-pressure gate that cannot contradict the hypothesis is not a gate.
```
