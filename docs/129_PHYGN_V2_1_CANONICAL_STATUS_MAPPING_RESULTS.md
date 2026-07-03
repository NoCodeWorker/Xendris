# Phygn v2.1 - Canonical Status Mapping & Compatibility Layer Results

Date: 2026-06-30

Source prompt:

```txt
docs/128_PHYGN_CODEX_V2_1_CANONICAL_STATUS_MAPPING_PROMPT.md
```

Supporting specs:

```txt
docs/124_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_docs/status/GOAL.md
docs/125_PHYGN_PERMISSION_GRAMMAR_AND_BLOCKED_REASON_REGISTRY.md
docs/126_PHYGN_COMPATIBILITY_ALIAS_LAYER.md
docs/127_PHYGN_REPORT_CONTRACT_CANONICALIZATION_PROTOCOL.md
docs/123_PHYGN_V2_0_REPOSITORY_ORCHESTRATION_AUDIT_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.1 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.1 implemented the safest next step after the v2.0 repository audit:

```txt
canonical status mapping tables
permission grammar
blocked reason registry
evidence/support/risk levels
compatibility aliases
normalization helpers
canonical report contract helpers
campaign reports
meta-tests
```

No destructive refactor was performed.

No public domain statuses were renamed.

No domain enums were deleted.

No existing gate output was changed.

Final validation:

```txt
pytest -q
484 passed in 18.53s
```

Baseline before v2.1:

```txt
pytest -q
471 passed in 17.94s
```

Net result:

```txt
471 baseline tests + 13 v2.1 tests = 484 passing tests
```

---

## 2. New Core Package

Created:

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

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `permissions.py` | Defines `CanonicalPermission` |
| `blocked_reasons.py` | Defines `CanonicalBlockedReason` |
| `evidence_levels.py` | Defines `CanonicalEvidenceLevel` |
| `support_levels.py` | Defines `CanonicalSupportLevel` |
| `risk_levels.py` | Defines `CanonicalRiskLevel` |
| `status_mapping.py` | Defines `CanonicalAuditEventType`, `CanonicalStatusRecord`, and `STATUS_COMPATIBILITY_MAP` |
| `compatibility.py` | Provides normalization and permission helper functions |
| `report_contract.py` | Provides canonical report contract model and rendering helpers |

---

## 3. Canonical Grammar Implemented

Canonical enums implemented:

```txt
CanonicalPermission
CanonicalBlockedReason
CanonicalEvidenceLevel
CanonicalSupportLevel
CanonicalRiskLevel
CanonicalAuditEventType
```

Pydantic models implemented:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

Core rule:

```txt
Domain status remains the source of local meaning.
Canonical mapping provides cross-system interpretability.
```

---

## 4. Compatibility Map

Implemented in:

```txt
phyng/core/status_mapping.py
```

Mapping table:

```python
STATUS_COMPATIBILITY_MAP: dict[str, CanonicalStatusRecord]
```

Mapped status count:

```txt
21
```

Mapped statuses:

| Domain Status | Domain | Canonical Permission | Blocked Reasons | Evidence | Support | Risk |
|---|---|---|---|---|---|---|
| `ACTION_BLOCKED` | `epistemic_modes` | `ACTION_BLOCKED` | `OUTSIDE_ACTION_BOUNDARY` | `HEURISTIC_ONLY` | `HEURISTIC` | `RISK_6_REAL_WORLD_ACTION` |
| `AUTOMATED_EXECUTION_ALLOWED` | `epistemic_modes` | `EXECUTION_ALLOWED` | `NO_BLOCK` | `OPERATIONALLY_VALIDATED` | `OPERATIONAL` | `RISK_7_AUTOMATED_EXECUTION` |
| `BENCHMARK_SUPPORTED` | `epistemic_ladder` | `CLAIM_LIMITED_ALLOWED` | `NO_BLOCK` | `BENCHMARK_SUPPORTED` | `BENCHMARK` | `RISK_4_CLIENT_DELIVERABLE` |
| `BUSINESS_BLOCKED_NO_CHANNEL` | `business_validation` | `SCALE_BLOCKED` | `NO_CHANNEL_SIGNAL` | `HEURISTIC_ONLY` | `HEURISTIC` | `BUSINESS_RISK` |
| `BUSINESS_BLOCKED_NO_CUSTOMER` | `business_validation` | `SCALE_BLOCKED` | `NO_CUSTOMER` | `NO_EVIDENCE` | `UNSUPPORTED` | `BUSINESS_RISK` |
| `BUSINESS_BLOCKED_NO_PROBLEM` | `business_validation` | `SCALE_BLOCKED` | `NO_PROBLEM` | `NO_EVIDENCE` | `UNSUPPORTED` | `BUSINESS_RISK` |
| `BUSINESS_BLOCKED_NO_WTP` | `business_validation` | `SCALE_BLOCKED` | `NO_PAYMENT_SIGNAL` | `NO_EVIDENCE` | `UNSUPPORTED` | `BUSINESS_RISK` |
| `BUSINESS_VALIDATED_LIMITED` | `business_validation` | `SCALE_ALLOWED` | `NO_BLOCK` | `OPERATIONALLY_VALIDATED` | `OPERATIONAL` | `BUSINESS_RISK` |
| `COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE` | `repository_audit` | `ACTION_LIMITED_ALLOWED` | `NO_BLOCK` | `HEURISTIC_ONLY` | `HEURISTIC` | `TECHNICAL_RISK` |
| `CROSSED_FALSEHOOD_BOUNDARY` | `copilot_truth_boundary` | `CLAIM_BLOCKED` | `CONTRADICTION` | `NO_EVIDENCE` | `UNSUPPORTED` | `RISK_4_CLIENT_DELIVERABLE` |
| `CROSSED_OVERCLAIM_BOUNDARY` | `copilot_truth_boundary` | `CLAIM_BLOCKED` | `OVERCLAIM` | `NO_EVIDENCE` | `UNSUPPORTED` | `RISK_4_CLIENT_DELIVERABLE` |
| `DETECTABLE_SYNTHETIC_DELTA` | `candidate_detectability` | `CLAIM_LIMITED_ALLOWED` | `NO_BLOCK` | `SYNTHETIC_ONLY` | `SYNTHETIC` | `TECHNICAL_RISK` |
| `FAIL_NO_BENCHMARK` | `benchmark_gate` | `CLAIM_BLOCKED` | `MISSING_BENCHMARK` | `HEURISTIC_ONLY` | `HEURISTIC` | `TECHNICAL_RISK` |
| `FAIL_NO_SOURCE_SUPPORT` | `source_support` | `CLAIM_BLOCKED` | `MISSING_SOURCE_SUPPORT` | `NO_EVIDENCE` | `UNSUPPORTED` | `TECHNICAL_RISK` |
| `FILTER_NOT_PREDICTIVELY_USEFUL_YET` | `prediction_accuracy` | `REVIEW_REQUIRED` | `HUMAN_REVIEW_REQUIRED` | `HEURISTIC_ONLY` | `HEURISTIC` | `TECHNICAL_RISK` |
| `OUTSIDE_CLAIM_BOUNDARY` | `copilot_truth_boundary` | `CLAIM_BLOCKED` | `OUTSIDE_CLAIM_BOUNDARY` | `NO_EVIDENCE` | `UNSUPPORTED` | `RISK_3_PUBLIC_CONTENT` |
| `SOURCE_BACKED_LIMITED` | `epistemic_ladder` | `CLAIM_LIMITED_ALLOWED` | `NO_BLOCK` | `SOURCE_BACKED_LIMITED` | `SOURCE_LIMITED` | `RISK_3_PUBLIC_CONTENT` |
| `SURVIVES_AS_TOY_NEGATIVE_CONTROL` | `candidate_survival` | `CLAIM_LIMITED_ALLOWED` | `NO_BLOCK` | `SYNTHETIC_ONLY` | `SYNTHETIC` | `TECHNICAL_RISK` |
| `UNDETECTABLE_SYNTHETIC_DELTA` | `candidate_detectability` | `CLAIM_BLOCKED` | `UNDETECTABLE_DELTA` | `SYNTHETIC_ONLY` | `SYNTHETIC` | `TECHNICAL_RISK` |
| `UNIT_ECONOMICS_NEGATIVE` | `business_validation` | `SCALE_BLOCKED` | `NEGATIVE_UNIT_ECONOMICS` | `HEURISTIC_ONLY` | `HEURISTIC` | `BUSINESS_RISK` |
| `WTP_7_PAID_PILOT` | `business_validation` | `ACTION_LIMITED_ALLOWED` | `NO_BLOCK` | `PAYMENT_SIGNAL` | `OPERATIONAL` | `BUSINESS_RISK` |

---

## 5. Normalization Helpers

Implemented in:

```txt
phyng/core/compatibility.py
```

Functions:

```python
normalize_status(domain_status: str, domain: str | None = None) -> CanonicalStatusRecord
get_canonical_permission(domain_status: str, domain: str | None = None) -> CanonicalPermission
get_blocked_reasons(domain_status: str, domain: str | None = None) -> list[CanonicalBlockedReason]
is_blocked(domain_status: str, domain: str | None = None) -> bool
requires_human_review(domain_status: str, domain: str | None = None) -> bool
```

Unknown status fallback:

| Field | Value |
|---|---|
| `canonical_permission` | `REVIEW_REQUIRED` |
| `blocked_reasons` | `HUMAN_REVIEW_REQUIRED` |
| `evidence_level` | `NO_EVIDENCE` |
| `support_level` | `UNSUPPORTED` |
| `audit_event_type` | `UNKNOWN_STATUS_REVIEW_REQUIRED` |

Safety result:

```txt
Unknown statuses are never elevated to valid claims or permissions.
```

---

## 6. Report Contract Helpers

Implemented in:

```txt
phyng/core/report_contract.py
```

Functions:

```python
build_report_contract(...)
render_canonical_report_section(...)
append_canonical_status_section(...)
```

Canonical report section exposes:

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

Progressive adoption rule preserved:

```txt
Historical reports remain unchanged.
New v2.1 reports include canonical sections.
```

---

## 7. Campaign

Created:

```txt
phyng/campaigns/canonical_status_mapping.py
```

Entrypoint:

```python
run_canonical_status_mapping_campaign(root: str | Path = ".")
```

Campaign status:

```txt
COMPLETE_COMPATIBILITY_LAYER_NO_BEHAVIOR_CHANGE
```

Generated reports:

```txt
reports/core/canonical_status_mapping_v2_1.md
reports/core/permission_grammar_v2_1.md
reports/core/compatibility_aliases_v2_1.md
reports/core/report_contract_canonicalization_v2_1.md
reports/campaigns/CANONICAL-STATUS-MAPPING-v2_1.md
```

---

## 8. Tests

Created:

```txt
tests/test_canonical_permissions_v2_1.py
tests/test_status_compatibility_mapping_v2_1.py
tests/test_status_normalization_v2_1.py
tests/test_report_contract_canonicalization_v2_1.py
tests/test_canonical_status_mapping_campaign_v2_1.py
```

New tests:

| Test | Purpose |
|---|---|
| `test_canonical_permission_enum_contains_core_permissions` | Confirms core canonical enums exist |
| `test_known_business_status_maps_to_scale_blocked` | Confirms `BUSINESS_BLOCKED_NO_WTP` maps to `SCALE_BLOCKED` |
| `test_outside_claim_boundary_maps_to_claim_blocked` | Confirms truth-boundary claim block mapping |
| `test_falsehood_boundary_maps_to_claim_blocked_with_contradiction` | Confirms contradiction mapping |
| `test_undetectable_delta_maps_to_claim_blocked` | Confirms undetectable synthetic delta blocks physical claims |
| `test_validated_limited_maps_to_limited_allowed` | Confirms limited business validation maps to allowed scale interpretation |
| `test_required_prompt_statuses_are_mapped` | Confirms all required prompt statuses are present |
| `test_unknown_status_requires_review` | Confirms conservative unknown fallback |
| `test_normalization_does_not_mutate_original_status` | Confirms normalization preserves original string |
| `test_existing_gate_result_status_remains_unchanged_after_normalization` | Confirms existing business gate output is not mutated |
| `test_report_contract_renders_canonical_section` | Confirms canonical report section rendering |
| `test_append_canonical_status_section_preserves_original_markdown` | Confirms append-only report behavior |
| `test_campaign_generates_reports` | Confirms v2.1 campaign report generation |

Focused v2.1 verification:

```txt
pytest -q tests/test_canonical_permissions_v2_1.py tests/test_status_compatibility_mapping_v2_1.py tests/test_status_normalization_v2_1.py tests/test_report_contract_canonicalization_v2_1.py tests/test_canonical_status_mapping_campaign_v2_1.py
13 passed in 0.70s
```

Final full-suite verification:

```txt
pytest -q
484 passed in 18.53s
```

---

## 9. Behavior Preservation

v2.1 explicitly avoided:

```txt
renaming public statuses
deleting domain enums
moving domain modules
changing gate outputs
changing campaign outputs silently
forcing historical reports into the new format
```

Behavior preservation test:

```txt
test_existing_gate_result_status_remains_unchanged_after_normalization
```

Result:

```txt
passed
```

Meaning:

```txt
Normalization can add canonical interpretation, but it does not mutate the original business gate status.
```

---

## 10. Final Assessment

v2.1 completed the compatibility-first canonicalization layer.

The repository now has a shared status grammar without erasing domain meaning.

The next safe architectural step is:

```txt
Use CanonicalReportContract in new active reports, then add mappings for any newly introduced domain statuses before those statuses are treated as permissions.
```

Final discipline note:

```txt
Canonicalization must increase clarity without erasing domain meaning.
```
