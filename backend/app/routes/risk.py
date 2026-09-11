from fastapi import APIRouter, Depends

from app.database import get_db
from app.security import get_current_user
from app.services.hotspot_service import get_district_risk_map, get_risk_map

router = APIRouter(tags=["risk"])


@router.get("/risk-map")
async def risk_map(user: dict = Depends(get_current_user)):
    hotspots = await get_risk_map()
    districts = await get_district_risk_map()
    return {
        "hotspots": hotspots,
        "districts": districts,
        "note": "District-level aggregated data. Precise farmer locations are not exposed. Demo/simulated entries may be included.",
    }


@router.get("/risk/{prediction_id}")
async def risk_for_prediction(prediction_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    pred = await db.predictions.find_one({"id": prediction_id, "user_id": user["id"]}, {"_id": 0, "risk": 1})
    if not pred:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred.get("risk", {})
