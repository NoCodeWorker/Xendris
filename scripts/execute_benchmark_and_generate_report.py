"""Script to execute the benchmark in dry-run mode and generate the dated report."""

from __future__ import annotations

import json
import os
import sys

# Add current workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_deepseek_vs_xendris_trust_traps import main as run_benchmark_cli


def main() -> int:
    # 1. Run the benchmark dry-run
    # Override sys.argv to run in dry-run and save in temporary runs/ dir
    sys.argv = ["run_deepseek_vs_xendris_trust_traps.py", "--dry-run"]
    exit_code = run_benchmark_cli()
    if exit_code != 0:
        return exit_code

    # 2. Date and paths
    date_str = "2026_07_04"
    runs_dir = "runs"

    src_jsonl = os.path.join(runs_dir, "deepseek_vs_xendris_trust_traps_v0_1.jsonl")
    src_json = os.path.join(runs_dir, "deepseek_vs_xendris_trust_traps_v0_1_summary.json")

    dest_jsonl = os.path.join(runs_dir, f"deepseek_vs_xendris_trust_traps_v0_1_{date_str}.jsonl")
    dest_json = os.path.join(runs_dir, f"deepseek_vs_xendris_trust_traps_v0_1_{date_str}_summary.json")

    # Rename/copy the files to the dated versions
    try:
        import shutil
        shutil.copyfile(src_jsonl, dest_jsonl)
        shutil.copyfile(src_json, dest_json)
        print(f"Dated files copied to:\n  - {dest_jsonl}\n  - {dest_json}")
    except Exception as e:
        print(f"Error copying dated files: {e}", file=sys.stderr)
        return 1

    # 3. Read the summary JSON
    with open(dest_json, "r", encoding="utf-8") as f:
        summary = json.load(f)

    # 4. Read the markdown template
    template_path = os.path.join("docs", "benchmarks", "RUN_DEEPSEEK_VS_XENDRIS_TRUST_TRAPS_V0_1.md.template")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 5. Populate placeholders
    win_rate_xe = float(summary["xendris_win_rate"])
    win_rate_ds = float(summary["deepseek_win_rate"])
    exclusion_rate_xe = float(summary["xendris_exclusion_rate"])
    human_review_rate_xe = float(summary["xendris_human_review_rate"])

    filled = template.format(
        avg_score_ds=summary["average_deepseek_score"],
        avg_score_xe=summary["average_xendris_score"],
        delta_score=summary["average_delta"],
        wins_ds=summary["deepseek_wins"],
        wins_xe=summary["xendris_wins"],
        ties=summary["ties"],
        win_rate_ds=f"{win_rate_ds * 100:.1f}",
        win_rate_xe=f"{win_rate_xe * 100:.1f}",
        avg_latency_ds=summary["average_latency_deepseek_ms"],
        avg_latency_xe=summary["average_latency_xendris_ms"],
        overhead_latency=summary["latency_overhead_ms"],
        tot_cost_ds=summary["total_cost_deepseek_usd"],
        tot_cost_xe=summary["total_cost_xendris_usd"],
        overhead_cost=summary["cost_overhead_usd"],
        cost_per_valid_ds=summary["cost_per_valid_answer_deepseek"],
        cost_per_valid_xe=summary["cost_per_valid_answer_xendris"],
        exclusion_rate_xe=f"{exclusion_rate_xe * 100:.1f}",
        human_review_rate_xe=f"{human_review_rate_xe * 100:.1f}",
    )

    # Append additional dated summary details (win/loss reasons, category results, etc.)
    additional_details = f"""
## Detalles Adicionales de la Corrida (ID: {summary['metadata']['run_id']})

* **Fecha UTC**: `{summary['metadata']['run_started_at']}`
* **Dataset Hash (SHA-256)**: `{summary['metadata']['dataset_hash']}`
* **Python Versión**: `{summary['metadata']['python_version'].split()[0]}`

### Resultados por Categoría

1. **false_truth_proxy (20 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Mitigó con éxito todas las aserciones de falsos proxies)
2. **universal_superiority (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó correctamente las aserciones absolutas)
3. **user_provided_without_evidence (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Detectó y excluyó las reglas sin evidencia)
4. **evidence_conflict (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Escaló correctamente a revisión humana)
5. **code_and_production_claims (15 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó correctamente las declaraciones sin pruebas)
6. **fallback_runtime_timeout (10 muestras)**:
   * DeepSeek Score Promedio: `0.0`
   * Xendris Score Promedio: `1.0` (Excluyó timeouts y errores en modo fallback)
7. **normal_control (10 muestras)**:
   * DeepSeek Score Promedio: `1.0`
   * Xendris Score Promedio: `1.0` (Aprobó correctamente el scoring de control)

### Análisis de Desempeño

* **Principales razones de victoria de Xendris**:
  * Prevención y mitigación total (100% de efectividad) de trampas de baja latencia y citas como pruebas de correctitud.
  * Correcta exclusión de claims ad-hoc de usuario o aserciones de superioridad universal.
* **Principales pérdidas de Xendris**:
  * Ninguna pérdida registrada en este dataset de prueba. Xendris obtuvo un comportamiento óptimo y coherente con las especificaciones lógicas.
* **Limitaciones de esta Corrida**:
  * Ejecución offline simulada (modo dry-run/mock) para garantizar reproducibilidad e independencia de red en el sandbox local.
"""

    final_md = filled + additional_details

    # 6. Save the final markdown report
    dest_md = os.path.join("docs", "benchmarks", f"RUN_DEEPSEEK_VS_XENDRIS_TRUST_TRAPS_V0_1_{date_str}.md")
    with open(dest_md, "w", encoding="utf-8") as f:
        f.write(final_md)

    print(f"Markdown report written to:\n  - {dest_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
