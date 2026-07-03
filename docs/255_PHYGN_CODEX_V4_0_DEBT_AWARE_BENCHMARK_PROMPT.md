# Codex Prompt — Phygn v4.0 Debt-Aware Benchmark Construction & SLOT_4 Resolution Plan

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
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
```

Therefore v4.0 starts at:

```txt
251
```

---

# 1. Read first

Read these v4.0 specs:

```txt
docs/251_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_docs/status/GOAL.md
docs/252_PHYGN_V4_0_BENCHMARK_DATASET_SCHEMA.md
docs/253_PHYGN_V4_0_SLOT4_DEBT_OBJECT_AND_RESOLUTION_PLAN.md
docs/254_PHYGN_V4_0_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
docs/238_PHYGN_V3_8_2_SEMANTIC_TRIAGE_RESULTS.md
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
```

Inspect:

```txt
phyng/source_pressure_decision/
phyng/priority_packet_review/
phyng/semantic_triage/
phyng/core/status_mapping.py
```

---

# 2. First action

Run focused prior validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_source_pressure_loader_v3_9.py tests/test_source_pressure_classifier_v3_9.py tests/test_source_pressure_slot_summary_v3_9.py tests/test_source_pressure_benchmark_alignment_v3_9.py tests/test_source_pressure_decision_engine_v3_9.py tests/test_source_pressure_reports_v3_9.py tests/test_phi_gradient_source_pressure_campaign_v3_9.py
```

Expected recent focused result:

```txt
27 passed
```

Full-suite may remain blocked by unrelated NumPy DLL collection errors.

---

# 3. Mission

Implement:

```txt
v4.0 — Debt-Aware Benchmark Construction & SLOT_4 Resolution Plan
```

Create:

```txt
Track A — benchmark dataset from survived source pressure.
Track B — explicit SLOT_4 debt object and resolution plan.
```

Do not validate PHI_GRADIENT.

Do not launder SLOT_4 debt into benchmark claims.

---

# 4. Input files

Load:

```txt
data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json
data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json
data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json
data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/source_hashes_v3_6.json
```

If source-pressure files are missing:

```txt
PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE
```

---

# 5. Create packages

Create:

```txt
phyng/benchmark_construction/
  __init__.py
  schemas.py
  loader.py
  observable_alignment.py
  benchmark_rows.py
  negative_controls.py
  manifest.py
  reports.py
  campaign.py
```

Create:

```txt
phyng/scientific_debt/
  __init__.py
  schemas.py
  debt_registry.py
  slot4_resolution.py
  reports.py
```

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_debt_aware_benchmark.py
```

Entrypoint:

```python
run_phi_gradient_debt_aware_benchmark_campaign(root: str | Path = ".")
```

---

# 6. Track A implementation

Use only extracts and pressure classes that survived v3.9 for:

```txt
baseline decoherence
visibility/coherence observable
benchmark ranges
parameter constraints
limitations
experimental context
```

Generate:

```txt
benchmark rows
observable alignment
negative control plan
dataset manifest
```

Each benchmark row must include:

```txt
gradient_claim_allowed = false
allowed_model_comparison = true only if observable/regime alignment exists
```

---

# 7. Track B implementation

Create debt object:

```txt
DEBT-SLOT4-GRADIENT-COMPONENT-GAP
```

Status:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Create resolution plan with tasks:

```txt
Pedernales manual review
targeted SLOT_4 source acquisition
exact SLOT_4 extraction
v3.8.3-style promotion
v3.9-style source pressure rerun
keep/revise/kill gradient mechanism
```

---

# 8. Output files

Create:

```txt
data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json
data/benchmarks/phi_gradient_observable_alignment_v4_0.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/debts/slot4_resolution_plan_v4_0.json
data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json
```

---

# 9. Reports

Generate:

```txt
reports/benchmark_construction/phi_gradient_benchmark_dataset_manifest_v4_0.md
reports/benchmark_construction/phi_gradient_observable_alignment_v4_0.md
reports/benchmark_construction/phi_gradient_benchmark_rows_v4_0.md
reports/benchmark_construction/phi_gradient_negative_control_plan_v4_0.md
reports/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.md
reports/debts/slot4_resolution_plan_v4_0.md
reports/campaigns/PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0.md
```

---

# 10. Statuses

Add:

```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_PARTIAL
PHI_GRADIENT_SLOT4_DEBT_OPEN_BLOCKING
PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE
PHI_GRADIENT_BENCHMARK_BLOCKED_NO_OBSERVABLE_ALIGNMENT
```

---

# 11. Tests

Create:

```txt
tests/test_debt_aware_benchmark_loader_v4_0.py
tests/test_benchmark_observable_alignment_v4_0.py
tests/test_benchmark_rows_v4_0.py
tests/test_negative_control_plan_v4_0.py
tests/test_scientific_debt_slot4_v4_0.py
tests/test_debt_aware_benchmark_reports_v4_0.py
tests/test_phi_gradient_debt_aware_benchmark_campaign_v4_0.py
```

Minimum tests:

```txt
test_missing_source_pressure_blocks_benchmark
test_observable_alignment_uses_survived_slots_only
test_benchmark_row_blocks_gradient_claim
test_benchmark_row_allows_model_comparison_only_with_observable
test_negative_control_plan_includes_no_slot4_control
test_slot4_debt_created_as_open_blocking
test_slot4_debt_blocks_gradient_claims
test_slot4_debt_does_not_block_benchmark_construction
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_9_behavior_preserved
```

---

# 12. Behavior preservation

Do not alter:

```txt
v3.9 source pressure decision
v3.8.3 priority packet review
v3.8.2 semantic triage
v3.8.1 PDF reader integration
v3.7 PDF extraction
v3.6 source registry
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
Benchmark dataset validates PHI_GRADIENT.
SLOT_4 debt is harmless.
Gradient mechanism is source-backed.
Frontera C is validated.
The invariant has empirical support.
```

Allowed:

```txt
A debt-aware benchmark dataset was constructed.
SLOT_4 debt was formalized and blocks mechanism claims.
Benchmark construction may proceed without gradient claims.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
focused v3.9 tests pass
v4.0 tests pass
benchmark manifest generated
observable alignment generated
benchmark rows generated
negative-control plan generated
SLOT_4 debt object generated
SLOT_4 resolution plan generated
reports generated
physical claims remain blocked
```

---

# 15. Final discipline

```txt
Do not let benchmark progress launder mechanism debt.
```
