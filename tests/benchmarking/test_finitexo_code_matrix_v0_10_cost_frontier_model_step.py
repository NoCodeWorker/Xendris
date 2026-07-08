"""Tests for Finitexo Code Matrix v0.10.0 Cost Frontier Model-Step."""

import json
import hashlib
from pathlib import Path
from typing import Any

import pytest

from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step import (
    COMPLETED,
    COST_FRONTIER_DECISIONS,
    PARTIAL,
    CostFrontierConfig,
    CostFrontierVariantSpec,
    aggregate_by_variant,
    build_cost_frontier_report,
    compute_cost_frontier,
    evaluate_cost_frontier_preflight,
    run_cost_frontier,
    score_cost_frontier_response,
    write_cost_frontier_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_scoring import (
    _efficient_frontier_decision,
)

FAMILIES = [
    "algorithmic_reasoning",
    "stateful_refactor",
    "edge_case_handling",
    "api_design_consistency",
    "performance_constraints",
]

VARIANTS = [
    "deepseek_v4_flash_base", "deepseek_v4_flash_calibrated_runtime", "deepseek_v4_pro_base",
    "gpt_4_1_nano_base", "gpt_4_1_nano_calibrated_runtime", "gpt_4_1_mini_base",
]


from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_gate import (
    _file_hash,
)


def _make_dataset(tmp_path: Path, count: int = 30) -> Path:
    root = tmp_path / "dataset"
    root.mkdir(parents=True, exist_ok=True)

    manifest = {"dataset_name": "finitexo_code_matrix_hard_programming_n30", "dataset_version": "0.8.0"}
    (root / "dataset_manifest.json").write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

    fake_dh = "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
    mh = hashlib.sha256((root / "dataset_manifest.json").read_bytes()).hexdigest()
    (root / "dataset_hashes.json").write_text(
        json.dumps({"dataset_hash": fake_dh, "manifest_hash": mh}, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    tasks_dir = root / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    for i in range(1, count + 1):
        family = FAMILIES[i % len(FAMILIES)]
        (tasks_dir / f"task_{i:03d}.json").write_text(
            json.dumps({
                "task_id": f"t{i:03d}",
                "task_version": "0.8.0",
                "content_hash": f"ch{i:03d}",
                "family": family,
                "prompt": "Return a diagnostic answer.",
                "constraints": ["format: return code only"],
                "public_contract": "return result",
                "scoring_focus": ["correctness"],
            }, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return root


def _config(tmp_path: Path) -> CostFrontierConfig:
    dataset = _make_dataset(tmp_path)
    return CostFrontierConfig(
        dataset_path=dataset,
        output_dir=tmp_path / "out",
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def test_config_has_six_variants():
    cfg = CostFrontierConfig()
    assert len(cfg.variants) == 6
    names = [v.variant_name for v in cfg.variants]
    for n in VARIANTS:
        assert n in names


def test_expected_attempts_180():
    cfg = CostFrontierConfig()
    assert cfg.expected_attempts == 180
    assert cfg.expected_attempts == cfg.expected_task_count * len(cfg.variants)


def test_calibrated_runtime_variants_exist():
    cfg = CostFrontierConfig()
    calibrated = [v for v in cfg.variants if v.execution_method == "CALIBRATED_RUNTIME"]
    assert len(calibrated) == 2
    names = [v.variant_name for v in calibrated]
    assert "deepseek_v4_flash_calibrated_runtime" in names
    assert "gpt_4_1_nano_calibrated_runtime" in names


def test_next_model_base_variants_exist():
    cfg = CostFrontierConfig()
    names = [v.variant_name for v in cfg.variants]
    assert "deepseek_v4_pro_base" in names
    assert "gpt_4_1_mini_base" in names


def test_calibrated_variants_have_runtime_loop():
    cfg = CostFrontierConfig()
    for v in cfg.variants:
        if v.execution_method == "CALIBRATED_RUNTIME":
            assert v.use_runtime_loop is True
            assert v.use_calibrated_runtime is True


def test_suffix_validation():
    cfg = CostFrontierConfig()
    suffixed = cfg.with_run_id_suffix("test_suffix")
    assert "test_suffix" in suffixed.run_id
    assert "test_suffix" in str(suffixed.output_dir)
    from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_config import (
        validate_run_id_suffix,
    )
    with pytest.raises(ValueError):
        validate_run_id_suffix("bad/suffix")
    with pytest.raises(ValueError):
        validate_run_id_suffix("")


# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

def test_preflight_blocks_without_confirmation(tmp_path):
    cfg = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=cfg.dataset_path,
        output_dir=tmp_path / "out2",
        environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"},
    )
    pf = evaluate_cost_frontier_preflight(cfg)
    assert pf.can_execute is False
    assert "missing_explicit_execution_confirmation" in pf.blockers or any("confirmation" in b for b in pf.blockers)


def test_preflight_blocks_missing_keys(tmp_path):
    cfg = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=cfg.dataset_path,
        output_dir=tmp_path / "out3",
        environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"},
    )
    pf = evaluate_cost_frontier_preflight(cfg)
    assert pf.can_execute is False
    assert any("missing_provider_key" in b for b in pf.blockers)


def test_preflight_validates_dataset_hash(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_cost_frontier_preflight(cfg, dataset_hash="WRONG")
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


def test_preflight_validates_manifest_hash(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_cost_frontier_preflight(cfg, manifest_hash="WRONG")
    assert pf.can_execute is False
    assert "manifest_hash_mismatch" in pf.blockers


def test_preflight_blocks_unsupported_model():
    cfg = CostFrontierConfig(
        variants=(
            CostFrontierVariantSpec("test_base", "deepseek", "unsupported-model", "DEEPSEEK_API_KEY", 0.0001, "BASE"),
        ),
        output_dir=Path("/tmp/nonexistent"),
        environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true", "DEEPSEEK_API_KEY": "present"},
    )
    pf = evaluate_cost_frontier_preflight(cfg, task_count=30)
    assert pf.can_execute is False
    assert any("unsupported_model" in b for b in pf.blockers)


def test_preflight_blocks_non_empty_output_dir(tmp_path):
    cfg = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=cfg.dataset_path,
        output_dir=cfg.output_dir,
        expected_dataset_hash=cfg.expected_dataset_hash,
        expected_manifest_hash=cfg.expected_manifest_hash,
        expected_attempts=cfg.expected_attempts,
        expected_task_count=cfg.expected_task_count,
        allow_overwrite=False,
        environ=cfg.environ,
    )
    (cfg.output_dir).mkdir(parents=True, exist_ok=True)
    (cfg.output_dir / "stale.txt").write_text("x", encoding="utf-8")
    pf = evaluate_cost_frontier_preflight(cfg)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


def test_preflight_passes_with_all_conditions(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_cost_frontier_preflight(cfg)
    assert pf.can_execute is True
    assert pf.decision == "COST_FRONTIER_PREFLIGHT_READY"
    assert pf.expected_attempts == 180


# ---------------------------------------------------------------------------
# Efficient frontier decisions
# ---------------------------------------------------------------------------

def test_frontier_cheap_calibrated_dominates():
    result = _efficient_frontier_decision("test", 0.01, -0.5)
    assert result == "CHEAP_CALIBRATED_DOMINATES_NEXT_MODEL"


def test_frontier_cheap_calibrated_higher_quality_higher_cost():
    result = _efficient_frontier_decision("test", 0.01, 0.5)
    assert result == "CHEAP_CALIBRATED_HIGHER_QUALITY_HIGHER_COST"


def test_frontier_tradeoff_cheaper_lower_score():
    result = _efficient_frontier_decision("test", -0.01, -0.5)
    assert result == "TRADEOFF_CHEAP_CALIBRATED_LOWER_COST_LOWER_SCORE"


def test_frontier_next_model_dominates():
    result = _efficient_frontier_decision("test", -0.01, 0.5)
    assert result == "NEXT_MODEL_DOMINATES_CHEAP_CALIBRATED"


def test_frontier_inconclusive_small_delta():
    result = _efficient_frontier_decision("test", 0.004, 0.5)
    assert result == "INCONCLUSIVE"

    result = _efficient_frontier_decision("test", -0.004, -0.5)
    assert result == "INCONCLUSIVE"


# ---------------------------------------------------------------------------
# Cost frontier computations
# ---------------------------------------------------------------------------

def test_cost_frontier_comparisons_computed(tmp_path):
    scored = []
    for i in range(30):
        tid = f"t{i:03d}"
        family = FAMILIES[i % len(FAMILIES)]
        for vn in VARIANTS:
            sr = score_cost_frontier_response(vn, "provider", "model", tid, family, "test response", estimated_cost_usd=0.001)
            scored.append(sr)
    agg = aggregate_by_variant(scored)
    cf = compute_cost_frontier(scored, agg)
    assert "comparisons" in cf
    assert len(cf["comparisons"]) == 6
    for comp in cf["comparisons"]:
        assert "comparison_name" in comp
        assert "mean_delta" in comp
        assert "efficient_frontier_decision" in comp


def test_cost_frontier_has_wins_losses_ties(tmp_path):
    scored = []
    for i in range(30):
        tid = f"t{i:03d}"
        family = FAMILIES[i % len(FAMILIES)]
        for vn in VARIANTS:
            sr = score_cost_frontier_response(vn, "provider", "model", tid, family, "test", estimated_cost_usd=0.001)
            scored.append(sr)
    agg = aggregate_by_variant(scored)
    cf = compute_cost_frontier(scored, agg)
    for comp in cf["comparisons"]:
        assert "wins" in comp
        assert "losses" in comp
        assert "ties" in comp


# ---------------------------------------------------------------------------
# Runner with stub adapter
# ---------------------------------------------------------------------------

class _StubResult:
    def __init__(self, task, variant):
        self.raw_response_text = f"{task['task_id']} diagnostic response preserves contract. Fixed. Returns result. Limitation: diagnostic only."
        self.normalized_response_text = self.raw_response_text
        self.estimated_cost_usd = variant.estimated_cost_per_task_usd
        self.provider_reported_model = variant.model_name
        self.prompt_tokens = 10
        self.completion_tokens = 20
        self.total_tokens = 30


def _stub_adapter(variant, task, config):
    return _StubResult(task, variant)


def test_runner_completes_180_with_stub(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_run",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    assert result["final_decision"] == COMPLETED
    assert result["summary"]["total_expected"] == 180
    assert result["summary"]["total_completed"] == 180
    assert len(result["records"]) == 180
    assert len(result["scored"]) == 180


def test_runner_produces_traces_and_calibration(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_trace",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    assert len(result["traces"]) == 60  # 2 calibrated variants * 30 tasks
    assert len(result["calibration_traces"]) == 60


def test_runner_produces_cost_frontier_artifact(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_cf",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    assert "cost_frontier" in result
    cf = result["cost_frontier"]
    assert "comparisons" in cf


def test_artifact_schema_includes_cost_frontier(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_schema",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    out = cfg.output_dir
    assert (out / "cost_frontier.json").exists()
    assert (out / "task_level_frontier.jsonl").exists()
    assert (out / "responses.jsonl").exists()
    assert (out / "scores.jsonl").exists()
    assert (out / "costs.json").exists()
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    assert (out / "preflight.json").exists()
    assert (out / "gate.json").exists()
    assert (out / "evidence_integrity.json").exists()
    assert (out / "runtime_traces.jsonl").exists()
    assert (out / "calibration_traces.jsonl").exists()
    assert (out / "claim_status.jsonl").exists()
    assert (out / "confidence_bands.jsonl").exists()
    assert (out / "allowed_blocked_language.jsonl").exists()
    assert (out / "calibrated_final_responses.jsonl").exists()


def test_report_builds_from_summary(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_report",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    report = build_cost_frontier_report(result["summary"], result.get("cost_frontier", {}))
    assert "Cost Frontier Model-Step Report" in report
    assert "deepseek_v4_flash_base" in report
    assert "gpt_4_1_mini_base" in report
    for c in ["flash_calibrated_vs_flash_base", "pro_base_vs_flash_base", "flash_calibrated_vs_pro_base"]:
        assert c in report
    for c in ["nano_calibrated_vs_nano_base", "mini_base_vs_nano_base", "nano_calibrated_vs_mini_base"]:
        assert c in report
    assert "Authorized Claims" in report
    assert "Prohibited Claims" in report


def test_runner_records_have_task_family(tmp_path):
    base = _config(tmp_path)
    cfg = CostFrontierConfig(
        dataset_path=base.dataset_path,
        output_dir=tmp_path / "out_tf",
        expected_dataset_hash=base.expected_dataset_hash,
        expected_manifest_hash=base.expected_manifest_hash,
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_cost_frontier(cfg, adapter=_stub_adapter)
    for r in result["records"]:
        assert "task_family" in r
        assert r["task_family"] in FAMILIES


# ---------------------------------------------------------------------------
# Blocked preflight artifact writing
# ---------------------------------------------------------------------------

def test_blocked_preflight_writes_artifacts(tmp_path):
    dataset = _make_dataset(tmp_path)
    out = tmp_path / "out_blocked"
    cfg = CostFrontierConfig(
        dataset_path=dataset,
        output_dir=out,
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"},
    )
    result = run_cost_frontier(cfg)
    assert result["final_decision"] == COST_FRONTIER_DECISIONS["BLOCKED"]
    assert (out / "preflight.json").exists()
    assert (out / "gate.json").exists()
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    summary = result.get("summary", {})
    assert summary.get("total_attempted", -1) == 0
    assert summary.get("providers_called") is False
    assert summary.get("blocked_reason") == "preflight"
    assert len(result.get("records", [None])) == 0
    assert len(result.get("scored", [None])) == 0
    assert len(result.get("traces", [None])) == 0


def test_blocked_preflight_no_responses_or_scores(tmp_path):
    dataset = _make_dataset(tmp_path)
    out = tmp_path / "out_blocked2"
    cfg = CostFrontierConfig(
        dataset_path=dataset,
        output_dir=out,
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"},
    )
    result = run_cost_frontier(cfg)
    assert result["final_decision"] == COST_FRONTIER_DECISIONS["BLOCKED"]
    assert not (out / "responses.jsonl").exists()
    assert not (out / "scores.jsonl").exists()
    assert not (out / "runtime_traces.jsonl").exists()
    assert not (out / "calibration_traces.jsonl").exists()
    assert not (out / "cost_frontier.json").exists()
    assert not (out / "costs.json").exists()


def test_blocked_preflight_no_provider_calls(tmp_path):
    call_log: list[str] = []

    class _FakeResult:
        raw_response_text = "stub"
        estimated_cost_usd = 0.001
        provider_reported_model = "stub"
        prompt_tokens = 10
        completion_tokens = 20
        total_tokens = 30

    def _adapter(variant, task, config):
        call_log.append(variant.variant_name)
        return _FakeResult()

    dataset = _make_dataset(tmp_path)
    out = tmp_path / "out_blocked3"
    cfg = CostFrontierConfig(
        dataset_path=dataset,
        output_dir=out,
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"},
    )
    result = run_cost_frontier(cfg, adapter=_adapter)
    assert result["final_decision"] == COST_FRONTIER_DECISIONS["BLOCKED"]
    assert len(call_log) == 0, f"adapter was called {len(call_log)} time(s): {call_log}"
    assert result.get("summary", {}).get("providers_called") is False


def test_non_empty_output_dir_not_overwritten(tmp_path):
    dataset = _make_dataset(tmp_path)
    out = tmp_path / "out_no_overwrite"
    out.mkdir(parents=True, exist_ok=True)
    (out / "stale.txt").write_text("older run data", encoding="utf-8")
    cfg = CostFrontierConfig(
        dataset_path=dataset,
        output_dir=out,
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=False,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    pf = evaluate_cost_frontier_preflight(cfg)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


def test_blocked_preflight_writes_gate_with_preflight_payload(tmp_path):
    dataset = _make_dataset(tmp_path)
    out = tmp_path / "out_gate"
    cfg = CostFrontierConfig(
        dataset_path=dataset,
        output_dir=out,
        expected_dataset_hash=_file_hash(dataset / "dataset_hashes.json"),
        expected_manifest_hash=_file_hash(dataset / "dataset_manifest.json"),
        expected_attempts=180,
        expected_task_count=30,
        allow_overwrite=True,
        environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"},
    )
    result = run_cost_frontier(cfg)
    gate = json.loads((out / "gate.json").read_text(encoding="utf-8"))
    assert gate["final_decision"] == COST_FRONTIER_DECISIONS["BLOCKED"]
    assert "preflight" in gate
    assert isinstance(gate["preflight"], dict)
    assert "blockers" in gate["preflight"]


# ---------------------------------------------------------------------------
# No provider calls in tests
# ---------------------------------------------------------------------------

def test_no_provider_calls():
    cfg = CostFrontierConfig(environ={})
    assert cfg.environ.get("FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM") != "true"
    assert cfg.environ.get("DEEPSEEK_API_KEY") != "present"
    assert cfg.environ.get("OPENAI_API_KEY") != "present"
