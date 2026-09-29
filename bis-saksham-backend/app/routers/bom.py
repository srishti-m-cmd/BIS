"""
BIS SAKSHAM - BOM Router
Handles Bill of Materials upload and compliance analysis.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

import io
import csv
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional

from app.models import BOMAnalyzeResponse, BOMComponent, BOMStatus
from app.seed_data import DEMO_LABEL, PRODUCTS_DB

router = APIRouter(prefix="/api/bom", tags=["BOM Analysis"])

# ---------------------------------------------------------------------------
# BOM column name aliases (case-insensitive)
# ---------------------------------------------------------------------------

COMPONENT_NAME_COLS = {"component", "name", "part name", "item", "description", "component name"}
MATERIAL_COLS = {"material", "material type", "substance", "material name"}
SUPPLIER_COLS = {"supplier", "vendor", "manufacturer", "make", "brand"}
QTY_COLS = {"qty", "quantity", "amount", "count", "pieces"}
UNIT_COLS = {"unit", "uom", "units"}
PART_NUM_COLS = {"part number", "part no", "part#", "sku", "model", "reference"}


def _normalise_header(header: str) -> str:
    return header.strip().lower()


def _find_col(headers: list[str], aliases: set[str]) -> Optional[int]:
    for i, h in enumerate(headers):
        if _normalise_header(h) in aliases:
            return i
    return None


def _assess_component_compliance(name: str, material: Optional[str]) -> tuple[BOMStatus, Optional[str], Optional[str]]:
    """
    Heuristic compliance assessment for a BOM component.
    Returns (BOMStatus, applicable_standard, action_required).
    [DEMO LOGIC - not authoritative]
    """
    name_lower = (name or "").lower()
    mat_lower = (material or "").lower()

    # Known high-risk keywords
    if any(kw in name_lower for kw in ["cable", "wire", "cord", "wiring"]):
        return (
            BOMStatus.POTENTIALLY_APPLICABLE,
            "IS 694 / IS 1554 [DEMO] - Wires and Cables",
            "Verify cable is sourced from a BIS ISI-licensed manufacturer.",
        )

    if any(kw in name_lower for kw in ["heating element", "heater element"]):
        return (
            BOMStatus.POTENTIALLY_APPLICABLE,
            "IS 1258:2018 Clause 9 [DEMO]",
            "Obtain heating element compliance declaration from supplier.",
        )

    if any(kw in name_lower for kw in ["pressure relief", "prv", "safety valve"]):
        return (
            BOMStatus.NEEDS_VERIFICATION,
            "Possibly IS 3624 [DEMO]",
            "Consult BIS to confirm IS 3624 applicability for this sub-component.",
        )

    if any(kw in name_lower for kw in ["circuit breaker", "mcb", "rccb", "switch"]):
        return (
            BOMStatus.POTENTIALLY_APPLICABLE,
            "IS 8828 / IS 12640 [DEMO]",
            "Verify MCB/switch is from BIS ISI-licensed supplier.",
        )

    if any(kw in name_lower for kw in ["led", "lamp", "bulb", "luminaire"]):
        return (
            BOMStatus.POTENTIALLY_APPLICABLE,
            "IS 15885 [DEMO] - LED luminaires",
            "Check if LED component is BIS CRS registered.",
        )

    if any(kw in name_lower for kw in ["motor", "compressor", "pump"]):
        return (
            BOMStatus.NEEDS_VERIFICATION,
            "IS 325 / IS 1231 [DEMO] - Electric Motors",
            "Verify motor compliance and check if it triggers additional QCO requirements.",
        )

    if any(kw in mat_lower for kw in ["lead", "cadmium", "mercury", "chromium vi"]):
        return (
            BOMStatus.HAS_REQUIREMENT,
            "RoHS / IS 9873-3 [DEMO]",
            "CRITICAL: Restricted substance detected. Replace or obtain exemption documentation.",
        )

    if any(kw in mat_lower for kw in ["pvc", "polyvinyl chloride"]):
        return (
            BOMStatus.POTENTIALLY_APPLICABLE,
            "IS 4985 / IS 694 [DEMO]",
            "Check if PVC material complies with relevant IS standard for intended application.",
        )

    # Default - no specific requirement identified
    return (BOMStatus.NO_REQUIREMENT_IDENTIFIED, None, None)


async def _parse_csv(content: bytes) -> list[dict]:
    """Parse CSV bytes into a list of row dicts."""
    decoded = content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(decoded))
    return [row for row in reader]


async def _parse_xlsx(content: bytes) -> list[dict]:
    """Parse XLSX bytes into a list of row dicts using openpyxl."""
    try:
        import openpyxl
    except ImportError:
        raise HTTPException(status_code=500, detail="openpyxl not installed. Cannot parse XLSX files.")

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []

    headers = [str(h) if h is not None else "" for h in rows[0]]
    result = []
    for row in rows[1:]:
        row_dict = {headers[i]: (str(row[i]) if row[i] is not None else "") for i in range(len(headers))}
        result.append(row_dict)
    return result


# ---------------------------------------------------------------------------
# POST /api/bom/analyze
# ---------------------------------------------------------------------------

@router.post("/analyze", response_model=BOMAnalyzeResponse, summary="Upload and analyze BOM")
async def analyze_bom(
    file: UploadFile = File(...),
    product_id: Optional[str] = Form(None),
):
    """
    Upload a CSV or XLSX Bill of Materials file and receive a compliance
    assessment for each component.

    - For demo product DEMO-PROD-001, the pre-defined BOM is returned.
    - For custom files, each row is assessed heuristically.

    [DEMO DATA - Heuristic assessment, not authoritative BIS guidance]
    """
    # If the product has a pre-defined BOM, use it
    if product_id and product_id in PRODUCTS_DB:
        product = PRODUCTS_DB[product_id]
        if product.bom_components:
            components = product.bom_components
            return BOMAnalyzeResponse(
                total_components=len(components),
                components=components,
                potentially_applicable_count=sum(1 for c in components if c.compliance_status == BOMStatus.POTENTIALLY_APPLICABLE),
                needs_verification_count=sum(1 for c in components if c.compliance_status == BOMStatus.NEEDS_VERIFICATION),
                has_requirement_count=sum(1 for c in components if c.compliance_status == BOMStatus.HAS_REQUIREMENT),
                summary=f"Pre-defined demo BOM for product {product_id}. [DEMO DATA]",
                data_label=DEMO_LABEL,
            )

    # Parse uploaded file
    filename = file.filename or ""
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if filename.lower().endswith(".csv"):
        rows = await _parse_csv(content)
    elif filename.lower().endswith((".xlsx", ".xls")):
        rows = await _parse_xlsx(content)
    else:
        # Attempt CSV as fallback
        try:
            rows = await _parse_csv(content)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a CSV or XLSX file.",
            )

    if not rows:
        raise HTTPException(status_code=400, detail="No data rows found in the uploaded file.")

    # Identify columns
    sample_headers = list(rows[0].keys())
    name_idx = _find_col(sample_headers, COMPONENT_NAME_COLS)
    mat_idx = _find_col(sample_headers, MATERIAL_COLS)
    supplier_idx = _find_col(sample_headers, SUPPLIER_COLS)
    qty_idx = _find_col(sample_headers, QTY_COLS)
    unit_idx = _find_col(sample_headers, UNIT_COLS)
    pn_idx = _find_col(sample_headers, PART_NUM_COLS)

    components: list[BOMComponent] = []
    for i, row in enumerate(rows):
        values = list(row.values())

        def _get(idx: Optional[int]) -> Optional[str]:
            if idx is None or idx >= len(values):
                return None
            v = values[idx]
            return v.strip() if v and v.strip() else None

        name = _get(name_idx) or f"Component {i + 1}"
        material = _get(mat_idx)
        supplier = _get(supplier_idx)
        part_num = _get(pn_idx)
        unit = _get(unit_idx)

        try:
            qty = float(_get(qty_idx) or 0)
        except ValueError:
            qty = 0.0

        status, std, action = _assess_component_compliance(name, material)

        components.append(
            BOMComponent(
                id=f"BOM-UPLOAD-{i + 1:03d}",
                name=name,
                material=material,
                supplier=f"{supplier} [DEMO]" if supplier else None,
                part_number=part_num,
                quantity=qty if qty > 0 else None,
                unit=unit,
                compliance_status=status,
                applicable_standard=std,
                remarks=f"Heuristic assessment. [DEMO DATA - not authoritative BIS guidance]",
                action_required=action,
            )
        )

    return BOMAnalyzeResponse(
        total_components=len(components),
        components=components,
        potentially_applicable_count=sum(1 for c in components if c.compliance_status == BOMStatus.POTENTIALLY_APPLICABLE),
        needs_verification_count=sum(1 for c in components if c.compliance_status == BOMStatus.NEEDS_VERIFICATION),
        has_requirement_count=sum(1 for c in components if c.compliance_status == BOMStatus.HAS_REQUIREMENT),
        summary=(
            f"Analyzed {len(components)} component(s) from uploaded BOM. "
            f"Assessment is heuristic only. [DEMO DATA - consult a BIS compliance expert for authoritative guidance]"
        ),
        data_label=DEMO_LABEL,
    )
