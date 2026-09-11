from __future__ import annotations

"""Curated advisory knowledge base — not AI-generated treatment advice."""

ADVISORY_KB: dict[str, dict] = {
    "Tomato_Early_blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "symptoms": "Brown concentric rings on lower leaves, yellowing, defoliation from bottom up.",
        "immediate_actions": [
            "Remove and destroy severely affected leaves.",
            "Improve air circulation by pruning lower foliage.",
            "Avoid overhead irrigation; water at the base in the morning.",
            "Apply recommended copper-based fungicide per local extension guidance.",
        ],
        "preventive_measures": [
            "Use disease-free seeds and resistant varieties where available.",
            "Rotate crops and maintain 2–3 year gap for solanaceous crops.",
            "Mulch soil to reduce splash dispersal of spores.",
        ],
        "monitoring": [
            "Inspect lower leaves every 3–4 days during humid weather.",
            "Track spread upward on the plant.",
            "Note new lesions after rain events.",
        ],
        "escalation_conditions": [
            "Lesions reach upper canopy or >30% leaf area affected.",
            "Rapid spread after fungicide application.",
            "Uncertain diagnosis or mixed symptoms.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Tomato_Late_blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "symptoms": "Water-soaked gray-green lesions on leaves; white mold under humid conditions; fruit rot.",
        "immediate_actions": [
            "Isolate affected plants if in greenhouse/nursery.",
            "Remove infected plant material and dispose away from field.",
            "Reduce leaf wetness duration; improve drainage.",
            "Consult local agri officer for region-specific fungicide protocol.",
        ],
        "preventive_measures": [
            "Plant resistant varieties where available.",
            "Avoid planting near potato fields during outbreak season.",
            "Monitor weather — cool, wet conditions favor spread.",
        ],
        "monitoring": [
            "Daily checks during cool, rainy periods.",
            "Watch stem and fruit for oily lesions.",
        ],
        "escalation_conditions": [
            "Lesions on stems or fruits.",
            "Weather forecast shows continued humidity/rain.",
            "Neighboring farms report confirmed late blight.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Tomato_healthy": {
        "crop": "Tomato",
        "disease": "Healthy",
        "symptoms": "No significant disease symptoms observed.",
        "immediate_actions": [
            "Continue routine monitoring.",
            "Maintain balanced nutrition and irrigation.",
        ],
        "preventive_measures": [
            "Scout weekly for early symptoms.",
            "Sanitize tools between plants.",
        ],
        "monitoring": [
            "Weekly leaf inspection.",
            "Track growth stage transitions.",
        ],
        "escalation_conditions": [
            "New spots, wilting, or pest damage appears.",
            "AI confidence is low or image quality is poor.",
        ],
        "source": "General crop management (curated prototype reference)",
    },
    "Potato_Early_blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "symptoms": "Dark brown spots with concentric rings on older leaves.",
        "immediate_actions": [
            "Remove heavily infected leaves.",
            "Ensure adequate potassium nutrition.",
            "Apply fungicide per local recommendation if spread is moderate.",
        ],
        "preventive_measures": [
            "Use certified seed tubers.",
            "Rotate with non-host crops.",
        ],
        "monitoring": [
            "Inspect crop after warm, humid periods.",
        ],
        "escalation_conditions": [
            "Defoliation exceeds 25%.",
            "Tuber infection suspected.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Potato_Late_blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "symptoms": "Dark lesions on leaves, white sporulation underside, tuber brown rot.",
        "immediate_actions": [
            "Destroy infected haulms per local protocol.",
            "Improve field drainage.",
            "Seek expert verification — high outbreak risk.",
        ],
        "preventive_measures": [
            "Plant resistant varieties.",
            "Avoid excessive nitrogen.",
        ],
        "monitoring": [
            "Daily during favorable weather for pathogen.",
        ],
        "escalation_conditions": [
            "Confirmed or suspected late blight in district.",
            "Rapid lesion expansion.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Potato_healthy": {
        "crop": "Potato",
        "disease": "Healthy",
        "symptoms": "No significant disease symptoms observed.",
        "immediate_actions": ["Continue monitoring and balanced irrigation."],
        "preventive_measures": ["Certified seed, crop rotation, field sanitation."],
        "monitoring": ["Weekly canopy inspection."],
        "escalation_conditions": ["New lesions or wilting."],
        "source": "General crop management (curated prototype reference)",
    },
    "Corn_Common_rust": {
        "crop": "Corn",
        "disease": "Common Rust",
        "symptoms": "Small reddish-brown pustules on both leaf surfaces.",
        "immediate_actions": [
            "Scout field to assess severity.",
            "Consider fungicide if economic threshold reached per local guidance.",
        ],
        "preventive_measures": [
            "Use resistant hybrids where available.",
            "Balanced fertilization.",
        ],
        "monitoring": [
            "Check upper leaves before tasseling.",
        ],
        "escalation_conditions": [
            "Pustules on flag leaf before grain fill.",
            "Severity increasing across field.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Corn_Northern_Leaf_Blight": {
        "crop": "Corn",
        "disease": "Northern Leaf Blight",
        "symptoms": "Long elliptical gray-green lesions on leaves.",
        "immediate_actions": [
            "Assess % leaf area affected.",
            "Improve residue management for next season.",
        ],
        "preventive_measures": [
            "Resistant hybrids, crop rotation.",
        ],
        "monitoring": [
            "Monitor during humid periods.",
        ],
        "escalation_conditions": [
            ">50% plants with lesions on ear leaf.",
        ],
        "source": "ICAR/IPM guidelines (curated prototype reference)",
    },
    "Corn_healthy": {
        "crop": "Corn",
        "disease": "Healthy",
        "symptoms": "No significant disease symptoms observed.",
        "immediate_actions": ["Routine scouting."],
        "preventive_measures": ["Resistant varieties, field hygiene."],
        "monitoring": ["Weekly inspection during vegetative growth."],
        "escalation_conditions": ["New leaf lesions appear."],
        "source": "General crop management (curated prototype reference)",
    },
    "Cotton_Bacterial_blight": {
        "crop": "Cotton",
        "disease": "Bacterial Blight",
        "symptoms": "Angular water-soaked spots on leaves, black-arm on stems, boll rot.",
        "immediate_actions": [
            "Remove and destroy infected plant debris.",
            "Avoid overhead irrigation and working in wet fields.",
            "Use acid-delinted, certified seed for the next sowing.",
            "Apply copper-based bactericide per local extension guidance if spread is active.",
        ],
        "preventive_measures": [
            "Grow resistant/tolerant varieties where available.",
            "Treat seed before sowing; follow crop rotation.",
            "Maintain field sanitation and balanced nutrition.",
        ],
        "monitoring": ["Inspect after rain/humid spells for angular spots.", "Watch stems for black-arm."],
        "escalation_conditions": ["Black-arm on main stem.", "Boll infection appearing."],
        "source": "ICAR-CICR / state IPM guidelines (curated prototype reference)",
    },
    "Cotton_Leaf_Curl_Virus": {
        "crop": "Cotton",
        "disease": "Leaf Curl Virus",
        "symptoms": "Upward/downward leaf curling, thickened veins, enations on undersides, stunting.",
        "immediate_actions": [
            "Rogue out and destroy infected plants early.",
            "Control the whitefly vector (yellow sticky traps, neem).",
            "Avoid ratoon/volunteer cotton acting as virus reservoirs.",
        ],
        "preventive_measures": [
            "Sow tolerant varieties; follow a common sowing window.",
            "Manage whitefly from the seedling stage.",
            "Remove alternate host weeds around fields.",
        ],
        "monitoring": ["Scout weekly for curling and whitefly counts."],
        "escalation_conditions": ["Rapid spread of curling across the field.", "High whitefly pressure."],
        "source": "ICAR-CICR / state IPM guidelines (curated prototype reference)",
    },
    "Soybean_Rust": {
        "crop": "Soybean",
        "disease": "Rust",
        "symptoms": "Small tan-to-reddish-brown pustules on lower leaf surface; premature defoliation.",
        "immediate_actions": [
            "Scout lower leaves during humid weather.",
            "Apply recommended fungicide at early onset per local guidance.",
            "Improve airflow; avoid dense canopy where possible.",
        ],
        "preventive_measures": [
            "Grow tolerant varieties; timely sowing.",
            "Avoid excessive nitrogen and overcrowding.",
        ],
        "monitoring": ["Check lower canopy from flowering onward."],
        "escalation_conditions": ["Pustules spreading to upper canopy before pod fill."],
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "Soybean_Yellow_Mosaic": {
        "crop": "Soybean",
        "disease": "Yellow Mosaic Virus",
        "symptoms": "Bright yellow mosaic/mottling on leaves, puckering, stunted pods.",
        "immediate_actions": [
            "Remove infected plants early.",
            "Control the whitefly vector (traps, neem).",
            "Use virus-free, certified seed.",
        ],
        "preventive_measures": [
            "Grow resistant varieties; follow common sowing window.",
            "Manage whitefly from early stages; remove host weeds.",
        ],
        "monitoring": ["Scout weekly for mosaic symptoms and whitefly."],
        "escalation_conditions": ["Rapid spread of mosaic in the field."],
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "Chilli_Anthracnose": {
        "crop": "Chilli",
        "disease": "Anthracnose (Fruit Rot)",
        "symptoms": "Sunken circular lesions with concentric rings on fruits; dieback of twigs.",
        "immediate_actions": [
            "Remove and destroy infected fruits and twigs.",
            "Avoid overhead irrigation; improve drainage.",
            "Apply recommended fungicide per local guidance if spread is active.",
        ],
        "preventive_measures": [
            "Use disease-free/treated seed and resistant varieties.",
            "Rotate crops; maintain field sanitation.",
        ],
        "monitoring": ["Inspect fruits during humid/rainy spells."],
        "escalation_conditions": ["Fruit rot spreading rapidly.", "Twig dieback appearing."],
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "Chilli_Leaf_Curl": {
        "crop": "Chilli",
        "disease": "Leaf Curl Complex",
        "symptoms": "Upward curling and crinkling of leaves, shortened internodes, flower drop (mites/thrips/virus).",
        "immediate_actions": [
            "Identify the driver (thrips, mites or virus) before treating.",
            "Use yellow/blue sticky traps; spray neem for early infestations.",
            "Rogue out virus-infected plants.",
        ],
        "preventive_measures": [
            "Grow tolerant varieties; manage thrips/mites from nursery stage.",
            "Avoid excess nitrogen; remove host weeds.",
        ],
        "monitoring": ["Scout weekly for curling, thrips and mite presence."],
        "escalation_conditions": ["Severe curling with heavy flower drop.", "Suspected virus spread."],
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
}

# ---------------------------------------------------------------------------
# Pest advisory knowledge base (rule-based pest reporting path).
#
# The trained classifier only knows a small set of PlantVillage *diseases*. Pests
# named in PS 26131 (e.g. bollworm) are handled through a farmer-submitted symptom
# checklist rather than image inference — this is an honest interim that surfaces
# pests alongside diseases without claiming a model can detect them. Each entry
# carries a `checklist` used to build the pest-report form.
# ---------------------------------------------------------------------------
PEST_KB: dict[str, dict] = {
    "Cotton_Bollworm": {
        "kind": "pest",
        "crop": "Cotton",
        "crops": ["Cotton"],
        "disease": "Bollworm",
        "pest": "Bollworm (Pink / American)",
        "symptoms": "Bored holes in squares, flowers and bolls; shed squares; larvae inside bolls; rosette flowers.",
        "checklist": [
            "Small round entry/exit holes on bolls",
            "Shedding of squares and young bolls",
            "Larvae (caterpillars) found inside bolls",
            "Rosette-shaped (twisted) flowers",
            "Excreta (frass) near feeding holes",
        ],
        "immediate_actions": [
            "Install pheromone traps (4–5 per acre) to confirm and monitor moth activity.",
            "Handpick and destroy damaged squares, bolls and visible larvae.",
            "Release Trichogramma egg parasitoids where available.",
            "Apply recommended insecticide only if economic threshold is crossed, per local extension guidance.",
        ],
        "preventive_measures": [
            "Sow Bt cotton with the mandated non-Bt refuge area.",
            "Avoid extended-duration and late-sown crops; follow a common sowing window.",
            "Destroy crop residue and stubble after harvest to break the pest cycle.",
        ],
        "monitoring": [
            "Check pheromone trap catches twice weekly.",
            "Scout 20 plants per acre for boll damage; note % damaged bolls.",
        ],
        "escalation_conditions": [
            "Boll damage exceeds the local economic threshold (commonly ~5–10%).",
            "Trap catches rising sharply over consecutive checks.",
        ],
        "safe_usage": "If spraying, wear gloves, mask and full-sleeve clothing; follow the label dose and pre-harvest interval; rotate insecticide groups to avoid resistance. Confirm the product and dose with your local KVK / agri officer.",
        "source": "ICAR-CICR / state IPM guidelines (curated prototype reference)",
    },
    "Corn_Fall_Armyworm": {
        "kind": "pest",
        "crop": "Corn",
        "crops": ["Corn"],
        "disease": "Fall Armyworm",
        "pest": "Fall Armyworm",
        "symptoms": "Ragged, elongated holes and windowing on leaves; moist sawdust-like frass in the whorl; larvae in the whorl.",
        "checklist": [
            "Ragged/elongated holes on leaves",
            "Papery 'windowpane' feeding on young leaves",
            "Sawdust-like frass in the leaf whorl",
            "Caterpillar with inverted-Y on head visible in whorl",
        ],
        "immediate_actions": [
            "Scout the whorl; handpick and crush egg masses and larvae.",
            "Apply sand + lime or neem-based formulation into the whorl for early instars.",
            "Set up pheromone/light traps to monitor moth build-up.",
            "Use recommended insecticide only at threshold, per local guidance.",
        ],
        "preventive_measures": [
            "Timely, uniform sowing across the area.",
            "Intercrop with pulses and conserve natural enemies.",
            "Deep summer ploughing to expose pupae.",
        ],
        "monitoring": [
            "Check 20 plants per acre for fresh whorl damage.",
            "Record % plants showing damage twice weekly.",
        ],
        "escalation_conditions": [
            "More than ~5% plants (seedling) or ~10% (whorl stage) damaged.",
            "Rapid rise in trap catches.",
        ],
        "safe_usage": "Direct any spray into the whorl in the evening; wear protective gear and observe the pre-harvest interval. Confirm product/dose with your local agri officer.",
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "Tomato_Fruit_Borer": {
        "kind": "pest",
        "crop": "Tomato",
        "crops": ["Tomato"],
        "disease": "Fruit Borer",
        "pest": "Fruit Borer (Helicoverpa)",
        "symptoms": "Circular bore holes on fruits; larvae feeding with body half inside fruit; internal fruit rot.",
        "checklist": [
            "Circular bore holes on green/ripe fruit",
            "Larva feeding with head inside the fruit",
            "Internal tunneling / rotting of fruit",
            "Flower and small-fruit drop",
        ],
        "immediate_actions": [
            "Handpick and destroy bored fruits and visible larvae.",
            "Install pheromone traps to monitor Helicoverpa moths.",
            "Encourage natural enemies; use NPV / neem-based options for early stages.",
            "Apply recommended insecticide only at threshold, per local guidance.",
        ],
        "preventive_measures": [
            "Grow marigold as a trap crop along tomato borders.",
            "Avoid continuous solanaceous cropping; rotate.",
            "Remove and destroy crop residue after harvest.",
        ],
        "monitoring": [
            "Check pheromone traps twice weekly.",
            "Scout for fresh bore holes on 20 plants per plot.",
        ],
        "escalation_conditions": [
            "Fruit damage crosses the local economic threshold.",
            "Trap catches climbing over consecutive checks.",
        ],
        "safe_usage": "If treatment is needed, wear gloves and mask, follow label dose and pre-harvest interval, and rotate chemistry. Confirm with your local KVK / agri officer.",
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "General_Aphids": {
        "kind": "pest",
        "crop": "General",
        "crops": ["Tomato", "Cotton", "Corn", "Potato", "Chilli", "Soybean"],
        "disease": "Aphids",
        "pest": "Aphids",
        "symptoms": "Clusters of soft-bodied insects on tender shoots/undersides; curled leaves; sticky honeydew with sooty mould; stunting.",
        "checklist": [
            "Clusters of tiny insects on shoot tips / leaf undersides",
            "Curling or crinkling of young leaves",
            "Sticky honeydew and black sooty mould",
            "Ants moving on the plant",
            "Stunted new growth",
        ],
        "immediate_actions": [
            "Dislodge colonies with a strong water spray on tender parts.",
            "Conserve/release ladybird beetles and lacewings.",
            "Spray neem oil (azadirachtin) for early infestation.",
            "Use recommended insecticide only if colonies persist and spread, per local guidance.",
        ],
        "preventive_measures": [
            "Use yellow sticky traps to detect and reduce winged aphids.",
            "Avoid excess nitrogen, which favours soft aphid-prone growth.",
            "Remove heavily infested weeds around the field.",
        ],
        "monitoring": [
            "Inspect shoot tips and leaf undersides twice weekly.",
            "Watch for honeydew/sooty mould as an indirect sign.",
        ],
        "escalation_conditions": [
            "Colonies spreading rapidly across plants.",
            "Signs of virus transmission (mosaic/leaf-curl) appearing.",
        ],
        "safe_usage": "Prefer neem/soft options first; if spraying insecticide, wear protective gear, follow the label dose and pre-harvest interval, and spray in cool hours. Confirm with your local agri officer.",
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
    "General_Whitefly": {
        "kind": "pest",
        "crop": "General",
        "crops": ["Cotton", "Tomato", "Chilli"],
        "disease": "Whitefly",
        "pest": "Whitefly",
        "symptoms": "Tiny white flies rising when plants are disturbed; yellowing and downward leaf curl; honeydew and sooty mould; virus (leaf-curl) transmission.",
        "checklist": [
            "Cloud of tiny white flies when the plant is shaken",
            "Yellowing and downward curling of leaves",
            "Sticky honeydew and sooty mould",
            "Leaf-curl / mosaic virus symptoms",
        ],
        "immediate_actions": [
            "Install yellow sticky traps to trap adults.",
            "Spray neem oil covering leaf undersides.",
            "Remove and destroy virus-infected plants early.",
            "Use recommended insecticide only at threshold, per local guidance.",
        ],
        "preventive_measures": [
            "Use virus-tolerant varieties where available.",
            "Avoid overlapping susceptible crops season to season.",
            "Keep field borders free of alternate host weeds.",
        ],
        "monitoring": [
            "Count adults on yellow sticky traps twice weekly.",
            "Check leaf undersides for nymphs.",
        ],
        "escalation_conditions": [
            "Rapid rise in trap counts.",
            "Leaf-curl virus spreading in the field.",
        ],
        "safe_usage": "Target leaf undersides; wear protective gear, follow label dose and pre-harvest interval, and rotate chemistry to slow resistance. Confirm with your local agri officer.",
        "source": "ICAR / state IPM guidelines (curated prototype reference)",
    },
}

# Catalog used to build the pest-report form (crop -> selectable pests + checklists).
PEST_CATALOG = [
    {
        "key": key,
        "pest": entry["pest"],
        "disease": entry["disease"],
        "crops": entry.get("crops", [entry["crop"]]),
        "checklist": entry.get("checklist", []),
        "symptoms": entry.get("symptoms", ""),
    }
    for key, entry in PEST_KB.items()
]


def list_pests_for_crop(crop: str) -> list[dict]:
    crop_l = crop.lower()
    return [p for p in PEST_CATALOG if any(c.lower() == crop_l for c in p["crops"])]


def get_pest_advisory(pest_key: str) -> dict | None:
    return PEST_KB.get(pest_key)


DEFAULT_ADVISORY = {
    "crop": "General",
    "disease": "Unknown / Uncertain",
    "symptoms": "Symptoms could not be matched to a curated advisory entry.",
    "immediate_actions": [
        "Capture a clearer image of affected plant parts.",
        "Request expert verification.",
        "Avoid chemical application until diagnosis is confirmed.",
    ],
    "preventive_measures": ["Maintain field sanitation and monitor daily."],
    "monitoring": ["Watch for spread to neighboring plants."],
    "escalation_conditions": ["Any rapid spread or uncertain diagnosis."],
    "source": "Platform default guidance (not AI-generated)",
}


def get_advisory(crop: str, disease: str) -> dict:
    disease_key = disease.replace(" ", "_")
    crop_key = crop.replace(" ", "_")
    combined = {**ADVISORY_KB, **PEST_KB}
    for key, entry in combined.items():
        if key.lower() == f"{crop_key}_{disease_key}".lower():
            return entry
    for key, entry in combined.items():
        if disease.lower() in entry["disease"].lower() and (
            crop.lower() in entry["crop"].lower() or crop.lower() in [c.lower() for c in entry.get("crops", [])]
        ):
            return entry
    return {**DEFAULT_ADVISORY, "crop": crop, "disease": disease}


def list_all_advisories() -> list[dict]:
    """Combined disease + pest advisories for the standalone Treatment Guide."""
    entries = []
    for key, entry in ADVISORY_KB.items():
        entries.append({"key": key, "kind": entry.get("kind", "disease"), **entry})
    for key, entry in PEST_KB.items():
        entries.append({"key": key, **entry})
    return entries


def build_recommendation(
    crop: str,
    disease: str,
    confidence_level: str,
    escalation_required: bool,
) -> dict:
    advisory = get_advisory(crop, disease)
    title = f"Management guidance for {advisory['disease']} on {advisory['crop']}"
    if confidence_level == "low":
        title = "Uncertain diagnosis — verify before treatment"
    elif confidence_level == "medium":
        title = f"Possible {advisory['disease']} — proceed with caution"

    escalation_message = None
    if escalation_required or confidence_level in ("low", "medium"):
        escalation_message = (
            "Expert verification is recommended before applying chemical treatments. "
            "This guidance is curated agricultural management information, not an AI-generated prescription."
        )

    return {
        "title": title,
        "immediate_actions": advisory["immediate_actions"],
        "monitoring": advisory["monitoring"],
        "preventive_measures": advisory["preventive_measures"],
        "escalation_required": escalation_required or confidence_level == "low",
        "escalation_message": escalation_message,
        "source": advisory.get("source"),
        "symptoms": advisory.get("symptoms"),
    }
