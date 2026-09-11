import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.schemas import ExpertReviewRequest, VerifyRequest
from app.security import get_current_user, require_role
from app.services.hotspot_service import refresh_hotspots

router = APIRouter(tags=["verification"])


@router.post("/verify-request")
async def request_verification(body: VerifyRequest, user: dict = Depends(get_current_user)):
    db = get_db()
    pred = await db.predictions.find_one({"id": body.prediction_id, "user_id": user["id"]})
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")

    await db.predictions.update_one(
        {"id": body.prediction_id},
        {
            "$set": {
                "verification_status": "pending",
                "verification": {"recommended": True, "status": "pending"},
            }
        },
    )
    if body.symptoms:
        await db.field_observations.update_one(
            {"prediction_id": body.prediction_id},
            {"$set": {"symptoms": body.symptoms}},
        )
    return {"prediction_id": body.prediction_id, "status": "pending"}


@router.get("/verify-status/{prediction_id}")
async def verify_status(prediction_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    pred = await db.predictions.find_one({"id": prediction_id, "user_id": user["id"]}, {"_id": 0})
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    review = await db.expert_reviews.find_one({"prediction_id": prediction_id}, {"_id": 0})
    return {
        "prediction_id": prediction_id,
        "status": pred.get("verification_status", "not_required"),
        "review": review,
    }


@router.post("/expert/review")
async def expert_review(body: ExpertReviewRequest, expert: dict = Depends(require_role("expert"))):
    db = get_db()
    pred = await db.predictions.find_one({"id": body.prediction_id})
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")

    status_map = {"confirm": "confirmed", "correct": "corrected", "uncertain": "uncertain"}
    new_status = status_map[body.decision]
    final_diagnosis = body.final_diagnosis or pred["disease"]
    if body.decision == "correct" and not body.final_diagnosis:
        raise HTTPException(status_code=400, detail="final_diagnosis required when correcting")

    review = {
        "id": str(uuid.uuid4()),
        "prediction_id": body.prediction_id,
        "expert_id": expert["id"],
        "expert_name": expert["name"],
        "original_prediction": pred["disease"],
        "decision": body.decision,
        "final_diagnosis": final_diagnosis,
        "remarks": body.remarks,
        "reviewed_at": datetime.now(timezone.utc),
    }
    await db.expert_reviews.insert_one(review)
    await db.predictions.update_one(
        {"id": body.prediction_id},
        {
            "$set": {
                "verification_status": new_status,
                "expert_id": expert["id"],
                "final_diagnosis": final_diagnosis,
                "verification": {"recommended": True, "status": new_status},
            }
        },
    )
    await refresh_hotspots()
    return review


@router.get("/expert/pending")
async def pending_reviews(expert: dict = Depends(require_role("expert"))):
    db = get_db()
    preds = await db.predictions.find(
        {"verification_status": "pending"},
        {"_id": 0},
    ).sort("timestamp", -1).to_list(50)
    enriched = []
    for p in preds:
        obs = await db.field_observations.find_one({"prediction_id": p["id"]}, {"_id": 0})
        farmer = await db.users.find_one({"id": p["user_id"]}, {"_id": 0, "password_hash": 0})
        enriched.append({**p, "field_observation": obs, "farmer": farmer})
    return enriched


@router.get("/expert/dashboard")
async def expert_dashboard(expert: dict = Depends(require_role("expert"))):
    db = get_db()
    pending = await db.predictions.count_documents({"verification_status": "pending"})
    confirmed = await db.predictions.count_documents({"verification_status": "confirmed"})
    hotspots = await db.hotspots.find({}, {"_id": 0}).sort("risk_score", -1).to_list(10)
    recent_reviews = await db.expert_reviews.find({}, {"_id": 0}).sort("reviewed_at", -1).to_list(10)
    return {
        "pending_verifications": pending,
        "confirmed_cases": confirmed,
        "hotspots": hotspots,
        "recent_reviews": recent_reviews,
        "note": "District-level data only; demo entries may be present.",
    }
