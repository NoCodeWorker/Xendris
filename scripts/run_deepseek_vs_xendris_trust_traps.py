#!/usr/bin/env python3
"""Script to run the DeepSeek Base vs Xendris+DeepSeek comparison on Trust Traps v0.1."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import platform
import sys
import uuid

# Add current workspace to path to allow clean imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xendris
from xendris.benchmarking import assess_benchmark_excellence, run_ab_benchmark, summarize_ab_results
from xendris.benchmarking.datasets import load_trust_traps_v0_1
from xendris.benchmarking.providers import DeepSeekBaseProvider, XendrisDeepSeekProvider
from xendris.benchmarking.export_jsonl import write_ab_results_jsonl, write_ab_summary_json


def compute_dataset_hash(path: str) -> str:
    """Calculate a stable SHA-256 hash of the dataset file."""
    if not os.path.exists(path):
        return ""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run A/B Benchmark DeepSeek base vs Xendris+DeepSeek.")
    parser.add_argument("--dry-run", action="store_true", help="Run offline using mock callables.")
    parser.add_argument("--model", default="deepseek-chat", help="DeepSeek model to use (default: deepseek-chat).")
    parser.add_argument("--output-dir", default="runs", help="Output directory for results (default: runs).")
    args = parser.parse_args()

    # 1. Load Trust Traps dataset
    try:
        samples = load_trust_traps_v0_1()
    except Exception as e:
        print(f"Error loading Trust Traps dataset: {e}", file=sys.stderr)
        return 1

    # Locate dataset path for hash
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(current_dir, "xendris", "benchmarking", "datasets", "trust_traps_v0_1.jsonl")
    dataset_hash = compute_dataset_hash(dataset_path)

    # 2. Setup providers
    try:
        ds_provider = DeepSeekBaseProvider(
            model=args.model,
            temperature=0.0,
            max_tokens=1024,
            mock_mode=args.dry_run,
        )
        xe_provider = XendrisDeepSeekProvider(
            model=args.model,
            temperature=0.0,
            max_tokens=1024,
            mock_mode=args.dry_run,
        )
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        print("Please set DEEPSEEK_API_KEY environment variable or run with --dry-run.", file=sys.stderr)
        return 1

    import datetime
    run_started_at = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

    # 3. Execute A/B benchmark run
    print(f"Starting A/B Benchmark run (dry-run={args.dry_run}) with {len(samples)} samples...")
    results = run_ab_benchmark(samples, ds_provider, xe_provider)
    summary = summarize_ab_results(results)

    # 4. Save results and summary
    os.makedirs(args.output_dir, exist_ok=True)
    jsonl_output = os.path.join(args.output_dir, "deepseek_vs_xendris_trust_traps_v0_1.jsonl")
    json_output = os.path.join(args.output_dir, "deepseek_vs_xendris_trust_traps_v0_1_summary.json")
    excellence_output = os.path.join(args.output_dir, "deepseek_vs_xendris_trust_traps_v0_1_excellence.json")
    report_output = os.path.join(args.output_dir, "deepseek_vs_xendris_trust_traps_v0_1_report.md")

    # Add metadata to summary
    summary_dict = summary.to_dict()
    summary_dict["metadata"] = {
        "run_id": str(uuid.uuid4()),
        "run_started_at": run_started_at,
        "execution_mode": "dry-run" if args.dry_run else "real-provider",
        "external_data_disclosure": (
            "No external provider call; deterministic local dry-run."
            if args.dry_run
            else "Only Trust Traps v0.1 benchmark prompts are sent to the configured DeepSeek provider."
        ),
        "xendris_version": xendris.__version__,
        "dataset_name": "Trust Traps v0.1",
        "dataset_version": "0.1",
        "dataset_hash": dataset_hash,
        "dataset_hash_algorithm": "sha256",
        "model": args.model,
        "base_model": args.model,
        "provider": "mock" if args.dry_run else "deepseek",
        "temperature": 0.0,
        "top_p": 1.0,
        "max_tokens": 1024,
        "pricing_assumptions": "Dry-run costs are deterministic placeholders; real runs use provider-reported usage.",
        "prompt_policy_hash": hashlib.sha256(b"standard-policy").hexdigest()[:12],
        "run_date": run_started_at[:10],
        "python_version": platform.python_version(),
    }
    report_text = _render_trust_report(summary_dict)
    excellence_assessment = assess_benchmark_excellence(summary_dict, report_text)

    try:
        write_ab_results_jsonl(results, jsonl_output)
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(summary_dict, f, ensure_ascii=False, indent=2)
        with open(report_output, "w", encoding="utf-8") as f:
            f.write(report_text)
        with open(excellence_output, "w", encoding="utf-8") as f:
            json.dump(excellence_assessment.to_dict(), f, ensure_ascii=False, indent=2, sort_keys=True)
    except Exception as e:
        print(f"Error saving results: {e}", file=sys.stderr)
        return 1

    # 5. Output compact summary to console
    print("\n" + "="*50)
    print("           A/B RUN SUMMARY (TRUST TRAPS v0.1)")
    print("="*50)
    print(f"Total Samples:        {summary.total_samples}")
    print(f"Xendris Wins:         {summary.xendris_wins}")
    print(f"DeepSeek Wins:        {summary.deepseek_wins}")
    print(f"Ties:                 {summary.ties}")
    print(f"Avg Score DeepSeek:   {summary.average_deepseek_score}")
    print(f"Avg Score Xendris:    {summary.average_xendris_score}")
    print(f"Average Delta:        {summary.average_delta}")
    print(f"Xendris Win Rate:     {summary.xendris_win_rate * 100:.1f}%")
    print(f"Avg Latency DeepSeek: {summary.average_latency_deepseek_ms} ms")
    print(f"Avg Latency Xendris:  {summary.average_latency_xendris_ms} ms")
    print(f"Latency Overhead:     {summary.latency_overhead_ms} ms")
    print(f"Xendris Exclusions:   {summary.xendris_exclusion_rate * 100:.1f}%")
    print(f"Xendris Human Review: {summary.xendris_human_review_rate * 100:.1f}%")
    print(f"Cost per Valid DS:    ${summary.cost_per_valid_answer_deepseek:.6f}")
    print(f"Cost per Valid XE:    ${summary.cost_per_valid_answer_xendris:.6f}")
    print("="*50)
    print(f"Results saved to: {jsonl_output}")
    print(f"Summary saved to: {json_output}")
    print(f"Report saved to: {report_output}")
    print(f"Excellence assessment saved to: {excellence_output}")
    print(f"Excellence Decision: {excellence_assessment.decision.value}")
    print("="*50 + "\n")

    return 0


def _render_trust_report(summary: dict[str, object]) -> str:
    """Render a minimal Markdown report for Trust Traps benchmark interpretation."""
    metadata = summary["metadata"]
    return f"""# DeepSeek Base vs Xendris+DeepSeek - Trust Traps v0.1

