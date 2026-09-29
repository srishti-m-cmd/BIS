"""
BIS SAKSHAM - Updates Router
Lists regulatory updates and change notifications.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.seed_data import DEMO_LABEL, REGULATORY_UPDATES

router = APIRouter(prefix="/api/updates", tags=["Regulatory Updates"])


# ---------------------------------------------------------------------------
# GET /api/updates
# ---------------------------------------------------------------------------

@router.get("", summary="List regulatory updates")
async def list_updates(
    impact: Optional[str] = Query(None, description="Filter by impact level: HIGH, MEDIUM, LOW"),
    category: Optional[str] = Query(None, description="Filter by product category keyword"),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Returns a list of demo regulatory updates and change notifications.
    Optionally filter by impact level or product category.
    [DEMO DATA - These are NOT real regulatory notifications]
    """
    updates = REGULATORY_UPDATES.copy()

    if impact:
        updates = [u for u in updates if u.get("impact", "").upper() == impact.upper()]

    if category:
        cat_lower = category.lower()
        updates = [
            u for u in updates
            if any(cat_lower in c.lower() for c in u.get("categories_affected", []))
        ]

    updates = updates[:limit]

    return {
        "updates": updates,
        "total": len(updates),
        "filters_applied": {"impact": impact, "category": category},
        "note": "All updates are DEMO DATA and do NOT represent real regulatory notifications. [DEMO DATA]",
        "data_label": DEMO_LABEL,
    }
