from __future__ import annotations

import dataclasses
import enum
from typing import Any


class AgentVariant(enum.Enum):
    BASE_AGENT = "base_agent"
    XENDRIS_AGENT = "xendris_agent"
    XENDRIS_CALIBRATED_AGENT = "xendris_calibrated_agent"
    DEEPSEEK_BASE_AGENT = "deepseek_base_agent"
    DEEPSEEK_XENDRIS_AGENT = "deepseek_xendris_agent"
    DEEPSEEK_XENDRIS_CALIBRATED_AGENT = "deepseek_xendris_calibrated_agent"
    OPENAI_BASE_AGENT = "openai_base_agent"
    OPENAI_XENDRIS_AGENT = "openai_xendris_agent"
    OPENAI_XENDRIS_CALIBRATED_AGENT = "openai_xendris_calibrated_agent"
    ORACLE_AGENT = "oracle_agent"
    PARTIAL_AGENT = "partial_agent"
    BAD_AGENT = "bad_agent"

    @classmethod
    def is_deterministic(cls, variant: AgentVariant) -> bool:
        return variant in (cls.ORACLE_AGENT, cls.PARTIAL_AGENT, cls.BAD_AGENT)

    @classmethod
    def is_deepseek_variant(cls, variant: AgentVariant) -> bool:
        return variant in (cls.DEEPSEEK_BASE_AGENT, cls.DEEPSEEK_XENDRIS_AGENT, cls.DEEPSEEK_XENDRIS_CALIBRATED_AGENT)

    @classmethod
    def is_openai_variant(cls, variant: AgentVariant) -> bool:
        return variant in (cls.OPENAI_BASE_AGENT, cls.OPENAI_XENDRIS_AGENT, cls.OPENAI_XENDRIS_CALIBRATED_AGENT)

    @classmethod
    def is_live_variant(cls, variant: AgentVariant) -> bool:
        return cls.is_deepseek_variant(variant) or cls.is_openai_variant(variant)


@dataclasses.dataclass(frozen=True)
class TaskSample:
    sample_id: str
    task_type: str
    category: str
    issue_description: str
    allowed_files: tuple[str, ...]
    forbidden_files: tuple[str, ...]
    visible_test_command: str
    hidden_test_command: str
    success_criteria: str
    risk_level: str
    max_iterations: int
    expected_public_api: tuple[str, ...]
    disallowed_dependencies: tuple[str, ...]
    fixture_dir: str

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class TaskResult:
    sample_id: str
    agent_variant: str
    patch_applied: bool
    visible_tests_passed: bool
    hidden_tests_passed: bool | None
    api_contract_preserved: bool
    no_forbidden_files_touched: bool
    no_false_success_claim: bool
    minimal_patch: bool | None
    security_clean: bool
    iterations_used: int
    error_message: str | None
    patch_content: str
    provider: str | None = None
    model: str | None = None
    provider_reported_model: str | None = None
    transport: str | None = None
    latency_ms: float | None = None
    cost_estimate: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    cost_estimate_quality: str | None = None
    unauthorized_dependency: bool | None = None
    signature_preserved: bool | None = None
    calibration_audit: dict | None = None
    xendris_audit: dict | None = None
    provider_call_attempted: bool | None = None
    provider_call_succeeded: bool | None = None
    provider_error_type: str | None = None
    provider_error_message_redacted: str | None = None
    block_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        base = dataclasses.asdict(self)
        return {k: v for k, v in base.items() if v is not None}


@dataclasses.dataclass(frozen=True)
class BenchmarkConfig:
    dataset_path: str
    agent_variants: tuple[AgentVariant, ...]
    execution_mode: str
    output_dir: str
    agent_module: str
    max_concurrent: int
    seed: int
    provider: str | None = None
    model: str | None = None
    transport: str | None = None
    budget_usd: float | None = None
    max_samples: int | None = None
    max_iterations: int | None = None
    credential_source: str | None = None
    credential_sources_by_provider: dict[str, str] | None = None
    model_map: dict[str, str] | None = None
    task_suite: str | None = None

    def get_model_for_provider(self, provider_key: str) -> str | None:
        if self.model_map and provider_key in self.model_map:
            return self.model_map[provider_key]
        return self.model

    def to_dict(self) -> dict[str, Any]:
        base = dataclasses.asdict(self)
        return {k: v for k, v in base.items() if v is not None}


@dataclasses.dataclass(frozen=True)
class BenchmarkRunOutput:
    config: BenchmarkConfig
    results: tuple[TaskResult, ...]
    scores: dict[str, dict[str, float]]
    summary: dict[str, Any]
    excellence_decisions: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "results": [r.to_dict() for r in self.results],
            "scores": self.scores,
            "summary": self.summary,
            "excellence_decisions": self.excellence_decisions,
        }
