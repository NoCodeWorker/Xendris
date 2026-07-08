"""Configuration for v0.7.0 paired Xendris lift n=30."""

from __future__ import annotations

import dataclasses
import os
import re
from dataclasses import dataclass, field
from pathlib import Path


SUFFIX_ALLOWED_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def validate_run_id_suffix(suffix: str) -> str:
    suffix = suffix.strip()
    if not suffix:
        raise ValueError("Run ID suffix must not be empty.")
    if not SUFFIX_ALLOWED_RE.match(suffix):
        raise ValueError(
            f"Run ID suffix {suffix!r} contains invalid characters. "
            "Only letters, numbers, underscore, and hyphen are allowed."
        )
    return suffix


@dataclass(frozen=True)
class PairedLiftVariantSpec:
    variant_name: str
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00025
    use_xendris_wrapper: bool = False
    endpoint_url: str = ""


@dataclass(frozen=True)
class PairedLiftConfig:
    run_id: str = "finitexo_v0_7_0_paired_xendris_lift_n30"
    provider_mode: str = "real"
    variants: tuple[PairedLiftVariantSpec, ...] = field(
        default_factory=lambda: (
            PairedLiftVariantSpec(
                "deepseek_base", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, False,
                "https://api.deepseek.com/chat/completions",
            ),
            PairedLiftVariantSpec(
                "deepseek_xendris", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, True,
                "https://api.deepseek.com/chat/completions",
            ),
            PairedLiftVariantSpec(
                "openai_base", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, False,
                "https://api.openai.com/v1/chat/completions",
            ),
            PairedLiftVariantSpec(
                "openai_xendris", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, True,
                "https://api.openai.com/v1/chat/completions",
            ),
        )
    )
    dataset_path: Path = Path(
        "benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30"
    )
    output_dir: Path = Path(
        "runs/finitexo_code_matrix_v0_7_0_paired_xendris_lift_n30"
    )
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    suffix_env_var: str = "FINITEXO_PAIRED_LIFT_RUN_ID_SUFFIX"
    expected_task_count: int = 30
    expected_attempts: int = 120
    budget_cap_usd: float = 0.75
    soft_target_usd: float = 0.30
    max_attempts_per_task_pair: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    request_timeout_seconds: float = 60.0
    allow_mock_fallback: bool = False
    allow_overwrite: bool = False
    expected_dataset_hash: str = (
        "04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010"
    )
    expected_manifest_hash: str = (
        "073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519"
    )
    environ: dict[str, str] = field(default_factory=lambda: dict(os.environ))

    def with_run_id_suffix(self, suffix: str) -> PairedLiftConfig:
        valid = validate_run_id_suffix(suffix)
        new_run_id = f"{self.run_id}_{valid}"
        new_dir = self.output_dir.parent / f"{self.output_dir.name}_{valid}"
        return dataclasses.replace(self, run_id=new_run_id, output_dir=new_dir)
