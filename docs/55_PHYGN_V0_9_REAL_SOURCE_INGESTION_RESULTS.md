# Phygn v0.9 Real Source Ingestion & Baseline Upgrade Attempt Results

Date: 2026-06-29

Source prompt:

```txt
docs/54_PHYGN_CODEX_V0_9_REAL_SOURCE_INGESTION_PROMPT.md
```

Supporting specs:

```txt
docs/50_PHYGN_V0_9_REAL_SOURCE_INGESTION_docs/status/GOAL.md
docs/51_PHYGN_BASELINE_SOURCE_PACK.md
docs/52_PHYGN_SOURCE_RECORD_AND_CITATION_AUDIT_PROTOCOL.md
docs/53_PHYGN_BASELINE_UPGRADE_ATTEMPT_PROTOCOL.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v0.9 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

Implemented:
- **Source Candidate Registry**: Evaluates whether candidates are url-only, metadata-incomplete, local-file-available, or ready-for-audit.
- **Citation Ingestion & In-depth Audit**: Verification matrix for metadata completion, local text availability, low-trust levels, and contradiction markers.
- **Baseline Source Pack**: Bundles all candidates and audits to check if minimum formula + observable supports are fulfilled.
- **Baseline Upgrade Attempt**: Evaluates transition rules A to F from `TOY_INTERNAL` up to `BASELINE_SOURCE_BACKED_LIMITED` or `BASELINE_SOURCE_BACKED_READY`.
- **Campaign 002 Integration**: Scans workspace folders to automatically evaluate the baseline status.
- **All 6 markdown reports** compiled in their respective target directories.
- **Automated Tests**: Total test count has been increased to **188 passed tests** (was 143, +45 tests added in v0.8 & v0.9 campaigns).

---

## 2. Implemented Modules

### Evidence v0.9 Extensions
- [source_candidates.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/source_candidates.py)
- [source_records_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/source_records_v0_9.py)
- [citation_audit_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/citation_audit_v0_9.py)
- [claim_source_links_v0_9.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/claim_source_links_v0_9.py)

### Baselines v0.9 Extensions
- [source_pack.py](file:///d:/BIOCULTOR/PHYNG/phyng/baselines/source_pack.py)
- [upgrade_attempt.py](file:///d:/BIOCULTOR/PHYNG/phyng/baselines/upgrade_attempt.py)

### Campaigns v0.9 Ingestion Runner
- [campaign_002_source_ingestion_upgrade.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/campaign_002_source_ingestion_upgrade.py)

---

## 3. Physicalization & Ingestion Outcomes

For a default campaign run on an empty `sources/baseline/` folder:
- **Pack Status**: `EMPTY`
- **Baseline Ingestion Result**: `BASELINE_REQUIRES_SOURCE`
- **Upgrade Success**: `False`
- **Max Allowed Claim Level**: `3` (Toy limit)

### Hard Physical Guardrails
Candidate physical predictions and validations of Frontera C remain strictly blocked under all circumstances:
1. *Phygn predicts gravitational decoherence.* (Blocked)
2. *The candidate model is validated.* (Blocked)
3. *SyntheticGain is physical PredictiveGain.* (Blocked)
4. *Frontera C is proven.* (Blocked)

---

## 4. Test Verification Summary

The test suite was run via `pytest -q` and returned **100% success** (188 passed tests, 0 failures, 0 warnings):
* `test_empty_source_pack_not_ready` (Verifies pack is blocked without sources) -> **PASSED**
* `test_partial_source_pack_not_minimum_coverage` (Only one requirement fulfilled) -> **PASSED**
* `test_url_only_is_candidate_not_ingested` (Url only does not constitute source ingestion) -> **PASSED**
* `test_no_fake_metadata_in_source_candidate` (Flags missing metadata fields) -> **PASSED**
* `test_url_only_fails_no_local_content` -> **PASSED**
* `test_metadata_only_does_not_unlock_baseline` (Passed metadata only, blocks formula support) -> **PASSED**
* `test_passed_limited_allows_direct_formula_support` -> **PASSED**
* `test_low_trust_blocks_hard_claim` -> **PASSED**
* `test_contradictory_source_blocks_claim` -> **PASSED**
* `test_no_sources_keeps_baseline_requires_source` -> **PASSED**
* `test_metadata_only_does_not_upgrade` -> **PASSED**
* `test_formula_only_does_not_make_limited_baseline` -> **PASSED**
* `test_formula_and_observable_support_upgrades_to_limited` (LIMITED state transition) -> **PASSED**
* `test_parameter_and_assumptions_upgrade_to_ready` (READY state transition) -> **PASSED**
* `test_contradiction_blocks_upgrade` (CONTRADICTED state transition) -> **PASSED**
* `test_limited_baseline_does_not_unlock_candidate_prediction` -> **PASSED**
* `test_empty_source_pack_run_upgrade_fails_honestly` (Workspace scan failure fallback check) -> **PASSED**
