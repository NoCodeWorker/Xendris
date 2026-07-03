"""Small markdown renderers for benchmarking artifacts."""

from __future__ import annotations


def render_key_value_report(title: str, payload: dict) -> str:
    lines = [f"# {title}", ""]
    for key, value in payload.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            lines.append(f"- {key}: `{value}`")
    return "\n".join(lines) + "\n"
