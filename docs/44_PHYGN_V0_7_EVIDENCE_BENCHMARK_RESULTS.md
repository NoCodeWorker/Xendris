# Phygn v0.7 Evidence Benchmark Results

Date: 2026-06-29

Source prompt:

```txt
docs/43_PHYGN_CODEX_V0_7_EVIDENCE_BENCHMARK_PROMPT.md
```

Supporting specs:

```txt
docs/39_PHYGN_V0_7_EVIDENCE_INGESTION_AND_BENCHMARK_GROUNDING.md
docs/40_PHYGN_RAG_FOUNDATIONAL_SOURCES_EXECUTION_PLAN.md
docs/41_PHYGN_BENCHMARK_DATA_PROTOCOL.md
docs/42_PHYGN_SOURCE_BACKED_MODEL_COMPARISON_PROTOCOL.md
```

## 1. Completion Status

Status: **COMPLETE UNDER THE v0.7 PROMPT ACCEPTANCE CRITERIA**

Implemented:

- Evidence records and audit results.
- Source requirements and source-ingestion execution scaffolding.
- Benchmark dataset protocol.
- Benchmark readiness classifier.
- Benchmark gain permission labels.
- Source-backed model spec.
- Source-backed comparison readiness evaluator.
- Reports for RAG, benchmarks and source-backed comparison readiness.
- Tests for all required v0.7 behaviors.

Important limitation:

```txt
No source ingestion is claimed.
No physical decoherence prediction is claimed.
No experimental evidence is claimed.
No Frontera C validation is claimed.
SyntheticGain is not PredictiveGain.
```

## 2. Implemented Modules

### Evidence

```txt
phyng/evidence/__init__.py
phyng/evidence/schemas.py
phyng/evidence/source_requirements.py
phyng/evidence/ingestion_plan.py
phyng/evidence/evidence_audit.py
phyng/evidence/report.py
```

Implemented objects:

- `SourceRequirement`
- `SourceIngestionResult`
- `EvidenceRecord`
- `EvidenceAuditResult`

### Benchmarks

```txt
phyng/benchmarks/__init__.py
phyng/benchmarks/schemas.py
phyng/benchmarks/readiness.py
phyng/benchmarks/registry.py
phyng/benchmarks/report.py
```

Implemented objects:

- `BenchmarkDataset`
- `BenchmarkReadinessResult`
- `classify_benchmark_readiness(...)`

### Source-Backed Model Comparison

```txt
phyng/model_comparison/source_backed.py
```

Implemented objects:

- `SourceBackedModelSpec`
- `SourceBackedComparisonReadiness`
- `evaluate_source_backed_comparison_readiness(...)`
- `generate_source_backed_readiness_report(...)`

### CAMPAIGN-002 Evidence Upgrade

```txt
phyng/campaigns/campaign_002_evidence_upgrade.py
```

Implemented objects:

- `Campaign002EvidenceUpgradeResult`
- `default_synthetic_visibility_benchmark(...)`
- `run_campaign_002_evidence_upgrade(...)`

## 3. Source Requirements

Generated default requirements:

| Requirement | Topic | Status |
|---|---|---|
| `REQ-SRC-001` | Reduced Compton wavelength | `REQUIRED` |
| `REQ-SRC-002` | Gravitational radius / Schwarzschild radius | `REQUIRED` |
| `REQ-SRC-003` | Planck scale | `REQUIRED` |
| `REQ-SRC-004` | Compton-Schwarzschild related work | `REQUIRED` |
| `REQ-SRC-005` | Mesoscopic matter-wave interferometry | `REQUIRED` |
| `REQ-SRC-006` | Environmental decoherence models | `REQUIRED` |
| `REQ-SRC-007` | Experimental visibility thresholds | `REQUIRED` |
| `REQ-SRC-008` | Benchmark or data source | `REQUIRED` |

No fake metadata rule:

```txt
Missing source -> SourceRequirement + ResearchTask.
Missing source does not create SourceRecord.
Unknown source_id is blocked as SOURCE_NOT_FOUND.
```

## 4. Benchmark Protocol

Supported provenance types:

```txt
PLACEHOLDER
SYNTHETIC
SIMULATED
LITERATURE_EXTRACTED
EXPERIMENTAL
```

Permission rules:

| Provenance | Gain Permission |
|---|---|
| `PLACEHOLDER` | no gain |
| `SYNTHETIC` | `SyntheticGain` only |
| `SIMULATED` | `SimulatedGain` only |
| `LITERATURE_EXTRACTED` | limited `PredictiveGainCandidate` if extraction is valid |
| `EXPERIMENTAL` | `PredictiveGain` only if source and uncertainty are valid |

Default generated benchmark:

```txt
dataset_id = BENCH-CAMPAIGN-002-SYNTH-VISIBILITY-001
provenance_type = SYNTHETIC
readiness_status = SYNTHETIC_READY
gain_label = SyntheticGain
can_compute_gain = True
```

Blocked interpretation:

```txt
SyntheticGain cannot become physical PredictiveGain.
```

## 5. Source-Backed Readiness Result

Generated readiness:

```txt
comparison_id = CAMPAIGN-002-source-backed-readiness
baseline_status = TOY_INTERNAL
candidate_status = HYPOTHETICAL_CANDIDATE
benchmark_status = SYNTHETIC_READY
can_compute_gain = True
gain_label = SyntheticGain
can_claim_physical_prediction = False
max_claim_level = 3
```

Missing requirements:

```txt
source-backed baseline model
direct candidate support for physical prediction
```

Blocked overclaims:

```txt
Phygn predicts decoherence.
Phygn validates Frontera C.
SyntheticGain proves physical gain.
```

## 6. Generated Reports

Generated artifacts:

```txt
reports/rag/source_requirements.md
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
reports/rag/claims_awaiting_sources.md
reports/rag/claims_unlocked_by_sources.md
reports/benchmarks/benchmark_registry.md
reports/benchmarks/BENCH-CAMPAIGN-002-SYNTH-VISIBILITY-001.md
reports/model_comparison/source_backed_readiness.md
```

Generated benchmark record:

```txt
benchmarks/BENCH-CAMPAIGN-002-SYNTH-VISIBILITY-001.json
```

Generated source requirement research tasks:

```txt
rag/research_tasks/RT-REQ-SRC-001.json
rag/research_tasks/RT-REQ-SRC-002.json
rag/research_tasks/RT-REQ-SRC-003.json
rag/research_tasks/RT-REQ-SRC-004.json
rag/research_tasks/RT-REQ-SRC-005.json
rag/research_tasks/RT-REQ-SRC-006.json
rag/research_tasks/RT-REQ-SRC-007.json
rag/research_tasks/RT-REQ-SRC-008.json
```

## 7. Tests

Latest verification:

```txt
pytest -q
143 passed
```

New v0.7 tests:

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

Covered behaviors:

- Missing Compton source creates a source requirement.
- Missing source does not create fake metadata.
- Background support does not unlock hard claims.
- Placeholder benchmark cannot compute gain.
- Synthetic benchmark allows `SyntheticGain` only.
- Experimental benchmark requires source and uncertainty.
- Literature-extracted benchmark requires extraction notes.
- Unsupported baseline blocks physical comparison.
- Source-backed baseline enables limited comparison.
- Hypothetical candidate limits claim level.
- v0.7 reports are generated.

## 8. Final Answer

Yes: `docs/43_PHYGN_CODEX_V0_7_EVIDENCE_BENCHMARK_PROMPT.md` is complete under its acceptance criteria.

The result is:

```txt
Phygn v0.7 now has an evidence and benchmark grounding layer.
Source requirements are explicit.
Missing sources create requirements and research tasks, not fake SourceRecords.
Benchmark datasets are classified by provenance.
Synthetic data can compute SyntheticGain only.
CAMPAIGN-002 can now carry a labelled synthetic benchmark.
The source-backed readiness evaluator still blocks physical prediction because the baseline is TOY_INTERNAL and the candidate is HYPOTHETICAL_CANDIDATE.
No physical decoherence claim is unlocked.
```
