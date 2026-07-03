# Codex Prompt — Phygn v0.8 Source-Backed Baseline

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
v0.7 complete.
Evidence and benchmark grounding layer exists.
Benchmark provenance is classified.
SyntheticGain is not PredictiveGain.
baseline_status = TOY_INTERNAL.
candidate_status = HYPOTHETICAL_CANDIDATE.
benchmark_status = SYNTHETIC_READY.
can_claim_physical_prediction = False.
143 tests passed.
```

Your task is to implement **v0.8: Source-Backed Baseline**.

This is not a frontend task.
This is not a claim expansion task.
This is not a physical prediction task.

Goal:

```txt
convert or prepare the CAMPAIGN-002 baseline from TOY_INTERNAL to SOURCE_BACKED_LIMITED / SOURCE_BACKED_READY if evidence exists,
or explicitly mark BASELINE_REQUIRES_SOURCE if not.
```

---

# 1. Read first

Read:

```txt
docs/44_PHYGN_V0_8_SOURCE_BACKED_BASELINE_docs/status/GOAL.md
docs/45_PHYGN_DECOHERENCE_BASELINE_LITERATURE_INGESTION.md
docs/46_PHYGN_VISIBILITY_DECAY_BASELINE_PROTOCOL.md
docs/47_PHYGN_CAMPAIGN_002_BASELINE_PHYSICALIZATION.md
```

Also read:

```txt
docs/43_PHYGN_CODEX_V0_7_EVIDENCE_BENCHMARK_PROMPT.md
docs/41_PHYGN_BENCHMARK_DATA_PROTOCOL.md
docs/42_PHYGN_SOURCE_BACKED_MODEL_COMPARISON_PROTOCOL.md
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
baseline source requirements
visibility decay baseline spec
baseline readiness classifier
baseline source support matrix
CAMPAIGN-002 baseline physicalization
reports
tests
```

Do not fake source ingestion.

---

# 4. New / extended modules

Create:

```txt
phyng/baselines/
  __init__.py
  schemas.py
  visibility_decay.py
  readiness.py
  source_support.py
  report.py
```

Extend:

```txt
phyng/campaigns/campaign_002_baseline_upgrade.py
```

---

# 5. Schemas

Implement:

```txt
BaselineSourceRequirement
VisibilityDecayBaselineSpec
BaselineReadinessResult
BaselineSourceSupport
Campaign002BaselineUpgradeResult
```

---

# 6. Baseline source requirements

Create requirements for:

```txt
visibility decay / coherence loss
environmental decoherence rate
matter-wave interferometry visibility
experimental visibility threshold
```

If no source exists:

```txt
BASELINE_REQUIRES_SOURCE
```

and create ResearchTasks.

Do not create SourceRecord unless actual source exists.

---

# 7. Visibility decay baseline

Implement:

```txt
V_base(t)=exp(-Gamma_env t)
```

But classify it according to evidence:

```txt
TOY_INTERNAL
BACKGROUND_SUPPORTED
SOURCE_BACKED_LIMITED
SOURCE_BACKED_READY
CONTRADICTED
```

Parameter status:

```txt
PARAMETER_TOY
PARAMETER_SOURCE_BACKED
PARAMETER_FITTED
PARAMETER_EXPERIMENTAL
```

---

# 8. Baseline readiness

Implement:

```python
classify_baseline_readiness(...)
```

Rules:

```txt
no source → TOY_INTERNAL or BASELINE_REQUIRES_SOURCE
background only → BACKGROUND_SUPPORTED but not ready
formula + observable direct support → SOURCE_BACKED_LIMITED
formula + observable + parameter mapping + assumptions → SOURCE_BACKED_READY
contradiction → CONTRADICTED
```

---

# 9. CAMPAIGN-002 baseline physicalization

Implement:

```python
run_campaign_002_baseline_physicalization(...)
```

It must:

```txt
read current CAMPAIGN-002 state if available
evaluate baseline readiness
create source requirements if needed
generate report
keep candidate prediction blocked
```

---

# 10. Reports

Generate:

```txt
reports/rag/baseline_source_requirements.md
reports/rag/baseline_literature_ingestion.md
reports/rag/baseline_source_support_matrix.md
reports/model_comparison/visibility_decay_baseline_readiness.md
reports/campaigns/CAMPAIGN-002_baseline_physicalization.md
```

---

# 11. Tests

Add:

```txt
tests/test_baseline_literature_requirements.py
tests/test_baseline_source_support_matrix.py
tests/test_visibility_decay_baseline.py
tests/test_baseline_readiness.py
tests/test_campaign_002_baseline_physicalization.py
```

Minimum tests:

```txt
test_missing_visibility_source_creates_requirement
test_baseline_without_sources_is_toy_internal_or_requires_source
test_arbitrary_gamma_is_parameter_toy
test_background_only_does_not_source_back_baseline
test_source_backed_formula_allows_limited_baseline
test_missing_assumptions_blocks_ready_status
test_baseline_upgrade_does_not_unlock_candidate_prediction
test_source_backed_baseline_updates_readiness_report
```

---

# 12. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
The source-backed baseline validates Frontera C.
The source-backed baseline validates the boundary-aware candidate.
SyntheticGain proves physical gain.
```

Allowed:

```txt
Phygn can use a source-backed limited baseline if evidence exists.
The candidate remains hypothetical.
Physical prediction remains blocked.
The baseline has been upgraded, not the theory.
```

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline requirements generated
visibility baseline spec exists
baseline readiness classifier works
CAMPAIGN-002 baseline physicalization runs
reports generated
missing sources create requirements
no fake source ingestion occurs
candidate physical prediction remains blocked
```

---

# 14. Final discipline

```txt
A physical baseline is not a victory.
It is a worthy opponent.
```
