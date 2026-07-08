"""Configuration for v0.6.0 real-provider controlled run n=30."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ControlledProviderSpec:
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00025
    endpoint_url: str = ""


@dataclass(frozen=True)
class ControlledRunConfig:
    run_id: str = "finitexo_v0_6_0_real_provider_controlled_run_n30"
    provider_mode: str = "real"
    providers: tuple[ControlledProviderSpec, ...] = field(
        default_factory=lambda: (
            ControlledProviderSpec(
                "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY",
                0.00035, "https://api.deepseek.com/chat/completions",
            ),
            ControlledProviderSpec(
                "openai", "gpt-4.1-nano", "OPENAI_API_KEY",
                0.00008, "https://api.openai.com/v1/chat/completions",
            ),
        )
    )
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30")
    readiness_summary_path: Path = Path(
        "runs/finitexo_code_matrix_v0_5_7_real_provider_report_admissibility_gate/report_admissibility_summary.json"
    )
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30")
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    expected_task_count: int = 30
    budget_cap_usd: float = 0.50
    soft_target_usd: float = 0.20
    max_attempts_per_provider_task_pair: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    request_timeout_seconds: float = 45.0
    allow_mock_fallback: bool = False
    allow_overwrite: bool = False
    expected_dataset_hash: str = "04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010"
    expected_manifest_hash: str = "073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519"
    environ: dict[str, str] = field(default_factory=lambda: dict(os.environ))
