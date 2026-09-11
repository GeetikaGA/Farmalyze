import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.data.advisory_kb import PEST_CATALOG, build_recommendation, get_pest_advisory, list_pests_for_crop
from app.database import get_db
from app.schemas import PestReportRequest
from app.security import get_current_user
from app.services.hotspot_service import refresh_hotspots

router = APIRouter(tags=["pests"])


@router.get("/meta/pests")
async def meta_pests(crop: str | None = None):
    """Pest catalog used to build the report form. Optionally filter by crop."""
    catalog = list_pests_for_crop(crop) if crop else PEST_CATALOG
    return {
        "pests": catalog,
        "note": (
            "Pests are reported through a farmer-verified symptom checklist, not image AI. "
            "This is an interim path until the classifier is trained on pest imagery."
        ),
    }


@router.post("/pest-report")
async def submit_pest_report(body: PestReportRequest, user: dict = Depends(get_current_user)):
    db = get_db()
    advisory = get_pest_advisory(body.pest_key)
    if not advisory:
        raise HTTPException(status_code=404, detail="Unknown pest")

    pest_name = advisory["disease"]
    report_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc)

    # Confidence scales with how many checklist symptoms were observed.
    checklist = advisory.get("checklist", []) or []
    matched = [s for s in body.observed_symptoms if s in checklist]
    match_ratio = (len(matched) / len(checklist)) if checklist else 0.6
    confidence = round(min(0.95, 0.5 + match_ratio * 0.45), 2)

    severity_score = {"low": 30, "moderate": 58, "high": 82}[body.severity]
    risk = {
        "score": severity_score,
        "level": body.severity,
        "factors": [
            {
                "name": "Field observation",
                "level": body.severity,
                "weight": 0.6,
                "explanation": f"{len(matched)}/{len(checklist)} checklist symptoms confirmed by the farmer.",
            },
            {
                "name": "Reported severity",
                "level": body.severity,
                "weight": 0.4,
                "explanation": f"Farmer graded the infestation as {body.severity}.",
            },
        ],
        "explanation": (
            f"Pest report for {pest_name} on {body.crop} in {body.district}. "
            "Rule-based severity from a farmer symptom checklist, not image AI."
        ),
    }

    recommendation = build_recommendation(body.crop, pest_name, "high" if body.severity == "high" else "medium", True)

    # Stored in the predictions collection with kind="pest" so it flows into the
    # same hotspot / risk-map / alert pipeline as disease detections.
    record = {
        "id": report_id,
        "user_id": user["id"],
        "kind": "pest",
        "image_url": None,
        "crop": body.crop,
        "disease": pest_name,
        "pest_key": body.pest_key,
        "confidence": confidence,
        "confidence_level": "high" if confidence >= 0.75 else "medium",
        "district": body.district,
        "growth_stage": "",
        "symptoms": ", ".join(body.observed_symptoms),
        "notes": body.notes,
        "image_quality": {"acceptable": True, "score": 1.0, "message": "Symptom checklist report"},
        "explanation": {"available": False, "heatmap_url": None, "message": "Farmer-submitted pest report."},
        "risk": risk,
        "recommendation": recommendation,
        "verification": {"recommended": True, "status": "recommended"},
        "verification_status": "recommended",
        "timestamp": timestamp,
    }
    await db.predictions.insert_one(record)

    # Broadcast an alert to every farmer with a crop registered in that district
    # (district-wide push, not just the reporter) for moderate/high infestations.
    if body.severity in ("moderate", "high"):
        district_crop_owners = await db.crops.distinct("user_id", {"district": body.district})
        recipients = set(district_crop_owners) | {user["id"]}
        alerts = [
            {
                "id": str(uuid.uuid4()),
                "user_id": uid,
                "district": body.district,
                "disease": pest_name,
                "kind": "pest",
                "severity": body.severity,
                "message": (
                    f"{body.severity.upper()} pest alert: {pest_name} reported on {body.crop} "
                    f"in {body.district}. Scout your field and set up traps."
                ),
                "created_at": timestamp,
                "read_status": False,
            }
            for uid in recipients
        ]
        if alerts:
            await db.alerts.insert_many(alerts)

    await refresh_hotspots()

    return {
        "report_id": report_id,
        "pest": pest_name,
        "crop": body.crop,
        "district": body.district,
        "confidence": confidence,
        "risk": risk,
        "recommendation": recommendation,
    }


@router.get("/pest-reports")
async def list_pest_reports(user: dict = Depends(get_current_user)):
    db = get_db()
    reports = await db.predictions.find(
        {"user_id": user["id"], "kind": "pest"}, {"_id": 0}
    ).sort("timestamp", -1).to_list(100)
    return reports
