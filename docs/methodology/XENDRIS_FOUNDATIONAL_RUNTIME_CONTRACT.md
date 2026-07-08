# Xendris Foundational Runtime Contract

## Non-Negotiable Doctrine

**Xendris Runtime is not a wrapper.**
**Xendris Calibrated Runtime is not a stylistic prompt.**

Runtime requires post-generation deterministic control.
Calibrate requires epistemic claim/status/language calibration.

These are foundational epistemic mechanisms and must be enforced by code, tests, and documentation.

## Execution Methods

| Method | Description |
|--------|-------------|
| `BASE` | Direct provider call, no modification. Score initial output. |
| `WRAPPER` | Provider call with Xendris admissibility instructions prepended. Score initial output. No post-generation control. |
| `RUNTIME` | Provider initial call → deterministic audit → audit decision → repair/degrade/block → final response → final audit. |
| `CALIBRATED_RUNTIME` | All runtime phases + claim classification + evidence status resolution + confidence banding + allowed/blocked language selection + final calibrated response. |

## Runtime Required Phases

1. **Initial generation** — provider produces a raw response.
2. **Deterministic audit** — structured evaluation of the response against defined criteria.
3. **Audit decision** — ALLOW, ALLOW_WITH_LIMITATIONS, REPAIR_REQUIRED, BLOCK, or HUMAN_REVIEW_REQUIRED.
4. **Repair/degrade/block consideration** — if repair is needed and possible, a repair pass occurs; otherwise degrade or block.
5. **Final response selection** — the best admissible response is selected (repaired, initial, or controlled limitation).
6. **Final audit** — the selected response is audited before recording.

## Calibrated Runtime Required Phases

All runtime phases (1-6) plus:

7. **Claim classification** — each substantive claim in the response is classified by type.
8. **Evidence status resolution** — each claim is assigned an evidence status.
9. **Confidence banding** — response-level or claim-level confidence is assigned.
10. **Allowed language selection** — language that is safe and appropriate is identified.
11. **Blocked language selection** — language that is unsafe, exaggerated, or inappropriate is identified or removed.
12. **Final calibrated response** — the response is finalized with calibrated language only.

## Forbidden Substitutions

The following are explicitly forbidden:

- Calling a prompt wrapper "runtime."
- Calling tone adjustment "calibration."
- Scoring the initial provider response as the runtime final response without audit.
- Reporting wrapper lift as runtime lift.
- Reporting calibrated runtime without calibration traces.
- Using runtime terminology in benchmark documentation when runtime traces do not exist.

## Required Artifacts for Runtime Benchmarks

1. `runtime_traces.jsonl` — full trace of every runtime variant execution.
2. `audit_decisions.jsonl` — audit decision per runtime variant per task.
3. `repair_attempts.jsonl` — repair pass details per attempt.
4. `final_audits.jsonl` — final audit results after selection/remediation.

## Required Artifacts for Calibrated Runtime Benchmarks

All runtime artifacts plus:

1. `calibration_traces.jsonl` — full calibration trace per calibrated variant per task.
2. `claim_status.jsonl` — claim-level status assignments.
3. `confidence_bands.jsonl` — confidence band assignments.
4. `allowed_blocked_language.jsonl` — language selection decisions.
5. `calibrated_final_responses.jsonl` — final calibrated responses.

## Claim Policy

### Allowed

- "This benchmark evaluates wrapper behavior" — only if the benchmark uses wrapper variants and does not claim runtime.
- "This benchmark evaluates runtime behavior" — only if runtime traces exist and pass the methodology guard.
- "This benchmark evaluates calibrated runtime behavior" — only if calibration traces exist and pass the methodology guard.

### Blocked

- "Xendris runtime was evaluated" when only wrapper was evaluated.
- "Xendris calibrated runtime was evaluated" without calibration traces.
- "Wrapper results generalize to runtime."
- "Runtime results generalize universally."
- "Statistical superiority" without a separate statistical gate.

## Development Rule

Any future benchmark version that touches Xendris Runtime or Calibrated Runtime must import and pass the methodology guard before execution.

## Final Doctrine Decision

`FOUNDATIONAL_RUNTIME_CONTRACT_ESTABLISHED`
