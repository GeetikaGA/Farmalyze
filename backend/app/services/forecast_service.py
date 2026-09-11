from __future__ import annotations

"""Forward-looking outbreak forecast (transparent heuristic).

This is NOT a trained time-series model — it is an explainable rule-based estimate
of the probability that an outbreak develops/worsens in the near term, combining:
  - weather favorability for pathogen/pest spread (humidity + rainfall)
  - report velocity / momentum (recent report volume and trend)
  - expert-confirmed cases (ground truth weight)
  - the current composite risk score

The output is a 0–100 "predicted outbreak" probability with the drivers exposed,
so it can be shown honestly alongside the current-state risk score.
"""

from typing import Any


def _weather_favorability(weather: dict[str, Any]) -> float:
    humidity = weather.get("humidity", 50) / 100
    rainfall = min(weather.get("rainfall_mm", 0) / 30, 1.0)
    return min(1.0, humidity * 0.6 + rainfall * 0.4)


def _level(prob: int) -> str:
    if prob >= 70:
        return "high"
    if prob >= 40:
        return "moderate"
    return "low"


def compute_forecast(
    *,
    weather: dict[str, Any],
    report_count: int = 0,
    trend: str = "stable",
    confirmed_count: int = 0,
    base_risk: int = 0,
) -> dict[str, Any]:
    weather_sig = _weather_favorability(weather)

    # Momentum from how many recent reports and whether the trend is rising.
    volume_sig = min(1.0, report_count / 20)
    trend_sig = {"increasing": 1.0, "stable": 0.45, "decreasing": 0.15}.get(trend, 0.45)
    momentum_sig = min(1.0, 0.6 * volume_sig + 0.4 * trend_sig)

    confirmed_sig = min(1.0, confirmed_count / 8)
    risk_sig = min(1.0, base_risk / 100)

    weights = {
        "weather": 0.30,
        "momentum": 0.30,
        "confirmed": 0.20,
        "current_risk": 0.20,
    }
    raw = (
        weather_sig * weights["weather"]
        + momentum_sig * weights["momentum"]
        + confirmed_sig * weights["confirmed"]
        + risk_sig * weights["current_risk"]
    )
    prob = int(min(100, max(0, round(raw * 100))))

    def lvl(v: float) -> str:
        return "high" if v >= 0.7 else "moderate" if v >= 0.4 else "low"

    drivers = [
        {"name": "Weather favorability", "level": lvl(weather_sig), "weight": weights["weather"]},
        {"name": "Report momentum", "level": lvl(momentum_sig), "weight": weights["momentum"]},
        {"name": "Expert-confirmed cases", "level": lvl(confirmed_sig), "weight": weights["confirmed"]},
        {"name": "Current risk", "level": lvl(risk_sig), "weight": weights["current_risk"]},
    ]

    return {
        "probability": prob,
        "level": _level(prob),
        "drivers": drivers,
        "explanation": (
            f"Predicted outbreak probability {prob}% over the coming days — a transparent "
            "heuristic from weather, report momentum, confirmations and current risk. "
            "Not a trained forecasting model."
        ),
    }
