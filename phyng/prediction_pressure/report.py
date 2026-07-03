"""
Phygn v1.3 — Prediction Pressure Reporting

Generates markdown reports for positive prediction gate and kill/pivot criteria.
"""

from __future__ import annotations

from pathlib import Path
from phyng.prediction_pressure.schemas import PositivePredictionGateResult, KillPivotResult

def write_prediction_pressure_reports(
    project_root: Path,
    gate_res: PositivePredictionGateResult,
    kp_res: KillPivotResult,
) -> list[str]:
    """
    Writes the two prediction pressure reports to reports/prediction_pressure/.
    """
    out_dir = project_root / "reports" / "prediction_pressure"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    p1 = out_dir / "positive_prediction_gate_v1_3.md"
    p1_lines = [
        "# Positive Prediction Gate Report — v1.3",
        "",
        f"- **Status**: **{gate_res.status}**",
        f"- **Message**: {gate_res.message}",
        ""
    ]
    if gate_res.missing_fields:
        p1_lines.extend([
            "### Missing Operationalization Fields",
            "",
            *[f"- `{f}`" for f in gate_res.missing_fields],
            ""
        ])
    p1_lines.extend([
        "## Discipline Note",
        "A theory that only blocks claims can become scientifically sterile.",
        "Frontera C must earn the right to predict."
    ])
    p1.write_text("\n".join(p1_lines), encoding="utf-8")
    
    p2 = out_dir / "kill_pivot_criteria_v1_3.md"
    p2_lines = [
        "# Kill / Pivot Criteria Report — v1.3",
        "",
        f"- **Status**: **{kp_res.status}**",
        f"- **Conclusion**: {kp_res.conclusion}",
        f"- **Rationale**: {kp_res.rationale}",
        "",
        "## Positive Prediction Roadmap",
        "- v1.4 — Source Pack Ingestion Attempt",
        "- v1.5 — Candidate Model Definition",
        "- v1.6 — Candidate vs Baseline Benchmark",
        "- v1.7 — Detectability & Failure Report",
        "",
        "## Red Team Statement",
        "If Frontera C cannot generate a candidate model that improves or differs detectably",
        "from a source-backed baseline, then it should be demoted from predictive theory",
        "to structural/epistemic framework.",
        "A theory that cannot risk losing cannot earn the right to win."
    ]
    p2.write_text("\n".join(p2_lines), encoding="utf-8")
    
    return [str(p1), str(p2)]
