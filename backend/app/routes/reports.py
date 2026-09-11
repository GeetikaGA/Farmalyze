from fastapi import APIRouter, Depends

from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
async def get_reports(user: dict = Depends(get_current_user)):
    db = get_db()
    preds = await db.predictions.find({"user_id": user["id"]}, {"_id": 0}).sort("timestamp", -1).to_list(100)
    return {
        "total_scans": len(preds),
        "scans": preds,
        "disclaimer": "Scan history from this platform. Not validated field epidemiology data.",
    }
