from __future__ import annotations

from typing import Any


def build_report(
    config: Any,
    artifacts: dict[str, Any],
    integrity_result: dict[str, Any],
    statistics: dict[str, Any],
    claims: dict[str, Any],
    cost_robustness: dict[str, Any],
    final_decision: str,
) -> str:
    lines: list[str] = []
    _add = lines.append

    summary = artifacts.get("summary", {})
    _add(f"# Finitexo Code Matrix v{config.benchmark_version} — Runtime Evidence Gate Report")
    _add("")
    _add(f"**Source run:** {config.source_run_id}")
    _add(f"**Source run dir:** {config.source_run_dir}")
    _add(f"**Gate version:** {config.benchmark_version}")
    _add(f"**Final gate decision:** {final_decision}")
    _add("")

    _add("---")
    _add("## Source Run Summary")
    _add("")
    _add(f"| Field | Value |")
    _add(f"|---|---|")
    _add(f"| Benchmark | {summary.get('benchmark_name', '')} v{summary.get('benchmark_version', '')} |")
    _add(f"| Experiment | {summary.get('experiment_type', '')} |")
    _add(f"| Final decision | {summary.get('final_decision', '')} |")
    _add(f"| Provider mode | {summary.get('provider_mode', '')} |")
    _add(f"| Total expected | {summary.get('total_expected', '')} |")
    _add(f"| Total attempted | {summary.get('total_attempted', '')} |")
    _add(f"| Total completed | {summary.get('total_completed', '')} |")
    _add(f"| Total failed | {summary.get('total_failed', '')} |")
    _add(f"| Total cost | ${summary.get('total_cost_usd', 0):.6f} |")
    _add(f"| Budget cap | ${summary.get('budget_cap_usd', 0):.2f} |")
    _add(f"| Budget decision | {summary.get('budget_decision', '')} |")
    _add(f"| Runtime traces | {summary.get('runtime_variant_trace_count', '')} |")
    _add(f"| Calibration traces | {summary.get('calibration_trace_count', '')} |")
    _add(f"| Dataset hash | {summary.get('dataset_hash', '')} |")
    _add(f"| Manifest hash | {summary.get('manifest_hash', '')} |")
    _add("")

    _add("---")
    _add("## Evidence Integrity")
    _add("")
    _add(f"**Integrity decision:** {integrity_result.get('integrity_decision', 'unknown')}")
    _add("")
    _add(f"| Check | Result |")
    _add(f"|---|---|")
    _add(f"| Source dir exists | {integrity_result.get('source_run_dir_exists', '?')} |")
    _add(f"| All artifacts exist | {integrity_result.get('all_required_artifacts_exist', '?')} |")
    _add(f"| Final decision matches | {integrity_result.get('final_decision_matches', '?')} |")
    _add(f"| Provider mode is real | {integrity_result.get('provider_mode_is_real', '?')} |")
    _add(f"| Dataset hash matches | {integrity_result.get('dataset_hash_matches', '?')} |")
    _add(f"| Manifest hash matches | {integrity_result.get('manifest_hash_matches', '?')} |")
    _add(f"| total_completed == 240 | {integrity_result.get('total_completed', '?')} |")
    _add(f"| total_failed == 0 | {integrity_result.get('total_failed', '?')} |")
    _add(f"| responses_count == 240 | {integrity_result.get('responses_count', '?')} |")
    _add(f"| scores_count == 240 | {integrity_result.get('scores_count', '?')} |")
    _add(f"| runtime_traces == 120 | {integrity_result.get('runtime_traces_count', '?')} |")
    _add(f"| calibration_traces == 60 | {integrity_result.get('calibration_traces_count', '?')} |")
    _add(f"| errors_count == 0 | {integrity_result.get('errors_count', '?')} |")
    _add(f"| Evidence integrity ready | {integrity_result.get('evidence_integrity_ready', '?')} |")
    _add(f"| All variants exist | {integrity_result.get('all_expected_variants_exist', '?')} |")
    _add(f"| All variants have 30 | {integrity_result.get('all_variants_have_30', '?')} |")
    _add(f"| Scores in [0,1] | {integrity_result.get('all_scores_in_0_1', '?')} |")
    _add(f"| Task IDs match | {integrity_result.get('task_id_set_identical', '?')} |")
    _add(f"| All families present | {integrity_result.get('all_expected_families_present', '?')} |")
    _add(f"| Failures | {integrity_result.get('failure_count', 0)} |")
    _add("")

    aggregates = summary.get("aggregates", [])
    _add("---")
    _add("## Score Absolute Table")
    _add("")
    _add("| Variant | Mean Score | Min | Max | Cost |")
    _add("|---|---|---|---|---|")
    for agg in aggregates:
        _add(
            f"| {agg.get('variant_name', '')} "
            f"| {agg.get('mean_score', 0):.6f} "
            f"| {agg.get('min_score', 0):.4f} "
            f"| {agg.get('max_score', 0):.4f} "
            f"| ${agg.get('total_cost_usd', 0):.6f} |"
        )
    _add("")

    _add("---")
    _add("## Paired Lift Table")
    _add("")
    _add("| Comparison | Mean Lift | Median Lift | Wins | Losses | Ties | NRR | Signal |")
    _add("|---|---|---|---|---|---|---|---|")
    for key, comp in statistics.items():
        if not isinstance(comp, dict) or "error" in comp:
            continue
        _add(
            f"| {key} "
            f"| {comp.get('mean_lift', 0):.6f} "
            f"| {comp.get('median_lift', 0):.6f} "
            f"| {comp.get('wins', 0)} "
            f"| {comp.get('losses', 0)} "
            f"| {comp.get('ties', 0)} "
            f"| {comp.get('non_negative_rate', 0):.4f} "
            f"| {comp.get('signal', '?')} |"
        )
    _add("")

    _add("---")
    _add("## Bootstrap CI Table")
    _add("")
    _add("| Comparison | Mean Lift | CI 95 Low | CI 95 High | Std Error | Sign Test p |")
    _add("|---|---|---|---|---|---|")
    for key, comp in statistics.items():
        if not isinstance(comp, dict) or "error" in comp:
            continue
        sp = comp.get("sign_test_two_sided_p_value")
        sp_str = f"{sp:.6f}" if sp is not None else "N/A"
        _add(
            f"| {key} "
            f"| {comp.get('mean_lift', 0):.6f} "
            f"| {comp.get('bootstrap_ci_95_low', 0):.6f} "
            f"| {comp.get('bootstrap_ci_95_high', 0):.6f} "
            f"| {comp.get('standard_error_lift', 0):.6f} "
            f"| {sp_str} |"
        )
    _add("")

    _add("---")
    _add("## Win/Loss/Tie Table")
    _add("")
    _add("| Comparison | Wins | Losses | Ties | Win Rate (ex ties) |")
    _add("|---|---|---|---|---|")
    for key, comp in statistics.items():
        if not isinstance(comp, dict) or "error" in comp:
            continue
        wr = comp.get("win_rate_excluding_ties", 0)
        _add(
            f"| {key} "
            f"| {comp.get('wins', 0)} "
            f"| {comp.get('losses', 0)} "
            f"| {comp.get('ties', 0)} "
            f"| {wr:.4f} |"
        )
    _add("")

    fl = artifacts.get("family_lift", {})
    fl_data = fl.get("family_lift", {})
    if fl_data:
        _add("---")
        _add("## Family Lift Summary")
        _add("")
        for family, data in fl_data.items():
            _add(f"**{family}:**")
            _add("")
            _add("| Variant | Mean |")
            _add("|---|---|")
            for key, val in data.items():
                _add(f"| {key} | {val:.6f} |")
            _add("")

    _add("---")
    _add("## Cost Table")
    _add("")
    _add("| Comparison | Cost Delta | Cost per Lift Point |")
    _add("|---|---|---|")
    for key, comp in statistics.items():
        if not isinstance(comp, dict) or "error" in comp:
            continue
        ml = comp.get("mean_lift", 0)
        cr = cost_robustness.get(key, {})
        cd = cr.get("cost_delta", "N/A")
        cpl = cr.get("cost_per_mean_lift_point", "N/A")
        if cpl is not None:
            cpl_str = f"${cpl:.6f}" if isinstance(cpl, float) else "N/A"
        else:
            cpl_str = "N/A (negative lift)"
        cd_str = f"${cd:.6f}" if isinstance(cd, float) else "N/A"
        _add(
            f"| {key} "
            f"| {cd_str} "
            f"| {cpl_str} |"
        )
    _add("")
    _add(f"Note: Runtime and calibrated runtime cost more than base/wrapper. Cost remains within budget (${summary.get('budget_cap_usd', 0):.2f}). Cost efficiency is diagnostic-only.")
    _add("")

    _add("---")
    _add("## Claims")
    _add("")
    _add("### Authorized Claims")
    for c in claims.get("authorized_claims", []):
        _add(f"- {c}")
    _add("")
    _add("### Conditional Claims")
    for c in claims.get("conditional_claims", []):
        _add(f"- {c}")
    _add("")
    _add("### Blocked Claims")
    for c in claims.get("blocked_claims", []):
        _add(f"- {c}")
    _add("")

    _add("---")
    _add("## Final Decision")
    _add("")
    _add(f"**{final_decision}**")
    _add("")

    _add("---")
    _add("## Warning")
    _add("")
    _add("This is a diagnostic-only evidence integrity and statistical robustness gate.")
    _add("No universal superiority claim is authorized.")
    _add("No statistical superiority claim is authorized.")
    _add("No production readiness claim is authorized.")
    _add("Results are specific to this controlled n=30 hard programming dataset and the two providers tested.")
    _add("")

    return "\n".join(lines)
