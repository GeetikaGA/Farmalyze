from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.schemas import AlertReadPatch
from app.security import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
async def list_alerts(user: dict = Depends(get_current_user)):
    db = get_db()
    alerts = await db.alerts.find(
        {"$or": [{"user_id": user["id"]}, {"district": {"$exists": True}}]},
        {"_id": 0},
    ).sort("created_at", -1).to_list(50)
    return alerts


@router.patch("/{alert_id}/read")
async def mark_alert_read(alert_id: str, body: AlertReadPatch, user: dict = Depends(get_current_user)):
    db = get_db()
    result = await db.alerts.update_one(
        {"id": alert_id, "user_id": user["id"]},
        {"$set": {"read_status": body.read, "read_at": datetime.now(timezone.utc)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"ok": True}
