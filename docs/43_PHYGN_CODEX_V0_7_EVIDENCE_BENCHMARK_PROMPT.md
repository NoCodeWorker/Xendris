# Codex Prompt — Phygn v0.7 Evidence Ingestion & Benchmark Grounding

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v0.6 complete.
Model comparison engine exists.
CAMPAIGN-002 runs in toy mode.
Gain_C is undefined without y_true.
Detectability is classified.
Evidence level = 3.
Physical decoherence claims remain blocked.
125 tests passed.
```

Your task is to implement **v0.7: Evidence Ingestion & Benchmark Grounding**.

This is not a frontend task.
This is not a styling task.
This is not a claim expansion task.

The goal is to move from:

```txt
MODEL_DELTA_ONLY
```

toward:

```txt
SOURCE_BACKED_MODEL_COMPARISON
```

without overclaiming.

---

# 1. Read first

Read:

```txt
docs/38_PHYGN_V0_7_EVIDENCE_INGESTION_AND_BENCHMARK_GROUNDING.md
docs/39_PHYGN_RAG_FOUNDATIONAL_SOURCES_EXECUTION_PLAN.md
docs/40_PHYGN_BENCHMARK_DATA_PROTOCOL.md
docs/41_PHYGN_SOURCE_BACKED_MODEL_COMPARISON_PROTOCOL.md
```

Also read:

```txt
docs/32_PHYGN_V0_6_HISTORIC_GOAL_MODEL_COMPARISON.md
docs/33_PHYGN_CAMPAIGN_002_DECOHERENCE_MODEL_COMPARISON.md
docs/34_PHYGN_RAG_SOURCE_INGESTION_CAMPAIGN_V0_6.md
docs/35_PHYGN_MODEL_COMPARISON_ENGINE_ARCHITECTURE.md
docs/36_PHYGN_NON_INFLATION_CLAIM_PROTOCOL_V0_6.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement:

```txt
evidence records
source requirements
source ingestion execution scaffolding
benchmark dataset protocol
benchmark readiness classifier
source-backed model spec
source-backed comparison readiness
reports
tests
```

Do not fake source ingestion.

---

# 4. New modules

Create:

```txt
phyng/evidence/
  __init__.py
  schemas.py
  source_requirements.py
  ingestion_plan.py
  evidence_audit.py
  report.py

phyng/benchmarks/
  __init__.py
  schemas.py
  readiness.py
  registry.py
  report.py
```

Extend:

```txt
phyng/model_comparison/
  source_backed.py
```

Optional:

```txt
phyng/campaigns/campaign_002_evidence_upgrade.py
```

---

# 5. Evidence schemas

Implement:

```txt
SourceRequirement
SourceIngestionResult
EvidenceRecord
EvidenceAuditResult
```

Rules:

```txt
no fake metadata
no source_id unless actual source exists
missing source creates requirement + research task
```

---

# 6. Benchmark schemas

Implement:

```txt
BenchmarkDataset
BenchmarkReadinessResult
```

Provenance types:

```txt
PLACEHOLDER
SYNTHETIC
SIMULATED
LITERATURE_EXTRACTED
EXPERIMENTAL
```

Gain permissions:

```txt
PLACEHOLDER → no gain
SYNTHETIC → SyntheticGain only
SIMULATED → SimulatedGain only
LITERATURE_EXTRACTED → limited PredictiveGain candidate
EXPERIMENTAL → PredictiveGain allowed if valid
```

---

# 7. Source-backed model schemas

Implement:

```txt
SourceBackedModelSpec
SourceBackedComparisonReadiness
```

Statuses:

```txt
UNSUPPORTED
TOY_INTERNAL
BACKGROUND_SUPPORTED
DIRECTLY_SUPPORTED
CONTRADICTED
REQUIRES_SOURCE
```

---

# 8. Benchmark readiness

Implement:

```python
classify_benchmark_readiness(dataset: BenchmarkDataset) -> BenchmarkReadinessResult
```

Rules:

```txt
PLACEHOLDER -> can_compute_gain=False
SYNTHETIC -> can_compute_gain=True, gain_label=SyntheticGain
EXPERIMENTAL -> requires source_ids and uncertainty
LITERATURE_EXTRACTED -> requires source_ids and extraction notes
```

---

# 9. Source requirements

Create default requirements for:

```txt
Reduced Compton wavelength
Gravitational/Schwarzschild radius
Planck scale
Compton-Schwarzschild related work
Mesoscopic matter-wave interferometry
Environmental decoherence models
Experimental visibility thresholds
Benchmark/y_true data
```

Generate:

```txt
reports/rag/source_requirements.md
```

---

# 10. Source-backed comparison readiness

Implement:

```python
evaluate_source_backed_comparison_readiness(...)
```

It must return:

```txt
baseline_status
candidate_status
benchmark_status
can_compute_gain
can_claim_physical_prediction
max_claim_level
missing_requirements
```

---

# 11. Reports

Generate:

```txt
reports/rag/source_requirements.md
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
reports/rag/claims_awaiting_sources.md
reports/rag/claims_unlocked_by_sources.md
reports/benchmarks/benchmark_registry.md
reports/model_comparison/source_backed_readiness.md
```

---

# 12. Tests

Add:

```txt
tests/test_source_requirements.py
tests/test_source_ingestion_execution_plan.py
tests/test_evidence_audit.py
tests/test_benchmark_dataset.py
tests/test_benchmark_readiness.py
tests/test_benchmark_gain_permissions.py
tests/test_source_backed_model_spec.py
tests/test_source_backed_comparison_readiness.py
```

Minimum cases:

```txt
test_source_requirement_created_for_missing_compton_source
test_no_fake_metadata_allowed
test_background_support_does_not_unlock_hard_claim
test_placeholder_cannot_compute_gain
test_synthetic_allows_synthetic_gain_only
test_experimental_requires_source
test_experimental_requires_uncertainty
test_literature_requires_extraction_notes
test_unsupported_baseline_blocks_physical_comparison
test_source_backed_baseline_allows_limited_comparison
test_candidate_hypothesis_limits_claim_level
test_reports_generated
```

---

# 13. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
Phygn validates Frontera C.
Phygn has experimental evidence.
SyntheticGain proves physical gain.
```

Allowed:

```txt
Phygn can compute SyntheticGain on synthetic benchmark data.
Phygn requires source-backed baseline before physical interpretation.
Phygn requires experimental benchmark before PredictiveGain.
Phygn keeps physical claims blocked until evidence exists.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
source requirements generated
benchmark protocol implemented
benchmark readiness works
source-backed comparison readiness works
reports generated
placeholder benchmark cannot compute gain
synthetic benchmark cannot become physical PredictiveGain
unsupported baseline blocks physical comparison
no physical prediction is claimed
```

---

# 15. Final discipline

```txt
The courtroom exists.
Now add admissible evidence.
```
