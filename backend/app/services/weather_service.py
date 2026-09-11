from __future__ import annotations

"""Weather service abstraction — swap provider without changing callers."""

from datetime import datetime, timezone
from typing import Any

import httpx

from app.config import get_settings

# Demo districts for simulated weather
DEMO_WEATHER: dict[str, dict] = {
    "Pune": {"temperature": 28.5, "humidity": 72, "rainfall_mm": 12.0, "forecast": "Partly cloudy with light showers"},
    "Nashik": {"temperature": 30.2, "humidity": 65, "rainfall_mm": 5.0, "forecast": "Dry, warm conditions"},
    "Nagpur": {"temperature": 34.0, "humidity": 58, "rainfall_mm": 0.0, "forecast": "Hot and dry"},
    "Aurangabad": {"temperature": 31.5, "humidity": 68, "rainfall_mm": 8.0, "forecast": "Humid, risk of fungal diseases"},
    "Kolhapur": {"temperature": 27.0, "humidity": 80, "rainfall_mm": 25.0, "forecast": "Heavy humidity — monitor blight risk"},
    "default": {"temperature": 29.0, "humidity": 70, "rainfall_mm": 10.0, "forecast": "Moderate conditions (simulated)"},
}


class WeatherService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def get_weather(self, district: str) -> dict[str, Any]:
        if self.settings.weather_api_key and self.settings.weather_api_url:
            try:
                return await self._fetch_live(district)
            except Exception:
                pass
        return self._simulated(district)

    async def _fetch_live(self, district: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                self.settings.weather_api_url,
                params={"q": district, "appid": self.settings.weather_api_key},
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "district": district,
                "temperature": data.get("main", {}).get("temp", 28),
                "humidity": data.get("main", {}).get("humidity", 70),
                "rainfall_mm": data.get("rain", {}).get("1h", 0),
                "forecast": data.get("weather", [{}])[0].get("description", "N/A"),
                "source": "live_api",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    def _simulated(self, district: str) -> dict[str, Any]:
        base = DEMO_WEATHER.get(district, DEMO_WEATHER["default"])
        return {
            "district": district,
            "temperature": base["temperature"],
            "humidity": base["humidity"],
            "rainfall_mm": base["rainfall_mm"],
            "forecast": base["forecast"],
            "source": "simulated_demo",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def disease_favorability(self, weather: dict[str, Any]) -> tuple[str, str]:
        """Return (level, explanation) for weather suitability for fungal diseases."""
        humidity = weather.get("humidity", 50)
        rainfall = weather.get("rainfall_mm", 0)
        if humidity >= 75 and rainfall >= 10:
            return "high", "High humidity and recent rainfall favor fungal pathogen spread (simulated assessment)."
        if humidity >= 65 or rainfall >= 5:
            return "moderate", "Moderate humidity/rainfall may support disease development."
        return "low", "Current weather is less favorable for rapid fungal spread."


weather_service = WeatherService()
