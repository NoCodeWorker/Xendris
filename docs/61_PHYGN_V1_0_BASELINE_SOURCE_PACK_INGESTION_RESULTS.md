# Phygn v1.0 Baseline Source Pack Ingestion — Results

Date: 2026-06-29

Source prompt:

```txt
docs/60_PHYGN_CODEX_V1_0_BASELINE_SOURCE_PACK_INGESTION_PROMPT.md
```

Supporting specs:

```txt
docs/55_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_docs/status/GOAL.md
docs/56_PHYGN_BASELINE_SOURCE_SELECTION_GUIDE.md
docs/57_PHYGN_LOCAL_SOURCE_FILE_PREPARATION_PROTOCOL.md
docs/58_PHYGN_BASELINE_LIMITED_UPGRADE_EXECUTION.md
```

Prior session:

```txt
docs/54_PHYGN_CODEX_V0_9_REAL_SOURCE_INGESTION_PROMPT.md
docs/55_PHYGN_V0_9_REAL_SOURCE_INGESTION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.0 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All 12 acceptance criteria from `§12` of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **224 passed, 0 failed** |
| BASELINE-SRC-PACK-001 runs | ✅ Campaign runner implemented |
| Empty case fails honestly | ✅ `BASELINE_REQUIRES_SOURCE`, `upgrade_success = False` |
| Manifest / local scanner works | ✅ Implemented with fallback to directory scan |
| Formula + observable support upgrades to LIMITED in tests | ✅ State machine Rules A–F enforced |
| Reports generated (6 files) | ✅ All 6 reports written |
| Candidate prediction remains blocked | ✅ Blocked in all paths |

---

## 2. New Modules Implemented (v1.0)

### Evidence Layer

- [local_source_scanner.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/local_source_scanner.py)
  — Scans `sources/baseline/`, loads `source_manifest.json`, falls back to directory scan if manifest is absent or malformed. Filters `.gitkeep`, infers requirement IDs from filenames.

### Baselines Layer

- [limited_upgrade_execution.py](file:///d:/BIOCULTOR/PHYNG/phyng/baselines/limited_upgrade_execution.py)
  — Orchestrates the full ingestion pipeline:
  `scan → _candidate_to_record → audit_citation_v0_9 → _link_from_audit → evaluate_source_pack → run_baseline_upgrade_attempt_v0_9 → write 6 reports`
  Returns `BaselineUpgradeExecutionResult`.

### Campaign Entry Point

- [baseline_source_pack_ingestion.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/baseline_source_pack_ingestion.py)
  — CLI entry point for `BASELINE-SRC-PACK-001`. Callable as `python -m phyng.campaigns.baseline_source_pack_ingestion [project_root]`.

### Reused from v0.9 (unchanged)

- [source_candidates.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/source_candidates.py)
- [source_records_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/source_records_v0_9.py)
- [citation_audit_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/citation_audit_v0_9.py)
- [claim_source_links_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/claim_source_links_v0_9.py)
- [source_pack.py](file:///d:/BIOCULTOR/PHYNG/phyng/baselines/source_pack.py)
- [upgrade_attempt.py](file:///d:/BIOCULTOR/PHYNG/phyng/baselines/upgrade_attempt.py)

---

## 3. Pipeline Execution Outcomes

### Empty `sources/baseline/` (default project state)

```txt
source_pack_status   = EMPTY
upgrade_success      = False
baseline_after       = BASELINE_REQUIRES_SOURCE
audited_sources      = 0
formula_support      = 0
observable_support   = 0
allowed_claims       = ["The baseline still requires source ingestion."]
```

### URL-only sources (no local file)

```txt
ingestion_status     = NOT_INGESTED
audit_status         = FAILED_NO_LOCAL_CONTENT
passed               = False
support links        = 0
upgrade_success      = False
baseline_after       = BASELINE_REQUIRES_SOURCE
```

### Local files with FORMULA_SUPPORT + OBSERVABLE_SUPPORT (test scenario)

```txt
upgrade_success      = True
baseline_after       = BASELINE_SOURCE_BACKED_LIMITED
max_claim_level      = 4
allowed_claims:
  - CAMPAIGN-002 has a source-backed limited visibility/coherence decay baseline.
