"""
BIS SAKSHAM - Standards Router
Handles IS standard search.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter, Query
from app.seed_data import DEMO_LABEL, STANDARDS_CATALOG

router = APIRouter(prefix="/api/standards", tags=["Standards"])


def _compute_relevance(standard: dict, query: str) -> float:
    """Simple relevance score based on keyword overlap."""
    if not query:
        return 1.0
    query_terms = query.lower().split()
    target = (standard.get("number", "") + " " + standard.get("title", "")).lower()
    matches = sum(1 for term in query_terms if term in target)
    return round(matches / max(len(query_terms), 1), 2)


# ---------------------------------------------------------------------------
# GET /api/standards/search
# ---------------------------------------------------------------------------

@router.get("/search", summary="Search IS standards")
async def search_standards(
    q: str = Query("", description="Search query (standard number or title keywords)"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Search the demo IS standards catalog by number or title keywords.
    [DEMO DATA - Not a real BIS standards database]
    """
    q_stripped = q.strip()

    results = []
    for std in STANDARDS_CATALOG:
        score = _compute_relevance(std, q_stripped)
        if not q_stripped or score > 0:
            results.append({
                "id": std["id"],
                "number": std["number"],
                "title": std["title"] + " [DEMO DATA]",
                "year": std["year"],
                "status": std["status"],
                "relevance_score": score,
                "data_label": DEMO_LABEL,
            })

    # Sort by relevance (desc), then year (desc)
    results.sort(key=lambda r: (-r["relevance_score"], -r["year"]))
    results = results[:limit]

    return {
        "query": q_stripped,
        "results": results,
        "total": len(results),
        "note": "This is a demo catalog with limited standards. The real BIS catalog has thousands of IS standards. [DEMO DATA]",
        "data_label": DEMO_LABEL,
    }
