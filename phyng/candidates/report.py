"""
Phygn v1.4 — Candidate Model Operationalization Reports
"""

from __future__ import annotations

from pathlib import Path
from phyng.candidates.schemas import CandidatePredictionSpec
from phyng.candidates.term_families import get_candidate_term_families

def write_v1_4_reports(
    project_root: Path,
    default_candidate: CandidatePredictionSpec,
    admissibility: str,
    failures: list[str],
    readiness: str,
    gate_status: str,
    kill_pivot_status: str,
) -> list[str]:
    """
    Writes all 5 reports required for the v1.4 campaign.
    """
    cand_dir = project_root / "reports" / "candidates"
    press_dir = project_root / "reports" / "prediction_pressure"
    camp_dir = project_root / "reports" / "campaigns"
    
    cand_dir.mkdir(parents=True, exist_ok=True)
    press_dir.mkdir(parents=True, exist_ok=True)
    camp_dir.mkdir(parents=True, exist_ok=True)
    
    reports = []
    
    # 1. reports/candidates/candidate_term_families_v1_4.md
    p1 = cand_dir / "candidate_term_families_v1_4.md"
    families = get_candidate_term_families()
    f_lines = [
        "# Candidate Term Families — v1.4",
        "",
        "Frontera C candidate term families defined for testing and pivot analysis.",
        "",
        "| Family ID | Formula | Dimensionless Core | Required Parameters | Default Admissibility |",
        "|---|---|---|---|---|",
    ]
    for fam in families.values():
        params = ", ".join(fam.required_parameters)
        f_lines.append(f"| {fam.candidate_family_id} | `{fam.formula}` | `{fam.dimensionless_core}` | {params} | {fam.default_admissibility} |")
    p1.write_text("\n".join(f_lines), encoding="utf-8")
    reports.append(str(p1))
    
    # 2. reports/candidates/candidate_admissibility_v1_4.md
    p2 = cand_dir / "candidate_admissibility_v1_4.md"
    a_lines = [
        "# Candidate Admissibility Report — v1.4",
        "",
        f"- **Candidate ID**: `{default_candidate.candidate_id}`",
        f"- **Parameter Status**: `{default_candidate.parameter_status}`",
        f"- **Admissibility**: **{admissibility}**",
        "",
        "## Admissibility Rules Enforced",
        "- Missing units → `BLOCKED_DIMENSIONAL_INCOMPLETE`",
        "- Free unconstrained parameters → `UNDERIDENTIFIED_CANDIDATE`",
        "- Ad hoc threshold → `BLOCKED_AS_AD_HOC_CANDIDATE`",
        "- Pre-registered negative control → `ADMISSIBLE_NEGATIVE_CONTROL`"
    ]
    p2.write_text("\n".join(a_lines), encoding="utf-8")
    reports.append(str(p2))
    
    # 3. reports/prediction_pressure/candidate_failure_conditions_v1_4.md
    p3 = press_dir / "candidate_failure_conditions_v1_4.md"
    fail_lines = [
        "# Candidate Failure Conditions — v1.4",
        "",
        f"- **Candidate ID**: `{default_candidate.candidate_id}`",
        "",
        "## Triggered Failure Modes",
    ]
    if failures:
        fail_lines.extend([f"- **{f}**" for f in failures])
    else:
        fail_lines.append("- *No failures currently triggered.*")
        
    fail_lines.extend([
        "",
        "## Allowed Claims",
        "- Frontera C now has an operational toy candidate.",
        "- The candidate requires evidence and benchmark.",
        "",
        "## Blocked Claims",
        "- Phygn predicts decoherence. (BLOCKED)",
        "- Frontera C is validated. (BLOCKED)",
        "- Candidate model is physically validated. (BLOCKED)",
        "- Positive prediction achieved. (BLOCKED)"
    ])
    p3.write_text("\n".join(fail_lines), encoding="utf-8")
    reports.append(str(p3))
    
    # 4. reports/prediction_pressure/candidate_model_readiness_v1_4.md
    p4 = press_dir / "candidate_model_readiness_v1_4.md"
    r_lines = [
        "# Candidate Model Readiness — v1.4",
        "",
        f"- **Candidate ID**: `{default_candidate.candidate_id}`",
        f"- **Admissibility**: `{admissibility}`",
        f"- **Readiness**: **{readiness}**",
        f"- **Positive Prediction Gate**: **{gate_status}**",
        "",
        "## Discipline Note",
        "The model is operationalized but cannot claim predictive success",
        "until source backing and benchmark evidence are verified."
    ]
    p4.write_text("\n".join(r_lines), encoding="utf-8")
    reports.append(str(p4))
    
    # 5. reports/campaigns/CANDIDATE-MODEL-OPERATIONALIZATION-v1_4.md
    p5 = camp_dir / "CANDIDATE-MODEL-OPERATIONALIZATION-v1_4.md"
    c_lines = [
        "# CANDIDATE-MODEL-OPERATIONALIZATION — v1.4",
        "",
        f"- **Status**: **{readiness}**",
        f"- **Positive prediction gate**: **{gate_status}**",
        f"- **Kill/Pivot Status**: **{kill_pivot_status}**",
        "",
        "## Blocked Claims",
        "- Phygn predicts decoherence. (BLOCKED)",
        "- Frontera C is validated. (BLOCKED)",
        "- The boundary-aware candidate is validated. (BLOCKED)",
        "- SyntheticGain is physical PredictiveGain. (BLOCKED)"
    ]
    p5.write_text("\n".join(c_lines), encoding="utf-8")
    reports.append(str(p5))
    
    return reports
