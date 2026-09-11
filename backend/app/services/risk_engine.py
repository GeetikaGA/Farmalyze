from __future__ import annotations

"""Transparent context-aware risk scoring engine."""

from typing import Any

from app.config import get_settings

# Crop stage vulnerability (prototype weights — configurable)
STAGE_VULNERABILITY: dict[str, dict[str, float]] = {
    "Tomato": {"seedling": 0.6, "vegetative": 0.7, "flowering": 0.85, "fruiting": 0.9, "harvest": 0.5},
    "Potato": {"seedling": 0.5, "vegetative": 0.75, "tuber_initiation": 0.9, "bulking": 0.85, "harvest": 0.4},
    "Corn": {"seedling": 0.55, "vegetative": 0.7, "tasseling": 0.85, "grain_fill": 0.8, "maturity": 0.45},
    "Cotton": {"seedling": 0.5, "squaring": 0.75, "flowering": 0.85, "boll_development": 0.9, "boll_opening": 0.7},
    "Soybean": {"seedling": 0.55, "vegetative": 0.7, "flowering": 0.85, "pod_development": 0.9, "maturity": 0.5},
    "Chilli": {"seedling": 0.6, "vegetative": 0.72, "flowering": 0.85, "fruiting": 0.9, "harvest": 0.55},
}


def _level_from_score(score: int) -> str:
    settings = get_settings()
    if score <= settings.risk_low_max:
        return "low"
    if score <= settings.risk_moderate_max:
        return "moderate"
    return "high"


def _signal_level(value: float) -> str:
    if value >= 0.7:
        return "high"
    if value >= 0.4:
        return "moderate"
    return "low"


class RiskEngine:
    def compute(
        self,
        *,
        disease: str,
        confidence: float,
        confidence_level: str,
        crop: str,
        growth_stage: str,
        district: str,
        weather: dict[str, Any],
        local_report_count: int = 0,
        expert_confirmed_count: int = 0,
        image_quality_acceptable: bool = True,
    ) -> dict[str, Any]:
        settings = get_settings()

        # Disease signal from AI
        is_healthy = "healthy" in disease.lower()
        if is_healthy:
            disease_signal = max(0.05, (1 - confidence) * 0.3)
        else:
            disease_signal = confidence
            if confidence_level == "low":
                disease_signal *= 0.5
            elif confidence_level == "medium":
                disease_signal *= 0.75

        if not image_quality_acceptable:
            disease_signal *= 0.3

        # Weather
        humidity = weather.get("humidity", 50) / 100
        rainfall = min(weather.get("rainfall_mm", 0) / 30, 1.0)
        weather_score = min(1.0, (humidity * 0.6 + rainfall * 0.4))

        # Stage vulnerability
        crop_stages = STAGE_VULNERABILITY.get(crop, STAGE_VULNERABILITY["Tomato"])
        stage_score = crop_stages.get(growth_stage.lower(), 0.6)

        # Local reports (normalized)
        local_score = min(1.0, (local_report_count * 0.15) + (expert_confirmed_count * 0.25))

        weights = {
            "disease_signal": 0.35,
            "weather_suitability": 0.20,
            "crop_stage_vulnerability": 0.20,
            "local_reports": 0.25,
        }

        raw = (
            disease_signal * weights["disease_signal"]
            + weather_score * weights["weather_suitability"]
            + stage_score * weights["crop_stage_vulnerability"]
            + local_score * weights["local_reports"]
        )
        score = int(min(100, max(0, round(raw * 100))))

        if is_healthy and confidence_level == "high":
            score = min(score, settings.risk_low_max)

        factors = [
            {
                "name": "Disease signal",
                "level": _signal_level(disease_signal),
                "weight": weights["disease_signal"],
                "explanation": (
                    f"AI detected '{disease}' with {confidence_level} confidence ({confidence:.0%})."
                    if not is_healthy
                    else "Plant appears healthy; residual uncertainty from model."
                ),
            },
            {
                "name": "Weather suitability",
                "level": _signal_level(weather_score),
                "weight": weights["weather_suitability"],
                "explanation": (
                    f"Humidity {weather.get('humidity')}%, rainfall {weather.get('rainfall_mm')}mm "
                    f"({weather.get('source', 'unknown')} data)."
                ),
            },
            {
                "name": "Crop stage vulnerability",
                "level": _signal_level(stage_score),
                "weight": weights["crop_stage_vulnerability"],
                "explanation": f"{crop} at '{growth_stage}' stage vulnerability factor.",
            },
            {
                "name": "Local reports",
                "level": _signal_level(local_score),
                "weight": weights["local_reports"],
                "explanation": (
                    f"{local_report_count} recent reports, {expert_confirmed_count} expert-confirmed in {district}."
                ),
            },
        ]

        level = _level_from_score(score)
        explanation = (
            f"Composite risk score {score}/100 ({level.upper()}) from weighted factors. "
            "This is a prototype rule-based engine, not advanced AI forecasting."
        )

        return {"score": score, "level": level, "factors": factors, "explanation": explanation}


risk_engine = RiskEngine()
