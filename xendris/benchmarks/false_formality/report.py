import os
import json
from typing import List
from xendris.benchmarks.false_formality.core.types import BenchmarkResult, BenchmarkSummary

class BenchmarkReportGenerator:
    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "outputs")
        self.output_dir = output_dir

    def generate(self, results: List[BenchmarkResult], summary: BenchmarkSummary):
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Write JSON output
        json_path = os.path.join(self.output_dir, "false_formality_results.json")
        full_payload = {
            "summary": summary.model_dump(),
            "results": [r.model_dump() for r in results]
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(full_payload, f, indent=2, ensure_ascii=False)

        # Write Markdown output
        md_path = os.path.join(self.output_dir, "false_formality_report.md")
        
        status_string = "PASSED_PATTERN_REUSABLE" if summary.passed else "FAILED_PATTERN_REUSABLE"
        
        md_lines = [
            "# Resultado Iteración v0.2 — Falsa Formalidad Matemática\n",
            "## 1. Objetivo",
            "Validar si la capa cognitiva de Xendris ofrece una mejora repetible y sistemática al evaluar falacias argumentales que simulan rigor matemático formal, en comparación con un modelo base directo.\n",
            "## 2. Familia de fallo evaluada",
            "**Falsa Formalidad Matemática**: Argumentos lógicos incorrectos o saltos injustificados que utilizan símbolos, lemas o estructuras matemáticas decorativas.\n",
            "## 3. Metadatos de la Ejecución",
            f"- **Modo de Ejecución (`execution_mode`)**: {summary.execution_mode}",
            f"- **Proveedor (`provider_name`)**: {summary.provider_name}",
            f"- **Marca de Tiempo (`timestamp`)**: {summary.timestamp}\n",
            "## 4. Métricas de Resumen",
            f"- **Número total de casos (`total_cases`)**: {summary.total_cases}",
            f"- **Victorias de Xendris (`xendris_wins`)**: {summary.xendris_wins}",
            f"- **Victorias del modelo base (`base_model_wins`)**: {summary.base_model_wins}",
            f"- **Empates (`ties`)**: {summary.ties}",
            f"- **Regresiones graves (`severe_regressions`)**: {summary.severe_regressions}\n",
            "## 5. Estado de la Validación",
            f"**Estado (`passed`)**: `{summary.passed}` (Status string: `{status_string}`)\n",
            "## 6. Tabla por caso",
            "| ID Caso | Tipo de Fallo Esperado | Score Base | Score Xendris | Delta | Ganador | Regresión Grave | Latencia Base (ms) | Latencia Xendris (ms) | Error/Timeout |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        
        for r in results:
            reg_str = "Sí" if r.xendris_score.severe_regression else "No"
            base_lat = f"{r.base_latency_ms:.1f}" if r.base_latency_ms is not None else "-"
            xend_lat = f"{r.xendris_latency_ms:.1f}" if r.xendris_latency_ms is not None else "-"
            
            err_list = []
            if r.base_timeout or r.xendris_timeout:
                err_list.append("TIMEOUT")
            if r.base_error:
                err_list.append(f"BaseErr: {r.base_error}")
            if r.xendris_error:
                err_list.append(f"XendrisErr: {r.xendris_error}")
            err_str = ", ".join(err_list) if err_list else "None"
            
            md_lines.append(
                f"| {r.case_id} | {r.failure_type} | {r.base_score.total_score:.4f} | {r.xendris_score.total_score:.4f} | {r.delta:+.4f} | {r.winner} | {reg_str} | {base_lat} | {xend_lat} | {err_str} |"
            )
            
        md_lines.extend([
            "\n## 7. Conclusión",
            f"{summary.conclusion}\n"
        ])
        
        md_content = "\n".join(md_lines)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
 
        return json_path, md_path


