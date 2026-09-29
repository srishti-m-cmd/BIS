"""
BIS SAKSHAM - Services Router
Lists BIS certification and registration services.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter
from app.seed_data import DEMO_LABEL, BIS_SERVICES

router = APIRouter(prefix="/api/services", tags=["BIS Services"])


# ---------------------------------------------------------------------------
# GET /api/services
# ---------------------------------------------------------------------------

@router.get("", summary="List BIS services")
async def list_services():
    """
    Returns the list of BIS certification and registration services available.
    [DEMO DATA]
    """
    return {
        "services": BIS_SERVICES,
        "total": len(BIS_SERVICES),
        "note": "This is a demo list. Visit https://www.bis.gov.in/ for the complete and current list of BIS services. [DEMO DATA]",
        "data_label": DEMO_LABEL,
    }
