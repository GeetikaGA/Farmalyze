import csv
import io
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.database import get_db
from app.security import require_role
from app.services.hotspot_service import get_district_risk_map

router = APIRouter(tags=["official"])


@router.get("/official/dashboard")
async def official_dashboard(official: dict = Depends(require_role("official"))):
    """Read-only district/state-level surveillance view for government officials.

    Reuses the same aggregated hotspot data plumbing as the risk map, presented as
    coverage + trend statistics. District-level only — no individual farmer data.
    """
    settings = get_settings()
    db = get_db()
    since = datetime.now(timezone.utc) - timedelta(days=settings.hotspot_window_days)

    districts = await get_district_risk_map()

    total_scans = await db.predictions.count_documents({"timestamp": {"$gte": since}})
    pest_reports = await db.predictions.count_documents({"kind": "pest", "timestamp": {"$gte": since}})
    disease_scans = total_scans - pest_reports
    confirmed = await db.predictions.count_documents(
        {"verification_status": "confirmed", "timestamp": {"$gte": since}}
    )
    registered_farmers = await db.users.count_documents({"role": "farmer"})
    active_districts = len(districts)
    high_risk_zones = sum(1 for d in districts if d["risk_level"] == "high")

    # Threat leaderboard across the state (disease + pest).
    threat_totals: dict[tuple[str, str], dict] = {}
    for d in districts:
        for th in d["threats"]:
            key = (th["name"], th["kind"])
            agg = threat_totals.setdefault(
                key, {"name": th["name"], "kind": th["kind"], "districts": 0, "reports": 0, "max_risk": 0}
            )
            agg["districts"] += 1
            agg["reports"] += th.get("report_count", 0)
            agg["max_risk"] = max(agg["max_risk"], th["risk_score"])
    top_threats = sorted(threat_totals.values(), key=lambda t: (t["max_risk"], t["reports"]), reverse=True)[:6]

    # Region rollup.
    region_rollup: dict[str, dict] = {}
    for d in districts:
        r = region_rollup.setdefault(d["region"], {"region": d["region"], "districts": 0, "high": 0, "reports": 0})
        r["districts"] += 1
        r["reports"] += d["total_reports"]
        if d["risk_level"] == "high":
            r["high"] += 1
    regions = sorted(region_rollup.values(), key=lambda r: r["high"], reverse=True)

    return {
        "summary": {
            "total_scans": total_scans,
            "disease_scans": disease_scans,
            "pest_reports": pest_reports,
            "confirmed_cases": confirmed,
            "registered_farmers": registered_farmers,
            "active_districts": active_districts,
            "high_risk_zones": high_risk_zones,
            "window_days": settings.hotspot_window_days,
        },
        "districts": districts,
        "top_threats": top_threats,
        "regions": regions,
        "note": (
            "District-level aggregated surveillance data only; no individual farmer "
            "records are exposed. Demo/simulated entries may be included."
        ),
    }


@router.get("/official/export")
async def official_export(official: dict = Depends(require_role("official"))):
    """Export the district risk table as CSV for offline reporting."""
    districts = await get_district_risk_map()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        ["District", "Region", "Risk Score", "Risk Level", "Dominant Threat", "Type", "Crops Affected", "Total Reports", "Recommended Action"]
    )
    for d in districts:
        writer.writerow(
            [
                d["district"],
                d.get("region", ""),
                d["risk_score"],
                d["risk_level"],
                d.get("dominant_threat", ""),
                d.get("dominant_kind", ""),
                "; ".join(d.get("crops_affected", [])),
                d.get("total_reports", 0),
                d.get("recommended_action", ""),
            ]
        )
    buf.seek(0)
    filename = f"farmalyze_district_surveillance_{datetime.now(timezone.utc).date()}.csv"
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
