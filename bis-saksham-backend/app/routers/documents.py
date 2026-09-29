"""
BIS SAKSHAM - Documents Router
Handles document upload and compliance analysis.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

import io
import re
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional

from app.models import DocumentAnalyzeResponse, DocumentStatus
from app.seed_data import DEMO_LABEL

router = APIRouter(prefix="/api/documents", tags=["Document Analysis"])

# ---------------------------------------------------------------------------
# Keyword dictionaries for document type detection
# ---------------------------------------------------------------------------

TEST_REPORT_KEYWORDS = [
    "test report", "test certificate", "lab report", "nabl", "accredited laboratory",
    "test result", "analysis report", "inspection report",
]

CERTIFICATE_KEYWORDS = [
    "certificate", "isi mark", "bis licence", "bis license", "hallmark", "certification",
    "approval certificate", "conformity", "declaration of conformity",
]

SPECIFICATION_KEYWORDS = [
    "specification", "technical datasheet", "product spec", "data sheet",
    "product description", "technical specification",
]

APPLICATION_KEYWORDS = [
    "application form", "application for", "licence application", "registration form",
    "cms application",
]

STANDARD_PATTERNS = [
    r"IS\s*\d{3,6}(?:[-:]\d+)?(?::\d{4})?",
    r"IEC\s*\d{3,6}(?:[-:]\d+)?",
    r"ISO\s*\d{3,6}(?:[-:]\d+)?",
    r"BS\s*\d{3,6}(?:[-:]\d+)?",
]

PRODUCT_KEYWORDS_MAP = {
    "water heater": "Electric Storage Water Heater [DEMO]",
    "geyser": "Electric Storage Water Heater [DEMO]",
    "toy": "Toys / Play Equipment [DEMO]",
    "helmet": "Safety Helmet [DEMO]",
    "hard hat": "Safety Helmet [DEMO]",
    "cable": "Electrical Cable [DEMO]",
    "led": "LED Luminaire [DEMO]",
    "motor": "Electric Motor [DEMO]",
}

CRITICAL_SECTION_PATTERNS = {
    "temperature_rise": [r"temperature rise", r"clause\s*6\.3", r"thermal test"],
    "leakage_current": [r"leakage current", r"clause\s*5\.2"],
    "electrical_safety": [r"electrical safety", r"dielectric", r"clause\s*5\.1"],
    "energy_efficiency": [r"energy efficiency", r"standing heat loss", r"clause\s*7\.1"],
    "pressure_test": [r"pressure test", r"hydraulic", r"clause\s*8\.1"],
    "mechanical_safety": [r"mechanical safety", r"drop test", r"clause\s*4"],
    "chemical_safety": [r"chemical", r"heavy metal", r"migration"],
    "flammability": [r"flammab", r"burn rate", r"clause\s*7"],
    "impact_test": [r"impact", r"attenuation", r"clause\s*4\.3"],
    "penetration_test": [r"penetration", r"clause\s*4\.4"],
    "retention_system": [r"retention", r"chin strap", r"clause\s*4\.6"],
}


def _extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception:
        return ""


def _detect_document_type(text: str, filename: str) -> str:
    text_l = text.lower()
    fname_l = filename.lower()
    combined = text_l + " " + fname_l

    if any(kw in combined for kw in CERTIFICATE_KEYWORDS):
        return "certificate"
    if any(kw in combined for kw in TEST_REPORT_KEYWORDS):
        return "test_report"
    if any(kw in combined for kw in APPLICATION_KEYWORDS):
        return "application"
    if any(kw in combined for kw in SPECIFICATION_KEYWORDS):
        return "specification"
    return "unknown"


def _detect_standards(text: str) -> Optional[str]:
    for pattern in STANDARD_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip() + " [DEMO - extracted]"
    return None


def _detect_product(text: str) -> Optional[str]:
    text_l = text.lower()
    for keyword, product_name in PRODUCT_KEYWORDS_MAP.items():
        if keyword in text_l:
            return product_name
    return None


def _find_sections(text: str) -> tuple[list[str], list[str]]:
    """Return (found_sections, missing_sections) based on keyword matching."""
    text_l = text.lower()
    found = []
    missing = []
    for section_name, patterns in CRITICAL_SECTION_PATTERNS.items():
        if any(re.search(p, text_l) for p in patterns):
            found.append(section_name.replace("_", " ").title())
        else:
            missing.append(section_name.replace("_", " ").title())
    return found, missing


def _determine_status(doc_type: str, found_sections: list[str], missing_sections: list[str]) -> DocumentStatus:
    if doc_type == "unknown":
        return DocumentStatus.PARTIAL
    if not missing_sections:
        return DocumentStatus.VALID
    if not found_sections:
        return DocumentStatus.MISSING
    return DocumentStatus.PARTIAL


# ---------------------------------------------------------------------------
# POST /api/documents/analyze
# ---------------------------------------------------------------------------

@router.post("/analyze", response_model=DocumentAnalyzeResponse, summary="Upload and analyze document")
async def analyze_document(
    file: UploadFile = File(...),
    product_id: Optional[str] = Form(None),
):
    """
    Upload a document (PDF, image, text) and receive a compliance analysis:
    - Detected document type
    - Referenced IS standard
    - Sections found vs. missing
    - Recommendations

    [DEMO DATA - Heuristic text analysis, not authoritative BIS review]
    """
    filename = file.filename or "uploaded_file"
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Extract text
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        text = _extract_text_from_pdf(content)
        if not text:
            # Fallback: treat as binary, use filename only
            text = filename
    elif ext in ("txt", "csv", "md"):
        text = content.decode("utf-8-sig", errors="replace")
    elif ext in ("jpg", "jpeg", "png", "gif", "bmp"):
        # Image - cannot extract text without OCR in demo
        text = filename
    elif ext in ("xlsx", "xls"):
        text = filename + " spreadsheet"
    else:
        text = content.decode("utf-8-sig", errors="replace")

    # Analysis
    doc_type = _detect_document_type(text, filename)
    detected_standard = _detect_standards(text)
    detected_product = _detect_product(text)
    found_sections, missing_sections = _find_sections(text)
    status = _determine_status(doc_type, found_sections, missing_sections)

    # Build gaps list
    gaps = []
    if missing_sections:
        gaps = [f"Section not found: {s}" for s in missing_sections[:5]]  # Cap at 5
    if doc_type == "unknown":
        gaps.append("Document type could not be determined from content.")

    # Recommendations
    recommendations = []
    if status == DocumentStatus.PARTIAL:
        recommendations.append(
            "Document appears incomplete. Ensure all required test clauses are covered before BIS submission. [DEMO]"
        )
    if not detected_standard:
        recommendations.append(
            "No IS standard reference found in document. Ensure the applicable IS standard is clearly cited. [DEMO]"
        )
    if doc_type == "test_report" and "nabl" not in text.lower():
        recommendations.append(
            "NABL accreditation reference not found. Ensure the lab's NABL certificate number is included in the test report. [DEMO]"
        )
    if status == DocumentStatus.VALID:
        recommendations.append("Document appears complete and well-structured. [DEMO]")

    recommendations.append("This is a demo heuristic analysis. Always verify with a qualified BIS consultant. [DEMO DATA]")

    return DocumentAnalyzeResponse(
        document_type=doc_type,
        detected_standard=detected_standard,
        detected_product=detected_product,
        status=status,
        gaps_found=gaps,
        valid_sections=found_sections[:10],
        recommendations=recommendations,
        data_label=DEMO_LABEL,
    )
