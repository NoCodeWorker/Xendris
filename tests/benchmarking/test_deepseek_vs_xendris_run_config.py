import json
import os
import tempfile
import sys
import pytest
from xendris.benchmarking.providers import DeepSeekBaseProvider, XendrisDeepSeekProvider
from xendris.benchmarking.datasets import load_trust_traps_v0_1
from scripts.run_deepseek_vs_xendris_trust_traps import compute_dataset_hash


def test_1_fixed_configuration_exists():
    # Verify default parameter properties of the adapters
    ds = DeepSeekBaseProvider(mock_mode=True)
    assert ds.model == "deepseek-chat"
    assert ds.temperature == 0.0
    assert ds.max_tokens == 1024
    assert ds.timeout == 95.0

    xe = XendrisDeepSeekProvider(mock_mode=True)
    assert xe.base_provider.model == "deepseek-chat"
    assert xe.base_provider.temperature == 0.0
    assert xe.base_provider.max_tokens == 1024


def test_2_missing_api_key_raises_controlled_error():
    # If API key is missing and mock_mode is False, raises ValueError
    old_key = os.environ.get("DEEPSEEK_API_KEY")
    if "DEEPSEEK_API_KEY" in os.environ:
        del os.environ["DEEPSEEK_API_KEY"]
    try:
        with pytest.raises(ValueError) as excinfo:
            DeepSeekBaseProvider(api_key=None, mock_mode=False)
        assert "DEEPSEEK_API_KEY environment variable is missing" in str(excinfo.value)
    finally:
        if old_key is not None:
            os.environ["DEEPSEEK_API_KEY"] = old_key


def test_3_dataset_hash_stable():
    # Ensure compute_dataset_hash handles non-existent paths and returns stable hash for real paths
    assert compute_dataset_hash("nonexistent_path_to_file") == ""

    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataset_path = os.path.join(current_dir, "xendris", "benchmarking", "datasets", "trust_traps_v0_1.jsonl")

    if os.path.exists(dataset_path):
        hash1 = compute_dataset_hash(dataset_path)
        hash2 = compute_dataset_hash(dataset_path)
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 is 64 hex chars


def test_4_dry_run_execution_and_summary_output():
    # Run the script programmatically in dry-run/mock mode and check outputs
    from scripts.run_deepseek_vs_xendris_trust_traps import main as run_script
    import sys

    with tempfile.TemporaryDirectory() as tmpdir:
        jsonl_output = os.path.join(tmpdir, "deepseek_vs_xendris_trust_traps_v0_1.jsonl")
        json_output = os.path.join(tmpdir, "deepseek_vs_xendris_trust_traps_v0_1_summary.json")
        excellence_output = os.path.join(tmpdir, "deepseek_vs_xendris_trust_traps_v0_1_excellence.json")
        report_output = os.path.join(tmpdir, "deepseek_vs_xendris_trust_traps_v0_1_report.md")

        # Override sys.argv to run the script in dry-run with temporary outputs
        sys.argv = [
            "run_deepseek_vs_xendris_trust_traps.py",
            "--dry-run",
            "--output-dir",
            tmpdir
        ]

        exit_code = run_script()
        assert exit_code == 0

        # Verify paths are correct
        assert os.path.exists(jsonl_output)
        assert os.path.exists(json_output)
        assert os.path.exists(excellence_output)
        assert os.path.exists(report_output)

        # Verify summary content and keys
        with open(json_output, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        assert summary_data["total_samples"] == 100
        assert "xendris_wins" in summary_data
        assert "deepseek_wins" in summary_data
        assert "ties" in summary_data
        assert "average_delta" in summary_data
        assert "xendris_win_rate" in summary_data
        assert "metadata" in summary_data

        meta = summary_data["metadata"]
        assert meta["dataset_name"] == "Trust Traps v0.1"
        assert meta["dataset_hash_algorithm"] == "sha256"
        assert meta["execution_mode"] == "dry-run"
        assert meta["external_data_disclosure"]
        assert meta["model"] == "deepseek-chat"
        assert meta["base_model"] == "deepseek-chat"
        assert meta["pricing_assumptions"]
        assert meta["provider"] == "mock"
        assert meta["run_date"]
        assert meta["temperature"] == 0.0
        assert meta["max_tokens"] == 1024
        assert meta["dataset_hash"]
        assert meta["xendris_version"]
        assert meta["python_version"]

        with open(excellence_output, "r", encoding="utf-8") as f:
            excellence_data = json.load(f)
        assert excellence_data["decision"] == "READY_FOR_INTERPRETATION"
        assert excellence_data["has_blockers"] is False
