# Phygn v3.8.2 - Semantic Triage & Priority Review Packet Results

Date: 2026-07-01

Source prompt:

```txt
docs/237_PHYGN_CODEX_V3_8_2_SEMANTIC_TRIAGE_PROMPT.md
```

Supporting specs:

```txt
docs/233_PHYGN_V3_8_2_SEMANTIC_TRIAGE_docs/status/GOAL.md
docs/234_PHYGN_V3_8_2_SEMANTIC_SCORING_AND_SLOT_RULES.md
docs/235_PHYGN_V3_8_2_PRIORITY_REVIEW_PACKET_SCHEMA.md
docs/236_PHYGN_V3_8_2_REPORTING_AND_NEXT_REVIEW_GATE.md
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.8.2 PROMPT SPECIFICATIONS**

Final campaign status:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
```

Interpretation:

```txt
The 548 v3.7 extracted candidates were semantically triaged.
A capped priority review packet was generated.
Slot review queues were generated.
Low-value candidates were excluded from the packet.
Pedernales SLOT_4 candidates were prioritized.
No validation-ready extract was created by v3.8.2.
No source support was granted.
No physical claim was upgraded.
```

Validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py tests/test_semantic_triage_loader_v3_8_2.py tests/test_semantic_triage_slot_rules_v3_8_2.py tests/test_semantic_triage_scoring_v3_8_2.py tests/test_semantic_triage_packet_builder_v3_8_2.py tests/test_semantic_triage_reports_v3_8_2.py tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py
43 passed in 1.76s
```

Focused v3.8.2 validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_semantic_triage_loader_v3_8_2.py tests/test_semantic_triage_slot_rules_v3_8_2.py tests/test_semantic_triage_scoring_v3_8_2.py tests/test_semantic_triage_packet_builder_v3_8_2.py tests/test_semantic_triage_reports_v3_8_2.py tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py
13 passed in 0.71s
```

---

## 2. New Package and Campaign

Created:

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

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_semantic_triage.py
```

Entrypoint:

```python
run_phi_gradient_semantic_triage_campaign(root: str | Path = ".")
```

Campaign command:

```txt
.\.venv\Scripts\python.exe -m phyng.campaigns.phi_gradient_semantic_triage
```

Campaign output:

```txt
status = PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
input_candidate_count = 548
triaged_candidate_count = 548
priority_packet_count = 60
critical_count = 12
high_count = 47
ready_for_v3_9 = false
```

---

## 3. Input Artifacts

Loaded:

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

Hash boundary preserved:

```txt
Only candidates whose source_id and sha256 match the v3.6 source hash manifest are triaged.
```

---

## 4. Triage Metrics

Summary:

| Metric | Result |
|---|---:|
| Input candidates | 548 |
| Triaged candidates | 548 |
| Priority packet items | 60 |
| Critical items | 12 |
| High items | 47 |
| Low-value exclusions | 124 |
| Validation-ready extracts created by v3.8.2 | 0 |
| Ready for positive v3.9 pressure gate | false |

Slot packet coverage:

| Slot | Items | Critical | High |
|---|---:|---:|---:|
| `SLOT_1_DECOHERENCE_BASELINE` | 6 | 0 | 6 |
| `SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE` | 20 | 8 | 12 |
| `SLOT_3_BENCHMARK_RANGES` | 17 | 0 | 17 |
| `SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS` | 1 | 0 | 1 |
| `SLOT_5_PARAMETER_CONSTRAINTS` | 9 | 3 | 6 |
| `SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS` | 3 | 1 | 2 |
| `SLOT_7_EXPERIMENTAL_CONTEXT` | 3 | 0 | 3 |
| `SLOT_8_ANALOGY_ONLY_OR_BACKGROUND` | 1 | 0 | 0 |

Pedernales SLOT_4 packet count:

```txt
5 semantic triage records matched Pedernales + SLOT_4 and were marked for packet inclusion.
1 Pedernales SLOT_4 item is present in the capped 60-item priority review packet.
```

---

## 5. Generated Data Artifacts

Created:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
data/real_sources/extracts/phi_gradient_triage_rejected_low_value_v3_8_2.json
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
```

Next gate readiness:

```txt
ready_for_v3_9 = false
manual_review_required = true
recommended_next_action = Run v3.8.3 priority packet review before any positive v3.9 pressure decision.
```

---

## 6. Generated Reports

Created:

```txt
reports/semantic_triage/phi_gradient_semantic_triage_summary_v3_8_2.md
reports/semantic_triage/phi_gradient_priority_review_packet_v3_8_2.md
reports/semantic_triage/phi_gradient_slot_review_queues_v3_8_2.md
reports/semantic_triage/phi_gradient_low_value_exclusions_v3_8_2.md
reports/semantic_triage/phi_gradient_next_gate_readiness_v3_8_2.md
reports/campaigns/PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2.md
```

All generated reports include the canonical status section.

---

## 7. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_COMPLETED
PHI_GRADIENT_SEMANTIC_TRIAGE_PARTIAL
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
PHI_GRADIENT_SEMANTIC_TRIAGE_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_SEMANTIC_TRIAGE_NO_USEFUL_CANDIDATES
PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS
```

The active status maps conservatively to:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Risk Level: TECHNICAL_RISK
```

---

## 8. New Tests

Created:

```txt
tests/test_semantic_triage_loader_v3_8_2.py
tests/test_semantic_triage_slot_rules_v3_8_2.py
tests/test_semantic_triage_scoring_v3_8_2.py
tests/test_semantic_triage_packet_builder_v3_8_2.py
tests/test_semantic_triage_reports_v3_8_2.py
tests/test_phi_gradient_semantic_triage_campaign_v3_8_2.py
```

Coverage includes:

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

## 9. Blocked Claims

The campaign explicitly blocks:

```txt
Priority packet validates PHI_GRADIENT.
High-priority candidate is source support.
Critical candidate is evidence.
Triage score is physical support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed statements:

```txt
Semantic triage was performed.
A priority review packet was generated.
Candidate review was reduced to a smaller set.
Pedernales SLOT_4 was prioritized if candidate text exists.
```

---

## 10. Next Gate

Recommended next phase:

```txt
v3.8.3 - Priority Packet Review & Validation-Ready Extract Promotion
```

v3.9 should not be run as a positive pressure gate until v3.8.3 produces validation-ready extracts.

---

## 11. Final Assessment

v3.8.2 reduced candidate review load from:

```txt
548 extracted candidates
```

to:

```txt
60 prioritized packet items
```

without granting support or relaxing gates.

Final discipline note:

```txt
v3.8.2 chooses what deserves attention.
v3.8.3 reviews it.
v3.9 judges it.
```

