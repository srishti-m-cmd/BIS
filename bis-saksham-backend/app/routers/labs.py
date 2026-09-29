"""
BIS SAKSHAM - Labs Router
Handles lab matching and optimisation for required product tests.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.models import LabMatchResponse, LabMatchResult, Laboratory
from app.seed_data import DEMO_LABEL, PRODUCTS_DB

router = APIRouter(prefix="/api/labs", tags=["Laboratory Matching"])


class LabMatchRequest(BaseModel):
    product_id: Optional[str] = None
    test_ids: Optional[List[str]] = None


# ---------------------------------------------------------------------------
# POST /api/labs/match
# ---------------------------------------------------------------------------

@router.post("/match", response_model=LabMatchResponse, summary="Match tests to labs")
async def match_labs(request: LabMatchRequest):
    """
    For a given product or list of test IDs, returns an optimised lab matching plan:
    - Groups tests by lab to minimise number of labs and travel costs
    - Returns recommendation scores and rationale

    [DEMO DATA - not real NABL database]
    """
    # Resolve tests from product or explicit test list
    if request.product_id:
        product = PRODUCTS_DB.get(request.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product '{request.product_id}' not found. [DEMO]")
        test_ids = [t.id for t in product.tests]
        labs_pool: List[Laboratory] = product.laboratories
    elif request.test_ids:
        test_ids = request.test_ids
        # Collect all labs from all demo products that cover any of these tests
        seen_lab_ids: set[str] = set()
        labs_pool = []
        for p in PRODUCTS_DB.values():
            for lab in p.laboratories:
                if lab.id not in seen_lab_ids:
                    if any(tid in lab.tests_covered for tid in test_ids):
                        labs_pool.append(lab)
                        seen_lab_ids.add(lab.id)
    else:
        raise HTTPException(status_code=400, detail="Provide either 'product_id' or 'test_ids'.")

    if not test_ids:
        raise HTTPException(status_code=400, detail="No tests found to match.")

    # Greedy optimisation: prefer labs that cover the most tests in the set
    remaining_tests = set(test_ids)
    matched_results: List[LabMatchResult] = []
    used_labs: set[str] = set()

    # Sort labs by coverage of remaining tests (descending) for greedy selection
    def _coverage(lab: Laboratory, remaining: set) -> int:
        return len(set(lab.tests_covered) & remaining)

    iteration = 0
    while remaining_tests and iteration < 20:
        iteration += 1
        best_lab = max(labs_pool, key=lambda l: _coverage(l, remaining_tests), default=None)
        if not best_lab or _coverage(best_lab, remaining_tests) == 0:
            break

        matched_tests_for_lab = list(set(best_lab.tests_covered) & remaining_tests)
        remaining_tests -= set(matched_tests_for_lab)
        used_labs.add(best_lab.id)

        # Proportional cost estimate
        fraction = len(matched_tests_for_lab) / max(len(best_lab.tests_covered), 1)
        cost_estimate = int((best_lab.estimated_cost_inr or 0) * fraction)

        matched_results.append(
            LabMatchResult(
                lab=best_lab,
                matched_tests=matched_tests_for_lab,
                total_estimated_cost_inr=cost_estimate,
                total_estimated_days=best_lab.estimated_turnaround_days or 0,
                recommendation_score=round(0.5 + 0.5 * fraction, 2),
                recommendation_reason=(
                    f"Lab covers {len(matched_tests_for_lab)} of your required test(s). "
                    f"NABL accredited until {best_lab.accreditation_valid_until}. [DEMO]"
                ),
            )
        )

    # If any tests remain unmatched, note them in the response summary
    unmatched_note = ""
    if remaining_tests:
        unmatched_note = (
            f" Note: {len(remaining_tests)} test(s) could not be matched to demo labs: "
            f"{list(remaining_tests)}. In practice, search the NABL portal for accredited labs."
        )

    total_cost = sum(r.total_estimated_cost_inr for r in matched_results)
    total_days = max((r.total_estimated_days for r in matched_results), default=0)

    return LabMatchResponse(
        product_id=request.product_id,
        test_ids=test_ids,
        optimized_lab_plan=matched_results,
        total_labs_needed=len(matched_results),
        estimated_total_cost_inr=total_cost,
        estimated_total_days=total_days,
        data_label=DEMO_LABEL + unmatched_note,
    )
