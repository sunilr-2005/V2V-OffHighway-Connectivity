"""Tests for the V2V risk engine."""

from src.risk_engine import RiskEngine


def test_high_risk_detection():
    risk_engine = RiskEngine(collision_distance=35.0, ttc_threshold=5.0)
    local = {
        "position": {"x": 0.0, "y": 0.0},
        "heading_deg": 0.0,
        "speed_mps": 5.0,
    }
    neighbor = {
        "position": {"x": 20.0, "y": 0.0},
        "heading_deg": 90.0,
        "speed_mps": 4.0,
    }
    level, message, distance = risk_engine.evaluate(local, neighbor)
    assert level in {"high", "medium", "low", "safe"}
    assert isinstance(distance, float)


def test_safe_distance_returns_safe():
    risk_engine = RiskEngine(collision_distance=35.0, ttc_threshold=5.0)
    local = {
        "position": {"x": 0.0, "y": 0.0},
        "heading_deg": 0.0,
        "speed_mps": 1.0,
    }
    neighbor = {
        "position": {"x": 200.0, "y": 0.0},
        "heading_deg": 0.0,
        "speed_mps": 1.0,
    }
    level, _, _ = risk_engine.evaluate(local, neighbor)
    assert level == "safe"
