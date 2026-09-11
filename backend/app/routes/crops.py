import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.schemas import CropCreate, CropUpdate
from app.security import get_current_user

router = APIRouter(prefix="/crops", tags=["crops"])


@router.get("")
async def list_crops(user: dict = Depends(get_current_user)):
    db = get_db()
    crops = await db.crops.find({"user_id": user["id"]}, {"_id": 0}).to_list(length=100)
    return crops


@router.post("")
async def create_crop(body: CropCreate, user: dict = Depends(get_current_user)):
    db = get_db()
    crop = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "crop": body.crop,
        "variety": body.variety,
        "growth_stage": body.growth_stage,
        "district": body.district,
        "location": body.location or body.district,
        "current_risk": {"score": 0, "level": "low"},
        "created_at": datetime.now(timezone.utc),
    }
    await db.crops.insert_one(crop)
    return {k: v for k, v in crop.items() if k != "_id"}


@router.get("/{crop_id}")
async def get_crop(crop_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    crop = await db.crops.find_one({"id": crop_id, "user_id": user["id"]}, {"_id": 0})
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.put("/{crop_id}")
async def update_crop(crop_id: str, body: CropUpdate, user: dict = Depends(get_current_user)):
    db = get_db()
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await db.crops.update_one({"id": crop_id, "user_id": user["id"]}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Crop not found")
    return await db.crops.find_one({"id": crop_id}, {"_id": 0})


@router.delete("/{crop_id}")
async def delete_crop(crop_id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    result = await db.crops.delete_one({"id": crop_id, "user_id": user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Crop not found")
    return {"ok": True}
