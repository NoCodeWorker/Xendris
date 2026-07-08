"""Configuration for v0.5.1 real-provider smoke runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RealProviderSpec:
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00025


@dataclass(frozen=True)
class RealSmokeConfig:
    run_id: str = "finitexo_v0_5_1_real_provider_smoke"
    provider_mode: str = "real"
    providers: tuple[RealProviderSpec, ...] = field(
        default_factory=lambda: (
            RealProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00035),
            RealProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00008),
        )
    )
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_1_real_provider_smoke")
    manifest_path: Path = Path("benchmarks/finitexo_code_matrix_v0_5/real_provider_smoke_manifest.json")
    max_iterations_per_task: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    budget_cap_usd: float = 0.50
    recommended_budget_target_usd: float = 0.05
    real_provider_confirmation: bool = False
    allow_mock_fallback: bool = False
    allow_partial_provider_failure: bool = True
    stop_on_budget_exhaustion: bool = True
    statistical_claim_authorized: bool = False
    provider_superiority_claim_authorized: bool = False
    xendris_superiority_claim_authorized: bool = False
    external_benchmark_validation_claim_authorized: bool = False
    production_readiness_claim_authorized: bool = False
    environ: dict[str, str] = field(default_factory=dict)

    def validate_static_boundaries(self) -> None:
        if self.provider_mode != "real":
            raise ValueError("v0.5.1 real provider smoke requires provider_mode='real'")
        if self.allow_mock_fallback:
            raise ValueError("mock fallback is not allowed for v0.5.1 real provider smoke")
        if self.max_iterations_per_task != 1:
            raise ValueError("max_iterations_per_task must be 1")
        if self.temperature != 0.0:
            raise ValueError("temperature must be 0.0")
        if self.max_tokens <= 0 or self.max_tokens > 4096:
            raise ValueError("max_tokens must be bounded")
        if self.budget_cap_usd <= 0:
            raise ValueError("budget_cap_usd must be positive")
        if self.statistical_claim_authorized:
            raise ValueError("statistical claims are not authorized")
        if self.provider_superiority_claim_authorized:
            raise ValueError("provider superiority claims are not authorized")
        if self.xendris_superiority_claim_authorized:
            raise ValueError("Xendris superiority claims are not authorized")
        if self.external_benchmark_validation_claim_authorized:
            raise ValueError("external benchmark validation claims are not authorized")
        if self.production_readiness_claim_authorized:
            raise ValueError("production-readiness claims are not authorized")
