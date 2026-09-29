"""
BIS SAKSHAM - Products Router
Handles product analysis, profiling, and compliance data retrieval.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import uuid
from datetime import datetime

from app.models import (
    ProductAnalyzeRequest, ProductAnalyzeResponse, ProductProfileRequest,
    ClarifyRequest, ClarifyResponse, Product, CompliancePassport,
    ProductAttribute, Standard, QCO, GraphNode, GraphEdge, ComplianceGraph,
    GraphNodeType, RequirementStatus,
)
from app.seed_data import PRODUCTS_DB, DEMO_LABEL, STANDARDS_PROD_001, QCOS_PROD_001

router = APIRouter(prefix="/api/products", tags=["Products"])

# ---------------------------------------------------------------------------
# Helper: keyword-based product matcher
# ---------------------------------------------------------------------------

def _detect_product_keywords(description: str) -> Optional[str]:
    """Return a demo product ID if the description matches known keywords."""
    desc_lower = description.lower()
    water_heater_kw = ["water heater", "geyser", "storage heater", "electric heater", "hot water"]
    toy_kw = ["toy", "building block", "lego", "children", "kids play", "plastic toy"]
    helmet_kw = ["helmet", "hard hat", "safety helmet", "head protection", "industrial helmet"]

    if any(kw in desc_lower for kw in water_heater_kw):
        return "DEMO-PROD-001"
    if any(kw in desc_lower for kw in toy_kw):
        return "DEMO-PROD-002"
    if any(kw in desc_lower for kw in helmet_kw):
        return "DEMO-PROD-003"
    return None


def _extract_generic_attributes(description: str) -> list[ProductAttribute]:
    """Return a generic attribute list for an unrecognised product description."""
    return [
        ProductAttribute(name="Product Description", value=description[:200], confidence=1.0, source="user_provided"),
        ProductAttribute(name="Category", value="General / Unknown", confidence=0.5, source="extracted"),
        ProductAttribute(name="Usage", value="To be determined", confidence=0.3, source="extracted"),
    ]


GENERIC_CLARIFICATION_QUESTIONS = [
    "What is the intended end-use of this product (e.g., domestic, industrial, commercial)?",
    "What materials are primarily used in this product?",
    "Is this product powered by electricity? If yes, what is the rated voltage and power?",
    "What is the target consumer age group (if applicable)?",
    "Is this product intended for import or domestic manufacture?",
    "Do you have an existing IS standard number in mind for this product?",
]

# ---------------------------------------------------------------------------
# POST /api/products/analyze
# ---------------------------------------------------------------------------

@router.post("/analyze", response_model=ProductAnalyzeResponse, summary="Analyze product description")
async def analyze_product(request: ProductAnalyzeRequest):
    """
    Parse a product description and extract structured attributes,
    applicable IS standards, and QCOs.

    For known demo products (water heater, toy, helmet) returns full demo data.
    For unknown products returns a generic extraction.
    [DEMO DATA]
    """
    matched_id = _detect_product_keywords(request.description)

    if matched_id == "DEMO-PROD-001":
        product = PRODUCTS_DB["DEMO-PROD-001"]
        return ProductAnalyzeResponse(
            extracted_name="Electric Storage Water Heater [DEMO]",
            extracted_category="ELECTRICAL",
            extracted_attributes=product.attributes,
            suggested_standards=product.applicable_standards,
            suggested_qcos=product.applicable_qcos,
            clarification_questions=[
                "What is the rated capacity in litres (e.g., 10L, 15L, 25L, 35L)?",
                "What is the rated wattage (e.g., 1500W, 2000W, 3000W)?",
                "Is the inner tank made of stainless steel, glass-lined, or other material?",
                "What is the working pressure rating (bar)?",
                "Is this for domestic use (single-phase 230V) or industrial use (three-phase)?",
                "Does the product have a BIS ISI Mark licence already?",
            ],
            matched_demo_product_id="DEMO-PROD-001",
            confidence_score=0.95,
            data_label=DEMO_LABEL,
        )

    if matched_id == "DEMO-PROD-002":
        product = PRODUCTS_DB["DEMO-PROD-002"]
        return ProductAnalyzeResponse(
            extracted_name="Plastic Toy [DEMO]",
            extracted_category="TOY",
            extracted_attributes=product.attributes,
            suggested_standards=product.applicable_standards,
            suggested_qcos=product.applicable_qcos,
            clarification_questions=[
                "What is the intended age group (e.g., 0-3 years, 3+, 6+, 14+)?",
                "What materials are used in the toy (plastic, fabric, metal, wood)?",
                "Does the toy have any electronic components or batteries?",
                "Are there any small parts that could be detached?",
                "Is the toy for import or domestic manufacture?",
            ],
            matched_demo_product_id="DEMO-PROD-002",
            confidence_score=0.90,
            data_label=DEMO_LABEL,
        )

    if matched_id == "DEMO-PROD-003":
        product = PRODUCTS_DB["DEMO-PROD-003"]
        return ProductAnalyzeResponse(
            extracted_name="Industrial Safety Helmet [DEMO]",
            extracted_category="SAFETY_EQUIPMENT",
            extracted_attributes=product.attributes,
            suggested_standards=product.applicable_standards,
            suggested_qcos=product.applicable_qcos,
            clarification_questions=[
                "What class of helmet (Class G - General, Class E - Electrical, Class C - Conductive)?",
                "What material is the shell (HDPE, ABS, Fibreglass, Polycarbonate)?",
                "Is the helmet for construction, mining, electrical, or general industrial use?",
                "Does it include accessories like face shield or ear protection?",
                "What is the working temperature range?",
            ],
            matched_demo_product_id="DEMO-PROD-003",
            confidence_score=0.88,
            data_label=DEMO_LABEL,
        )

    # Generic fallback
    generic_attrs = _extract_generic_attributes(request.description)
    return ProductAnalyzeResponse(
        extracted_name="Unknown Product [DEMO]",
        extracted_category=request.category_hint or "GENERAL",
        extracted_attributes=generic_attrs,
        suggested_standards=[],
        suggested_qcos=[],
        clarification_questions=GENERIC_CLARIFICATION_QUESTIONS,
        matched_demo_product_id=None,
        confidence_score=0.3,
        data_label=DEMO_LABEL,
    )


# ---------------------------------------------------------------------------
# POST /api/products/profile
# ---------------------------------------------------------------------------

@router.post("/profile", summary="Confirm and save product profile")
async def save_product_profile(request: ProductProfileRequest):
    """
    Confirms and saves a product profile to the in-memory store.
    If it matches a demo product, returns the full demo product.
    Otherwise creates a minimal profile.
    [DEMO DATA]
    """
    matched_id = _detect_product_keywords(request.description)
    if matched_id and matched_id in PRODUCTS_DB:
        product = PRODUCTS_DB[matched_id]
        return {
            "success": True,
            "product_id": product.id,
            "message": "Product profile matched to demo product. [DEMO DATA]",
            "product": product.model_dump(),
            "data_label": DEMO_LABEL,
        }

    # Create a new generic product entry
    new_id = f"PROD-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow().isoformat()
    new_product = Product(
        id=new_id,
        name=request.name,
        description=request.description,
        category=request.category,  # type: ignore[arg-type]
        hs_code=request.hs_code,
        manufacturer=request.manufacturer,
        model_number=request.model_number,
        attributes=request.attributes,
        applicable_standards=[],
        applicable_qcos=[],
        requirements=[],
        tests=[],
        laboratories=[],
        bom_components=[],
        documents=[],
        evidence_gaps=[],
        change_events=[],
        compliance_score=0.0,
        overall_status="PENDING",
        created_at=now,
        updated_at=now,
        data_label=DEMO_LABEL,
    )
    PRODUCTS_DB[new_id] = new_product
    return {
        "success": True,
        "product_id": new_id,
        "message": "New product profile created (demo). [DEMO DATA]",
        "product": new_product.model_dump(),
        "data_label": DEMO_LABEL,
    }


# ---------------------------------------------------------------------------
# POST /api/products/clarify
# ---------------------------------------------------------------------------

@router.post("/clarify", response_model=ClarifyResponse, summary="Get clarification questions")
async def get_clarification_questions(request: ClarifyRequest):
    """
    Returns context-sensitive clarification questions for a product description.
    [DEMO DATA]
    """
    matched_id = _detect_product_keywords(request.product_description)

    if matched_id == "DEMO-PROD-001":
        questions = [
            {"id": "q1", "question": "What is the storage capacity in litres?", "type": "select",
             "options": ["10L", "15L", "25L", "35L", "50L", "Other"]},
            {"id": "q2", "question": "What is the rated electrical power?", "type": "select",
             "options": ["1500W", "2000W", "3000W", "Other"]},
            {"id": "q3", "question": "What material is the inner tank?", "type": "select",
             "options": ["Stainless Steel (SS 304)", "Glass-lined mild steel", "Copper", "Other"]},
            {"id": "q4", "question": "Does the product already have a BIS ISI Mark licence?", "type": "boolean"},
            {"id": "q5", "question": "Has the product been tested at an NABL-accredited lab?", "type": "boolean"},
        ]
    elif matched_id == "DEMO-PROD-002":
        questions = [
            {"id": "q1", "question": "What is the target age group for this toy?", "type": "select",
             "options": ["0-3 years", "3-6 years", "6-12 years", "12+ years"]},
            {"id": "q2", "question": "Does the toy contain any electronic components?", "type": "boolean"},
            {"id": "q3", "question": "Does the toy contain any small detachable parts?", "type": "boolean"},
            {"id": "q4", "question": "What primary material is the toy made from?", "type": "select",
             "options": ["Plastic (ABS/PP/PE)", "Fabric/Plush", "Wood", "Metal", "Mixed"]},
        ]
    elif matched_id == "DEMO-PROD-003":
        questions = [
            {"id": "q1", "question": "What class is the safety helmet?", "type": "select",
             "options": ["Class G (General)", "Class E (Electrical)", "Class C (Conductive)"]},
            {"id": "q2", "question": "What is the primary application?", "type": "select",
             "options": ["Construction", "Mining", "Electrical work", "General industrial"]},
            {"id": "q3", "question": "What is the shell material?", "type": "select",
             "options": ["HDPE", "ABS", "Fibreglass", "Polycarbonate"]},
        ]
    else:
        questions = [
            {"id": "q1", "question": "What is the primary intended use of this product?", "type": "text"},
            {"id": "q2", "question": "Is this product electrically powered?", "type": "boolean"},
            {"id": "q3", "question": "Who is the end-user (consumer, industrial, commercial)?", "type": "select",
             "options": ["Consumer / Domestic", "Industrial", "Commercial", "Government"]},
            {"id": "q4", "question": "What materials are primarily used?", "type": "text"},
            {"id": "q5", "question": "Do you have an existing IS standard number?", "type": "text"},
        ]

    return ClarifyResponse(questions=questions, data_label=DEMO_LABEL)


# ---------------------------------------------------------------------------
# GET /api/products
# ---------------------------------------------------------------------------

@router.get("/", summary="List all demo products")
async def list_products():
    """Returns a list of all demo products in the system. [DEMO DATA]"""
    products = []
    for p in PRODUCTS_DB.values():
        products.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "overall_status": p.overall_status,
            "compliance_score": p.compliance_score,
            "manufacturer": p.manufacturer,
            "applicable_standards": [s.number for s in p.applicable_standards],
            "requirements_count": len(p.requirements),
            "gaps_count": len(p.evidence_gaps),
            "updated_at": p.updated_at,
            "data_label": DEMO_LABEL,
        })
    return {"products": products, "total": len(products), "data_label": DEMO_LABEL}


# ---------------------------------------------------------------------------
# GET /api/products/{id}
# ---------------------------------------------------------------------------

@router.get("/{product_id}", response_model=Product, summary="Get product details")
async def get_product(product_id: str):
    """Returns full product details including all compliance data. [DEMO DATA]"""
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")
    return product


# ---------------------------------------------------------------------------
# GET /api/products/{id}/requirements
# ---------------------------------------------------------------------------

@router.get("/{product_id}/requirements", summary="Get requirement matrix")
async def get_requirements(product_id: str):
    """Returns the full compliance requirement matrix for a product. [DEMO DATA]"""
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    status_counts: dict[str, int] = {}
    for req in product.requirements:
        key = req.status.value
        status_counts[key] = status_counts.get(key, 0) + 1

    return {
        "product_id": product_id,
        "product_name": product.name,
        "requirements": [r.model_dump() for r in product.requirements],
        "summary": status_counts,
        "total": len(product.requirements),
        "data_label": DEMO_LABEL,
    }


# ---------------------------------------------------------------------------
# GET /api/products/{id}/graph
# ---------------------------------------------------------------------------

@router.get("/{product_id}/graph", response_model=ComplianceGraph, summary="Get compliance graph")
async def get_compliance_graph(product_id: str):
    """
    Returns a graph (nodes + edges) representing the compliance relationships
    for a product. Suitable for rendering in a graph visualisation library.
    [DEMO DATA]
    """
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    # Product node
    nodes.append(GraphNode(
        id=product.id,
        label=product.name,
        type=GraphNodeType.PRODUCT,
        status=product.overall_status,
        metadata={"compliance_score": product.compliance_score},
    ))

    # Standard nodes
    for std in product.applicable_standards:
        nodes.append(GraphNode(id=std.id, label=std.number, type=GraphNodeType.STANDARD,
                               status=std.status, metadata={"title": std.title}))
        edges.append(GraphEdge(id=f"e-{product.id}-{std.id}", source=product.id,
                               target=std.id, label="governed_by"))

    # QCO nodes
    for qco in product.applicable_qcos:
        nodes.append(GraphNode(id=qco.id, label=qco.title[:40], type=GraphNodeType.QCO,
                               status="MANDATORY" if qco.mandatory_certification else "VOLUNTARY"))
        edges.append(GraphEdge(id=f"e-{product.id}-{qco.id}", source=product.id,
                               target=qco.id, label="covered_by"))

    # Requirement nodes
    for req in product.requirements:
        nodes.append(GraphNode(id=req.id, label=req.name, type=GraphNodeType.REQUIREMENT,
                               status=req.status.value, metadata={"category": req.category}))
        # Link product -> requirement
        edges.append(GraphEdge(id=f"e-{product.id}-{req.id}", source=product.id,
                               target=req.id, label="has_requirement"))
        # Link standard -> requirement (use first standard)
        if product.applicable_standards:
            edges.append(GraphEdge(id=f"e-std-{req.id}", source=product.applicable_standards[0].id,
                                   target=req.id, label="mandates"))

    # Test nodes
    for test in product.tests:
        nodes.append(GraphNode(id=test.id, label=test.name, type=GraphNodeType.TEST,
                               metadata={"estimated_days": test.estimated_days,
                                         "estimated_cost_inr": test.estimated_cost_inr}))
        # Link requirement -> test
        for req in product.requirements:
            if req.test_id == test.id:
                edges.append(GraphEdge(id=f"e-{req.id}-{test.id}", source=req.id,
                                       target=test.id, label="verified_by"))

    # Lab nodes
    for lab in product.laboratories:
        nodes.append(GraphNode(id=lab.id, label=lab.name[:40], type=GraphNodeType.LAB,
                               metadata={"city": lab.city, "nabl_id": lab.nabl_id}))
        for test_id in lab.tests_covered:
            edges.append(GraphEdge(id=f"e-{lab.id}-{test_id}", source=test_id,
                                   target=lab.id, label="conducted_at"))

    # Document nodes
    for doc in product.documents:
        nodes.append(GraphNode(id=doc.id, label=doc.name[:40], type=GraphNodeType.DOCUMENT,
                               status=doc.status.value))
        edges.append(GraphEdge(id=f"e-{product.id}-{doc.id}", source=product.id,
                               target=doc.id, label="evidenced_by"))

    return ComplianceGraph(product_id=product_id, nodes=nodes, edges=edges, data_label=DEMO_LABEL)


# ---------------------------------------------------------------------------
# GET /api/products/{id}/tests
# ---------------------------------------------------------------------------

@router.get("/{product_id}/tests", summary="Get required tests")
async def get_tests(product_id: str):
    """Returns the list of required tests for a product. [DEMO DATA]"""
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    total_cost = sum((t.estimated_cost_inr or 0) for t in product.tests)
    max_days = max((t.estimated_days or 0) for t in product.tests) if product.tests else 0

    return {
        "product_id": product_id,
        "tests": [t.model_dump() for t in product.tests],
        "total_tests": len(product.tests),
        "estimated_total_cost_inr": total_cost,
        "estimated_max_days": max_days,
        "data_label": DEMO_LABEL,
    }


# ---------------------------------------------------------------------------
# GET /api/products/{id}/passport
# ---------------------------------------------------------------------------

@router.get("/{product_id}/passport", summary="Get compliance passport")
async def get_compliance_passport(product_id: str):
    """
    Returns the compliance passport summarising the product's compliance status,
    critical gaps, and next steps. [DEMO DATA]
    """
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    status_counts: dict[str, int] = {}
    for req in product.requirements:
        key = req.status.value
        status_counts[key] = status_counts.get(key, 0) + 1

    critical_gaps = [
        gap.gap_description for gap in product.evidence_gaps
        if gap.status == RequirementStatus.MISSING
    ]

    next_steps = list({gap.action_required for gap in product.evidence_gaps if gap.action_required})

    passport = CompliancePassport(
        product_id=product_id,
        product_name=product.name,
        overall_status=product.overall_status,
        compliance_score=product.compliance_score,
        standards=product.applicable_standards,
        qcos=product.applicable_qcos,
        requirements_summary=status_counts,
        critical_gaps=critical_gaps,
        next_steps=next_steps,
        generated_at=datetime.utcnow().isoformat(),
        valid_for_days=30,
        data_label=DEMO_LABEL,
    )
    return passport.model_dump()


# ---------------------------------------------------------------------------
# GET /api/products/{id}/gaps
# ---------------------------------------------------------------------------

@router.get("/{product_id}/gaps", summary="Get compliance gaps")
async def get_gaps(product_id: str):
    """Returns all identified compliance gaps and evidence shortfalls. [DEMO DATA]"""
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    # Also include partial documents as gaps
    doc_gaps = [
        {
            "type": "document_gap",
            "document_id": doc.id,
            "document_name": doc.name,
            "status": doc.status.value,
            "gaps": doc.gaps or [],
        }
        for doc in product.documents
        if doc.gaps
    ]

    return {
        "product_id": product_id,
        "evidence_gaps": [g.model_dump() for g in product.evidence_gaps],
        "document_gaps": doc_gaps,
        "total_evidence_gaps": len(product.evidence_gaps),
        "total_document_gaps": len(doc_gaps),
        "summary": f"{len(product.evidence_gaps)} evidence gap(s) and {len(doc_gaps)} document gap(s) identified. [DEMO]",
        "data_label": DEMO_LABEL,
    }


# ---------------------------------------------------------------------------
# GET /api/products/{id}/changes
# ---------------------------------------------------------------------------

@router.get("/{product_id}/changes", summary="Get change events")
async def get_change_events(product_id: str):
    """Returns regulatory change events affecting the product. [DEMO DATA]"""
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found. [DEMO]")

    return {
        "product_id": product_id,
        "change_events": [ce.model_dump() for ce in product.change_events],
        "total": len(product.change_events),
        "high_impact_count": sum(1 for ce in product.change_events if ce.impact_level == "HIGH"),
        "data_label": DEMO_LABEL,
    }
