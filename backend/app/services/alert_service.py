from __future__ import annotations

"""District-wide alert broadcast.

Instead of alerting only the farmer who ran a scan, a moderate/high detection is
pushed to every farmer who has a crop registered in the affected district. A short
dedupe window prevents spamming the same farmers for the same threat repeatedly.
"""

import uuid
from datetime import datetime, timedelta, timezone


async def broadcast_district_alert(
    db,
    *,
    district: str,
    disease: str,
    severity: str,
    kind: str = "disease",
    crop: str | None = None,
    dedupe_hours: int = 12,
) -> int:
    """Insert an alert for every farmer with a crop in `district`. Returns count sent."""
    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=dedupe_hours)

    owner_ids = await db.crops.distinct("user_id", {"district": district})
    if not owner_ids:
        return 0

    crop_txt = f" on {crop}" if crop else ""
    noun = "pest alert" if kind == "pest" else "disease alert"
    message = (
        f"{severity.upper()} {noun}: {disease}{crop_txt} reported in {district}. "
        "Scout your field and review the advisory."
    )

    alerts = []
    for uid in set(owner_ids):
        recent = await db.alerts.find_one(
            {"user_id": uid, "district": district, "disease": disease, "created_at": {"$gte": since}}
        )
        if recent:
            continue
        alerts.append(
            {
                "id": str(uuid.uuid4()),
                "user_id": uid,
                "district": district,
                "disease": disease,
                "kind": kind,
                "severity": severity,
                "message": message,
                "created_at": now,
                "read_status": False,
                "broadcast": True,
            }
        )
    if alerts:
        await db.alerts.insert_many(alerts)
    return len(alerts)
