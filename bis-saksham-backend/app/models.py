"""
BIS SAKSHAM - Pydantic Models
All entities and API request/response schemas.
[DEMO DATA] - All models contain demo data structures clearly labeled.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RequirementStatus(str, Enum):
    MET = "MET"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PENDING = "PENDING"


class RequirementType(str, Enum):
    MANDATORY = "MANDATORY"
    OPTIONAL = "OPTIONAL"
    CONDITIONAL = "CONDITIONAL"


class BOMStatus(str, Enum):
    CONFIRMED_NO_REQUIREMENT = "CONFIRMED_NO_REQUIREMENT"
    POTENTIALLY_APPLICABLE = "POTENTIALLY_APPLICABLE"
    NEEDS_VERIFICATION = "NEEDS_VERIFICATION"
    NO_REQUIREMENT_IDENTIFIED = "NO_REQUIREMENT_IDENTIFIED"
    HAS_REQUIREMENT = "HAS_REQUIREMENT"


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    EXPIRED = "EXPIRED"
    VALID = "VALID"


class ProductCategory(str, Enum):
    ELECTRICAL = "ELECTRICAL"
    TOY = "TOY"
    SAFETY_EQUIPMENT = "SAFETY_EQUIPMENT"
    CHEMICAL = "CHEMICAL"
    FOOD = "FOOD"
    AUTOMOTIVE = "AUTOMOTIVE"
    CONSTRUCTION = "CONSTRUCTION"
    GENERAL = "GENERAL"


class ChangeEventType(str, Enum):
    AMENDMENT = "AMENDMENT"
    NEW_STANDARD = "NEW_STANDARD"
    QCO_UPDATE = "QCO_UPDATE"
    WITHDRAWAL = "WITHDRAWAL"
    CLARIFICATION = "CLARIFICATION"


class GraphNodeType(str, Enum):
    PRODUCT = "PRODUCT"
    STANDARD = "STANDARD"
    QCO = "QCO"
    REQUIREMENT = "REQUIREMENT"
    TEST = "TEST"
    LAB = "LAB"
    DOCUMENT = "DOCUMENT"
    CERTIFICATION = "CERTIFICATION"


# ---------------------------------------------------------------------------
# Core Entity Models
# ---------------------------------------------------------------------------

class ProductAttribute(BaseModel):
    """Extracted or confirmed attribute of a product."""
    name: str
    value: str
    unit: Optional[str] = None
    confidence: Optional[float] = None  # 0.0 to 1.0 for AI-extracted attributes
    source: Optional[str] = None  # "extracted", "user_confirmed", "default"


class Standard(BaseModel):
    """Indian Standard (IS) applicable to a product."""
    id: str
    title: str
    number: str  # e.g. "IS 1258:2018"
    year: int
    status: str  # "ACTIVE", "WITHDRAWN", "UNDER_REVISION"
    scope: str
    amendment: Optional[str] = None
    bis_catalog_url: Optional[str] = None
    data_label: str = "DEMO DATA"


class QCO(BaseModel):
    """Quality Control Order applicable to a product."""
    id: str
    title: str
    notification_number: str
    effective_date: str
    ministry: str
    product_categories: List[str]
    mandatory_certification: bool
    data_label: str = "DEMO DATA"


class TestRequirement(BaseModel):
    """Individual test required under a standard."""
    id: str
    name: str
    clause: str  # Standard clause reference
    method: str  # Test method description
    parameter: str  # What is being measured
    acceptance_criteria: str
    lab_required: bool = True
    nabl_accreditation_required: bool = True
    estimated_cost_inr: Optional[int] = None
    estimated_days: Optional[int] = None


class Requirement(BaseModel):
    """A compliance requirement for a product."""
    id: str
    name: str
    category: str
    type: RequirementType
    status: RequirementStatus
    standard_ref: str  # e.g. "IS 1258:2018 Clause 5.1"
    description: str
    test_required: bool = False
    test_id: Optional[str] = None
    evidence_type: Optional[str] = None  # "test_report", "certificate", "declaration"
    evidence_status: Optional[str] = None
    remarks: Optional[str] = None


class Laboratory(BaseModel):
    """NABL-accredited testing laboratory."""
    id: str
    name: str
    city: str
    state: str
    nabl_id: str
    accreditation_valid_until: str
    tests_covered: List[str]  # List of test IDs
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    estimated_cost_inr: Optional[int] = None
    estimated_turnaround_days: Optional[int] = None
    website: Optional[str] = None
    data_label: str = "DEMO DATA"


class BOMComponent(BaseModel):
    """Bill of Materials component with compliance assessment."""
    id: str
    name: str
    material: Optional[str] = None
    supplier: Optional[str] = None
    part_number: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    compliance_status: BOMStatus
    applicable_standard: Optional[str] = None
    remarks: Optional[str] = None
    action_required: Optional[str] = None


class Document(BaseModel):
    """Document associated with a product's compliance dossier."""
    id: str
    name: str
    type: str  # "test_report", "certificate", "specification", "application"
    status: DocumentStatus
    file_name: Optional[str] = None
    uploaded_at: Optional[str] = None
    valid_until: Optional[str] = None
    issuing_body: Optional[str] = None
    remarks: Optional[str] = None
    gaps: Optional[List[str]] = None  # Missing sections or issues found


class Evidence(BaseModel):
    """Evidence item for a specific requirement."""
    requirement_id: str
    requirement_name: str
    evidence_type: str
    status: RequirementStatus
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    gap_description: Optional[str] = None
    action_required: Optional[str] = None


class ChangeEvent(BaseModel):
    """Regulatory change event affecting a product."""
    id: str
    event_type: ChangeEventType
    title: str
    description: str
    standard_affected: str
    effective_date: str
    impact_level: str  # "HIGH", "MEDIUM", "LOW"
    action_required: str
    source_url: Optional[str] = None
    data_label: str = "DEMO DATA"


