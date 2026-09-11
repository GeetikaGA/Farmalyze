"""Seed demo data for SIH demo — clearly simulated where noted."""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.security import hash_password


async def seed():
    db = get_db()
    await db.users.delete_many({})
    await db.crops.delete_many({})
    await db.predictions.delete_many({})
    await db.alerts.delete_many({})
    await db.hotspots.delete_many({})
    await db.expert_reviews.delete_many({})
    await db.field_observations.delete_many({})

    farmer1_id = str(uuid.uuid4())
    farmer2_id = str(uuid.uuid4())
    expert_id = str(uuid.uuid4())
    official_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    farmers = [
        {
            "id": farmer1_id,
            "name": "Ramesh Patil",
            "email": "farmer@demo.com",
            "phone": "9876543210",
            "password_hash": hash_password("farmer123"),
            "role": "farmer",
            "language": "en",
            "created_at": now,
        },
        {
            "id": farmer2_id,
            "name": "Sunita Devi",
            "email": "farmer2@demo.com",
            "phone": "9876543211",
            "password_hash": hash_password("farmer123"),
            "role": "farmer",
            "language": "hi",
            "created_at": now,
        },
        {
            "id": expert_id,
            "name": "Dr. Anil Sharma",
            "email": "expert@demo.com",
            "phone": "9876500000",
            "password_hash": hash_password("expert123"),
            "role": "expert",
            "language": "en",
            "created_at": now,
        },
        {
            "id": official_id,
            "name": "Smt. Kavita Deshmukh",
            "email": "official@demo.com",
            "phone": "9876000000",
            "password_hash": hash_password("official123"),
            "role": "official",
            "language": "en",
            "district": "Pune",
            "created_at": now,
        },
    ]
    await db.users.insert_many(farmers)

    crops = [
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer1_id,
            "crop": "Tomato",
            "variety": "Pusa Ruby",
            "growth_stage": "fruiting",
            "district": "Pune",
            "location": "Pune",
            "current_risk": {"score": 72, "level": "high"},
            "created_at": now - timedelta(days=30),
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer1_id,
            "crop": "Potato",
            "variety": "Kufri Jyoti",
            "growth_stage": "bulking",
            "district": "Nashik",
            "location": "Nashik",
            "current_risk": {"score": 45, "level": "moderate"},
            "created_at": now - timedelta(days=20),
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer2_id,
            "crop": "Corn",
            "variety": "Hybrid 900M",
            "growth_stage": "vegetative",
            "district": "Nagpur",
            "location": "Nagpur",
            "current_risk": {"score": 28, "level": "low"},
            "created_at": now - timedelta(days=15),
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer2_id,
            "crop": "Cotton",
            "variety": "Bt Cotton RCH-2",
            "growth_stage": "boll_development",
            "district": "Yavatmal",
            "location": "Yavatmal",
            "current_risk": {"score": 82, "level": "high"},
            "created_at": now - timedelta(days=25),
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer1_id,
            "crop": "Soybean",
            "variety": "JS-335",
            "growth_stage": "pod_development",
            "district": "Amravati",
            "location": "Amravati",
            "current_risk": {"score": 40, "level": "moderate"},
            "created_at": now - timedelta(days=18),
        },
    ]
    await db.crops.insert_many(crops)

    predictions = []
    for i, (disease, conf, level, district, crop, status) in enumerate(
        [
            ("Early blight", 0.88, "high", "Pune", "Tomato", "confirmed"),
            ("Late blight", 0.62, "medium", "Pune", "Tomato", "pending"),
            ("Common rust", 0.91, "high", "Nagpur", "Corn", "confirmed"),
            ("healthy", 0.85, "high", "Nashik", "Potato", "not_required"),
            ("Early blight", 0.42, "low", "Aurangabad", "Tomato", "recommended"),
        ]
    ):
        pid = str(uuid.uuid4())
        predictions.append(
            {
                "id": pid,
                "user_id": farmer1_id if i < 4 else farmer2_id,
                "crop_id": crops[0]["id"],
                "image_url": "/uploads/demo-placeholder.jpg",
                "crop": crop,
                "disease": disease,
                "confidence": conf,
                "confidence_level": level if level != "high" else ("high" if conf >= 0.75 else "medium"),
                "district": district,
                "growth_stage": "fruiting",
                "image_quality": {"acceptable": True, "score": 0.82},
                "explanation": {"available": False, "heatmap_url": None, "message": "Demo seed record"},
                "risk": {
                    "score": 75 if conf > 0.8 else 55 if conf > 0.5 else 30,
                    "level": "high" if conf > 0.8 else "moderate" if conf > 0.5 else "low",
                    "factors": [],
                    "explanation": "Demo risk from seed data",
                },
                "verification_status": status,
                "verification": {"recommended": status != "not_required", "status": status},
                "timestamp": now - timedelta(days=i * 2),
                "demo": True,
            }
        )
    await db.predictions.insert_many(predictions)

    alerts = [
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer1_id,
            "district": "Pune",
            "disease": "Early blight",
            "severity": "high",
            "message": "HIGH risk for Early blight in Pune. Monitor tomato fields closely. (Demo alert)",
            "created_at": now - timedelta(hours=6),
            "read_status": False,
            "demo": True,
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer1_id,
            "district": "Nashik",
            "disease": "Late blight",
            "severity": "moderate",
            "message": "MODERATE potato disease risk in Nashik district. (Demo alert)",
            "created_at": now - timedelta(days=1),
            "read_status": True,
            "demo": True,
        },
    ]
    await db.alerts.insert_many(alerts)

    # A couple of farmer-submitted pest reports (kind="pest") so pests surface on
    # the map and in the official view alongside disease detections.
    pest_reports = [
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer2_id,
            "kind": "pest",
            "image_url": None,
            "crop": "Cotton",
            "disease": "Bollworm",
            "pest_key": "Cotton_Bollworm",
            "confidence": 0.88,
            "confidence_level": "high",
            "district": "Yavatmal",
            "growth_stage": "",
            "symptoms": "Larvae found inside bolls, Shedding of squares and young bolls",
            "image_quality": {"acceptable": True, "score": 1.0},
            "explanation": {"available": False, "heatmap_url": None, "message": "Farmer-submitted pest report."},
            "risk": {"score": 82, "level": "high", "factors": [], "explanation": "Demo pest report"},
            "verification_status": "recommended",
            "verification": {"recommended": True, "status": "recommended"},
            "timestamp": now - timedelta(days=1),
            "demo": True,
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": farmer2_id,
            "kind": "pest",
            "image_url": None,
            "crop": "Corn",
            "disease": "Fall Armyworm",
            "pest_key": "Corn_Fall_Armyworm",
            "confidence": 0.79,
            "confidence_level": "high",
            "district": "Nagpur",
            "growth_stage": "",
            "symptoms": "Sawdust-like frass in the leaf whorl, Ragged/elongated holes on leaves",
            "image_quality": {"acceptable": True, "score": 1.0},
            "explanation": {"available": False, "heatmap_url": None, "message": "Farmer-submitted pest report."},
            "risk": {"score": 58, "level": "moderate", "factors": [], "explanation": "Demo pest report"},
            "verification_status": "recommended",
            "verification": {"recommended": True, "status": "recommended"},
            "timestamp": now - timedelta(days=2),
            "demo": True,
        },
    ]
    await db.predictions.insert_many(pest_reports)

    hotspots = [
        {
            "district": "Pune", "disease": "Early blight", "kind": "disease",
            "crops": ["Tomato"], "risk_score": 78, "risk_level": "high",
            "report_count": 47, "confirmed_count": 18, "trend": "increasing",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Nagpur", "disease": "Common rust", "kind": "disease",
            "crops": ["Corn"], "risk_score": 65, "risk_level": "moderate",
            "report_count": 23, "confirmed_count": 9, "trend": "stable",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Nagpur", "disease": "Fall Armyworm", "kind": "pest",
            "crops": ["Corn"], "risk_score": 58, "risk_level": "moderate",
            "report_count": 11, "confirmed_count": 2, "trend": "increasing",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Nashik", "disease": "Late blight", "kind": "disease",
            "crops": ["Potato"], "risk_score": 52, "risk_level": "moderate",
            "report_count": 15, "confirmed_count": 4, "trend": "increasing",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Yavatmal", "disease": "Bollworm", "kind": "pest",
            "crops": ["Cotton"], "risk_score": 82, "risk_level": "high",
            "report_count": 29, "confirmed_count": 7, "trend": "increasing",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Jalgaon", "disease": "Whitefly", "kind": "pest",
            "crops": ["Cotton"], "risk_score": 44, "risk_level": "moderate",
            "report_count": 12, "confirmed_count": 1, "trend": "stable",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Kolhapur", "disease": "Early blight", "kind": "disease",
            "crops": ["Tomato"], "risk_score": 33, "risk_level": "low",
            "report_count": 6, "confirmed_count": 1, "trend": "stable",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
        {
            "district": "Aurangabad", "disease": "Aphids", "kind": "pest",
            "crops": ["Tomato"], "risk_score": 48, "risk_level": "moderate",
            "report_count": 9, "confirmed_count": 0, "trend": "stable",
            "updated_at": now, "demo": True, "data_note": "Simulated/demo aggregated district data",
        },
    ]
    await db.hotspots.insert_many(hotspots)

    await db.expert_reviews.insert_one(
        {
            "id": str(uuid.uuid4()),
            "prediction_id": predictions[0]["id"],
            "expert_id": expert_id,
            "expert_name": "Dr. Anil Sharma",
            "original_prediction": "Early blight",
            "decision": "confirm",
            "final_diagnosis": "Early blight",
            "remarks": "Symptoms match early blight. Recommend copper fungicide per local protocol.",
            "reviewed_at": now - timedelta(days=1),
            "demo": True,
        }
    )

    print("Seed complete.")
    print("Demo accounts:")
    print("  Farmer: farmer@demo.com / farmer123")
    print("  Farmer 2: farmer2@demo.com / farmer123")
    print("  Expert: expert@demo.com / expert123")
    print("  Official: official@demo.com / official123")


if __name__ == "__main__":
    asyncio.run(seed())
