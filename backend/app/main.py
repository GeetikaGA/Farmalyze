from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import close_db
from app.routes import (
    advisory,
    alerts,
    auth,
    crops,
    official,
    pests,
    predictions,
    reports,
    risk,
    verification,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.heatmap_dir).mkdir(parents=True, exist_ok=True)
    yield
    await close_db()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Farmalyze API",
        description="Farmalyze — Detect → Assess Risk → Alert → Act → Verify → Monitor",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(crops.router)
    app.include_router(predictions.router)
    app.include_router(risk.router)
    app.include_router(alerts.router)
    app.include_router(advisory.router)
    app.include_router(verification.router)
    app.include_router(reports.router)
    app.include_router(pests.router)
    app.include_router(official.router)

    uploads = Path(settings.upload_dir)
    app.mount("/uploads", StaticFiles(directory=str(uploads)), name="uploads")

    @app.get("/health")
    async def health():
        return {"status": "ok", "service": "crop-health-api"}

    @app.get("/meta/crops")
    async def meta_crops():
        from app.data.districts import ALL_DISTRICTS
        from app.ml.class_map import CROP_CAPABILITY, GROWTH_STAGES, MODEL_CROPS, SUPPORTED_CROPS

        return {
            "crops": SUPPORTED_CROPS,
            "growth_stages": GROWTH_STAGES,
            "districts": ALL_DISTRICTS,
            "crop_capability": CROP_CAPABILITY,
            "model_crops": MODEL_CROPS,
        }

    return app


app = create_app()
