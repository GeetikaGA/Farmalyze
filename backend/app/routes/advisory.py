from fastapi import APIRouter

from app.data.advisory_kb import get_advisory, list_all_advisories

router = APIRouter(tags=["advisory"])


@router.get("/treatments")
async def list_treatments():
    """Browsable list of all curated advisory entries (diseases + pests),
    independent of any scan. Powers the standalone Treatment Guide page.
    """
    return list_all_advisories()


@router.get("/treatment/{disease}")
async def get_treatment(disease: str, crop: str = "Tomato"):
    advisory = get_advisory(crop, disease)
    return {
        **advisory,
        "disclaimer": (
            "This is curated agricultural management guidance, not AI-generated treatment advice. "
            "Consult local extension officers before applying chemicals."
        ),
    }
