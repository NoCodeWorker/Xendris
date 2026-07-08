"""Configuration for provider smoke runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SmokeConfig:
    run_id: str = "finitexo_v0_5_mock_smoke"
    provider_mode: str = "mock"
    providers: tuple[str, ...] = ("mock_provider",)
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_provider_smoke")
    max_iterations_per_task: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    budget_cap_usd: float = 0.50
    require_explicit_real_provider_confirmation: bool = True
    allow_network_only_in_real_mode: bool = False
    statistical_claim_authorized: bool = False
    provider_superiority_claim_authorized: bool = False
    xendris_superiority_claim_authorized: bool = False
    provider_models: dict[str, str] = field(default_factory=lambda: {"mock_provider": "mock-smoke-model"})

    def validate(self) -> None:
        if self.statistical_claim_authorized:
            raise ValueError("statistical claims are not authorized")
        if self.provider_superiority_claim_authorized:
            raise ValueError("provider superiority claims are not authorized")
        if self.xendris_superiority_claim_authorized:
            raise ValueError("Xendris superiority claims are not authorized")
        if self.provider_mode == "real" and self.require_explicit_real_provider_confirmation:
            raise ValueError("real provider mode requires explicit external confirmation")
