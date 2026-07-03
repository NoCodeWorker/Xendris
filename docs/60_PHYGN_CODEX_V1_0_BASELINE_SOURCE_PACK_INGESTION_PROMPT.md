# Codex Prompt — Phygn v1.0 Baseline Source Pack Ingestion

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
v0.9 complete.
Real source ingestion pipeline exists.
SourceCandidates exist.
CitationAudit exists.
BaselineSourcePack exists.
BaselineUpgradeAttempt exists.
Default empty sources/baseline/ fails honestly.
baseline_after = BASELINE_REQUIRES_SOURCE.
candidate physical prediction remains blocked.
188 tests passed.
```

Important numbering:

```txt
Previous doc:
54_PHYGN_CODEX_V0_9_REAL_SOURCE_INGESTION_PROMPT.md

v1.0 docs:
55_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_docs/status/GOAL.md
56_PHYGN_BASELINE_SOURCE_SELECTION_GUIDE.md
57_PHYGN_LOCAL_SOURCE_FILE_PREPARATION_PROTOCOL.md
58_PHYGN_BASELINE_LIMITED_UPGRADE_EXECUTION.md
59_PHYGN_CODEX_V1_0_BASELINE_SOURCE_PACK_INGESTION_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/55_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_docs/status/GOAL.md
docs/56_PHYGN_BASELINE_SOURCE_SELECTION_GUIDE.md
docs/57_PHYGN_LOCAL_SOURCE_FILE_PREPARATION_PROTOCOL.md
docs/58_PHYGN_BASELINE_LIMITED_UPGRADE_EXECUTION.md
```

Also read:

```txt
docs/54_PHYGN_CODEX_V0_9_REAL_SOURCE_INGESTION_PROMPT.md
docs/50_PHYGN_V0_9_REAL_SOURCE_INGESTION_docs/status/GOAL.md
docs/51_PHYGN_BASELINE_SOURCE_PACK.md
docs/52_PHYGN_SOURCE_RECORD_AND_CITATION_AUDIT_PROTOCOL.md
docs/53_PHYGN_BASELINE_UPGRADE_ATTEMPT_PROTOCOL.md
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

Implement or refine:

```txt
BASELINE-SRC-PACK-001 ingestion campaign
local source file scanning
manifest loading
source candidate registration
content availability audit
citation audit integration
support matrix generation
baseline limited upgrade execution
reports
tests
```

Do not fake source ingestion.

If `sources/baseline/` is empty:

```txt
fail honestly and keep BASELINE_REQUIRES_SOURCE.
```

If sources exist but are URL-only:

```txt
register candidates but do not ingest.
```

If sources exist with local files and direct support:

```txt
attempt upgrade to BASELINE_SOURCE_BACKED_LIMITED.
```

---

# 4. Expected files

Input folder:

```txt
sources/baseline/
```

Optional manifest:

```txt
sources/baseline/source_manifest.json
```

Optional extracts:

```txt
sources/baseline/extracts/*.md
```

---

# 5. New or extended modules

Create or extend:

```txt
phyng/campaigns/baseline_source_pack_ingestion.py
phyng/baselines/limited_upgrade_execution.py
phyng/evidence/local_source_scanner.py
```

Reuse:

```txt
phyng/evidence/source_candidates.py
phyng/evidence/source_records_v0_9.py
phyng/evidence/citation_audit_v0_9.py
phyng/evidence/claim_source_links_v0_9.py
phyng/baselines/source_pack.py
phyng/baselines/upgrade_attempt.py
```

---

# 6. Main function

Implement:

```python
run_baseline_source_pack_ingestion_v1_0(project_root: Path) -> BaselineUpgradeExecutionResult
```

It must:

```txt
scan sources/baseline/
load manifest if present
register candidates
check local content
run citation audit
build support matrix
run upgrade attempt
write reports
return execution result
```

---

# 7. Empty case

If no sources:

```txt
source_pack_status = EMPTY
upgrade_success = False
baseline_after = BASELINE_REQUIRES_SOURCE
allowed_claims = ["The baseline still requires source ingestion."]
blocked_claims include all physical/candidate claims.
```

---

# 8. Limited upgrade case

If audited sources provide:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
no contradiction
```

then:

```txt
baseline_after = BASELINE_SOURCE_BACKED_LIMITED
upgrade_success = True
```

Allowed claim:

```txt
CAMPAIGN-002 has a source-backed limited visibility/coherence decay baseline.
```

Still blocked:

```txt
Phygn predicts gravitational decoherence.
Frontera C is validated.
The boundary-aware candidate is validated.
SyntheticGain is physical PredictiveGain.
```

---

# 9. Reports

Generate:

```txt
reports/campaigns/BASELINE-SRC-PACK-001_ingestion_result.md
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md
reports/model_comparison/CAMPAIGN-002_source_backed_baseline_status_v1_0.md
reports/rag/baseline_source_pack_v1_0.md
reports/rag/baseline_support_matrix_v1_0.md
reports/rag/citation_audit_v1_0.md
```

---

# 10. Tests

Add:

```txt
tests/test_baseline_limited_upgrade_execution.py
tests/test_baseline_source_pack_ingestion_v1_0.py
tests/test_local_source_scanner.py
```

Minimum cases:

```txt
test_execution_empty_sources_fails_honestly
test_execution_url_only_sources_do_not_upgrade
test_execution_formula_observable_sources_upgrade_limited
test_execution_contradiction_blocks_upgrade
test_execution_limited_baseline_does_not_validate_candidate
test_execution_reports_generated
test_manifest_loads_source_candidates
test_local_files_are_detected
```

---

# 11. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
The source-backed baseline validates Frontera C.
The baseline validates the candidate.
Baseline upgrade gives physical PredictiveGain.
```

Allowed:

```txt
The baseline upgrade succeeded or failed under audited source rules.
A limited baseline is a better adversary, not a validation of the candidate.
Physical prediction remains blocked.
```

---

# 12. Acceptance criteria

Complete when:

```txt
pytest -q passes
BASELINE-SRC-PACK-001 runs
empty case fails honestly
manifest/local scanner works
direct formula + observable support upgrades to LIMITED in tests
reports generated
candidate prediction remains blocked
```

---

# 13. Final discipline

```txt
The source-backed baseline is not the trophy.
It is the opponent entering the ring.
```
