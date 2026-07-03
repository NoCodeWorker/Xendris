# Codex Prompt — Phygn v3.8.3 Priority Packet Review & Validation-Ready Extract Promotion

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
docs/238_PHYGN_V3_8_2_SEMANTIC_TRIAGE_RESULTS.md
```

Therefore v3.8.3 starts at:

```txt
239
```

---

# 1. Read first

Read these v3.8.3 specs:

```txt
docs/239_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_docs/status/GOAL.md
docs/240_PHYGN_V3_8_3_PROMOTION_DECISION_RULES.md
docs/241_PHYGN_V3_8_3_VALIDATION_READY_PACK_SCHEMA.md
docs/242_PHYGN_V3_8_3_REPORTING_AND_V3_9_GATE.md
```

Also read:

```txt
docs/238_PHYGN_V3_8_2_SEMANTIC_TRIAGE_RESULTS.md
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
```

Inspect:

```txt
phyng/semantic_triage/
phyng/extract_candidate_review/
phyng/pdf_text_extraction/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py tests/test_semantic_triage_loader_v3_8_2.py tests/test_semantic_triage_slot_rules_v3_8_2.py tests/test_semantic_triage_scoring_v3_8_2.py tests/test_semantic_triage_packet_builder_v3_8_2.py tests/test_semantic_triage_reports_v3_8_2.py tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py
```

Expected recent focused result:

```txt
43 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v3.8.3 — Priority Packet Review & Validation-Ready Extract Promotion
```

Review the 60-item priority packet and all relevant Pedernales SLOT_4 triage records.

Promote only clean, exact, traceable items to validation-ready extracts.

Do not grant source support.

---

# 4. Input files

Load:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/source_hashes_v3_6.json
```

If inputs are missing:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS
```

---

# 5. Create package

Create:

```txt
phyng/priority_packet_review/
  __init__.py
  schemas.py
  loader.py
  promotion_rules.py
  pedernales_expander.py
  decision_engine.py
  validation_ready_pack.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_gradient_priority_packet_review.py
```

Entrypoint:

```python
run_phi_gradient_priority_packet_review_campaign(root: str | Path = ".")
```

---

# 6. Promotion rules

Implement conservative promotion.

A record may be promoted only if:

```txt
source_id exists
sha256 matches v3.6 hash manifest
page_number or exact location exists
text is non-empty
text is legible
slot/component role is clear
decision question can be answered by the extract
limitations are recorded
```

No promoted extract is support.

It is only validation-ready.

---

# 7. Pedernales expansion

In addition to the 60 packet items, include:

```txt
all Pedernales SLOT_4 records from semantic triage map
```

when:

```txt
priority in [CRITICAL, HIGH, MEDIUM]
or include_in_priority_packet = true
```

Deduplicate by:

```txt
candidate_id
source_id
page_number
normalized_text
```

---

# 8. Output files

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json
data/real_sources/extracts/phi_gradient_rejected_priority_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json
data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json
```

---

# 9. Reports

Generate:

```txt
reports/priority_packet_review/phi_gradient_priority_packet_review_summary_v3_8_3.md
reports/priority_packet_review/phi_gradient_validation_ready_extract_pack_v3_8_3.md
reports/priority_packet_review/phi_gradient_review_decisions_v3_8_3.md
reports/priority_packet_review/phi_gradient_rejected_priority_items_v3_8_3.md
reports/priority_packet_review/phi_gradient_analogy_only_items_v3_8_3.md
reports/priority_packet_review/phi_gradient_manual_review_queue_v3_8_3.md
reports/priority_packet_review/phi_gradient_next_source_pressure_gate_v3_8_3.md
reports/campaigns/PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3.md
```

---

# 10. Statuses

Add status mappings:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_COMPLETED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_PARTIAL
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS
```

If validation-ready extracts exist, active status:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE
```

If none:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS
```

---

# 11. Tests

Create:

```txt
tests/test_priority_packet_review_loader_v3_8_3.py
tests/test_priority_packet_review_promotion_rules_v3_8_3.py
tests/test_priority_packet_review_pedernales_expander_v3_8_3.py
tests/test_priority_packet_review_pack_v3_8_3.py
tests/test_priority_packet_review_reports_v3_8_3.py
tests/test_phi_gradient_priority_packet_review_campaign_v3_8_3.py
```

Minimum tests:

```txt
test_missing_inputs_block_priority_packet_review
test_promotion_requires_source_hash
test_promotion_requires_page_or_location
test_promotion_requires_clear_slot_role
test_ambiguous_item_goes_to_manual_review
test_negative_or_limitation_item_can_be_promoted
test_pedernales_slot4_records_are_expanded_beyond_capped_packet
test_validation_ready_extract_is_not_support
test_ready_for_v3_9_requires_validation_ready_extract
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_8_2_behavior_preserved
```

---

# 12. Behavior preservation

Do not alter:

```txt
v3.8.2 semantic triage
v3.8.1 PDF reader integration
v3.8 extract candidate review
v3.7 PDF extraction
v3.6 source registry
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
Validation-ready extract supports PHI_GRADIENT.
Priority packet review proves source support.
Pedernales proves gradient component.
Benchmark candidate grants benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed:

```txt
Priority packet items were reviewed.
Some items may be promoted to validation-ready extracts.
v3.9 may judge source pressure if validation-ready extracts exist.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
focused prior tests pass
v3.8.3 tests pass
priority packet reviewed
Pedernales SLOT_4 expanded inspection performed
validation-ready pack generated
next source-pressure inputs generated
reports generated
physical claims remain blocked
```

---

# 15. Final discipline

```txt
Promotion means ready to be judged, not judged.
```
