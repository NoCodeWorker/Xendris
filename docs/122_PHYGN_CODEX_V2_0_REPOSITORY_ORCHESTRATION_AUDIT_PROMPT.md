# Codex Prompt — Phygn v2.0 Repository Orchestration, Consistency & Refactor Audit

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
docs/117_PHYGN_V1_9_BUSINESS_MODEL_VALIDATION_GATE_RESULTS.md
```

Therefore v2.0 starts at:

```txt
118
```

---

# 1. Read first

Read these v2.0 specs:

```txt
docs/118_PHYGN_V2_0_REPOSITORY_ORCHESTRATION_AUDIT_docs/status/GOAL.md
docs/119_PHYGN_CORE_ONTOLOGY_AND_STATE_CONSISTENCY_AUDIT.md
docs/120_PHYGN_MODULE_BOUNDARIES_AND_REFACTOR_MAP.md
docs/121_PHYGN_CAMPAIGN_REPORT_TEST_ORCHESTRATION_AUDIT.md
```

Also read the latest result:

```txt
docs/117_PHYGN_V1_9_BUSINESS_MODEL_VALIDATION_GATE_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
433 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Perform a repository-wide audit and produce a safe refactor map.

Do not aggressively refactor.

First discover, report and classify.

Implement only low-risk meta-infrastructure if it does not change existing behavior.

---

# 4. New package

Create:

```txt
phyng/repository_audit/
  __init__.py
  schemas.py
  structure.py
  ontology.py
  modules.py
  campaigns.py
  reports.py
  tests.py
  refactor_map.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/repository_orchestration_audit.py
```

---

# 5. Schemas

Implement:

```txt
RepositoryAuditResult
ModuleAuditRecord
StateFamilyRecord
StatusMappingRecord
DependencyRecord
CampaignAuditRecord
ReportAuditRecord
TestAuditRecord
RefactorRecommendation
RepositoryAuditCampaignResult
```

Recommendation risk levels:

```txt
NO_CHANGE
DOCUMENT_ONLY
LOW_RISK_EXTRACT_CONSTANTS
LOW_RISK_EXTRACT_ENUM
MEDIUM_RISK_SCHEMA_UNIFICATION
MEDIUM_RISK_REPORT_CONTRACT_UNIFICATION
HIGH_RISK_MODULE_MOVE
HIGH_RISK_PUBLIC_API_CHANGE
BLOCKED_NEEDS_HUMAN_REVIEW
```

---

# 6. Repository structure audit

Implement:

```python
audit_repository_structure(root: Path) -> RepositoryAuditResult
```

It should discover:

```txt
packages
modules
tests
reports
campaigns
schemas
enums
status strings
imports
```

---

# 7. Core ontology audit

Implement:

```python
audit_core_ontology(root: Path) -> list[StateFamilyRecord]
```

Search for state families:

```txt
EpistemicMode
RiskLevel
FrictionLevel
LadderLevel
TruthBoundaryStatus
PermissionLevel
ClaimStatus
ActionStatus
EvidenceLevel
SourceSupportStatus
BenchmarkStatus
DetectabilityStatus
CandidateSurvivalStatus
FailureConditionStatus
PredictionStatus
CalibrationStatus
BusinessValidationStatus
WTPLevel
ChannelValidationLevel
UnitEconomicsStatus
BusinessRiskStatus
```

Also detect likely string-only statuses.

---

# 8. Module boundary audit

Implement:

```python
audit_module_boundaries(root: Path) -> list[ModuleAuditRecord]
```

Must record:

```txt
responsibility_guess
imports
imported_by
defined_schemas
defined_enums
reports_written
tests_covering_module
possible_duplicates
boundary_warnings
```

---

# 9. Dependency audit

Implement:

```python
audit_dependencies(root: Path) -> list[DependencyRecord]
```

Detect:

```txt
import cycles if feasible
core importing domain modules
highly coupled modules
domain boundary violations
```

Do not fail the campaign for heuristic uncertainty. Report warnings.

---

# 10. Campaign audit

Implement:

```python
audit_campaigns(root: Path) -> list[CampaignAuditRecord]
```

For every campaign:

```txt
campaign_id
entrypoint
reports
gatekeepers
tests
warnings
```

---

# 11. Report audit

Implement:

```python
audit_reports(root: Path) -> list[ReportAuditRecord]
```

Check whether reports include or can be mapped to:

```txt
title
date
campaign id
inputs
core results
gate results
allowed claims
blocked claims
failure conditions
next actions
tests
```

---

# 12. Test audit

Implement:

```python
audit_tests(root: Path) -> list[TestAuditRecord]
```

Summarize:

```txt
test files
test count estimate
modules covered
campaign tests
negative tests
contract tests
report tests
```

---

# 13. Refactor map

Implement:

```python
generate_refactor_map(audit_result) -> list[RefactorRecommendation]
```

Recommendations must include:

```txt
title
description
affected_modules
risk_level
expected_benefit
behavior_change_expected: bool
requires_human_review: bool
suggested_order
```

Hard rule:

```txt
Do not recommend high-risk moves before low-risk canonicalization.
```

---

# 14. Reports

Generate:

```txt
reports/audit/repository_structure_audit_v2_0.md
reports/audit/core_ontology_consistency_v2_0.md
reports/audit/module_boundary_refactor_map_v2_0.md
reports/audit/campaign_report_test_orchestration_v2_0.md
reports/audit/refactor_recommendations_v2_0.md
reports/campaigns/REPOSITORY-ORCHESTRATION-AUDIT-v2_0.md
```

---

# 15. Tests

Create:

```txt
tests/test_repository_structure_audit_v2_0.py
tests/test_core_ontology_audit_v2_0.py
tests/test_module_boundary_audit_v2_0.py
tests/test_campaign_report_test_audit_v2_0.py
tests/test_refactor_map_v2_0.py
tests/test_repository_orchestration_audit_campaign_v2_0.py
```

Minimum tests:

```txt
test_repository_audit_discovers_packages
test_repository_audit_discovers_campaigns
test_ontology_audit_detects_known_state_families
test_module_audit_records_imports
test_refactor_recommendations_have_risk_levels
test_high_risk_refactors_require_human_review
test_campaign_report_generated
test_audit_does_not_change_existing_gate_behavior
```

---

# 16. Do not over-refactor

Do not:

```txt
move modules aggressively
rename public enums without aliases
change gate decisions
delete reports
change campaign outputs silently
collapse domain statuses without mapping
```

Allowed:

```txt
add audit package
add reports
add meta-tests
add compatibility mapping tables
add low-risk constants/enums only when behavior-preserving
```

---

# 17. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
repository audit reports are generated
ontology/state consistency report exists
module boundary/refactor map exists
campaign/report/test audit exists
refactor recommendations are risk-ranked
no existing behavior changes silently
```

Expected test count:

```txt
433 + new v2.0 tests
```

---

# 18. Final discipline

```txt
A system that audits reality must first audit its own machinery.
```