## Purpose

Measure benchmark-local resistance to trust traps under the fixed Trust Traps
v0.1 dataset and configured Xendris gates.

## Configuration

| Field | Value |
|---|---|
| Execution mode | `{metadata['execution_mode']}` |
| Provider | `{metadata['provider']}` |
| Model | `{metadata['model']}` |
| Temperature | `{metadata['temperature']}` |
| Max tokens | `{metadata['max_tokens']}` |
| Dataset hash | `{metadata['dataset_hash']}` |
| Xendris version | `{metadata['xendris_version']}` |

## No Universal Superiority Warning

This benchmark does not imply universal model superiority. It only measures a
closed benchmark-local behavior under Trust Traps v0.1 and this configuration.

## Results

| Metric | Value |
|---|---:|
| Total samples | {summary['total_samples']} |
| DeepSeek average score | {summary['average_deepseek_score']} |
| Xendris average score | {summary['average_xendris_score']} |
| Average delta | {summary['average_delta']} |
| Xendris wins | {summary['xendris_wins']} |
| DeepSeek wins | {summary['deepseek_wins']} |
| Ties | {summary['ties']} |
| Cost per valid DeepSeek answer | {summary['cost_per_valid_answer_deepseek']} |
| Cost per valid Xendris answer | {summary['cost_per_valid_answer_xendris']} |
| DeepSeek average latency ms | {summary['average_latency_deepseek_ms']} |
| Xendris average latency ms | {summary['average_latency_xendris_ms']} |

## Limitations

- Closed dataset.
- Benchmark-local interpretation only.
- Dry-run results do not measure real provider performance.
- Passing the excellence gate does not validate universal superiority.
"""


if __name__ == "__main__":
    sys.exit(main())
