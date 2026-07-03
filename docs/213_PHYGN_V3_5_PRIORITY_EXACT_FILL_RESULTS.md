# Phygn v3.5 - Priority Exact Extract Fill Results

Date: 2026-06-30

Source prompt:

```txt
docs/212_PHYGN_CODEX_V3_5_PRIORITY_EXACT_FILL_PROMPT.md
```

Supporting specs:

```txt
docs/208_PHYGN_V3_5_PRIORITY_EXACT_EXTRACT_FILL_docs/status/GOAL.md
docs/209_PHYGN_PRIORITY_SOURCE_REVIEW_PROTOCOL.md
docs/210_PHYGN_PRIORITY_EXACT_FILL_SCHEMA_AND_FILES.md
docs/211_PHYGN_V3_5_REPORTING_AND_NEXT_DECISION.md
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.5 PROMPT SPECIFICATIONS**

Final campaign status:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
```

Interpretation:

```txt
Priority exact fill was attempted.
The five priority sources were selected and mapped to the reviewed v3.2 seed pack.
No locally available source text was present for exact quote/equation/range extraction.
No exact source text, quote, equation, observable, parameter range, benchmark range, or negative constraint was fabricated.
Physical claims remain blocked.
```

Validation:

```txt
pytest -q
670 passed in 45.55s
```

Focused v3.5 validation:

```txt
pytest -q tests/test_priority_exact_fill_schema_v3_5.py tests/test_priority_source_availability_v3_5.py tests/test_priority_exact_fill_records_v3_5.py tests/test_priority_exact_fill_mapping_v3_5.py tests/test_priority_exact_fill_reports_v3_5.py tests/test_phi_gradient_priority_exact_fill_campaign_v3_5.py
12 passed in 1.54s
```

Baseline before v3.5:

```txt
658 passed in 45.30s
```

Net result:

```txt
658 baseline tests + 12 v3.5 tests = 670 passing tests
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/priority_exact_fill/
  __init__.py
  schemas.py
  loader.py
  source_availability.py
  priority_fill.py
  equation_observable_map.py
  parameter_range_map.py
  review_gate.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_priority_exact_fill.py
```

Entrypoint:

```python
run_phi_gradient_priority_exact_fill_campaign(root: str | Path = ".")
```

Gate entrypoint:

```python
run_phi_gradient_priority_exact_fill_gate(root: str = ".")
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/priority_exact_fill/schemas.py
```

Schemas:

```txt
PrioritySourceAvailabilityRecord
PriorityExactFillRecord
PriorityExactFillLocationRecord
PriorityEquationObservableMapEntry
PriorityEquationObservableMap
PriorityParameterRangeMapEntry
PriorityParameterRangeMap
PhiGradientPriorityExactFillGateResult
PhiGradientPriorityExactFillCampaignResult
```

---

## 4. Priority Sources Processed

The v3.5 priority set was processed as requested:

| Priority source | Local reviewed seed source | Source text status | Validation ready |
|---|---|---|---|
| `SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE` | `SRC-PHI-V32-001` | `SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD` | `false` |
| `SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE` | `SRC-PHI-V32-002` | `SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD` | `false` |
| `SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST` | `SRC-PHI-V32-005` | `SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD` | `false` |
| `SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` | `SRC-PHI-V32-009` | `SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD` | `false` |
| `SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING` | `SRC-PHI-V32-010` | `SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD` | `false` |

Summary:

| Metric | Result |
|---|---:|
| Priority sources processed | 5 |
| Validation-ready priority records | 0 |
| Unresolved priority records | 5 |
| Records requiring source text | 5 |
| Equation/observable map entries | 0 |
| Parameter/range map entries | 0 |

---

## 5. Source Text Boundary

The v3.5 source text rule was preserved:

```txt
Availability of a source URL or arXiv identifier does not count as exact source text.
```

All five priority records were generated as unresolved records:

```txt
source_text_status = SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD
review_status = EXACT_FILL_REQUIRES_SOURCE_TEXT
validation_ready = false
```

No fabricated fields were added:

```txt
exact_quote = null
equation_text = null
observable_text = null
parameter_range_text = null
benchmark_range_text = null
negative_constraint_text = null
```

---

