"""Public API import tests for Xendris framework v0.2.2."""

import importlib
import warnings
from typing import Any


def _import(module: str, name: str | None = None) -> Any:
    mod = importlib.import_module(module)
    if name:
        return getattr(mod, name)
    return mod


# ── Stable public API ──────────────────────────────────────────────────

def test_xendris_top_level() -> None:
    m = _import("xendris")
    assert m.__version__ == "0.2.0"
    assert hasattr(m, "frontera_c")


def test_frontera_c() -> None:
    m = _import("xendris.frontera_c")
    expected = [
        "C", "HBAR", "G",
        "planck_length", "planck_mass", "planck_area",
        "ClaimType", "Layer", "TraceType",
        "InvalidMassError",
        "validate_compton_gravity_invariant", "compton_wavelength",
        "gravitational_radius", "OperationalScale",
        "review_operational_scale", "frontier_signature",
        "predictive_gain", "epistemic_trace",
        "Claim", "evaluate_claim",
    ]
    for sym in expected:
        assert hasattr(m, sym), f"frontera_c missing {sym}"


def test_core_rag() -> None:
    m = _import("xendris.core.rag")
    for sym in ["SourceRecord", "ClaimRecord", "add_source", "add_claim", "audit_claim_support"]:
        assert hasattr(m, sym), f"core.rag missing {sym}"


def test_core_response_contract() -> None:
    m = _import("xendris.core.response_contract")
    for sym in ["ClaimAssessment", "ResponseContractAssessment", "assess_response_contract"]:
        assert hasattr(m, sym), f"core.response_contract missing {sym}"


def test_models_aggregator() -> None:
    m = _import("xendris.models")
    for sym in ["Claim", "BenchmarkCase", "ModelResponse"]:
        assert hasattr(m, sym), f"models missing {sym}"


# ── Experimental public API ────────────────────────────────────────────

def test_benchmarking() -> None:
    m = _import("xendris.benchmarking")
    for sym in ["run_ab_benchmark", "BenchmarkEvidenceRegistry", "assess_benchmark_excellence"]:
        assert hasattr(m, sym), f"benchmarking missing {sym}"


def test_core_runtime() -> None:
    m = _import("xendris.core.runtime")
    for sym in ["RuntimeRequest", "AgenticTrustRuntime", "ProviderAdapterSandbox"]:
        assert hasattr(m, sym), f"core.runtime missing {sym}"


def test_core_ledger() -> None:
    m = _import("xendris.core.ledger")
    for sym in ["TrustLedgerWriter", "TrustLedgerReader", "TrustEventType",
                 "record_boundary_decision", "record_sector_transition_decision",
                 "record_representation_consistency_decision", "record_model_fingerprint",
                 "record_route_decision"]:
        assert hasattr(m, sym), f"core.ledger missing {sym}"


def test_core_fingerprints() -> None:
    m = _import("xendris.core.fingerprints")
    for sym in ["FingerprintMetric", "ModelEpistemicFingerprint", "FingerprintAggregator"]:
        assert hasattr(m, sym), f"core.fingerprints missing {sym}"


def test_core_router() -> None:
    m = _import("xendris.core.router")
    for sym in ["RouteRequest", "RouteDecision", "MultiModelSelector"]:
        assert hasattr(m, sym), f"core.router missing {sym}"


def test_core_representations() -> None:
    m = _import("xendris.core.representations")
    for sym in ["ClaimRepresentation", "RepresentationConsistencyGate", "compare_representations"]:
        assert hasattr(m, sym), f"core.representations missing {sym}"


def test_core_campaigns() -> None:
    m = _import("xendris.core.campaigns")
    for sym in ["CampaignInput", "run_mesoscopic_boundary_campaign", "build_atlas"]:
        assert hasattr(m, sym), f"core.campaigns missing {sym}"


def test_benchmarks() -> None:
    m = _import("xendris.benchmarks")
    assert hasattr(m, "false_formality"), "benchmarks missing false_formality"


# ── Submodule structure ────────────────────────────────────────────────

def test_benchmarking_submodules() -> None:
    for sub in ["types", "ab_runner", "ablation", "frontier_gap",
                "excellence_gate", "evidence_registry", "scoring", "export_jsonl"]:
        _import(f"xendris.benchmarking.{sub}")


def test_runtime_submodules() -> None:
    for sub in ["request", "response", "adapter", "mock_adapter",
                "claim_extractor", "runtime_policy", "runtime_audit",
                "orchestrator", "provider_adapter", "sandbox", "sandbox_audit"]:
        _import(f"xendris.core.runtime.{sub}")


def test_ledger_submodules() -> None:
    for sub in ["event_type", "record", "hashchain", "writer", "reader", "export", "ledger_audit"]:
        _import(f"xendris.core.ledger.{sub}")


# ── Empty namespaces ───────────────────────────────────────────────────

def _public_symbols(module: str) -> list[str]:
    """Return non-dunder symbols exported by a module."""
    m = _import(module)
    return [x for x in dir(m) if not x.startswith("_")]


def test_prompts_empty() -> None:
    syms = _public_symbols("xendris.prompts")
    assert syms == [], f"prompts should be empty, got {syms}"


def test_outputs_empty() -> None:
    syms = _public_symbols("xendris.outputs")
    assert syms == [], f"outputs should be empty, got {syms}"


def test_scripts_empty() -> None:
    syms = _public_symbols("xendris.scripts")
    assert syms == [], f"scripts should be empty, got {syms}"
