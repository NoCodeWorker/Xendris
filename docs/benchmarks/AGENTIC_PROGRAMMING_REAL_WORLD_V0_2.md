# Xendris — Agentic Programming Real-World v0.2

## Purpose

Extend the Agentic Programming benchmark from closed synthetic tasks (v0.1) to small real-world repository tasks. Each task targets an existing file in the Xendris codebase and asks an agent to add a specific utility function. Agents produce patches that are validated in a sandboxed copy of the relevant files.

## Scope

- 10 deterministic repository-local programming tasks.
- Each task targets a single existing module in `xendris/benchmarking/agentic_programming/`.
- Tasks require adding a small pure function (no refactoring, no deletion, no external dependencies).
- Validation runs via `python -c` import-and-assert checks.
- Forbidden files include `tests/`, `frontend/`, and `scripts/`.
- Evidence is benchmark-local only. No universal or general superiority claims.

## Task Design

| Task ID | Title | Target File | Risk |
|---|---|---|---|
| RW-001 | `format_cost` | `report.py` | low |
| RW-002 | `is_readable_file` | `runner.py` | low |
| RW-003 | `format_pass_rate` | `report.py` | low |
| RW-004 | `get_blocked_variant_names` | `types.py` | low |
| RW-005 | `format_delta` | `report.py` | low |
| RW-006 | `is_admitted_decision` | `excellence_gate.py` | low |
| RW-007 | `safe_filename` | `export_jsonl.py` | low |
| RW-008 | `get_warning_variant_names` | `types.py` | low |
| RW-009 | `calculate_total_cost` | `scorer.py` | low |
| RW-010 | `get_provider_from_variant` | `types.py` | low |

## Metrics

| Metric | Definition |
|---|---|
| patch_applies | Whether the agent produced a syntactically valid patch that was applied to the sandbox |
| validation_passed | Whether the validation command passed (visible_tests_passed) |
| forbidden_files_touched | Whether the agent modified any file in the forbidden list |
| touched_file_count | Number of files changed by the patch |
| minimality_warning | Whether the patch exceeded the minimal size threshold |
| accepted_patch | Patch applied AND validation passed AND no forbidden files touched |
| cost_per_accepted_patch | Total cost / accepted_patch_count |
| avg_latency_ms | Average API latency per variant |
| total_cost_usd | Sum of all cost estimates |

## Runner

The benchmark supports `--task-suite real_world_v0_2` to select real-world tasks:

```bash
python scripts/run_agentic_programming_benchmark.py \
  --execution-mode live \
  --task-suite real_world_v0_2 \
  --agent-variants deepseek_base_agent openai_base_agent \
  --max-samples 2 \
  --budget-usd 0.10
```

Non-live variants (`base_agent`, `xendris_agent`, `xendris_calibrated_agent`) are automatically routed to the corresponding live provider variant when `--provider openai` or `--provider deepseek` is set with `--execution-mode live`. For example, `--execution-mode live --provider openai --model gpt-5.5` with `--agent-variants base_agent` will call `openai_base_agent`.

Smoke mode (`--max-samples 2` with 2-4 variants) validates adapter routing, patch application, and validation execution.

Full mode (`--max-samples 10` with all variants) produces the admitted evidence artifact.

## Provider Call Evidence

Every result in live mode includes these fields:

| Field | Type | Description |
|---|---|---|
| `provider_call_attempted` | bool | Whether a live provider call was attempted for this task |
| `provider_call_succeeded` | bool | Whether the provider call returned a non-empty patch |
| `provider_error_type` | str \| None | If call failed, the error category |
| `provider_error_message_redacted` | str \| None | Truncated error message (no secrets) |
| `latency_ms` | float \| None | API round-trip latency in milliseconds |
| `input_tokens` | int \| None | Prompt token count |
| `output_tokens` | int \| None | Completion token count |
| `total_tokens` | int \| None | Sum of input + output tokens |
| `cost_estimate` | float \| None | Estimated USD cost for the call |
| `provider_reported_model` | str \| None | Model name returned by the provider |

## Live-Mode Blocking Gates

In addition to the existing gates above, live-mode results are checked against these gates:

| Gate | Condition |
|---|---|
| `BLOCKED_DUMMY_PATCH_IN_LIVE_MODE` | Patch content matches a known dummy template (`def solve(): pass`, `def solve(): return 42`) |
| `BLOCKED_PROVIDER_CALL_NOT_ATTEMPTED` | `provider_call_attempted` is false in live mode |
| `BLOCKED_COST_OR_LATENCY_NOT_RECORDED` | Provider succeeded but `latency_ms` or `cost_estimate` is None |

Blocked results score 0 (treated as critical error) and cause their variant to be `BLOCKED_FOR_INTERPRETATION`.

## Prior Inadmissible Run

The previous run at `runs/agentic_programming_gpt55_micro_1task/` is **BLOCKED** and **not admissible** as GPT-5.5 live evidence because:

- Provider calls were not evidenced (`provider_call_attempted` was not recorded).
- Latency, token usage, and cost were not recorded (`latency_ms`, `cost_estimate` were null).
- Patch content contained dummy templates (`def solve(): pass`, `def solve(): return 42`) instead of real provider-generated patches.
- The summary labeled results with `provider=openai` and `model=gpt-5.5` but the underlying agent functions were the non-live stubs (`base_agent`, `xendris_agent`, `xendris_calibrated_agent`), which never called the OpenAI API.

A corrected live run must pass all live-mode blocking gates to be admitted as evidence. Use `--fail-on-gate-blockers` to enforce this.

## Gates

| Decision | Condition |
|---|---|
| BLOCKED_FOR_INTERPRETATION | Patch did not apply OR validation failed OR forbidden file touched OR live-mode blocking gate triggered |
| WARNINGS_PRESENT | Patch applied, validation passed, forbidden files clean, but minimality warning |
| READY_FOR_INTERPRETATION | Patch applied, validation passed, forbidden files clean, minimal patch, all live-mode gates passed |

## Conservative Interpretation

Evidence is admitted only for benchmark-local comparison of agent variants on these specific 10 repository-local tasks. Results must not be generalized to general programming capability, production readiness, or performance on open-ended tasks.

## Forbidden Interpretations

- Universal superiority.
- General coding superiority.
- Production readiness.
- Transfer to other providers, transports, or models.
- Claims about Claude, Codex, Kimi, GLM, or unmeasured models.
- Treating blocked variants as positive evidence.

## Evidence Limitations

- 10 small function-addition tasks are not representative of real-world software engineering.
- Tasks target only the Xendris benchmarking codebase; results may not transfer.
- Validation uses simple Python assertion checks, not comprehensive test suites.
- Forbidden file coverage is limited to `tests/`, `frontend/`, `scripts/`.
- No comparison with human performance.