## 6. Generated Data Artifacts

Created:

```txt
data/real_sources/extracts/phi_gradient_priority_exact_extracts_v3_5.json
data/real_sources/extracts/phi_gradient_priority_exact_extract_locations_v3_5.json
data/real_sources/extracts/phi_gradient_priority_equation_observable_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_parameter_range_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_review_notes_v3_5.md
```

The exact extract file contains five priority records and no fabricated exact content.

The equation/observable and parameter/range maps are intentionally empty because no priority record is validation-ready.

---

## 7. Generated Reports

Created:

```txt
reports/priority_exact_fill/phi_gradient_priority_source_review_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_exact_extracts_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_locations_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_equation_observable_map_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_parameter_ranges_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_risk_and_negative_pressure_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_next_gate_v3_5.md
reports/campaigns/PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md
```

All generated reports include the canonical status section.

Campaign report:

```txt
reports/campaigns/PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md
```

---

## 8. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_COMPLETED
PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL
PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED
```

The active status maps to:

```txt
Canonical Permission: REVIEW_REQUIRED
Blocked Reasons: MISSING_SOURCE_SUPPORT
Evidence Level: NO_EVIDENCE
Support Level: UNSUPPORTED
Risk Level: TECHNICAL_RISK
```

---

## 9. New Tests

Created:

```txt
tests/test_priority_exact_fill_schema_v3_5.py
tests/test_priority_source_availability_v3_5.py
tests/test_priority_exact_fill_records_v3_5.py
tests/test_priority_exact_fill_mapping_v3_5.py
tests/test_priority_exact_fill_reports_v3_5.py
tests/test_phi_gradient_priority_exact_fill_campaign_v3_5.py
```

Coverage includes:

| Test | Purpose |
|---|---|
| `test_priority_sources_are_selected` | Confirms the five priority sources map to reviewed local seed IDs |
| `test_source_text_unavailable_does_not_fabricate_extract` | Confirms URLs/arXiv IDs do not become source text |
| `test_unresolved_priority_record_requires_source_text` | Confirms unresolved record defaults |
| `test_validation_ready_requires_exact_content` | Confirms exact content is required for validation readiness |
| `test_no_quote_or_range_fabrication` | Confirms no quote/range fabrication |
| `test_partial_status_when_some_sources_ready` | Confirms mixed ready/unresolved state |
| `test_all_unavailable_status_requires_source_text` | Confirms all-unavailable campaign status |
| `test_reports_include_canonical_section` | Confirms report contract integration |
| `test_campaign_generates_reports` | Confirms campaign report generation |
| `test_physical_claims_remain_blocked` | Confirms blocked claim discipline |
| `test_existing_v3_4_behavior_preserved` | Confirms v3.4 exact extract review behavior remains unchanged |

---

## 10. Behavior Preservation

v3.5 did not alter:

```txt
v3.4 exact extract review behavior
v3.3 source pack validation behavior
v3.2 source pack population behavior
v3.1 reviewed manifest behavior
v3.0 real source acquisition behavior
v2.9 real source ingestion behavior
historical reports
```

Preservation evidence:

```txt
test_existing_v3_4_behavior_preserved
```

Result:

```txt
passed
```

---

## 11. Blocked Claims

The campaign explicitly blocks:

```txt
Priority exact fill validates PHI_GRADIENT.
Unresolved priority records count as source support.
Availability of a source URL counts as exact source text.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
```

Allowed statement:

```txt
Priority exact fill was attempted under source-text controls.
```

---

## 12. Next Gate

Current next action:

```txt
Manually acquire local source text for the five priority sources, then rerun exact fill.
```

The next validation gate should not run as a source-pressure upgrade until at least one priority record has:

```txt
SOURCE_TEXT_AVAILABLE_LOCAL
known location_type
non-empty location_value
at least one exact content field
validation_ready = true
```

---

## 13. Final Assessment

v3.5 correctly converted the priority-source list into a measurable exact-fill queue.

It did not create false support.

The useful result is the explicit unresolved boundary:

```txt
Five priority sources are selected, but all require manually available local source text before exact extraction.
```

Final discipline note:

```txt
The smallest useful exact extract is worth more than a large decorative bibliography.
```
