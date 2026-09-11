from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "crop_health"
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    confidence_high: float = 0.75
    confidence_medium: float = 0.50

    risk_low_max: int = 39
    risk_moderate_max: int = 69

    max_image_size_mb: int = 10
    allowed_image_types: str = "image/jpeg,image/png,image/webp"

    weather_api_key: str = ""
    weather_api_url: str = ""

    model_path: str = "app/ml/artifacts/model.keras"
    class_map_path: str = "app/ml/artifacts/class_map.json"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"

    upload_dir: str = "uploads"
    heatmap_dir: str = "uploads/heatmaps"

    hotspot_min_reports: int = 3
    hotspot_min_confidence: float = 0.50
    hotspot_window_days: int = 14

    @property
    def allowed_types_list(self) -> list[str]:
        return [t.strip() for t in self.allowed_image_types.split(",")]

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
