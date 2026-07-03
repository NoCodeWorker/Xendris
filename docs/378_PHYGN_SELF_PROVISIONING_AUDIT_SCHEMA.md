# Phygn — Self-Provisioning Audit Schema

## 0. Purpose

Every self-provisioning cycle must be auditable.

---

## 1. Required artifact

Create or update:

```txt
data/frontera_c/self_provisioning/self_provisioning_audit_log.json
```

---

## 2. Schema

```python
class SelfProvisioningAuditRecord(BaseModel):
    cycle_id: str
    phase: str
    gate_name: str
    gate_status_before: str
    blocker_id: str
    blocker_type: str
    missing_capability_type: str
    proposed_improvement: str
    why_minimal: str
    files_created: list[str]
    files_modified: list[str]
    tests_added: list[str]
    tests_run: list[str]
    tests_passed: bool
    gate_retried: bool
    gate_status_after: str
    blocker_removed: bool
    next_action: str
    forbidden_actions_avoided: list[str]
    notes: list[str]
```

---

## 3. Reporting

Create:

```txt
reports/frontera_c/self_provisioning/self_provisioning_audit_log.md
```

The report must show:

```txt
cycles used per gate
blockers encountered
capabilities built
tests added
gates retried
terminal reason
```

---

## 4. Stop conditions

If stopped, report:

```txt
why it stopped
why blocker is not removable internally
what human must provide
or what experiment must measure
```

---

## 5. Final principle

```txt
If the agent improves itself, the improvement must leave footprints.
```
