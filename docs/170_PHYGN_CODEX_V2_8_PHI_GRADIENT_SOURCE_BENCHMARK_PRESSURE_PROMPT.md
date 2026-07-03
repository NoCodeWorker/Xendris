# Codex Prompt — Phygn v2.8 PHI_GRADIENT Source-Support & Benchmark-Data Pressure

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
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

Therefore v2.8 starts at:

```txt
166
```

---

# 1. Read first

Read these v2.8 specs:

```txt
docs/166_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_docs/status/GOAL.md
docs/167_PHYGN_PHI_GRADIENT_SOURCE_SLOT_REGISTRY.md
docs/168_PHYGN_SOURCE_SUPPORT_VS_ANALOGY_GATE.md
docs/169_PHYGN_PHI_GRADIENT_BENCHMARK_DATA_PRESSURE_PROTOCOL.md
```

Also read:

```txt
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/synthetic_benchmark_design/
phyng/source_grounding/
phyng/evidence/
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
566 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.8:

```txt
PHI_GRADIENT Source-Support Pressure
Benchmark-Data Pressure
Evidence Slot Registry
Source Support vs Analogy Gate
Negative Source Handling
Benchmark Comparability Records
Alpha Constraint Requirement
Canonical Reports
Closed Loop Feedback
Tests
```

Do not authorize physical claims unless explicit external evidence supports only a limited source/benchmark status.

---

# 4. New package

Create if not already present:

```txt
phyng/source_pressure/
  __init__.py
  schemas.py
  slots.py
  source_gate.py
  benchmark_pressure.py
  phi_gradient_audit.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/phi_gradient_source_benchmark_pressure.py
```

---

# 5. Schemas

Implement:

```txt
SourceEvidenceSlot
SourceCandidate
SourceSupportAssessment
BenchmarkPressureRecord
PhiGradientSourcePressureResult
PhiGradientBenchmarkPressureResult
PhiGradientSourceBenchmarkCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. Slot registry

Implement registry for:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS
SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS
SLOT_4_GRADIENT_TRANSITION_OPERATORS
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

---

# 7. Source gate

Implement:

```python
assess_source_support(source: SourceCandidate) -> SourceSupportAssessment
```

It must distinguish:

```txt
SOURCE_REJECTED_DECORATIVE_ANALOGY
SOURCE_ANALOGY_ONLY
SOURCE_SUPPORTS_OBSERVABLE
SOURCE_SUPPORTS_BASELINE
SOURCE_SUPPORTS_COMPONENT
SOURCE_CONSTRAINS_PARAMETER
SOURCE_PROVIDES_BENCHMARK_DATA
SOURCE_CONTRADICTS_CANDIDATE
```

Block upgrades from vague similarity.

---

# 8. PHI_GRADIENT audit

Implement:

```python
run_phi_gradient_source_pressure_audit(sources: list[SourceCandidate]) -> PhiGradientSourcePressureResult
```

Rules:

```txt
source-backed limited requires observable/baseline support
and gradient/transition component support
and no unaddressed contradiction
analogy-only sources do not count
negative sources must be recorded
missing alpha constraints must remain blocked
```

---

# 9. Benchmark pressure

Implement:

```python
assess_benchmark_pressure(record: BenchmarkPressureRecord) -> PhiGradientBenchmarkPressureResult
```

Benchmark must include:

```txt
observable
mass range
length/separation range
time range
visibility or decoherence measure
environmental baseline
citation or local path
limitations
```

Classifications:

```txt
BENCHMARK_REJECTED_NOT_COMPARABLE
BENCHMARK_BASELINE_ONLY
BENCHMARK_CONSTRAINS_ALPHA
BENCHMARK_SUPPORTS_OBSERVABLE_ONLY
BENCHMARK_SUPPORTS_COMPONENT_LIMITED
BENCHMARK_SUPPORTS_CANDIDATE_LIMITED
BENCHMARK_CONTRADICTS_CANDIDATE
```

---

# 10. Canonical statuses

Add if needed:

```txt
PHI_GRADIENT_SOURCE_UNSUPPORTED
PHI_GRADIENT_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_BACKED_LIMITED
PHI_GRADIENT_BENCHMARK_DATA_FOUND
PHI_GRADIENT_CONTRADICTED_BY_SOURCE
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_AUDIT_BLOCKED
```

