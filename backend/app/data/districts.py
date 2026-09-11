from __future__ import annotations

"""Maharashtra district reference data — centroids and administrative regions.

Centroids are approximate polygon centroids derived from the 2011 Census district
boundaries (same source as frontend/public/maharashtra-districts.geojson), used to
place markers/labels on the risk map. The `district` property in the GeoJSON keys
directly against the names below.
"""

# (latitude, longitude)
DISTRICT_CENTROIDS: dict[str, tuple[float, float]] = {
    "Ahmednagar": (19.1875, 74.7542),
    "Akola": (20.7144, 77.0465),
    "Amravati": (21.1455, 77.7143),
    "Aurangabad": (20.1291, 75.3634),
    "Beed": (18.986, 75.7263),
    "Bhandara": (21.0318, 79.8001),
    "Buldhana": (20.5225, 76.4258),
    "Chandrapur": (20.1209, 79.3466),
    "Dhule": (21.0734, 74.5629),
    "Gadchiroli": (19.9049, 80.2807),
    "Gondia": (21.088, 80.1283),
    "Hingoli": (19.6123, 77.0776),
    "Jalgaon": (20.824, 75.4425),
    "Jalna": (19.8776, 76.0137),
    "Kolhapur": (16.5041, 74.1099),
    "Latur": (18.3775, 76.7763),
    "Mumbai": (19.044, 72.8502),
    "Nagpur": (21.183, 79.0439),
    "Nanded": (19.188, 77.6857),
    "Nandurbar": (21.4433, 74.1241),
    "Nashik": (20.2443, 74.0749),
    "Osmanabad": (18.1798, 76.0223),
    "Palghar": (19.8018, 72.9797),
    "Parbhani": (19.3159, 76.6682),
    "Pune": (18.4972, 74.141),
    "Raigad": (18.4504, 73.288),
    "Ratnagiri": (17.2174, 73.4816),
    "Sangli": (17.1447, 74.7089),
    "Satara": (17.7029, 74.2466),
    "Sindhudurg": (16.1987, 73.7522),
    "Solapur": (17.814, 75.3626),
    "Thane": (19.3762, 73.3217),
    "Wardha": (20.7831, 78.5941),
    "Washim": (20.2528, 77.2038),
    "Yavatmal": (19.9969, 78.0588),
}

# Revenue divisions (administrative regions) — useful for official-level rollups.
DISTRICT_REGION: dict[str, str] = {
    "Mumbai": "Konkan", "Thane": "Konkan", "Palghar": "Konkan", "Raigad": "Konkan",
    "Ratnagiri": "Konkan", "Sindhudurg": "Konkan",
    "Pune": "Pune", "Satara": "Pune", "Sangli": "Pune", "Solapur": "Pune", "Kolhapur": "Pune",
    "Nashik": "Nashik", "Dhule": "Nashik", "Nandurbar": "Nashik", "Jalgaon": "Nashik",
    "Ahmednagar": "Nashik",
    "Aurangabad": "Aurangabad", "Jalna": "Aurangabad", "Beed": "Aurangabad",
    "Osmanabad": "Aurangabad", "Nanded": "Aurangabad", "Latur": "Aurangabad",
    "Parbhani": "Aurangabad", "Hingoli": "Aurangabad",
    "Amravati": "Amravati", "Akola": "Amravati", "Washim": "Amravati",
    "Buldhana": "Amravati", "Yavatmal": "Amravati",
    "Nagpur": "Nagpur", "Wardha": "Nagpur", "Bhandara": "Nagpur", "Gondia": "Nagpur",
    "Chandrapur": "Nagpur", "Gadchiroli": "Nagpur",
}

ALL_DISTRICTS: list[str] = sorted(DISTRICT_CENTROIDS.keys())


def get_centroid(district: str) -> tuple[float, float] | None:
    return DISTRICT_CENTROIDS.get(district)


def get_region(district: str) -> str:
    return DISTRICT_REGION.get(district, "Other")
