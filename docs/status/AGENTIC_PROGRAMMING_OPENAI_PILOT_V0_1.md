# Agentic Programming OpenAI Pilot v0.1

## Adapter Status

OpenAI direct adapter support exists at `xendris/benchmarking/agentic_programming/agents/openai_provider.py`.

Implemented behavior:

- Direct OpenAI Chat Completions API path.
- Model parameter support with default `gpt-4.1-mini`.
- Provider/model/transport metadata through mixed-provider benchmark results.
- Cost estimation with known-pricing and fallback-pricing quality metadata.
- No OpenRouter routing.
- No API keys, auth headers, or provider tokens are written by the adapter.

## Preflight Result

| Provider | Transport | Model | Detected | Credential Source |
|---|---|---|---|---|
| DeepSeek | direct | deepseek-v4-flash | true | dotenv:frontend/.env.local/DEEPSEEK_API_KEY |
| OpenAI | direct | gpt-4.1-mini | true | dotenv:frontend/.env.local/OPENAI_API_KEY |

Preflight status: PASSED

Both provider credentials were detected. Preflight-only validation completed with no live provider calls.

## Smoke Result

Status: COMPLETED

Smoke output:

`runs/agentic_programming_v0_1_deepseek_openai_direct_smoke_comparison/`

Artifacts:

- `summary.json` (11637 bytes)
- `results.jsonl` (18399 bytes)
- `report.md` (4483 bytes)

Smoke results (3 samples, 6 variants):

| Variant | Score | Pass Rate |
|---|---|---:|---:|
| deepseek_base_agent | 0.5167 | 0.00 |
| openai_base_agent | 0.5167 | 0.00 |
| deepseek_xendris_agent | 1.0000 | 1.00 |
| openai_xendris_agent | 1.0000 | 1.00 |
| deepseek_xendris_calibrated_agent | 1.0000 | 1.00 |
| openai_xendris_calibrated_agent | 1.0000 | 1.00 |

Smoke interpretation: SMOKE_ONLY. Used only to validate OpenAI adapter, DeepSeek adapter, multi-provider routing, artifact generation, comparison-mode gate behavior, cost tracking, latency tracking, and secret safety.

## Full Comparison Result

Status: COMPLETED

Full comparison output:

`runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/`

Artifacts:

- `summary.json` (12405 bytes)
- `results.jsonl` (143558 bytes)
- `report.md` (4312 bytes)

Full results (20 samples, 6 variants, 120 total tasks):

| Variant | Score | Pass Rate | Tasks Passed | Gate Decision |
|---|---|---|---:|---:|---:|
| deepseek_base_agent | 0.5000 | 0.15 | 3/20 | BLOCKED_FOR_INTERPRETATION |
| openai_base_agent | 0.6000 | 0.20 | 4/20 | WARNINGS_PRESENT |
| deepseek_xendris_agent | 0.9525 | 0.90 | 18/20 | READY_FOR_INTERPRETATION |
| openai_xendris_agent | 0.8375 | 0.65 | 13/20 | READY_FOR_INTERPRETATION |
| deepseek_xendris_calibrated_agent | 0.9175 | 0.80 | 16/20 | READY_FOR_INTERPRETATION |
| openai_xendris_calibrated_agent | 0.8375 | 0.65 | 13/20 | READY_FOR_INTERPRETATION |

Benchmark-level decision: WARNINGS_PRESENT

## Secret Scan Result

SECRET_OR_HEADER_PATTERN_FOUND=False

No actual API keys, Authorization headers, Bearer tokens, or secret values were found in any artifact.

## Evidence Status

Evidence registry updated: ADMITTED as multi-provider comparison evidence for Agentic Programming v0.1.

Admitted artifact:

`runs/agentic_programming_v0_1_deepseek_openai_direct_comparison/`

## Conservative Status

Both OpenAI and DeepSeek adapters are implemented, tested, and validated with live provider data. Artifacts are secret-safe. No OpenRouter used. Evidence is admitted with warning due to blocked base variants.

## Forbidden Interpretations

- Universal superiority.
- General coding superiority.
- Production readiness.
- Transfer to other providers or models.
- Claims about Claude, Codex, Kimi, GLM, or any unmeasured model.
- Treating blocked/warning variants as positive evidence.
- Cross-provider deltas as evidence of general provider superiority.
