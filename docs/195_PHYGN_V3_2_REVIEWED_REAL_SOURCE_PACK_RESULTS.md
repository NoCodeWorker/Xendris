# Phygn v3.2 - PHI_GRADIENT Reviewed Real Source Pack Population Results

Date: 2026-06-30

Source prompt:

```txt
docs/194_PHYGN_CODEX_V3_2_REVIEWED_REAL_SOURCE_PACK_PROMPT.md
```

Supporting specs:

```txt
docs/190_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_POPULATION_docs/status/GOAL.md
docs/191_PHYGN_REVIEWED_SOURCE_PACK_SEED_MANIFEST_SPEC.md
docs/192_PHYGN_REVIEWED_EXTRACT_PACK_POPULATION_PROTOCOL.md
docs/193_PHYGN_SOURCE_PACK_VALIDATION_AND_NEXT_GATE.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v3.2 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v3.2 populated a reviewed real source candidate pack for PHI_GRADIENT.

The pack is a seed queue for review and validation.

It is not validated source support.

No seed source was treated as evidence.

No seed extract was treated as validated support.

No benchmark candidate was treated as benchmark support.

No physical validation claim was unlocked.

Final campaign status:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

Final validation:

```txt
pytest -q
633 passed in 43.90s
```

Baseline before v3.2:

```txt
620 passed
```

Net result:

```txt
620 baseline tests + 13 v3.2 tests = 633 passing tests
```

---

## 2. Implemented Package

Created:

```txt
phyng/source_pack_population/
  __init__.py
  schemas.py
  seed_pack.py
  validation.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_source_pack_population.py
```

Entrypoint:

```python
run_phi_gradient_source_pack_population_campaign(root: str | Path = ".")
```

---

## 3. Seed Files Generated

Created:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

Seed manifest result:

| Metric | Result |
|---|---:|
| Manifest entries | 13 |
| Traceable entries | 13 |
| Valid slot-targeted entries | 13 |
| Benchmark candidate sources | 5 |
| Negative candidate sources | 3 |

Seed extract pack result:

| Metric | Result |
|---|---:|
| Extract candidates | 8 |
| Manual-review extracts | 8 |
| Validated support extracts | 0 |

All source entries are marked:

```txt
evidence_status=CANDIDATE_NOT_VALIDATED
```

All extract entries are marked:

```txt
initial_validation_status=EXTRACT_CANDIDATE_REQUIRES_REVIEW
manual_review_required=true
```

---

## 4. Source Pack Composition

The seed pack includes candidate pressure for:

```txt
decoherence baseline / visibility decay
matter-wave interferometry benchmarks
environmental decoherence models
gravitational decoherence / collapse models
gradient or transition operators
scale/log-coordinate formulations
alpha-like parameter constraints
negative/conflicting sources
```

Included risk flags:

```txt
RISK_ANALOGY_ONLY
RISK_BENCHMARK_NOT_COMPARABLE
RISK_NO_ALPHA_CONSTRAINT
RISK_REVIEW_REQUIRED
RISK_SOURCE_MAY_BE_NEGATIVE
RISK_OBSERVABLE_MISMATCH
RISK_NOT_DIRECTLY_PHI_GRADIENT
```

Interpretation:

```txt
The source pack makes uncertainty searchable and reviewable. It does not settle the claim.
```

---

## 5. Validation Results

Implemented in:

```txt
phyng/source_pack_population/validation.py
```

Validation checks:

```txt
all seed entries have DOI/arXiv/URL/local_path
all seed entries target at least one valid PHI_GRADIENT slot
all seed entries remain CANDIDATE_NOT_VALIDATED
all seed extracts require manual review
all seed extracts start as EXTRACT_CANDIDATE_REQUIRES_REVIEW
negative source candidates are present
benchmark candidate sources are present
```

Validation status:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

Canonical interpretation:

```txt
permission=REVIEW_REQUIRED
evidence_level=SYNTHETIC_ONLY
support_level=SYNTHETIC
blocked_reasons=MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

---

## 6. Reports Generated

The v3.2 campaign generated:

```txt
reports/source_pack_population/phi_gradient_source_pack_manifest_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_extracts_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_slot_targets_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_risk_flags_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_next_gate_v3_2.md
reports/campaigns/PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2.md
```

This document consolidates the result into:

```txt
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
```

---

## 7. Gate Results

Allowed claim:

```txt
A reviewed source candidate pack was populated.
```

Blocked claims:

```txt
The seed source pack proves PHI_GRADIENT.
A seed extract is validated support.
A candidate benchmark is benchmark support.
PHI_GRADIENT has real source support.
PHI_GRADIENT has benchmark support.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
```

Next gate:

```txt
v3.3 - Source Pack Extract Validation & Slot Coverage Scoring
```

v3.3 must:

```txt
load v3.2 seed manifest
load v3.2 seed extract pack
validate extracts with v2.9 rules
score slot coverage
identify analogy-only sources
identify negative pressure
determine whether limited source-backed status is allowed
determine whether benchmark-data status is allowed
keep physical claims blocked
```

---

## 8. New Tests

Created:

```txt
tests/test_source_pack_population_manifest_v3_2.py
tests/test_source_pack_population_extracts_v3_2.py
tests/test_source_pack_population_slots_v3_2.py
tests/test_source_pack_population_reports_v3_2.py
tests/test_phi_gradient_source_pack_population_campaign_v3_2.py
```

Focused v3.2 verification:

```txt
pytest -q tests/test_source_pack_population_manifest_v3_2.py tests/test_source_pack_population_extracts_v3_2.py tests/test_source_pack_population_slots_v3_2.py tests/test_source_pack_population_reports_v3_2.py tests/test_phi_gradient_source_pack_population_campaign_v3_2.py
13 passed in 0.75s
```

Full-suite verification:

```txt
pytest -q
633 passed in 43.90s
```

---

## 9. Behavior Preservation

v3.2 explicitly preserved v3.1 behavior:

```txt
test_existing_v3_1_behavior_preserved
```

Result:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
validated_extract_count=0
```

Historical behavior preservation also remains covered by the existing suite for:

```txt
v3.0 real source acquisition
v2.9 real source ingestion
v2.8 source pressure
v2.7 phi search outputs
v2.6 ablation outputs
v2.5 synthetic execution
```

---

## 10. Source Traceability Note

Seed entries use traceable identifiers such as arXiv IDs and URLs.

The entries are still review candidates only.

They must not be cited as support until v3.3 validates exact extracts against the source text.

---

## 11. Final Assessment

v3.2 changed the system state from an empty reviewed-manifest template to a populated source-pressure queue:

```txt
empty reviewed manifest -> traceable seed source pack -> manual-review extract candidates -> next validation gate
```

The correct final status is:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

The next meaningful move is not claim promotion.

The next meaningful move is:

```txt
Run v3.3 source-pack extract validation and slot coverage scoring.
```

Final discipline note:

```txt
A source pack can only become positive by surviving validation.
Until then, it is organized pressure waiting to happen.
```