class CompliancePassport(BaseModel):
    """Comprehensive compliance passport for a product."""
    product_id: str
    product_name: str
    overall_status: str  # "COMPLIANT", "NON_COMPLIANT", "PARTIAL"
    compliance_score: float  # 0.0 to 100.0
    standards: List[Standard]
    qcos: List[QCO]
    requirements_summary: Dict[str, int]  # e.g. {"MET": 5, "MISSING": 2, "PARTIAL": 1}
    critical_gaps: List[str]
    next_steps: List[str]
    generated_at: str
    valid_for_days: int = 30
    data_label: str = "DEMO DATA"


class Product(BaseModel):
    """Complete product entity with all compliance data."""
    id: str
    name: str
    description: str
    category: ProductCategory
    hs_code: Optional[str] = None
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    attributes: List[ProductAttribute]
    applicable_standards: List[Standard]
    applicable_qcos: List[QCO]
    requirements: List[Requirement]
    tests: List[TestRequirement]
    laboratories: List[Laboratory]
    bom_components: List[BOMComponent]
    documents: List[Document]
    evidence_gaps: List[Evidence]
    change_events: List[ChangeEvent]
    compliance_score: float
    overall_status: str
    created_at: str
    updated_at: str
    data_label: str = "DEMO DATA"


# ---------------------------------------------------------------------------
# Graph Models
# ---------------------------------------------------------------------------

class GraphNode(BaseModel):
    """Node in the compliance graph."""
    id: str
    label: str
    type: GraphNodeType
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class GraphEdge(BaseModel):
    """Edge/relationship in the compliance graph."""
    id: str
    source: str
    target: str
    label: str
    type: Optional[str] = None


class ComplianceGraph(BaseModel):
    """Graph representation of compliance relationships."""
    product_id: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    data_label: str = "DEMO DATA"


# ---------------------------------------------------------------------------
# Lab Matching Models
# ---------------------------------------------------------------------------

class LabMatchResult(BaseModel):
    """Result of lab matching for a set of tests."""
    lab: Laboratory
    matched_tests: List[str]
    total_estimated_cost_inr: int
    total_estimated_days: int
    recommendation_score: float  # 0.0 to 1.0
    recommendation_reason: str


class LabMatchResponse(BaseModel):
    """Response for lab matching request."""
    product_id: Optional[str] = None
    test_ids: List[str]
    optimized_lab_plan: List[LabMatchResult]
    total_labs_needed: int
    estimated_total_cost_inr: int
    estimated_total_days: int
    data_label: str = "DEMO DATA"


# ---------------------------------------------------------------------------
# Request / Response Models for API Endpoints
# ---------------------------------------------------------------------------

class ProductAnalyzeRequest(BaseModel):
    """Request to analyze a product description."""
    description: str = Field(..., min_length=10, description="Product description text")
    category_hint: Optional[str] = None


class ProductAnalyzeResponse(BaseModel):
    """Response with extracted product attributes."""
    extracted_name: str
    extracted_category: str
    extracted_attributes: List[ProductAttribute]
    suggested_standards: List[Standard]
    suggested_qcos: List[QCO]
    clarification_questions: List[str]
    matched_demo_product_id: Optional[str] = None
    confidence_score: float
    data_label: str = "DEMO DATA"


class ProductProfileRequest(BaseModel):
    """Request to confirm and save a product profile."""
    name: str
    description: str
    category: str
    attributes: List[ProductAttribute]
    hs_code: Optional[str] = None
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None


class ClarifyRequest(BaseModel):
    """Request for clarification questions about a product."""
    product_description: str
    current_attributes: Optional[List[ProductAttribute]] = None


class ClarifyResponse(BaseModel):
    """Response with clarification questions."""
    questions: List[Dict[str, str]]  # [{"id": "q1", "question": "...", "type": "text|select|boolean"}]
    data_label: str = "DEMO DATA"


class BOMAnalyzeResponse(BaseModel):
    """Response for BOM analysis."""
    total_components: int
    components: List[BOMComponent]
    potentially_applicable_count: int
    needs_verification_count: int
    has_requirement_count: int
    summary: str
    data_label: str = "DEMO DATA"


class DocumentAnalyzeResponse(BaseModel):
    """Response for document analysis."""
    document_type: str
    detected_standard: Optional[str] = None
    detected_product: Optional[str] = None
    status: DocumentStatus
    gaps_found: List[str]
    valid_sections: List[str]
    recommendations: List[str]
    data_label: str = "DEMO DATA"


class ChatMessage(BaseModel):
    """A chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request to the chat assistant."""
    message: str
    product_id: Optional[str] = None
    context: Optional[str] = None
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Response from the chat assistant."""
    message: str
    suggestions: Optional[List[str]] = None
    related_requirements: Optional[List[str]] = None
    data_label: str = "DEMO DATA"


class StandardSearchResult(BaseModel):
    """Search result for a standard."""
    id: str
    number: str
    title: str
    year: int
    status: str
    relevance_score: float
    data_label: str = "DEMO DATA"


class BISService(BaseModel):
    """BIS certification service."""
    id: str
    name: str
    description: str
    url: str
    category: str
    applicable_to: List[str]
    data_label: str = "DEMO DATA"


class RegulatoryUpdate(BaseModel):
    """Regulatory update / notification."""
    id: str
    title: str
    summary: str
    ministry: str
    date: str
    impact: str  # "HIGH", "MEDIUM", "LOW"
    categories_affected: List[str]
    source_url: Optional[str] = None
    data_label: str = "DEMO DATA"


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    environment: str
    data_label: str = "DEMO DATA"
