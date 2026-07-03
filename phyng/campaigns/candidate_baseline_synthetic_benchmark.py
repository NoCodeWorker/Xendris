"""
Phygn v1.5 — Candidate vs Baseline Synthetic Benchmark Campaign

Orchestrates the full synthetic benchmark for CAND-FC-B-NEGCTRL-001:
    - Runs synthetic benchmark (default alpha)
    - Runs alpha sweep
    - Generates all reports
    - Evaluates candidate survival
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from phyng.candidates.synthetic_benchmark import (
    CandidateSyntheticBenchmarkInput,
    run_synthetic_benchmark,
)
from phyng.candidates.alpha_sweep import (
    run_alpha_sweep,
    find_first_detectable_alpha,
    DEFAULT_ALPHA_VALUES,
    AlphaSweepRow,
)
from phyng.candidates.detectability import (
    classify_detectability,
    classify_alpha_reasonableness,
    estimate_alpha_min_for_detectability,
)
from phyng.candidates.failure_report_v1_5 import (
    evaluate_v1_5_failure_conditions,
    classify_candidate_survival,
)


# ---------------------------------------------------------------------------
# Default parameters (CAMPAIGN-002 mesoscopic)
# ---------------------------------------------------------------------------

DEFAULT_SYSTEM_ID = "CAMPAIGN-002-MESOSCOPIC"
DEFAULT_CANDIDATE_ID = "CAND-FC-B-NEGCTRL-001"
DEFAULT_BENCHMARK_ID = "BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001"

DEFAULT_M_KG: float = 1e-17
DEFAULT_L_VALUE_M: float = 1e-7
DEFAULT_B: float = 7.426160269118667e-38
DEFAULT_QB: float = 2.612280302374279e-56
DEFAULT_GAMMA_ENV: float = 0.05
DEFAULT_ALPHA: float = 1.0
DEFAULT_EPSILON_EXP: float = 1e-6
DEFAULT_T_GRID: list[float] = [i * 10.0 / 100 for i in range(101)]  # linspace(0, 10, 101)


# ---------------------------------------------------------------------------
# Campaign runner
# ---------------------------------------------------------------------------

def run_candidate_baseline_synthetic_benchmark_campaign(
    reports_dir: str | Path = "reports",
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    benchmark_id: str = DEFAULT_BENCHMARK_ID,
    system_id: str = DEFAULT_SYSTEM_ID,
    m_kg: float = DEFAULT_M_KG,
    L_value_m: float = DEFAULT_L_VALUE_M,
    B: float = DEFAULT_B,
    QB: float = DEFAULT_QB,
    gamma_env: float = DEFAULT_GAMMA_ENV,
    alpha: float = DEFAULT_ALPHA,
    t_grid: list[float] | None = None,
    epsilon_exp: float = DEFAULT_EPSILON_EXP,
    y_true: list[float] | None = None,
    error_metric: str = "MAE",
) -> dict:
    """
    Full campaign: synthetic benchmark + alpha sweep + reports.

    Returns a dict with keys:
        benchmark_result, alpha_sweep_rows, candidate_survival, report_paths
    """
    if t_grid is None:
        t_grid = DEFAULT_T_GRID

    reports_root = Path(reports_dir)

    # 1. Run default benchmark
    inp = CandidateSyntheticBenchmarkInput(
        benchmark_id=benchmark_id,
        candidate_id=candidate_id,
        system_id=system_id,
        m_kg=m_kg,
        L_value_m=L_value_m,
        B=B,
        QB=QB,
        gamma_env=gamma_env,
        alpha=alpha,
        t_grid=t_grid,
        epsilon_exp=epsilon_exp,
        y_true=y_true,
        error_metric=error_metric,
        benchmark_provenance="SYNTHETIC",
    )
    result = run_synthetic_benchmark(inp)

    # 2. Alpha sweep
    sweep_rows = run_alpha_sweep(
        B=B,
        gamma_env=gamma_env,
        t_grid=t_grid,
        epsilon_exp=epsilon_exp,
        alpha_values=DEFAULT_ALPHA_VALUES,
    )
    first_detectable_alpha = find_first_detectable_alpha(sweep_rows)

    # 3. Candidate survival
    survival_status = classify_candidate_survival(result.triggered_failure_conditions)

    # 4. Alpha min estimate
    alpha_min = estimate_alpha_min_for_detectability(B, gamma_env, t_grid, epsilon_exp)

    # 5. Write reports
    report_paths = _write_all_reports(
        reports_root=reports_root,
        candidate_id=candidate_id,
        benchmark_id=benchmark_id,
        result=result,
        sweep_rows=sweep_rows,
        first_detectable_alpha=first_detectable_alpha,
        alpha_min=alpha_min,
        survival_status=survival_status,
        inp=inp,
    )

    return {
        "benchmark_result": result,
        "alpha_sweep_rows": sweep_rows,
        "candidate_survival": survival_status,
        "report_paths": report_paths,
        "alpha_min_for_detectability": alpha_min,
        "first_detectable_alpha_in_sweep": first_detectable_alpha,
    }


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------

def _write_all_reports(
    reports_root: Path,
    candidate_id: str,
    benchmark_id: str,
    result,
    sweep_rows: list[AlphaSweepRow],
    first_detectable_alpha: float | None,
    alpha_min: float | None,
    survival_status: str,
    inp: CandidateSyntheticBenchmarkInput,
) -> dict[str, str]:
    paths: dict[str, str] = {}

    # Ensure directories
    for sub in ("benchmarks", "candidates", "prediction_pressure", "campaigns"):
        (reports_root / sub).mkdir(parents=True, exist_ok=True)

    # a) Benchmark report
    bench_path = reports_root / "benchmarks" / f"{benchmark_id}.md"
    bench_path.write_text(_render_benchmark_report(benchmark_id, result, inp), encoding="utf-8")
    paths["benchmark"] = str(bench_path)

    # b) Synthetic benchmark candidate report
    cand_bench_path = reports_root / "candidates" / f"{candidate_id}_synthetic_benchmark_v1_5.md"
    cand_bench_path.write_text(_render_candidate_benchmark_report(candidate_id, result, inp), encoding="utf-8")
    paths["candidate_benchmark"] = str(cand_bench_path)

    # c) Alpha sweep report
    sweep_path = reports_root / "candidates" / f"{candidate_id}_alpha_sweep_v1_5.md"
    sweep_path.write_text(_render_alpha_sweep_report(candidate_id, sweep_rows, first_detectable_alpha, alpha_min), encoding="utf-8")
    paths["alpha_sweep"] = str(sweep_path)

    # d) Failure report
    failure_path = reports_root / "prediction_pressure" / f"{candidate_id}_failure_report_v1_5.md"
    failure_path.write_text(
        _render_failure_report(candidate_id, result, sweep_rows, alpha_min, survival_status, inp),
        encoding="utf-8",
    )
    paths["failure_report"] = str(failure_path)

    # e) Campaign report
    campaign_path = reports_root / "campaigns" / "CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5.md"
    campaign_path.write_text(
        _render_campaign_report(candidate_id, benchmark_id, result, survival_status, sweep_rows),
        encoding="utf-8",
    )
    paths["campaign"] = str(campaign_path)

    return paths


def _render_benchmark_report(benchmark_id: str, result, inp: CandidateSyntheticBenchmarkInput) -> str:
    lines = [
        f"# Benchmark Report — {benchmark_id}",
        "",
        "## Provenance",
        "",
        f"- benchmark_id: `{benchmark_id}`",
        f"- candidate_id: `{result.candidate_id}`",
        f"- provenance: `{inp.benchmark_provenance}`",
        "",
        "## Parameters",
        "",
        f"| Parameter | Value |",
        f"|---|---|",
        f"| m_kg | {inp.m_kg:.3e} |",
        f"| L_value_m | {inp.L_value_m:.3e} |",
        f"| B | {inp.B:.6e} |",
        f"| gamma_env | {inp.gamma_env} |",
        f"| alpha | {inp.alpha:.3e} |",
        f"| epsilon_exp | {inp.epsilon_exp} |",
        "",
        "## Results",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| max_abs_delta | {result.max_abs_delta:.6e} |",
        f"| detectability_status | `{result.detectability_status}` |",
        f"| alpha_min_for_detectability | {result.alpha_min_for_detectability} |",
        f"| synthetic_gain_status | `{result.synthetic_gain_status}` |",
        "",
        "## Failure Conditions",
        "",
    ]
    for f in result.triggered_failure_conditions:
        lines.append(f"- `{f}`")
    lines.extend([
        "",
        "## Allowed Claims",
        "",
    ])
    for c in result.allowed_claims:
        lines.append(f"- {c}")
    lines.extend([
        "",
        "## Blocked Claims",
        "",
    ])
    for c in result.blocked_claims:
        lines.append(f"- {c}")
    return "\n".join(lines) + "\n"


def _render_candidate_benchmark_report(candidate_id: str, result, inp: CandidateSyntheticBenchmarkInput) -> str:
    lines = [
        f"# Candidate Synthetic Benchmark — {candidate_id} (v1.5)",
        "",
        "## Summary",
        "",
        f"- candidate_id: `{candidate_id}`",
        f"- benchmark_provenance: `SYNTHETIC`",
        f"- detectability_status: `{result.detectability_status}`",
        f"- max_abs_delta: `{result.max_abs_delta:.6e}`",
        f"- synthetic_gain_status: `{result.synthetic_gain_status}`",
        "",
        "## Equations",
        "",
        "- V_base(t) = exp(-gamma_env * t)",
        "- V_candidate(t) = exp(-(gamma_env + alpha * B) * t)",
        "- delta(t) = V_candidate(t) - V_base(t)",
        "",
        f"With alpha = {inp.alpha:.3e}, B = {inp.B:.6e}, gamma_env = {inp.gamma_env}",
        "",
        "## Failure Conditions",
        "",
    ]
    for f in result.triggered_failure_conditions:
        lines.append(f"- `{f}`")
    lines.extend([
        "",
        "## Note",
        "",
        "This is a synthetic (toy) benchmark. No physical claim is unlocked by this result.",
    ])
    return "\n".join(lines) + "\n"


def _render_alpha_sweep_report(
    candidate_id: str,
    sweep_rows: list[AlphaSweepRow],
    first_detectable_alpha: float | None,
    alpha_min: float | None,
) -> str:
    lines = [
        f"# Alpha Sweep Report — {candidate_id} (v1.5)",
        "",
        "## Purpose",
        "",
        "Identify the alpha scale at which the B-suppressed candidate becomes synthetically detectable.",
        "",
        "## Alpha Sweep Table",
        "",
        "| alpha | delta_gamma_c | max_abs_delta | detectability_status | alpha_reasonableness_status | triggered_failures |",
        "|---|---|---|---|---|---|",
    ]
    for row in sweep_rows:
        failures = ", ".join(row.triggered_failures) if row.triggered_failures else "—"
        lines.append(
            f"| {row.alpha:.2e} | {row.delta_gamma_c:.3e} | {row.max_abs_delta:.3e} "
            f"| `{row.detectability_status}` | `{row.alpha_reasonableness_status}` | {failures} |"
        )
    lines.extend([
        "",
        "## Key Results",
        "",
        f"- alpha_min (first-order estimate): `{alpha_min}`",
        f"- First detectable alpha in sweep: `{first_detectable_alpha}`",
        "",
        "## Interpretation",
        "",
        "- Detectability at alpha > 1e35 triggers `REQUIRES_UNPHYSICAL_ALPHA`.",
        "- These thresholds are heuristic toy classifications and do not constitute physical constraints.",
    ])
    return "\n".join(lines) + "\n"


def _render_failure_report(
    candidate_id: str,
    result,
    sweep_rows: list[AlphaSweepRow],
    alpha_min: float | None,
    survival_status: str,
    inp: CandidateSyntheticBenchmarkInput,
) -> str:
    lines = [
        f"# Candidate Failure Report — {candidate_id} (v1.5)",
        "",
        "## Candidate Summary",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| candidate_id | `{candidate_id}` |",
        f"| candidate_family | `B_SUPPRESSED` |",
        f"| candidate_term | `DeltaGamma_C = alpha * B` |",
        f"| observable | `visibility_loss` |",
        f"| parameter_status | `PRE_REGISTERED` |",
        f"| source_support_status | `FAIL_NO_SOURCE_SUPPORT` |",
        f"| benchmark_status | `SYNTHETIC` |",
        "",
        "## Benchmark Summary",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| max_abs_delta | `{result.max_abs_delta:.6e}` |",
        f"| epsilon_exp | `{inp.epsilon_exp}` |",
        f"| detectability_status | `{result.detectability_status}` |",
        f"| alpha_min_estimate | `{alpha_min}` |",
        f"| survival_status | `{survival_status}` |",
        "",
        "## Baseline Equation",
        "",
        "```",
        "V_base(t) = exp(-gamma_env * t)",
        "```",
        "",
        "## Candidate Equation",
        "",
        "```",
        "V_candidate(t) = exp(-(gamma_env + alpha * B) * t)",
        "DeltaGamma_C = alpha * B",
        "```",
        "",
        "## Parameter Table",
        "",
        f"| Parameter | Value |",
        f"|---|---|",
        f"| B | `{inp.B:.6e}` |",
        f"| gamma_env | `{inp.gamma_env}` |",
        f"| alpha (default) | `{inp.alpha:.3e}` |",
        f"| epsilon_exp | `{inp.epsilon_exp}` |",
        "",
        "## Delta Results",
        "",
        f"max_abs_delta = `{result.max_abs_delta:.6e}`",
        "",
        "Under default alpha = 1.0, the B-suppressed candidate produces a delta far below the declared threshold.",
        "",
        "## Alpha Sweep Summary",
        "",
    ]
    for row in sweep_rows:
        lines.append(f"- alpha={row.alpha:.2e}: {row.detectability_status} ({row.alpha_reasonableness_status})")
    lines.extend([
        "",
        "## Detectability Result",
        "",
        f"`{result.detectability_status}`",
        "",
        "## Failure Conditions Triggered",
        "",
    ])
    for f in result.triggered_failure_conditions:
        lines.append(f"- `{f}`")
    lines.extend([
        "",
        "## Allowed Claims",
        "",
    ])
    for c in result.allowed_claims:
        lines.append(f"- {c}")
    lines.extend([
        "",
        "## Blocked Claims",
        "",
    ])
    for c in result.blocked_claims:
        lines.append(f"- {c}")
    lines.extend([
        "",
        "## Next Action",
        "",
        "- Obtain independently justified alpha value from literature or experimental constraint.",
        "- Transition from SYNTHETIC to LITERATURE_EXTRACTED benchmark provenance.",
        "- Evaluate source-backed detectability before unlocking physical claims.",
    ])
    return "\n".join(lines) + "\n"


def _render_campaign_report(
    candidate_id: str,
    benchmark_id: str,
    result,
    survival_status: str,
    sweep_rows: list[AlphaSweepRow],
) -> str:
    lines = [
        "# Campaign Report — CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5",
        "",
        "## Campaign",
        "",
        "- campaign_id: `CANDIDATE-vs-BASELINE-SYNTH-v1_5`",
        f"- candidate_id: `{candidate_id}`",
        f"- benchmark_id: `{benchmark_id}`",
        f"- provenance: `SYNTHETIC`",
        "",
        "## Status",
        "",
        f"- detectability_status: `{result.detectability_status}`",
        f"- candidate_survival: `{survival_status}`",
        f"- max_abs_delta: `{result.max_abs_delta:.6e}`",
        "",
        "## Failure Conditions",
        "",
    ]
    for f in result.triggered_failure_conditions:
        lines.append(f"- `{f}`")
    lines.extend([
        "",
        "## Alpha Sweep Summary",
        "",
    ])
    first_detect = next(
        (r for r in sweep_rows if r.detectability_status == "DETECTABLE_SYNTHETIC_DELTA"), None
    )
    if first_detect:
        lines.append(f"First detectable alpha in sweep: `{first_detect.alpha:.2e}` ({first_detect.alpha_reasonableness_status})")
    else:
        lines.append("No detectable alpha found in default sweep range.")
    lines.extend([
        "",
        "## Physical Claims",
        "",
        "- Physical claims remain **BLOCKED**.",
        "- Synthetic benchmark does not unlock PredictiveGain.",
        "- Frontera C is not validated by this result.",
        "",
        "## Conclusion",
        "",
        f"CAND-FC-B-NEGCTRL-001 survives v1.5 as: **{survival_status}**.",
        "",
        "A visible synthetic delta was not achieved under default parameters.",
        "This is expected for a B-suppressed negative control candidate.",
        "The result is numerical information, not failure of the framework.",
    ])
    return "\n".join(lines) + "\n"
