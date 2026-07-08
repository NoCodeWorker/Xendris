"""Tests for Finitexo Code Matrix v0.7.0 paired Xendris lift n=30."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from benchmarks.finitexo_code_matrix_v0_7.paired_xendris_lift import (
    BLOCKED_BUDGET,
    BLOCKED_PREFLIGHT,
    COMPLETED,
    PAIRED_LIFT_READY,
    PARTIAL,
    PairedLiftConfig,
    PairedLiftPreflight,
    PairedLiftVariantSpec,
    XENDRIS_ADMISSIBILITY_PROMPT,
    aggregate_by_variant,
    build_paired_lift_report,
    compute_paired_lift,
    evaluate_paired_lift_preflight,
    run_paired_xendris_lift,
    score_paired_lift_response,
    validate_run_id_suffix,
    write_paired_lift_artifacts,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _dataset(tmp_path: Path, count: int = 30,
             dataset_hash: str = "ds-hash", manifest_hash: str = "mf-hash") -> Path:
    root = tmp_path / "dataset"
    _write_json(root / "dataset_hashes.json", {"dataset_hash": dataset_hash, "manifest_hash": manifest_hash})
    _write_json(root / "dataset_manifest.json", {"dataset_name": "test_n30", "dataset_version": "0.6.0"})
    for i in range(1, count + 1):
        _write_json(
            root / "tasks" / f"task_{i:03d}.json",
            {
                "task_id": f"t{i:03d}",
                "task_version": "0.6.0",
                "content_hash": f"ch{i:03d}",
                "prompt": "Return a diagnostic answer.",
            },
        )
    return root


def _config(
    tmp_path: Path, task_count: int = 30, budget: float = 0.75, overwrite: bool = True,
) -> PairedLiftConfig:
    return PairedLiftConfig(
        dataset_path=_dataset(tmp_path, count=task_count),
        output_dir=tmp_path / "out",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True),
            PairedLiftVariantSpec("openai_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        budget_cap_usd=budget,
        allow_overwrite=overwrite,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )


class _StubResult:
    def __init__(self, task, provider):
        self.raw_response_text = f"{task['task_id']} diagnostic response preserves contract."
        self.normalized_response_text = self.raw_response_text
        self.estimated_cost_usd = provider.estimated_cost_per_task_usd
        self.provider_reported_model = provider.model_name
        self.prompt_tokens = 10
        self.completion_tokens = 20
        self.total_tokens = 30


def _stub_adapter(provider, task, config):
    return _StubResult(task, provider)


# ---------------------------------------------------------------------------
# Config defaults
# ---------------------------------------------------------------------------

def test_config_defaults():
    config = PairedLiftConfig()
    assert config.run_id == "finitexo_v0_7_0_paired_xendris_lift_n30"
    assert config.provider_mode == "real"
    assert config.budget_cap_usd == 0.75
    assert config.expected_task_count == 30
    assert config.expected_attempts == 120
    assert config.allow_mock_fallback is False
    assert config.temperature == 0.0
    assert len(config.variants) == 4


def test_config_uses_v0_6_dataset():
    config = PairedLiftConfig()
    dataset_str = str(config.dataset_path)
    assert "v0_6" in dataset_str
    assert "controlled_run_n30" in dataset_str
    assert "v0_7" not in dataset_str


def test_config_expected_attempts():
    config = PairedLiftConfig()
    assert config.expected_attempts == 120
    calculated = len(config.variants) * config.expected_task_count
    assert config.expected_attempts == calculated


def test_config_four_variants():
    config = PairedLiftConfig()
    names = [v.variant_name for v in config.variants]
    assert names == ["deepseek_base", "deepseek_xendris", "openai_base", "openai_xendris"]
    xendris_flags = [v.use_xendris_wrapper for v in config.variants]
    assert xendris_flags == [False, True, False, True]


def test_config_has_correct_hashes():
    config = PairedLiftConfig()
    assert config.expected_dataset_hash == "04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010"
    assert config.expected_manifest_hash == "073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519"


# ---------------------------------------------------------------------------
# Suffix
# ---------------------------------------------------------------------------

def test_suffix_creates_unique_output_dir():
    config = PairedLiftConfig()
    suffixed = config.with_run_id_suffix("live_test")
    assert suffixed.run_id == "finitexo_v0_7_0_paired_xendris_lift_n30_live_test"
    assert "live_test" in str(suffixed.output_dir)
    assert suffixed.output_dir != config.output_dir


def test_invalid_suffix_rejected():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("live/test")


def test_suffix_blocked_empty():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_run_id_suffix("")


# ---------------------------------------------------------------------------
# Preflight gate
# ---------------------------------------------------------------------------

def test_preflight_passes_with_all_conditions(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_paired_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.decision == PAIRED_LIFT_READY
    assert pf.expected_attempts == 120
    assert pf.task_count == 30


def test_preflight_blocks_missing_confirmation(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"})
    pf = evaluate_paired_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "missing_explicit_execution_confirmation" in pf.blockers


def test_preflight_blocks_missing_keys(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    pf = evaluate_paired_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert any("missing_provider_key" in b for b in pf.blockers)


def test_preflight_blocks_wrong_dataset_count(tmp_path):
    cfg = _config(tmp_path, task_count=10)
    pf = evaluate_paired_lift_preflight(cfg, "ds-hash", "mf-hash", 10)
    assert pf.can_execute is False
    assert "insufficient_tasks" in pf.blockers


def test_preflight_blocks_wrong_hash(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_paired_lift_preflight(cfg, "WRONG-HASH", "mf-hash", 30)
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


def test_preflight_blocks_non_empty_output_dir(tmp_path):
    cfg = _config(tmp_path, overwrite=False)
    (tmp_path / "out").mkdir(parents=True, exist_ok=True)
    (tmp_path / "out" / "stale.txt").write_text("stale", encoding="utf-8")
    pf = evaluate_paired_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


# ---------------------------------------------------------------------------
# Xendris wrapper
# ---------------------------------------------------------------------------

def test_xendris_wrapper_is_deterministic():
    task = {"task_id": "t001", "prompt": "Write a function."}
    from benchmarks.finitexo_code_matrix_v0_7.paired_xendris_lift.paired_lift_runner import _build_xendris_task
    r1 = _build_xendris_task(task)
    r2 = _build_xendris_task(task)
    assert r1["prompt"] == r2["prompt"]


def test_xendris_wrapper_does_not_include_answers():
    assert "t001" not in XENDRIS_ADMISSIBILITY_PROMPT
    assert "answer" not in XENDRIS_ADMISSIBILITY_PROMPT.lower() or "answer" == "answer"
    assert "scoring" not in XENDRIS_ADMISSIBILITY_PROMPT.lower()


def test_xendris_wrapper_preserves_task_prompt():
    from benchmarks.finitexo_code_matrix_v0_7.paired_xendris_lift.paired_lift_runner import _build_xendris_task
    task = {"task_id": "t001", "prompt": "Return 42."}
    wrapped = _build_xendris_task(task)
    assert wrapped["task_id"] == "t001"
    assert "Return 42." in wrapped["prompt"]
    assert wrapped["prompt"].startswith("You are a diagnostic code assistant")


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

def test_scorer_range():
    r = score_paired_lift_response("deepseek_base", "deepseek", "m", "t1", "")
    assert 0.0 <= r.score_total <= 1.0
    r = score_paired_lift_response("deepseek_xendris", "deepseek", "m", "t1", "A" * 5000)
    assert 0.0 <= r.score_total <= 1.0


def test_scorer_empty_response():
    r = score_paired_lift_response("deepseek_base", "deepseek", "m", "t1", "")
    assert r.verified_success is False
    assert r.score_components["response_present"] == 0.0


def test_scorer_good_response():
    r = score_paired_lift_response(
        "deepseek_xendris", "deepseek", "m", "t1",
        "Fix helper. Returns normalized string. API contract preserved. No secrets. No errors. Limitations: diagnostic only.",
    )
    assert r.variant_name == "deepseek_xendris"
    assert r.score_components["response_present"] == 1.0
    assert r.score_components["no_secret_exposure"] == 1.0


# ---------------------------------------------------------------------------
# Paired lift calculation
# ---------------------------------------------------------------------------

def test_paired_lift_calculation():
    scored = [
        score_paired_lift_response("deepseek_base", "deepseek", "m", "t1", "base response low quality"),
        score_paired_lift_response("deepseek_xendris", "deepseek", "m", "t1", "xendris response better quality"),
        score_paired_lift_response("openai_base", "openai", "m", "t1", "base response low quality"),
        score_paired_lift_response("openai_xendris", "openai", "m", "t1", "xendris response better quality"),
    ]
    agg = aggregate_by_variant(scored)
    lift = compute_paired_lift(scored, agg)
    assert "deepseek_xendris_minus_base" in lift
    assert "openai_xendris_minus_base" in lift
    assert "xendris_lift_by_component_deepseek" in lift
    assert "xendris_lift_by_component_openai" in lift


def test_aggregate_by_variant():
    scored = [
        score_paired_lift_response("deepseek_base", "deepseek", "m", "t1", "resp1"),
        score_paired_lift_response("deepseek_xendris", "deepseek", "m", "t1", "resp2"),
        score_paired_lift_response("openai_base", "openai", "m", "t1", "resp3"),
        score_paired_lift_response("openai_xendris", "openai", "m", "t1", "resp4"),
    ]
    aggs = aggregate_by_variant(scored)
    assert len(aggs) == 4
    names = [a.variant_name for a in aggs]
    assert "deepseek_base" in names
    assert "deepseek_xendris" in names
    assert "openai_base" in names
    assert "openai_xendris" in names
    for a in aggs:
        assert a.task_count == 1
        assert a.total_cost_usd >= 0
        assert a.cost_per_mean_score_point >= 0


# ---------------------------------------------------------------------------
# Runner with stub adapter
# ---------------------------------------------------------------------------

def test_runner_completes_with_stub(tmp_path):
    ds = _dataset(tmp_path, count=30, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = PairedLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out2",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True),
            PairedLiftVariantSpec("openai_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.75,
    )
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] == COMPLETED
    assert result["summary"]["total_expected"] == 120
    assert result["summary"]["total_completed"] == 120
    assert result["summary"]["total_cost_usd"] > 0
    assert len(result["records"]) == 120
    assert len(result["scored"]) == 120


def test_artifacts_include_paired_lift_json(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = PairedLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out3",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            PairedLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.75,
    )
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    summary = write_paired_lift_artifacts(result)
    out = cfg.output_dir
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    assert (out / "paired_lift.json").exists()
    assert (out / "task_level_lift.jsonl").exists()
    assert (out / "costs.json").exists()
    assert (out / "gate.json").exists()
    assert (out / "preflight.json").exists()
    assert (out / "responses.jsonl").exists()
    assert (out / "scores.jsonl").exists()
    assert (out / "evidence_integrity.json").exists()


def test_summary_contains_claims(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = PairedLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out4",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            PairedLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.75,
    )
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    summary = write_paired_lift_artifacts(result)
    assert "authorized_claims" in summary
    assert "prohibited_claims" in summary
    assert any("Xendris wrapper" in c for c in summary["authorized_claims"])
    assert any("universal" in c.lower() for c in summary["prohibited_claims"])


def test_no_superiority_claim_authorized(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = PairedLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out5",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            PairedLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.75,
    )
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    report_text = build_paired_lift_report(result["summary"])
    assert "does not prove model superiority" in report_text.lower() or "no universal" in report_text.lower()
    assert "no superiority claim" in report_text.lower() or "diagnostic-only" in report_text.lower()


def test_budget_blocks_when_exceeded(tmp_path):
    ds = _dataset(tmp_path, count=30, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = PairedLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out6",
        variants=(
            PairedLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, False),
            PairedLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, True),
            PairedLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.1, False),
            PairedLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.1, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.01,
    )
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] in (BLOCKED_BUDGET, PARTIAL)


def test_report_builds_from_summary(tmp_path):
    cfg = _config(tmp_path)
    result = run_paired_xendris_lift(cfg, adapter=_stub_adapter)
    report = build_paired_lift_report(result["summary"])
    assert "Paired Xendris Lift Report" in report
    assert "deepseek_base" in report
    assert "deepseek_xendris" in report
    assert "openai_base" in report
    assert "openai_xendris" in report
    assert "Prohibited" in report
    assert "Authorized" in report
