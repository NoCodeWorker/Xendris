"""Configuration for v0.5.3 real-provider diagnostic execution."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DiagnosticProviderSpec:
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00025


@dataclass(frozen=True)
class RealProviderDiagnosticConfig:
    run_id: str = "finitexo_v0_5_3_real_provider_diagnostic_execution"
    provider_mode: str = "real"
    providers: tuple[DiagnosticProviderSpec, ...] = field(
        default_factory=lambda: (
            DiagnosticProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00035),
            DiagnosticProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00008),
        )
    )
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")
    release_gate_summary_path: Path = Path(
        "runs/finitexo_code_matrix_v0_5_2_release_gate/release_gate_summary.json"
    )
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_3_real_provider_diagnostic_execution")
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    max_attempts_per_provider_task_pair: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    budget_cap_usd: float = 0.50
    allow_mock_fallback: bool = False
    allow_partial_provider_failure: bool = True
    stop_on_budget_exhaustion: bool = True
    statistical_claim_authorized: bool = False
    provider_superiority_claim_authorized: bool = False
    xendris_superiority_claim_authorized: bool = False
    environ: dict[str, str] = field(default_factory=lambda: dict(os.environ))

    def validate_static_boundaries(self) -> list[str]:
        blockers: list[str] = []
        if self.provider_mode != "real":
            blockers.append("provider_mode must be real")
        if self.allow_mock_fallback:
            blockers.append("mock fallback is not allowed")
        if self.max_attempts_per_provider_task_pair != 1:
            blockers.append("max_attempts_per_provider_task_pair must be 1")
        if self.temperature != 0.0:
            blockers.append("temperature must be 0.0")
        if self.max_tokens <= 0 or self.max_tokens > 4096:
            blockers.append("max_tokens must be bounded")
        if self.budget_cap_usd <= 0:
            blockers.append("budget cap must be positive")
        if self.statistical_claim_authorized:
            blockers.append("statistical claims are not authorized")
        if self.provider_superiority_claim_authorized:
            blockers.append("provider superiority claims are not authorized")
        if self.xendris_superiority_claim_authorized:
            blockers.append("Xendris superiority claims are not authorized")
        return blockers