```

### Hard Physical Guardrails — blocked under **all** outcomes

```txt
1. Phygn predicts gravitational decoherence.           → BLOCKED
2. Frontera C is validated.                            → BLOCKED
3. The boundary-aware candidate is validated.          → BLOCKED
4. SyntheticGain is physical PredictiveGain.           → BLOCKED
```

---

## 4. Reports Generated

All 6 reports are always written by `run_limited_upgrade_execution()`:

```txt
reports/rag/baseline_source_pack_v1_0.md
reports/rag/baseline_support_matrix_v1_0.md
reports/rag/citation_audit_v1_0.md
reports/campaigns/BASELINE-SRC-PACK-001_ingestion_result.md
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md
reports/model_comparison/CAMPAIGN-002_source_backed_baseline_status_v1_0.md
```

---

## 5. Test Verification Summary

Test suite: `pytest -q` → **224 passed, 0 failed, 0 warnings**
Previous baseline (v0.9): 188 passed → **+36 new tests added**.

### New test files (v1.0)

#### [test_local_source_scanner.py](file:///d:/BIOCULTOR/PHYNG/tests/test_local_source_scanner.py) — 8 tests

| Test | Result |
|---|---|
| `test_empty_dir_returns_empty` | ✅ PASSED |
| `test_missing_baseline_dir_returns_empty` | ✅ PASSED |
| `test_manifest_single_entry_url_only` | ✅ PASSED |
| `test_manifest_entry_with_local_file` | ✅ PASSED |
| `test_no_manifest_falls_back_to_file_scan` | ✅ PASSED |
| `test_gitkeep_ignored` | ✅ PASSED |
| `test_manifest_fallback_on_malformed_json` | ✅ PASSED |
| `test_requirement_inference_from_filename` | ✅ PASSED |
| `test_multiple_manifest_entries` | ✅ PASSED |

#### [test_baseline_limited_upgrade_execution.py](file:///d:/BIOCULTOR/PHYNG/tests/test_baseline_limited_upgrade_execution.py) — 16 tests

| Test | Result |
|---|---|
| `test_no_local_path_gives_not_ingested` | ✅ PASSED |
| `test_nonexistent_local_path_gives_not_ingested` | ✅ PASSED |
| `test_existing_local_path_gives_ingested` | ✅ PASSED |
| `test_existing_path_partial_metadata` | ✅ PASSED |
| `test_failed_audit_returns_none` | ✅ PASSED |
| `test_passed_audit_creates_link` | ✅ PASSED |
| `test_bsr003_maps_to_observable_support` | ✅ PASSED |
| `test_bsr004_maps_to_context_support` | ✅ PASSED |
| `test_long_notes_not_included_as_excerpt` | ✅ PASSED |
| `test_empty_sources_dir_stays_baseline_requires_source` | ✅ PASSED |
| `test_no_sources_dir_stays_baseline_requires_source` | ✅ PASSED |
| `test_result_always_has_blocked_claims` | ✅ PASSED |
| `test_report_paths_generated` | ✅ PASSED |
| `test_execution_id_propagated` | ✅ PASSED |
| `test_campaign_id_is_fixed` | ✅ PASSED |

#### [test_baseline_source_pack_ingestion_v1_0.py](file:///d:/BIOCULTOR/PHYNG/tests/test_baseline_source_pack_ingestion_v1_0.py) — 12 tests

| Test | Result |
|---|---|
| `test_empty_baseline_does_not_upgrade` | ✅ PASSED |
| `test_url_only_source_does_not_upgrade` | ✅ PASSED |
| `test_six_reports_always_generated` | ✅ PASSED |
| `test_rag_reports_exist` | ✅ PASSED |
| `test_campaign_reports_exist` | ✅ PASSED |
| `test_model_comparison_report_exists` | ✅ PASSED |
| `test_ingestion_result_mentions_blocked_claims` | ✅ PASSED |
| `test_physical_prediction_blocked_in_result` | ✅ PASSED |
| `test_upgrade_attempt_report_says_blocked` | ✅ PASSED |
| `test_main_runs_without_exception` | ✅ PASSED |
| `test_main_prints_blocked_claims` | ✅ PASSED |
| `test_run_twice_is_idempotent` | ✅ PASSED |

---

## 6. Discipline Note

> The source-backed baseline is not the trophy.
> It is the opponent entering the ring.

A `BASELINE_SOURCE_BACKED_LIMITED` result means the standard model has a
legitimate, audited opponent. It does not validate Frontera C, does not validate
the boundary-aware candidate, and does not unlock physical prediction claims.
Physical prediction remains blocked until the candidate model is independently
source-backed and passes its own full audit protocol.
