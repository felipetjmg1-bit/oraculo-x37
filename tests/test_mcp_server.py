from __future__ import annotations

from app.mcp.server import (
    assess_decision,
    audit_algorithm,
    explain_prediction,
    monitor_asset,
    simulate_future,
)


def test_simulate_future_is_deterministic_and_labeled_as_exploratory():
    result = simulate_future(
        {"population": 100.0},
        [{"name": "growth", "growth_rates": {"population": 0.1}}],
        horizon=2,
    )
    assert result["operation"] == "simulate_future"
    assert result["human_review_required"] is True
    assert result["data"]["scenarios"][0]["series"][-1]["values"]["population"] == 121.0
    assert any("não representa probabilidade" in warning for warning in result["warnings"])


def test_explain_prediction_exposes_linear_contributions():
    result = explain_prediction(8.0, {"a": 2.0, "b": 3.0}, {"a": 1.0, "b": 2.0})
    data = result["data"]
    assert data["reconstructed_score"] == 8.0
    assert data["contributions"] == {"a": 2.0, "b": 6.0}
    assert data["ranked_drivers"][0]["feature"] == "b"


def test_audit_algorithm_reports_metrics_and_fingerprints():
    result = audit_algorithm(
        "synthetic-model",
        [{"x": 1}, {"x": 2}],
        [1.2, 1.8],
        outcomes=[1.0, 2.0],
    )
    metrics = result["data"]["metrics"]
    assert metrics["observations"] == 2
    assert metrics["mae"] == 0.2
    assert len(result["data"]["input_fingerprint"]) == 64


def test_monitor_asset_applies_declared_thresholds():
    result = monitor_asset(
        "synthetic-asset",
        {"temperature": 95.0},
        {"temperature": {"warning_high": 80.0, "critical_high": 90.0}},
    )
    assert result["data"]["overall_status"] == "critical"


def test_assess_decision_returns_weighted_ranking():
    result = assess_decision(
        "synthetic choice",
        [{"name": "cost", "weight": 1}, {"name": "quality", "weight": 3}],
        [
            {"name": "A", "scores": {"cost": 10, "quality": 5}},
            {"name": "B", "scores": {"cost": 4, "quality": 9}},
        ],
    )
    ranking = result["data"]["ranking"]
    assert ranking[0]["option"] == "B"
    assert ranking[0]["score"] == 7.75
