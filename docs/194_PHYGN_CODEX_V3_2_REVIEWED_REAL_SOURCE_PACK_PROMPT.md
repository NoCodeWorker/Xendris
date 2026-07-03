# Codex Prompt — Phygn v3.2 PHI_GRADIENT Reviewed Real Source Pack Population

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
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
```

Therefore v3.2 starts at:

```txt
190
```

---

# 1. Read first

Read these v3.2 specs:

```txt
docs/190_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_POPULATION_docs/status/GOAL.md
docs/191_PHYGN_REVIEWED_SOURCE_PACK_SEED_MANIFEST_SPEC.md
docs/192_PHYGN_REVIEWED_EXTRACT_PACK_POPULATION_PROTOCOL.md
docs/193_PHYGN_SOURCE_PACK_VALIDATION_AND_NEXT_GATE.md
```

Also read:

```txt
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

Inspect:

```txt
phyng/reviewed_manifest/
phyng/real_source_acquisition/
phyng/real_source_ingestion/
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
620 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.2:

```txt
Reviewed Real Source Pack Population
Seed Manifest Generation
Seed Extract Pack Generation
Candidate Source Traceability
Slot Targeting
Risk Flags
Negative Source Candidates
Benchmark Candidate Sources
Canonical Reports
Closed Loop Feedback
Tests
```

Do not treat seed sources as validated support.

---

# 4. Files to create

Create:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

Also generate reports:

```txt
reports/source_pack_population/phi_gradient_source_pack_manifest_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_extracts_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_slot_targets_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_risk_flags_v3_2.md
reports/source_pack_population/phi_gradient_source_pack_next_gate_v3_2.md
reports/campaigns/PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2.md
```

---

# 5. Seed pack policy

All seed sources must be marked:

```txt
evidence_status: CANDIDATE_NOT_VALIDATED
```

All seed extracts must be marked:

```txt
initial_validation_status: EXTRACT_CANDIDATE_REQUIRES_REVIEW
manual_review_required: true
```

No v3.2 source may unlock:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

---

# 6. Suggested seed sources

Use the seed manifest included with this pack if available:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
```

It includes candidate sources for:

```txt
collisional decoherence observed in matter-wave interferometry
thermal-emission decoherence of matter waves
collapse-model tests with matter-wave interferometry
MAQRO macroscopic quantum resonator proposals
quantum-classical hypothesis tests
decoherence overview / baseline theory
air-molecule scattering decoherence rates
motional dynamical decoupling with gradient-related interferometry
dielectric particle thermal decoherence
gravitational decoherence overview or tests
```

Review every entry before treating it as source pressure.

---

# 7. Campaign final status

Expected v3.2 status:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

Canonical interpretation:

```txt
permission: REVIEW_REQUIRED
evidence_level: SYNTHETIC_ONLY
support_level: SYNTHETIC
blocked_reasons:
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
  MISSING_EXPERIMENTAL_DATA
```

---

# 8. Tests

Create:

```txt
tests/test_source_pack_population_manifest_v3_2.py
tests/test_source_pack_population_extracts_v3_2.py
tests/test_source_pack_population_slots_v3_2.py
tests/test_source_pack_population_reports_v3_2.py
tests/test_phi_gradient_source_pack_population_campaign_v3_2.py
```

Minimum tests:

```txt
test_seed_manifest_exists
test_seed_extract_pack_exists
test_seed_manifest_entries_have_traceable_identifiers
test_seed_manifest_entries_target_valid_slots
test_seed_sources_are_not_validated_support
test_seed_extracts_require_manual_review
test_negative_source_candidates_present
test_benchmark_candidate_sources_present
test_source_pack_status_is_review_required
test_physical_claims_remain_blocked
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v3_1_behavior_preserved
```

---

# 9. Behavior preservation

Do not alter:

```txt
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

# 10. Do not overclaim

Do not write:

```txt
The seed source pack proves PHI_GRADIENT.
A seed extract is validated support.
A candidate benchmark is benchmark support.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
A reviewed source candidate pack was populated.
The pack is ready for validation.
Physical claims remain blocked.
```

---

# 11. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
seed manifest exists
seed extract pack exists
all entries are traceable
all entries target valid slots
seed entries do not count as support
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
620 + new v3.2 tests
```

---

# 12. Final discipline

```txt
A source pack can only become positive by surviving validation.
Until then, it is organized pressure waiting to happen.
```
