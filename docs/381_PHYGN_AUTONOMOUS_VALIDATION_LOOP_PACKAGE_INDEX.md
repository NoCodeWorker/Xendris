# Phygn Autonomous Validation Loop Package Index

This package upgrades the master Frontera C validation prompt into an autonomous validate-if-possible loop with tool and knowledge self-provisioning.

## Files

```txt
375_PHYGN_AUTONOMOUS_VALIDATION_LOOP_docs/status/GOAL.md
376_PHYGN_TOOL_AND_KNOWLEDGE_SELF_PROVISIONING_PROTOCOL.md
377_PHYGN_VALIDATE_IF_POSSIBLE_LOOP_RUNTIME.md
378_PHYGN_SELF_PROVISIONING_AUDIT_SCHEMA.md
379_PHYGN_CODEX_VALIDATE_FRONTERA_C_WITH_AUTONOMOUS_LOOP_PROMPT.md
380_PHYGN_AUTONOMOUS_LOOP_RESULT_REPORT_TEMPLATE.md
381_PHYGN_AUTONOMOUS_VALIDATION_LOOP_PACKAGE_INDEX.md
```

## Main prompt

Use:

```txt
docs/379_PHYGN_CODEX_VALIDATE_FRONTERA_C_WITH_AUTONOMOUS_LOOP_PROMPT.md
```

## Core runtime

```txt
Gate → Blocker → Missing Capability → Tool/Knowledge Self-Provisioning → Tests → Re-run Gate → Continue/Stop
```

## Critical override

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT is not terminal until candidate construction/self-provisioning has been attempted and failed.
```

## Central rule

```txt
Do not stop because the next capability is missing.
Build the capability under the rails, then retry the gate.
```

## Final discipline

```txt
Validate if possible.
Block if necessary.
Falsify if forced.
Do not stop at removable absence.
```
