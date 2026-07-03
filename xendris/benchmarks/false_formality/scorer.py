from typing import List
from xendris.benchmarks.false_formality.core.types import BenchmarkCase, RubricScore, BenchmarkResult, BenchmarkSummary, ModelResponse

class BenchmarkScorer:
    def score_case(
        self,
        case: BenchmarkCase,
        base_score: RubricScore,
        xendris_score: RubricScore,
        base_resp: ModelResponse = None,
        xendris_resp: ModelResponse = None
    ) -> BenchmarkResult:
        delta = round(xendris_score.total_score - base_score.total_score, 4)
        
        if xendris_score.total_score > base_score.total_score:
            winner = "xendris"
            observation = "Xendris outperformed base model by correcting false mathematical formalisms."
        elif base_score.total_score > xendris_score.total_score:
            winner = "base_model"
            observation = "Base model scored higher than Xendris."
        else:
            winner = "tie"
            observation = "Both systems scored equally."

        base_lat = base_resp.raw_metadata.get("latency_ms") if base_resp and base_resp.raw_metadata else None
        xendris_lat = xendris_resp.raw_metadata.get("latency_ms") if xendris_resp and xendris_resp.raw_metadata else None
        base_to = base_resp.raw_metadata.get("timeout") if base_resp and base_resp.raw_metadata else None
        xendris_to = xendris_resp.raw_metadata.get("timeout") if xendris_resp and xendris_resp.raw_metadata else None
        base_err = base_resp.raw_metadata.get("error") if base_resp and base_resp.raw_metadata else None
        xendris_err = xendris_resp.raw_metadata.get("error") if xendris_resp and xendris_resp.raw_metadata else None

        return BenchmarkResult(
            case_id=case.id,
            failure_type=case.expected_failure_type,
            base_score=base_score,
            xendris_score=xendris_score,
            winner=winner,
            delta=delta,
            observation=observation,
            base_latency_ms=base_lat,
            xendris_latency_ms=xendris_lat,
            base_timeout=base_to,
            xendris_timeout=xendris_to,
            base_error=base_err,
            xendris_error=xendris_err
        )


    def summarize(
        self,
        results: List[BenchmarkResult],
        execution_mode: str = "mock",
        provider_name: str = "mock",
        timestamp: str = ""
    ) -> BenchmarkSummary:
        total_cases = len(results)
        xendris_wins = sum(1 for r in results if r.winner == "xendris")
        base_model_wins = sum(1 for r in results if r.winner == "base_model")
        ties = sum(1 for r in results if r.winner == "tie")
        severe_regressions = sum(1 for r in results if r.xendris_score.severe_regression)
        
        # Success criteria: Wins >= 14/20 and SevereRegression = 0
        passed = (xendris_wins >= 14) and (severe_regressions == 0)
        
        if execution_mode == "mock":
            conclusion = (
                "La suite ha validado infraestructura y scoring, pero no constituye "
                "evidencia empírica frente a un modelo real."
            )
        else:
            if passed:
                conclusion = (
                    "Xendris demuestra mejora local repetible frente al modelo base real en la "
                    "familia de errores de falsa formalidad matemática, bajo esta rúbrica y esta "
                    "batería de 20 casos. Esta conclusión no implica superioridad universal ni "
                    "superioridad general en todos los dominios."
                )
            else:
                conclusion = (
                    "Xendris no ha demostrado todavía mejora repetible en esta familia de fallo. "
                    "Los resultados solo permiten hablar de correcciones puntuales o evidencia insuficiente."
                )

        return BenchmarkSummary(
            total_cases=total_cases,
            xendris_wins=xendris_wins,
            base_model_wins=base_model_wins,
            ties=ties,
            severe_regressions=severe_regressions,
            passed=passed,
            conclusion=conclusion,
            execution_mode=execution_mode,
            provider_name=provider_name,
            timestamp=timestamp
        )

