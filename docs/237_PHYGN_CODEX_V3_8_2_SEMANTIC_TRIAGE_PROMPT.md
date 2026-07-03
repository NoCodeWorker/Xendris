# Codex Prompt — Phygn v3.8.2 Semantic Triage & Priority Review Packet

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
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
```

Therefore v3.8.2 starts at:

```txt
233
```

---

# 1. Read first

Read these v3.8.2 specs:

```txt
docs/233_PHYGN_V3_8_2_SEMANTIC_TRIAGE_docs/status/GOAL.md
docs/234_PHYGN_V3_8_2_SEMANTIC_SCORING_AND_SLOT_RULES.md
docs/235_PHYGN_V3_8_2_PRIORITY_REVIEW_PACKET_SCHEMA.md
docs/236_PHYGN_V3_8_2_REPORTING_AND_NEXT_REVIEW_GATE.md
```

Also read:

```txt
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
```

Inspect:

```txt
phyng/pdf_text_extraction/
phyng/extract_candidate_review/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
```

Expected recent focused result:

```txt
30 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors. Do not treat that as v3.8.2 failure.

---

# 3. Mission

Implement:

```txt
v3.8.2 — Semantic Triage & Priority Review Packet
```

Convert the 548 extracted candidates into a compact prioritized packet.

Do not validate PHI_GRADIENT.

Do not grant support.

---

# 4. Input files

Load:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
data/real_sources/source_hashes_v3_6.json
```

If inputs are missing:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS
```

---

# 5. Create package

Create:

```txt
phyng/semantic_triage/
  __init__.py
  schemas.py
  loader.py
  slot_rules.py
  scoring.py
  prioritizer.py
  packet_builder.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_semantic_triage.py
```

Entrypoint:

```python
run_phi_gradient_semantic_triage_campaign(root: str | Path = ".")
```

---

# 6. Implement slot taxonomy

Use:

```txt
SLOT_1_DECOHERENCE_BASELINE
SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE
SLOT_3_BENCHMARK_RANGES
SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
SLOT_5_PARAMETER_CONSTRAINTS
SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS
SLOT_7_EXPERIMENTAL_CONTEXT
SLOT_8_ANALOGY_ONLY_OR_BACKGROUND
```

Pedernales + SLOT_4 must be prioritized if non-garbage candidates exist.

---

# 7. Scoring

Implement:

```txt
semantic_score
source_priority_score
slot_relevance_score
cleanliness_score
specificity_score
risk_score
triage_score
priority
```

Use the formula in:

```txt
docs/234_PHYGN_V3_8_2_SEMANTIC_SCORING_AND_SLOT_RULES.md
```

---

# 8. Packet target

Target:

```txt
30 to 60 priority review items
5 to 15 CRITICAL
10 to 25 HIGH
```

If fewer meaningful candidates exist, return fewer.

Do not stuff packet with garbage to hit the target.

---

# 9. Outputs

Create:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
data/real_sources/extracts/phi_gradient_triage_rejected_low_value_v3_8_2.json
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
```

---

# 10. Reports

Generate:

```txt
reports/semantic_triage/phi_gradient_semantic_triage_summary_v3_8_2.md
reports/semantic_triage/phi_gradient_priority_review_packet_v3_8_2.md
reports/semantic_triage/phi_gradient_slot_review_queues_v3_8_2.md
reports/semantic_triage/phi_gradient_low_value_exclusions_v3_8_2.md
reports/semantic_triage/phi_gradient_next_gate_readiness_v3_8_2.md
reports/campaigns/PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2.md
```

---

# 11. Statuses

Add status mappings:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_COMPLETED
PHI_GRADIENT_SEMANTIC_TRIAGE_PARTIAL
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
PHI_GRADIENT_SEMANTIC_TRIAGE_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_SEMANTIC_TRIAGE_NO_USEFUL_CANDIDATES
PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS
```

Active status should usually be:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
```

if packet_count > 0 and validation_ready_count remains 0.

---

# 12. Tests

Create:

```txt
tests/test_semantic_triage_loader_v3_8_2.py
tests/test_semantic_triage_slot_rules_v3_8_2.py
tests/test_semantic_triage_scoring_v3_8_2.py
tests/test_semantic_triage_packet_builder_v3_8_2.py
tests/test_semantic_triage_reports_v3_8_2.py
tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py
```

Minimum tests:

```txt
test_missing_inputs_block_triage
test_slot_assignment_detects_decoherence_baseline
test_slot_assignment_detects_visibility_observable
test_slot_assignment_detects_gradient_dynamics
test_slot_assignment_detects_parameter_constraints
test_pedernales_slot4_gets_minimum_high_priority
test_packet_size_is_capped
test_low_value_candidates_excluded
test_priority_packet_does_not_grant_support
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_8_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
v3.8.1 reader integration
v3.8 extract candidate review
v3.7 PDF extraction
v3.6 local source registry
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Critical candidate supports PHI_GRADIENT.
High-priority packet validates the model.
Triage score is evidence.
Pedernales candidate proves gradient component.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed:

```txt
Semantic triage was performed.
A priority review packet was generated.
The review burden was reduced.
Candidates require v3.8.3 review before validation-ready promotion.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
focused prior tests pass
v3.8.2 tests pass
triage map generated
priority packet generated
slot review queues generated
next gate readiness generated
reports generated
physical claims remain blocked
```

---

# 16. Final discipline

```txt
v3.8.2 chooses what deserves attention.
v3.8.3 reviews it.
v3.9 judges it.
```
