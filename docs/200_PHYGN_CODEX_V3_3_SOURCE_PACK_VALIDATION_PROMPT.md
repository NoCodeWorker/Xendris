# Codex Prompt — Phygn v3.3 Source Pack Extract Validation & Slot Coverage Scoring

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
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
```

Therefore v3.3 starts at:

```txt
196
```

---

# 1. Read first

Read these v3.3 specs:

```txt
docs/196_PHYGN_V3_3_SOURCE_PACK_EXTRACT_VALIDATION_docs/status/GOAL.md
docs/197_PHYGN_EXTRACT_VALIDATION_DECISION_RULES.md
docs/198_PHYGN_SLOT_COVERAGE_SCORING_PROTOCOL.md
docs/199_PHYGN_V3_3_REPORTING_AND_LOOP_FEEDBACK.md
```

Also read:

```txt
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

Inspect:

```txt
phyng/source_pack_population/
phyng/reviewed_manifest/
phyng/real_source_ingestion/
phyng/real_source_acquisition/
phyng/core/
phyng/closed_loop/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
633 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.3:

```txt
Source Pack Extract Validation
Strict Extract Decision Rules
Slot Coverage Scoring
Analogy Rejection
Negative Source Pressure
Benchmark Comparability Scoring
Canonical Final Gate
Closed Loop Feedback
Reports
Tests
```

Do not make physical claims.

---

# 4. Input files

Load:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

If missing, return:

```txt
PHI_GRADIENT_SOURCE_PACK_VALIDATION_BLOCKED
```

Do not invent replacement data.

---

# 5. Extend package

Create or extend:

```txt
phyng/source_pack_validation/
  __init__.py
  schemas.py
  extract_validator.py
  slot_scoring.py
  analogy_rejection.py
  negative_pressure.py
  benchmark_scoring.py
  final_gate.py
  report.py
  campaign.py
```

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_source_pack_validation.py
```

---

# 6. Schemas

Implement:

```txt
SourcePackExtractValidationResult
SourcePackValidatedExtract
SourcePackSlotCoverageRecord
SourcePackSlotCoverageMatrix
SourcePackBenchmarkScoringResult
SourcePackNegativePressureResult
PhiGradientSourcePackValidationGateResult
PhiGradientSourcePackValidationCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 7. Validation behavior

The default seed extracts from v3.2 have:

```txt
manual_review_required=true
initial_validation_status=EXTRACT_CANDIDATE_REQUIRES_REVIEW
exact_quote_available=false
```

Therefore, unless additional exact reviewed fields are present, they must not automatically validate as support.

Expected conservative default:

```txt
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

or:

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
```

with:

```txt
validated_support_count = 0
manual_review_count > 0
```

No seed extract may silently become source support.

---

# 8. Decision rules

Implement exactly:

```txt
manual review required blocks support
analogy-only blocks support
benchmark requires comparable ranges
negative contradiction overrides promotion
source-backed limited requires observable/baseline + gradient component
benchmark-data found requires comparable benchmark extract
physical claims remain blocked
```

---

# 9. Final status priority

```txt
PHI_GRADIENT_SOURCE_PACK_VALIDATION_BLOCKED
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

---

# 10. Reports

Generate:

```txt
reports/source_pack_validation/phi_gradient_extract_validation_v3_3.md
reports/source_pack_validation/phi_gradient_slot_coverage_v3_3.md
reports/source_pack_validation/phi_gradient_analogy_rejections_v3_3.md
reports/source_pack_validation/phi_gradient_negative_pressure_v3_3.md
reports/source_pack_validation/phi_gradient_benchmark_comparability_v3_3.md
reports/source_pack_validation/phi_gradient_final_gate_v3_3.md
reports/source_pack_validation/phi_gradient_loop_feedback_v3_3.md
reports/campaigns/PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3.md
```

Reports must include:

```txt
canonical status section
manual review debt
validated support count
rejected analogy count
negative pressure count
benchmark comparable count
slot coverage
blocked claims
next actions
discipline note
```

---

# 11. Tests

Create:

```txt
tests/test_source_pack_validation_extracts_v3_3.py
tests/test_source_pack_validation_slot_scoring_v3_3.py
tests/test_source_pack_validation_negative_pressure_v3_3.py
tests/test_source_pack_validation_benchmark_scoring_v3_3.py
tests/test_source_pack_validation_reports_v3_3.py
tests/test_phi_gradient_source_pack_validation_campaign_v3_3.py
```

Minimum tests:

```txt
test_seed_extracts_do_not_auto_validate_without_manual_review
test_manual_review_required_blocks_support
test_observable_plus_component_can_allow_source_backed_limited_when_reviewed
test_benchmark_requires_comparable_ranges
test_negative_contradiction_overrides_promotion
test_analogy_only_extract_is_rejected
test_slot_coverage_tracks_manual_review_debt
test_final_gate_keeps_physical_claims_blocked
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v3_2_behavior_preserved
```

---

# 12. Behavior preservation

Do not alter:

```txt
existing v3.2 source pack population behavior
existing v3.1 reviewed manifest behavior
existing v3.0 real source acquisition behavior
existing v2.9 real source ingestion behavior
existing v2.8 source pressure behavior
existing v2.7 phi search outputs
existing v2.6 ablation results
existing v2.5 synthetic execution outputs
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
Seed extract validation proves PHI_GRADIENT.
Manual-review extract counts as support.
Benchmark candidate counts as benchmark data.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
Extract validation was completed.
Some extracts may require manual review.
Validated extracts may provide limited source or benchmark pressure if strict requirements are met.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
seed files are loaded
extract validation works
slot scoring works
negative pressure works
benchmark scoring works
reports generated
loop feedback generated
physical claims blocked
manual-review extracts do not auto-promote
```

Expected test count:

```txt
633 + new v3.3 tests
```

---

# 15. Final discipline

```txt
A candidate source becomes evidence pressure only when its extract survives the gate.
```
