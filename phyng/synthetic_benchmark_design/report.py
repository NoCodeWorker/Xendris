"""Report writers for v2.3 synthetic benchmark design."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.synthetic_benchmark_design.schemas import HeuristicToBenchmarkCampaignResult


def write_synthetic_benchmark_design_reports(
    result: HeuristicToBenchmarkCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    design_dir = root / "synthetic_benchmark_design"
    campaigns_dir = root / "campaigns"
    design_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "formalization": design_dir / "log_boundary_candidate_formalization_v2_3.md",
        "design": design_dir / "log_boundary_synthetic_benchmark_design_v2_3.md",
        "detectability": design_dir / "log_boundary_detectability_failure_protocol_v2_3.md",
        "contract": design_dir / "heuristic_to_benchmark_canonical_contract_v2_3.md",
        "campaign": campaigns_dir / "HEURISTIC-CANDIDATE-SYNTHETIC-BENCHMARK-v2_3.md",
    }
    paths["formalization"].write_text(_canonical(_render_formalization(result), result.status, result.campaign_id), encoding="utf-8")
    paths["design"].write_text(_canonical(_render_design(result), result.status, result.campaign_id), encoding="utf-8")
    paths["detectability"].write_text(_canonical(_render_detectability(result), result.status, result.campaign_id), encoding="utf-8")
    paths["contract"].write_text(_canonical(_render_contract(result), result.status, result.campaign_id), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result.status, result.campaign_id, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, status: str, campaign_id: str, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Heuristic Candidate Synthetic Benchmark v2.3",
        campaign_id=campaign_id,
        domain_status=status,
        reports_generated=reports_generated or [],
        discipline_note="Synthetic benchmark design is not physical validation.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_formalization(result: HeuristicToBenchmarkCampaignResult) -> str:
    spec = result.candidate_spec
    return "\n".join([
        "# LOG_BOUNDARY Candidate Formalization v2.3",
        "",
        f"- Candidate ID: `{spec.candidate_id}`",
        f"- Candidate Family: `{spec.candidate_family}`",
        "- Heuristic Origin: `HEUR-PHY-003 / LOG_BOUNDARY`",
        f"- Observable: `{spec.observable}`",
        f"- Baseline Equation: `{spec.baseline_equation}`",
        f"- Candidate Equation: `{spec.candidate_equation}`",
        f"- DeltaGamma Equation: `{spec.delta_gamma_equation}`",
        f"- Phi Function: `{spec.phi_function}`",
        f"- Dimensionless Variables: `{', '.join(spec.dimensionless_variables)}`",
        "",
        "## Parameter Ranges",
        "",
        *[f"- `{key}`: `{value}`" for key, value in spec.parameter_ranges.items()],
        "",
        "## Failure Conditions",
        "",
        *[f"- `{item}`" for item in spec.failure_conditions],
        "",
        "## Blocked Claims",
        "",
        "- LOG_BOUNDARY predicts decoherence.",
        "- LOG_BOUNDARY validates Frontera C.",
        "- Synthetic design proves a physical effect.",
    ]) + "\n"


def _render_design(result: HeuristicToBenchmarkCampaignResult) -> str:
    design = result.design_result.benchmark_design
    if design is None:
        return "# LOG_BOUNDARY Synthetic Benchmark Design v2.3\n\nDesign blocked by admissibility checks.\n"
    return "\n".join([
        "# LOG_BOUNDARY Synthetic Benchmark Design v2.3",
        "",
        f"- Candidate ID: `{design.candidate_id}`",
        f"- Baseline Model: `{design.baseline_model}`",
        f"- Candidate Model: `{design.candidate_model}`",
        f"- Delta Metric: `{design.delta_metric}`",
        f"- Epsilon Experimental Threshold: `{design.epsilon_exp}`",
        f"- t_grid_count: `{len(design.t_grid)}`",
        "",
        "## Parameter Sweep Plan",
        "",
        *[f"- `{key}`: `{value}`" for key, value in design.parameter_sweep_plan.items()],
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in result.design_result.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.design_result.blocked_claims],
    ]) + "\n"


def _render_detectability(result: HeuristicToBenchmarkCampaignResult) -> str:
    protocol = result.design_result.detectability_protocol
    if protocol is None:
        return "# LOG_BOUNDARY Detectability Failure Protocol v2.3\n\nProtocol blocked by admissibility checks.\n"
    return "\n".join([
        "# LOG_BOUNDARY Detectability Failure Protocol v2.3",
        "",
        f"- V_base: `{protocol.baseline_equation}`",
        f"- V_log: `{protocol.candidate_equation}`",
        f"- delta(t): `{protocol.delta_equation}`",
        f"- max_abs_delta: `{protocol.detectability_metric}`",
        f"- epsilon_exp: `{protocol.epsilon_exp}`",
        f"- detectability_classification: `{protocol.detectability_classification_rule}`",
        "",
        "## Failure Classification Rules",
        "",
        *[f"- `{rule}`" for rule in protocol.failure_classification_rules],
    ]) + "\n"


def _render_contract(result: HeuristicToBenchmarkCampaignResult) -> str:
    return "\n".join([
        "# Heuristic-to-Benchmark Canonical Contract v2.3",
        "",
        "## Required Sections",
        "",
        "- Title",
        "- Date",
        "- Candidate ID",
        "- Candidate Family",
        "- Heuristic Origin",
        "- Canonical Status",
        "- Observable",
        "- Baseline Equation",
        "- Candidate Equation",
        "- Dimensionless Variables",
        "- Parameter Ranges",
        "- Detectability Metric",
        "- Failure Conditions",
        "- Synthetic Benchmark Design",
        "- Allowed Claims",
        "- Blocked Claims",
        "- Next Actions",
        "- Tests",
        "- Discipline Note",
    ]) + "\n"


def _render_campaign(result: HeuristicToBenchmarkCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - HEURISTIC-CANDIDATE-SYNTHETIC-BENCHMARK-v2_3",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- candidate_id: `{result.candidate_spec.candidate_id}`",
        f"- candidate_family: `{result.candidate_spec.candidate_family}`",
        "",
        "## Core Results",
        "",
        "- LOG_BOUNDARY has an explicit synthetic benchmark design.",
        "- LOG_BOUNDARY is ready for synthetic execution.",
        "- LOG_BOUNDARY remains unsupported by sources/data.",
        "",
        "## Blocked Claims",
        "",
        "- LOG_BOUNDARY predicts decoherence.",
        "- LOG_BOUNDARY validates Frontera C.",
        "- Synthetic design proves the effect.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
        "",
        "## Tests",
        "",
        "- `tests/test_log_boundary_candidate_formalization_v2_3.py`",
        "- `tests/test_log_boundary_admissibility_v2_3.py`",
        "- `tests/test_synthetic_benchmark_design_v2_3.py`",
        "- `tests/test_log_boundary_detectability_protocol_v2_3.py`",
        "- `tests/test_heuristic_to_benchmark_report_contract_v2_3.py`",
        "- `tests/test_heuristic_candidate_synthetic_benchmark_campaign_v2_3.py`",
    ]) + "\n"
