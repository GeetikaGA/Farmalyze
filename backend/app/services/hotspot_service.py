from __future__ import annotations

"""Hotspot aggregation at district level with confidence filtering.

Aggregates both AI disease predictions and farmer-submitted pest reports (stored in
the same `predictions` collection with a `kind` field: "disease" | "pest"). The
per-district rollup powers the choropleth risk map and the official surveillance view.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from app.config import get_settings
from app.data.advisory_kb import get_advisory
from app.data.districts import get_centroid, get_region
from app.database import get_db
from app.services.forecast_service import compute_forecast
from app.services.weather_service import weather_service


async def get_local_counts(district: str, disease: str, window_days: int | None = None) -> tuple[int, int]:
    settings = get_settings()
    window = window_days or settings.hotspot_window_days
    since = datetime.now(timezone.utc) - timedelta(days=window)
    db = get_db()

    query = {
        "district": district,
        "disease": disease,
        "timestamp": {"$gte": since},
        "image_quality.acceptable": True,
        "confidence": {"$gte": settings.hotspot_min_confidence},
    }
    report_count = await db.predictions.count_documents(query)
    confirmed_count = await db.predictions.count_documents({**query, "verification_status": "confirmed"})
    return report_count, confirmed_count


def _level_from_score(score: int) -> str:
    settings = get_settings()
    if score <= settings.risk_low_max:
        return "low"
    if score <= settings.risk_moderate_max:
        return "moderate"
    return "high"


async def refresh_hotspots() -> None:
    settings = get_settings()
    db = get_db()
    since = datetime.now(timezone.utc) - timedelta(days=settings.hotspot_window_days)

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": since},
                "image_quality.acceptable": True,
                "confidence": {"$gte": settings.hotspot_min_confidence},
                "disease": {"$not": {"$regex": "healthy", "$options": "i"}},
            }
        },
        {
            "$group": {
                "_id": {
                    "district": "$district",
                    "disease": "$disease",
                    "kind": {"$ifNull": ["$kind", "disease"]},
                },
                "report_count": {"$sum": 1},
                "confirmed_count": {
                    "$sum": {"$cond": [{"$eq": ["$verification_status", "confirmed"]}, 1, 0]}
                },
                "avg_confidence": {"$avg": "$confidence"},
                "avg_risk": {"$avg": "$risk.score"},
                "crops": {"$addToSet": "$crop"},
            }
        },
    ]

    results = await db.predictions.aggregate(pipeline).to_list(length=500)
    for row in results:
        district = row["_id"]["district"]
        disease = row["_id"]["disease"]
        kind = row["_id"].get("kind", "disease")
        report_count = row["report_count"]
        if report_count < settings.hotspot_min_reports:
            continue

        confirmed = row["confirmed_count"]
        avg_risk = row.get("avg_risk") or 40
        risk_score = int(min(100, avg_risk + confirmed * 3))
        risk_level = _level_from_score(risk_score)

        trend = "stable"
        if report_count >= settings.hotspot_min_reports * 2:
            trend = "increasing"

        await db.hotspots.update_one(
            {"district": district, "disease": disease, "kind": kind},
            {
                "$set": {
                    "district": district,
                    "disease": disease,
                    "kind": kind,
                    "crops": [c for c in (row.get("crops") or []) if c],
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "report_count": report_count,
                    "confirmed_count": confirmed,
                    "trend": trend,
                    "updated_at": datetime.now(timezone.utc),
                    "data_note": "Aggregated from platform reports; demo data may be included.",
                }
            },
            upsert=True,
        )


def _recommended_action(level: str, kind: str) -> str:
    if level == "high":
        base = "Escalate: alert farmers in the district and prioritise expert/field verification."
    elif level == "moderate":
        base = "Monitor closely and issue an advisory to farmers in the district."
    else:
        base = "Routine surveillance; no immediate action required."
    if kind == "pest":
        base += " Deploy pheromone/sticky traps and confirm on the ground before any spray."
    return base


def _enrich(h: dict[str, Any]) -> dict[str, Any]:
    """Attach map coordinates + region to a hotspot record."""
    coord = get_centroid(h.get("district", ""))
    out = dict(h)
    if coord:
        out["lat"], out["lng"] = coord[0], coord[1]
    out["region"] = get_region(h.get("district", ""))
    out.setdefault("kind", "disease")
    return out


async def get_risk_map() -> list[dict[str, Any]]:
    """Flat list of hotspots (per district+threat), enriched with coordinates."""
    db = get_db()
    hotspots = await db.hotspots.find({}, {"_id": 0}).sort("risk_score", -1).to_list(200)
    return [_enrich(h) for h in hotspots]


async def get_district_risk_map() -> list[dict[str, Any]]:
    """One aggregated entry per district for the choropleth map.

    Each district takes its highest-risk active threat as the headline, but also
    lists every disease/pest and affected crop detected there, plus a recommended
    action and map coordinates for click-to-inspect popups.
    """
    hotspots = await get_risk_map()
    by_district: dict[str, dict[str, Any]] = {}
    for h in hotspots:
        d = h["district"]
        entry = by_district.setdefault(
            d,
            {
                "district": d,
                "region": h.get("region", get_region(d)),
                "lat": h.get("lat"),
                "lng": h.get("lng"),
                "risk_score": 0,
                "risk_level": "low",
                "threats": [],
                "crops_affected": set(),
                "total_reports": 0,
                "demo": False,
            },
        )
        entry["threats"].append(
            {
                "name": h["disease"],
                "kind": h.get("kind", "disease"),
                "risk_score": h["risk_score"],
                "risk_level": h["risk_level"],
                "report_count": h.get("report_count", 0),
                "trend": h.get("trend", "stable"),
            }
        )
        for c in h.get("crops", []) or []:
            entry["crops_affected"].add(c)
        entry["total_reports"] += h.get("report_count", 0)
        if h.get("demo"):
            entry["demo"] = True
        if h["risk_score"] >= entry["risk_score"]:
            entry["risk_score"] = h["risk_score"]
            entry["risk_level"] = h["risk_level"]
            entry["dominant_threat"] = h["disease"]
            entry["dominant_kind"] = h.get("kind", "disease")

    out = []
    for entry in by_district.values():
        entry["crops_affected"] = sorted(entry.pop("crops_affected"))
        entry["threats"].sort(key=lambda t: t["risk_score"], reverse=True)
        entry["recommended_action"] = _recommended_action(
            entry["risk_level"], entry.get("dominant_kind", "disease")
        )
        top = entry["threats"][0] if entry["threats"] else {"report_count": 0, "trend": "stable"}
        weather = await weather_service.get_weather(entry["district"])
        forecast = compute_forecast(
            weather=weather,
            report_count=top.get("report_count", 0),
            trend=top.get("trend", "stable"),
            confirmed_count=0,
            base_risk=entry["risk_score"],
        )
        entry["outbreak_forecast"] = forecast["probability"]
        entry["forecast_level"] = forecast["level"]
        out.append(entry)
    out.sort(key=lambda e: e["risk_score"], reverse=True)
    return out