Mapping:

```txt
SOURCE_BACKED_LIMITED:
  CLAIM_LIMITED_ALLOWED
  SOURCE_BACKED_LIMITED
  SOURCE_LIMITED
  blocked: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA

BENCHMARK_DATA_FOUND:
  CLAIM_LIMITED_ALLOWED
  BENCHMARK_SUPPORTED
  BENCHMARK
  blocked: MISSING_EXPERIMENTAL_DATA

ANALOGY_ONLY:
  REVIEW_REQUIRED or CLAIM_BLOCKED
  HEURISTIC_ONLY/SYNTHETIC_ONLY
  blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK

CONTRADICTED:
  CLAIM_BLOCKED
  NO_EVIDENCE or SYNTHETIC_ONLY
  blocked: CONTRADICTION
```

---

# 11. Campaign seed data

Because real literature ingestion may not be available yet, include deterministic test fixtures:

```txt
source_analogy_only_fixture
source_observable_support_fixture
source_gradient_component_support_fixture
source_parameter_constraint_fixture
source_negative_conflict_fixture
benchmark_baseline_only_fixture
benchmark_candidate_limited_fixture
benchmark_not_comparable_fixture
```

The campaign should report fixture-based audit status and explicitly mark that real literature acquisition is still required unless real sources are provided.

---

# 12. Reports

Generate:

```txt
reports/source_pressure/phi_gradient_source_slots_v2_8.md
reports/source_pressure/phi_gradient_source_support_gate_v2_8.md
reports/source_pressure/phi_gradient_benchmark_pressure_v2_8.md
reports/source_pressure/phi_gradient_negative_sources_v2_8.md
reports/source_pressure/phi_gradient_source_benchmark_loop_feedback_v2_8.md
reports/campaigns/PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8.md
```

Reports must include:

```txt
canonical status section
source slots
support vs analogy assessment
benchmark comparability
negative source handling
blocked claims
next actions
discipline note
```

---

# 13. Tests

Create:

```txt
tests/test_phi_gradient_source_slots_v2_8.py
tests/test_source_support_vs_analogy_gate_v2_8.py
tests/test_phi_gradient_source_pressure_audit_v2_8.py
tests/test_phi_gradient_benchmark_pressure_v2_8.py
tests/test_phi_gradient_source_pressure_reports_v2_8.py
tests/test_phi_gradient_source_benchmark_campaign_v2_8.py
```

Minimum tests:

```txt
test_source_slots_exist
test_analogy_only_source_does_not_count_as_support
test_source_support_requires_component_or_observable
test_negative_source_blocks_unaddressed_upgrade
test_alpha_constraint_missing_remains_blocked
test_benchmark_requires_comparable_observable
test_benchmark_not_comparable_is_rejected
test_source_backed_limited_requires_minimum_slots
test_benchmark_data_found_requires_comparable_record
test_phi_gradient_physical_claims_remain_blocked
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v2_7_behavior_preserved
```

---

# 14. Behavior preservation

Do not alter:

```txt
existing v2.7 phi search outputs
existing v2.6 ablation results
existing v2.5 synthetic execution outputs
existing v2.4 closed loop outputs
existing v2.3 benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing business/candidate/copilot gates
historical reports
```

---

# 15. Do not overclaim

Do not write:

```txt
PHI_GRADIENT is physically validated.
PHI_GRADIENT proves Frontera C.
A source analogy validates the candidate.
Benchmark pressure confirms the real effect.
```

Allowed:

```txt
PHI_GRADIENT received source/benchmark pressure.
Evidence is limited, analogy-only, contradictory, or benchmark-supported according to the gate.
Physical claims remain blocked unless explicit external evidence supports only limited claims.
```

---

# 16. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
source slots exist
source gate works
analogy-only is blocked
negative sources are recorded
benchmark comparability works
reports generated
loop feedback generated
physical claims remain blocked
```

Expected test count:

```txt
566 + new v2.8 tests
```

---

# 17. Final discipline

```txt
A source is useful when it can hurt the candidate.
A decorative analogy is just another way to overfit language.
```
