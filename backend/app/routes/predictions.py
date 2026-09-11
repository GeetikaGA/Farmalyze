import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.config import get_settings
from app.data.advisory_kb import build_recommendation
from app.database import get_db
from app.ml.class_map import crop_capability, is_model_crop
from app.ml.inference import get_classifier
from app.schemas import PredictResponse
from app.security import get_current_user
from app.services.alert_service import broadcast_district_alert
from app.services.forecast_service import compute_forecast
from app.services.hotspot_service import get_local_counts, refresh_hotspots
from app.services.risk_engine import risk_engine
from app.services.weather_service import weather_service

router = APIRouter(tags=["predictions"])


def _confidence_level(confidence: float) -> str:
    settings = get_settings()
    if confidence >= settings.confidence_high:
        return "high"
    if confidence >= settings.confidence_medium:
        return "medium"
    return "low"


@router.post("/predict", response_model=PredictResponse)
async def predict(
    crop_id: str = Form(...),
    growth_stage: str = Form(...),
    district: str = Form(...),
    symptoms: str = Form(""),
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    settings = get_settings()
    db = get_db()

    crop_doc = await db.crops.find_one({"id": crop_id, "user_id": user["id"]})
    if not crop_doc:
        raise HTTPException(status_code=404, detail="Crop not found")

    if file.content_type not in settings.allowed_types_list:
        raise HTTPException(status_code=400, detail="Unsupported image format. Use JPEG, PNG, or WebP.")

    content = await file.read()
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"Image exceeds {settings.max_image_size_mb}MB limit.")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if file.content_type == "image/jpeg" else Path(file.filename or "img").suffix or ".png"
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = upload_dir / filename
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    # --- Crop capability gate (honest) ---
    # For crops the image model was never trained on (Cotton/Soybean/Chilli), do NOT
    # run inference — it would return a wrong Tomato/Potato/Corn class. Instead return
    # an honest response with environmental (weather+stage) risk, a forward forecast,
    # and a pointer to pest reporting + curated advisories.
    if not is_model_crop(crop_doc["crop"]):
        weather = await weather_service.get_weather(district)
        local_reports, expert_confirmed = await get_local_counts(district, crop_doc["crop"])
        risk = risk_engine.compute(
            disease="unknown",
            confidence=0.0,
            confidence_level="low",
            crop=crop_doc["crop"],
            growth_stage=growth_stage,
            district=district,
            weather=weather,
            local_report_count=local_reports,
            expert_confirmed_count=expert_confirmed,
            image_quality_acceptable=True,
        )
        forecast = compute_forecast(
            weather=weather,
            report_count=local_reports,
            trend="increasing" if local_reports >= settings.hotspot_min_reports else "stable",
            confirmed_count=expert_confirmed,
            base_risk=risk["score"],
        )
        recommendation = build_recommendation(crop_doc["crop"], "Unknown", "low", True)
        recommendation["title"] = f"Image disease detection for {crop_doc['crop']} is coming soon"
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc)
        disease_label = f"Not analysed — image AI unavailable for {crop_doc['crop']}"
        image_quality = {
            "acceptable": True,
            "score": 0.0,
            "message": "Image disease detection is not yet available for this crop. Use pest reporting and advisories.",
        }
        explanation = {"available": False, "heatmap_url": None, "message": "No image model for this crop yet."}
        record = {
            "id": prediction_id,
            "user_id": user["id"],
            "crop_id": crop_id,
            "kind": "advisory",
            "capability": "advisory_pest",
            "image_url": f"/uploads/{filename}",
            "crop": crop_doc["crop"],
            "disease": disease_label,
            "confidence": 0.0,
            "confidence_level": "low",
            "district": district,
            "growth_stage": growth_stage,
            "symptoms": symptoms,
            "image_quality": image_quality,
            "explanation": explanation,
            "risk": risk,
            "forecast": forecast,
            "recommendation": recommendation,
            "verification": {"recommended": True, "status": "recommended"},
            "verification_status": "recommended",
            "timestamp": timestamp,
        }
        await db.predictions.insert_one(record)
        return PredictResponse(
            prediction_id=prediction_id,
            crop=crop_doc["crop"],
            disease=disease_label,
            confidence=0.0,
            confidence_level="low",
            image_quality=image_quality,
            explanation=explanation,
            risk=risk,
            recommendation=recommendation,
            verification={"recommended": True, "status": "recommended"},
            forecast=forecast,
            capability="advisory_pest",
            image_url=record["image_url"],
            district=district,
            timestamp=timestamp,
        )

    classifier = get_classifier(settings.model_path, settings.class_map_path, settings.heatmap_dir)
    ml_result = classifier.predict(
        str(file_path),
        crop_doc["crop"],
        settings.confidence_high,
        settings.confidence_medium,
    )

    prediction_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc)

    if ml_result.get("skipped_inference"):
        record = {
            "id": prediction_id,
            "user_id": user["id"],
            "crop_id": crop_id,
            "image_url": f"/uploads/{filename}",
            "crop": crop_doc["crop"],
            "disease": "Analysis skipped",
            "confidence": 0.0,
            "confidence_level": "low",
            "district": district,
            "growth_stage": growth_stage,
            "symptoms": symptoms,
            "image_quality": ml_result["image_quality"],
            "explanation": ml_result["explanation"],
            "risk": {"score": 0, "level": "low", "factors": [], "explanation": "Inference skipped due to poor image quality."},
            "recommendation": build_recommendation(crop_doc["crop"], "Unknown", "low", True),
            "verification": {"recommended": True, "status": "recommended"},
            "verification_status": "recommended",
            "timestamp": timestamp,
        }
        await db.predictions.insert_one(record)
        await db.field_observations.insert_one(
            {
                "id": str(uuid.uuid4()),
                "prediction_id": prediction_id,
                "symptoms": symptoms,
                "crop_stage": growth_stage,
                "location": district,
                "timestamp": timestamp,
            }
        )
        return PredictResponse(
            prediction_id=prediction_id,
            crop=crop_doc["crop"],
            disease=record["disease"],
            confidence=0.0,
            confidence_level="low",
            image_quality=ml_result["image_quality"],
            explanation=ml_result["explanation"],
            risk=record["risk"],
            recommendation=record["recommendation"],
            verification=record["verification"],
            image_url=record["image_url"],
            district=district,
            timestamp=timestamp,
        )

    weather = await weather_service.get_weather(district)
    local_reports, expert_confirmed = await get_local_counts(district, ml_result["disease"])

    risk = risk_engine.compute(
        disease=ml_result["disease"],
        confidence=ml_result["confidence"],
        confidence_level=ml_result["confidence_level"],
        crop=crop_doc["crop"],
        growth_stage=growth_stage,
        district=district,
        weather=weather,
        local_report_count=local_reports,
        expert_confirmed_count=expert_confirmed,
        image_quality_acceptable=ml_result["image_quality"]["acceptable"],
    )

    conf_level = ml_result["confidence_level"]
    verification_recommended = conf_level in ("low", "medium") or risk["level"] == "high"
    recommendation = build_recommendation(
        crop_doc["crop"],
        ml_result["disease"],
        conf_level,
        verification_recommended,
    )

    verification_status = "recommended" if verification_recommended else "not_required"

    forecast = compute_forecast(
        weather=weather,
        report_count=local_reports,
        trend="increasing" if local_reports >= settings.hotspot_min_reports else "stable",
        confirmed_count=expert_confirmed,
        base_risk=risk["score"],
    )

    record = {
        "id": prediction_id,
        "user_id": user["id"],
        "crop_id": crop_id,
        "image_url": f"/uploads/{filename}",
        "crop": crop_doc["crop"],
        "disease": ml_result["disease"],
        "confidence": ml_result["confidence"],
        "confidence_level": conf_level,
        "district": district,
        "growth_stage": growth_stage,
        "symptoms": symptoms,
        "image_quality": ml_result["image_quality"],
        "explanation": ml_result["explanation"],
        "risk": risk,
        "recommendation": recommendation,
        "forecast": forecast,
        "kind": "disease",
        "verification": {"recommended": verification_recommended, "status": verification_status},
        "verification_status": verification_status,
        "timestamp": timestamp,
    }
    await db.predictions.insert_one(record)
    await db.field_observations.insert_one(
        {
            "id": str(uuid.uuid4()),
            "prediction_id": prediction_id,
            "symptoms": symptoms,
            "crop_stage": growth_stage,
            "location": district,
            "timestamp": timestamp,
        }
    )

    if risk["level"] in ("moderate", "high") and conf_level != "low":
        # District-wide broadcast: alert every farmer with a crop in this district,
        # not just the scanning user (deduped over a short window).
        await broadcast_district_alert(
            db,
            district=district,
            disease=ml_result["disease"],
            severity=risk["level"],
            kind="disease",
            crop=crop_doc["crop"],
        )

    await db.crops.update_one(
        {"id": crop_id},
        {"$set": {"current_risk": {"score": risk["score"], "level": risk["level"]}}},
    )

    if ml_result["confidence"] >= settings.hotspot_min_confidence:
        await refresh_hotspots()

    return PredictResponse(
        prediction_id=prediction_id,
        crop=crop_doc["crop"],
        disease=ml_result["disease"],
        confidence=ml_result["confidence"],
        confidence_level=conf_level,
        image_quality=ml_result["image_quality"],
        explanation=ml_result["explanation"],
        risk=risk,
        recommendation=recommendation,
        verification={"recommended": verification_recommended, "status": verification_status},
        forecast=forecast,
        capability="ai_disease",
        image_url=record["image_url"],
        district=district,
        timestamp=timestamp,
    )


@router.get("/predictions")
async def list_predictions(user: dict = Depends(get_current_user)):
    db = get_db()
    preds = await db.predictions.find({"user_id": user["id"]}, {"_id": 0}).sort("timestamp", -1).to_list(50)
    return preds


@router.get("/predictions/{prediction_id}")
async def get_prediction(prediction_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    pred = await db.predictions.find_one({"id": prediction_id, "user_id": user["id"]}, {"_id": 0})
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred
