# Codex Prompt — Phygn v0.9 Real Source Ingestion & Baseline Upgrade Attempt

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
v0.8 complete.
Baseline subsystem exists.
Visibility decay baseline exists.
CAMPAIGN-002 baseline physicalization runs.
No sources were ingested.
baseline_after = BASELINE_REQUIRES_SOURCE.
can_be_used_as_baseline = False.
Candidate prediction remains blocked.
169 tests passed.
```

Your task is to implement **v0.9: Real Source Ingestion & Baseline Upgrade Attempt**.

Important numbering:

```txt
Previous doc:
49_PHYGN_CODEX_V0_8_SOURCE_BACKED_BASELINE_PROMPT.md

v0.9 docs:
50_PHYGN_V0_9_REAL_SOURCE_INGESTION_docs/status/GOAL.md
51_PHYGN_BASELINE_SOURCE_PACK.md
52_PHYGN_SOURCE_RECORD_AND_CITATION_AUDIT_PROTOCOL.md
53_PHYGN_BASELINE_UPGRADE_ATTEMPT_PROTOCOL.md
54_PHYGN_CODEX_V0_9_REAL_SOURCE_INGESTION_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/50_PHYGN_V0_9_REAL_SOURCE_INGESTION_docs/status/GOAL.md
docs/51_PHYGN_BASELINE_SOURCE_PACK.md
docs/52_PHYGN_SOURCE_RECORD_AND_CITATION_AUDIT_PROTOCOL.md
docs/53_PHYGN_BASELINE_UPGRADE_ATTEMPT_PROTOCOL.md
```

Also read:

```txt
docs/49_PHYGN_CODEX_V0_8_SOURCE_BACKED_BASELINE_PROMPT.md
docs/45_PHYGN_DECOHERENCE_BASELINE_LITERATURE_INGESTION.md
docs/46_PHYGN_VISIBILITY_DECAY_BASELINE_PROTOCOL.md
docs/47_PHYGN_CAMPAIGN_002_BASELINE_PHYSICALIZATION.md
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
source candidates
baseline source pack
source record v0.9
citation audit
claim-source link v0.9
baseline upgrade attempt
reports
tests
```

Do not fake source ingestion.

If no local source files exist:

```txt
the upgrade attempt must fail honestly.
```

If local source files exist in `sources/baseline/`:

```txt
register them as SourceCandidates
audit metadata/content availability
create SourceRecords if allowed
create ClaimSourceLinks only when support is explicit
attempt baseline upgrade
```

---

# 4. New modules

Create or extend:

```txt
phyng/evidence/source_candidates.py
phyng/evidence/source_records_v0_9.py
phyng/evidence/citation_audit_v0_9.py
phyng/evidence/claim_source_links_v0_9.py

phyng/baselines/source_pack.py
phyng/baselines/upgrade_attempt.py
```

Optional:

```txt
phyng/campaigns/campaign_002_source_ingestion_upgrade.py
```

---

# 5. Schemas

Implement:

```txt
SourceCandidate
BaselineSourcePack
SourceRecordV09
CitationAuditResult
ClaimSourceLinkV09
BaselineUpgradeAttemptResult
```

---

# 6. Source candidate behavior

Rules:

```txt
URL-only candidate -> CANDIDATE_ONLY, not ingested.
Missing local file -> CANDIDATE_REGISTERED, not ingested.
Local file available -> LOCAL_FILE_AVAILABLE.
Metadata incomplete -> METADATA_INCOMPLETE.
Ready source -> READY_FOR_AUDIT.
```

No fake metadata.

---

# 7. Citation audit behavior

Rules:

```txt
no local content -> FAILED_NO_LOCAL_CONTENT
missing metadata -> FAILED_MISSING_METADATA
low trust -> FAILED_LOW_TRUST for hard claims
contradiction -> FAILED_CONTRADICTORY
direct formula/observable support + metadata -> PASSED_LIMITED
metadata only -> PASSED_METADATA_ONLY
```

---

# 8. Baseline source pack

Build from:

```txt
sources/baseline/
rag/source_manifest.json if present
manual source candidate records if present
```

Minimum support required for upgrade to LIMITED:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
citation audit passed
```

---

# 9. Baseline upgrade attempt

Implement:

```python
run_baseline_upgrade_attempt_v0_9(...)
```

Rules:

```txt
no audited sources -> BASELINE_REQUIRES_SOURCE
metadata only -> BASELINE_REQUIRES_DIRECT_SUPPORT
formula only -> BASELINE_BACKGROUND_SUPPORTED
formula + observable -> BASELINE_SOURCE_BACKED_LIMITED
formula + observable + parameter + assumptions -> BASELINE_SOURCE_BACKED_READY
contradiction -> BASELINE_CONTRADICTED
```

Candidate prediction must remain blocked.

---

# 10. Reports

Generate:

```txt
reports/rag/baseline_source_pack.md
reports/rag/baseline_source_candidates.md
reports/rag/citation_audit_v0_9.md
reports/rag/claim_source_links_v0_9.md
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v0_9.md
reports/model_comparison/baseline_upgrade_attempt_v0_9.md
```

---

# 11. Tests

Add:

```txt
tests/test_baseline_source_pack.py
tests/test_citation_audit_v0_9.py
tests/test_claim_source_links_v0_9.py
tests/test_baseline_upgrade_attempt_v0_9.py
```

Minimum cases:

```txt
test_empty_source_pack_not_ready
test_partial_source_pack_not_minimum_coverage
test_url_only_is_candidate_not_ingested
test_metadata_only_does_not_unlock_baseline
test_passed_limited_allows_direct_formula_support
test_formula_only_does_not_make_limited_baseline
test_formula_and_observable_support_upgrades_to_limited
test_parameter_and_assumptions_upgrade_to_ready
test_contradiction_blocks_upgrade
test_limited_baseline_does_not_unlock_candidate_prediction
test_reports_generated
```

---

# 12. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
Frontera C is validated.
The source-backed baseline validates the candidate.
The baseline proves the theory.
```

Allowed:

```txt
The baseline upgrade attempt succeeded/failed under explicit citation-audit rules.
A source-backed limited baseline does not validate the candidate.
Physical prediction remains blocked.
```

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
source candidates implemented
citation audit implemented
baseline source pack implemented
baseline upgrade attempt implemented
reports generated
empty/no-source case fails honestly
formula+observable audited support upgrades to LIMITED in tests
candidate physical prediction remains blocked
```

---

# 14. Final discipline

```txt
Accept evidence.
Reject inflation.
```
