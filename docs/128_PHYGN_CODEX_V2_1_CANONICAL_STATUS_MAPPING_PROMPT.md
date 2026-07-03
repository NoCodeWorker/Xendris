# Codex Prompt — Phygn v2.1 Canonical Status Mapping & Compatibility Layer

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
docs/123_PHYGN_V2_0_REPOSITORY_ORCHESTRATION_AUDIT_RESULTS.md
```

Therefore v2.1 starts at:

```txt
124
```

---

# 1. Read first

Read these v2.1 specs:

```txt
docs/124_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_docs/status/GOAL.md
docs/125_PHYGN_PERMISSION_GRAMMAR_AND_BLOCKED_REASON_REGISTRY.md
docs/126_PHYGN_COMPATIBILITY_ALIAS_LAYER.md
docs/127_PHYGN_REPORT_CONTRACT_CANONICALIZATION_PROTOCOL.md
```

Also read the latest v2.0 result:

```txt
docs/123_PHYGN_V2_0_REPOSITORY_ORCHESTRATION_AUDIT_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
471 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.1:

```txt
Canonical Status Mapping
Permission Grammar
Blocked Reason Registry
Evidence/Support Levels
Compatibility Alias Layer
Status Normalization Helpers
Canonical Report Contract Helpers
Reports
Meta-tests
```

Do not perform destructive refactor.

Do not change existing gate behavior.

---

# 4. New package

Create or extend:

```txt
phyng/core/
  __init__.py
  permissions.py
  blocked_reasons.py
  evidence_levels.py
  risk_levels.py
  support_levels.py
  status_mapping.py
  compatibility.py
  report_contract.py
```

Create campaign:

```txt
phyng/campaigns/canonical_status_mapping.py
```

---

# 5. Canonical enums

Implement:

```txt
CanonicalPermission
CanonicalBlockedReason
CanonicalEvidenceLevel
CanonicalSupportLevel
CanonicalRiskLevel
CanonicalAuditEventType
```

Also implement:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

Use Pydantic where appropriate.

---

# 6. Compatibility map

Implement:

```python
STATUS_COMPATIBILITY_MAP: dict[str, CanonicalStatusRecord]
```

Include representative statuses from these domains:

```txt
business_validation
copilot/truth_boundary
candidate/detectability
epistemic_modes
financial/action gates
source/benchmark gates
prediction/calibration
repository_audit
```

Minimum mappings:

```txt
BUSINESS_BLOCKED_NO_WTP
BUSINESS_BLOCKED_NO_CUSTOMER
BUSINESS_VALIDATED_LIMITED
UNIT_ECONOMICS_NEGATIVE
WTP_7_PAID_PILOT
OUTSIDE_CLAIM_BOUNDARY
CROSSED_OVERCLAIM_BOUNDARY
CROSSED_FALSEHOOD_BOUNDARY
ACTION_BLOCKED
AUTOMATED_EXECUTION_ALLOWED
UNDETECTABLE_SYNTHETIC_DELTA
DETECTABLE_SYNTHETIC_DELTA
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
SURVIVES_AS_TOY_NEGATIVE_CONTROL
SOURCE_BACKED_LIMITED
BENCHMARK_SUPPORTED
FILTER_NOT_PREDICTIVELY_USEFUL_YET
COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE
```

---

# 7. Normalization helpers

Implement:

```python
normalize_status(domain_status: str, domain: str | None = None) -> CanonicalStatusRecord
get_canonical_permission(domain_status: str, domain: str | None = None) -> CanonicalPermission
get_blocked_reasons(domain_status: str, domain: str | None = None) -> list[CanonicalBlockedReason]
is_blocked(domain_status: str, domain: str | None = None) -> bool
requires_human_review(domain_status: str, domain: str | None = None) -> bool
```

Unknown status fallback:

```txt
permission: REVIEW_REQUIRED
blocked_reason: HUMAN_REVIEW_REQUIRED
evidence_level: NO_EVIDENCE
support_level: UNSUPPORTED
```

---

# 8. Report contract helpers

Implement:

```python
build_report_contract(...)
render_canonical_report_section(...)
append_canonical_status_section(...)
```

The canonical section must expose:

```txt
Domain Status
Canonical Permission
Blocked Reasons
Evidence Level
Support Level
Risk Level
Allowed Uses
Blocked Uses
Next Actions
Discipline Note
```

---

# 9. Campaign

Implement:

```python
run_canonical_status_mapping_campaign(root: str | Path = ".")
```

It should generate:

```txt
reports/core/canonical_status_mapping_v2_1.md
reports/core/permission_grammar_v2_1.md
reports/core/compatibility_aliases_v2_1.md
reports/core/report_contract_canonicalization_v2_1.md
reports/campaigns/CANONICAL-STATUS-MAPPING-v2_1.md
```

---

# 10. Tests

Create:

```txt
tests/test_canonical_permissions_v2_1.py
tests/test_status_compatibility_mapping_v2_1.py
tests/test_status_normalization_v2_1.py
tests/test_report_contract_canonicalization_v2_1.py
tests/test_canonical_status_mapping_campaign_v2_1.py
```

Minimum tests:

```txt
test_canonical_permission_enum_contains_core_permissions
test_known_business_status_maps_to_scale_blocked
test_unknown_status_requires_review
test_outside_claim_boundary_maps_to_claim_blocked
test_falsehood_boundary_maps_to_claim_blocked_with_contradiction
test_undetectable_delta_maps_to_claim_blocked
test_validated_limited_maps_to_limited_allowed
test_normalization_does_not_mutate_original_status
test_report_contract_renders_canonical_section
test_campaign_generates_reports
```

---

# 11. Behavior preservation

Add at least one behavior preservation test:

```txt
existing gate result status remains unchanged after normalization
```

Normalization may add interpretation.

It must not mutate original output.

---

# 12. Do not over-refactor

Do not:

```txt
rename public statuses
delete domain enums
move domain modules
change gate outputs
change campaign outputs silently
force all reports to new format
```

Allowed:

```txt
add core compatibility layer
add mapping tables
add helpers
append canonical sections to new v2.1 reports
add meta-tests
```

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
canonical enums exist
compatibility map exists
normalization helpers work
unknown statuses require review
report contract helpers work
campaign reports generated
existing gate behavior preserved
```

Expected test count:

```txt
471 + new v2.1 tests
```

---

# 14. Final discipline

```txt
Canonicalization must increase clarity without erasing domain meaning.
```
