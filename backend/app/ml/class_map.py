"""Crop + class metadata.

IMPORTANT — honest capability model:
The trained classifier only knows PlantVillage disease classes for Tomato, Potato
and Corn (`CLASS_MAP`). Cotton, Soybean and Chilli are Maharashtra-critical crops
that the model has NOT been trained on. Rather than silently running the model and
returning a wrong Tomato/Potato/Corn class for them, we expose a per-crop
capability flag so the UI and API can be honest:

    "ai_disease"    -> image-based disease detection available (model-backed)
    "advisory_pest" -> no image model yet; pest reporting + curated advisories +
                       weather/stage risk are available; image detection "coming soon"
"""

CLASS_MAP = [
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Bacterial_spot",
    "Tomato_healthy",
    "Potato_Early_blight",
    "Potato_Late_blight",
    "Potato_healthy",
    "Corn_Common_rust",
    "Corn_Northern_Leaf_Blight",
    "Corn_healthy",
]

CROP_ALIASES = {
    "tomato": "Tomato",
    "potato": "Potato",
    "corn": "Corn",
    "maize": "Corn",
}

# Crops the image classifier is actually trained on.
MODEL_CROPS = ["Tomato", "Potato", "Corn"]

# Full crop list offered in the app (Maharashtra-relevant). Cotton/Soybean/Chilli
# are usable for pest reports, advisories and risk — but not image disease AI yet.
SUPPORTED_CROPS = ["Tomato", "Potato", "Corn", "Cotton", "Soybean", "Chilli"]

CROP_CAPABILITY = {
    "Tomato": "ai_disease",
    "Potato": "ai_disease",
    "Corn": "ai_disease",
    "Cotton": "advisory_pest",
    "Soybean": "advisory_pest",
    "Chilli": "advisory_pest",
}


def crop_capability(crop: str) -> str:
    return CROP_CAPABILITY.get(CROP_ALIASES.get(crop.lower(), crop), "advisory_pest")


def is_model_crop(crop: str) -> bool:
    return crop_capability(crop) == "ai_disease"


GROWTH_STAGES = {
    "Tomato": ["seedling", "vegetative", "flowering", "fruiting", "harvest"],
    "Potato": ["seedling", "vegetative", "tuber_initiation", "bulking", "harvest"],
    "Corn": ["seedling", "vegetative", "tasseling", "grain_fill", "maturity"],
    "Cotton": ["seedling", "squaring", "flowering", "boll_development", "boll_opening"],
    "Soybean": ["seedling", "vegetative", "flowering", "pod_development", "maturity"],
    "Chilli": ["seedling", "vegetative", "flowering", "fruiting", "harvest"],
}

DEMO_DISTRICTS = ["Pune", "Nashik", "Nagpur", "Aurangabad", "Kolhapur"]
