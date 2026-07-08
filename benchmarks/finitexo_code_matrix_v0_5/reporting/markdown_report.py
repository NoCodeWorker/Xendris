"""Public markdown rendering wrapper."""

from __future__ import annotations

from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.smoke_report_builder import build_markdown_report


def render_report(summary: dict[str, Any]) -> str:
    return build_markdown_report(summary)
