from datetime import datetime, timezone
import os
import json
import argparse
from typing import List
from xendris.benchmarks.false_formality.core.types import BenchmarkCase, BenchmarkResult
from xendris.benchmarks.false_formality.core.base_model_client import BaseModelClient
from xendris.benchmarks.false_formality.core.xendris_pipeline import XendrisPipelineClient
from xendris.benchmarks.false_formality.evaluator import RubricEvaluator
from xendris.benchmarks.false_formality.scorer import BenchmarkScorer
from xendris.benchmarks.false_formality.report import BenchmarkReportGenerator

def load_cases(cases_path: str) -> List[BenchmarkCase]:
    with open(cases_path, "r", encoding="utf-8") as f:
        cases_json = json.load(f)
    return [BenchmarkCase(**case) for case in cases_json]

def run_benchmark(
    mode: str = "mock",
    provider: str = "deepseek",
    endpoint_url: str = "http://localhost:3000/api/chat"
):
    cases_path = os.path.join(os.path.dirname(__file__), "cases.json")
    cases = load_cases(cases_path)
    
    # In mock mode, force the provider name to mock
    active_provider = "mock" if mode == "mock" else provider
    
    base_client = BaseModelClient(endpoint_url, active_provider)
    xendris_client = XendrisPipelineClient(endpoint_url, active_provider)
    evaluator = RubricEvaluator(endpoint_url, active_provider)
    scorer = BenchmarkScorer()
    report_gen = BenchmarkReportGenerator()
    
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"Starting False Formality Benchmark Iteration v0.2")
    print(f"Execution Mode: {mode}")
    print(f"Provider: {active_provider}")
    print(f"Endpoint: {endpoint_url}")
    print(f"Timestamp: {timestamp}")
    print(f"Loaded {len(cases)} cases.\n")

    results: List[BenchmarkResult] = []
    
    for case in cases:
        print(f"Running case {case.id}: {case.title}...")
        
        # 1. Base model response & evaluation
        base_resp = base_client.generate(case.id, case.prompt)
        base_score = evaluator.evaluate(case, base_resp)
        
        # 2. Xendris response & evaluation
        xendris_resp = xendris_client.generate(case.id, case.prompt)
        xendris_score = evaluator.evaluate(case, xendris_resp)
        
        # 3. Score & compare, passing response metadata
        res = scorer.score_case(
            case=case,
            base_score=base_score,
            xendris_score=xendris_score,
            base_resp=base_resp,
            xendris_resp=xendris_resp
        )
        results.append(res)
        
        base_lat = f"{res.base_latency_ms:.1f}ms" if res.base_latency_ms is not None else "-"
        xend_lat = f"{res.xendris_latency_ms:.1f}ms" if res.xendris_latency_ms is not None else "-"
        err_info = ""
        if res.base_error or res.xendris_error:
            err_info = f" | Error: {res.base_error or res.xendris_error}"
            
        print(f"  Base Score   : {res.base_score.total_score:.4f} (Regression: {res.base_score.severe_regression}) [Latency: {base_lat}]")
        print(f"  Xendris Score: {res.xendris_score.total_score:.4f} (Regression: {res.xendris_score.severe_regression}) [Latency: {xend_lat}]")
        print(f"  Winner       : {res.winner.upper()} (Delta: {res.delta:+.4f}){err_info}")
        print(f"  Notes        : {res.xendris_score.notes}\n")

    # Compile summary
    summary = scorer.summarize(
        results=results,
        execution_mode=mode,
        provider_name=active_provider,
        timestamp=timestamp
    )
    
    # Generate reports
    json_path, md_path = report_gen.generate(results, summary)
    
    print("=" * 60)
    print("BENCHMARK COMPLETED")
    print(f"Execution Mode: {summary.execution_mode}")
    print(f"Provider: {summary.provider_name}")
    print(f"Total Cases: {summary.total_cases}")
    print(f"Xendris Wins: {summary.xendris_wins}")
    print(f"Base Model Wins: {summary.base_model_wins}")
    print(f"Ties: {summary.ties}")
    print(f"Severe Regressions: {summary.severe_regressions}")
    print(f"Validation Status: {'PASSED' if summary.passed else 'FAILED'}")
    print(f"Conclusion: {summary.conclusion}")
    print("=" * 60)
    print(f"JSON Output   : {json_path}")
    print(f"Markdown Report: {md_path}")
    print("=" * 60)
    
    return summary.passed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Xendris False Formality Benchmark Suite.")
    parser.add_argument(
        "--mode",
        choices=["mock", "real_provider"],
        default="mock",
        help="Execution mode (default: mock)"
    )
    parser.add_argument(
        "--provider",
        default="deepseek",
        help="Model provider to use when in real_provider mode (default: deepseek)"
    )
    parser.add_argument(
        "--endpoint",
        default="http://localhost:3000/api/chat",
        help="Xendris HTTP API endpoint URL (default: http://localhost:3000/api/chat)"
    )
    
    args = parser.parse_args()
    success = run_benchmark(args.mode, args.provider, args.endpoint)
    exit(0 if success else 1)

