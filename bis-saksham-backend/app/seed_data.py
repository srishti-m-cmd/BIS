"""
BIS SAKSHAM - Comprehensive Demo Seed Data
===========================================
ALL DATA IN THIS FILE IS DEMO / SYNTHETIC DATA.
It is clearly labeled and does NOT represent real government records,
real laboratory certifications, or real regulatory decisions.

Data is provided for demonstration purposes only.
"""

from app.models import (
    Product, ProductAttribute, Standard, QCO, Requirement, TestRequirement,
    Laboratory, BOMComponent, Document, Evidence, ChangeEvent,
    RequirementStatus, RequirementType, BOMStatus, DocumentStatus,
    ProductCategory, ChangeEventType,
)

# ---------------------------------------------------------------------------
# SHARED DEMO LABEL
# ---------------------------------------------------------------------------
DEMO_LABEL = "DEMO DATA"

# ===========================================================================
# PRODUCT 1: Electric Storage Water Heater
# ===========================================================================

STANDARDS_PROD_001 = [
    Standard(
        id="STD-001",
        title="Electric Storage Water Heaters - Specification [DEMO DATA]",
        number="IS 1258:2018",
        year=2018,
        status="ACTIVE",
        scope=(
            "This standard specifies requirements for electric storage water heaters "
            "for household and similar purposes, including safety, performance and "
            "energy efficiency requirements. [DEMO DATA - For illustration only]"
        ),
        amendment="Amendment 1 (2022) - Updated energy efficiency clause",
        bis_catalog_url="https://www.bis.gov.in/",  # Demo URL
        data_label=DEMO_LABEL,
    )
]

QCOS_PROD_001 = [
    QCO(
        id="QCO-001",
        title="Electric and Electronic Appliances Quality Control Order [DEMO DATA]",
        notification_number="SO 4664(E) [DEMO]",
        effective_date="2023-01-01",
        ministry="Ministry of Heavy Industries [DEMO]",
        product_categories=["Electric Water Heaters", "Electric Geysers", "Immersion Heaters"],
        mandatory_certification=True,
        data_label=DEMO_LABEL,
    )
]

REQUIREMENTS_PROD_001 = [
    Requirement(
        id="REQ-001-01",
        name="Electrical Safety",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 1258:2018 Clause 5.1 [DEMO]",
        description="The appliance shall withstand a dielectric strength test and show no breakdown. [DEMO DATA]",
        test_required=True,
        test_id="TEST-001-01",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Test report uploaded. Valid. [DEMO]",
    ),
    Requirement(
        id="REQ-001-02",
        name="Leakage Current Test",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 1258:2018 Clause 5.2 [DEMO]",
        description="Leakage current shall not exceed 0.75 mA under normal conditions. [DEMO DATA]",
        test_required=True,
        test_id="TEST-001-02",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Passed. Leakage current measured at 0.42 mA. [DEMO]",
    ),
    Requirement(
        id="REQ-001-03",
        name="Temperature Rise Test",
        category="Performance",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MISSING,
        standard_ref="IS 1258:2018 Clause 6.3 [DEMO]",
        description=(
            "Temperature rise of external parts shall not exceed 60°C above ambient. "
            "IS 1258:2018 Amendment 1 updated temperature limits. [DEMO DATA]"
        ),
        test_required=True,
        test_id="TEST-001-03",
        evidence_type="test_report",
        evidence_status="MISSING",
        remarks="Test report section missing. Amendment requires re-test with new limits. [DEMO]",
    ),
    Requirement(
        id="REQ-001-04",
        name="Energy Efficiency",
        category="Performance",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MISSING,
        standard_ref="IS 1258:2018 Clause 7.1 [DEMO]",
        description="Standing heat loss shall comply with Bureau of Energy Efficiency (BEE) star rating norms. [DEMO DATA]",
        test_required=True,
        test_id="TEST-001-04",
        evidence_type="test_report",
        evidence_status="MISSING",
        remarks="Energy efficiency test report not uploaded. [DEMO]",
    ),
    Requirement(
        id="REQ-001-05",
        name="Pressure Test",
        category="Structural",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 1258:2018 Clause 8.1 [DEMO]",
        description="Tank shall withstand 1.5 times the working pressure for 1 hour without leakage. [DEMO DATA]",
        test_required=True,
        test_id="TEST-001-05",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Passed at 10.5 bar. [DEMO]",
    ),
    Requirement(
        id="REQ-001-06",
        name="Insulation Resistance",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 1258:2018 Clause 5.3 [DEMO]",
        description="Insulation resistance between live parts and earthed metal parts shall not be less than 2 MΩ. [DEMO DATA]",
        test_required=False,
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Measured at 4.7 MΩ. Compliant. [DEMO]",
    ),
    Requirement(
        id="REQ-001-07",
        name="BIS Certification (ISI Mark)",
        category="Certification",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MISSING,
        standard_ref="IS 1258:2018 + QCO-001 [DEMO]",
        description=(
            "Product must hold a valid BIS ISI Mark licence under IS 1258:2018. "
            "Mandatory under applicable QCO. [DEMO DATA]"
        ),
        test_required=False,
        evidence_type="certificate",
        evidence_status="MISSING",
        remarks="BIS application not yet submitted. CRITICAL GAP. [DEMO]",
    ),
    Requirement(
        id="REQ-001-08",
        name="ISI Mark on Product",
        category="Marking",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.PARTIAL,
        standard_ref="IS 1258:2018 Clause 11 [DEMO]",
        description="Product and packaging must bear the ISI Mark with licence number. [DEMO DATA]",
        test_required=False,
        evidence_type="declaration",
        evidence_status="PARTIAL",
        remarks="Marking layout submitted but licence number pending. [DEMO]",
    ),
]

TESTS_PROD_001 = [
    TestRequirement(
        id="TEST-001-01",
        name="Electrical Safety Test",
        clause="IS 1258:2018 Clause 5.1 [DEMO]",
        method="High-voltage dielectric strength test at 1500 V AC for 1 minute",
        parameter="Dielectric breakdown",
        acceptance_criteria="No breakdown or flashover",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=8000,
        estimated_days=5,
    ),
    TestRequirement(
        id="TEST-001-02",
        name="Leakage Current Test",
        clause="IS 1258:2018 Clause 5.2 [DEMO]",
        method="Measurement under normal and single-fault conditions per IEC 60335",
        parameter="Leakage current (mA)",
        acceptance_criteria="≤ 0.75 mA (normal), ≤ 3.5 mA (single fault)",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=6000,
        estimated_days=3,
    ),
    TestRequirement(
        id="TEST-001-03",
        name="Temperature Rise Test",
        clause="IS 1258:2018 Clause 6.3 (amended) [DEMO]",
        method="Continuous operation at rated input until thermal equilibrium, measure surface temperatures",
        parameter="Surface temperature rise (°C above ambient)",
        acceptance_criteria="≤ 60°C on accessible surfaces, ≤ 75°C on handles",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=10000,
        estimated_days=7,
    ),
    TestRequirement(
        id="TEST-001-04",
        name="Energy Efficiency Test",
        clause="IS 1258:2018 Clause 7.1 [DEMO]",
        method="Standing heat loss measurement per BEE protocol",
        parameter="Standing heat loss (W)",
        acceptance_criteria="Meets BEE 5-star rating threshold for rated capacity",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=12000,
        estimated_days=10,
    ),
    TestRequirement(
        id="TEST-001-05",
        name="Pressure Test",
        clause="IS 1258:2018 Clause 8.1 [DEMO]",
        method="Hydraulic pressure at 1.5x working pressure for 60 minutes",
        parameter="Structural integrity under pressure",
        acceptance_criteria="No leakage, deformation, or failure",
        lab_required=True,
        nabl_accreditation_required=False,
        estimated_cost_inr=5000,
        estimated_days=2,
    ),
]

LABS_PROD_001 = [
    Laboratory(
        id="LAB-001",
        name="NABL Lab A - National Electrical Testing Laboratory [DEMO DATA]",
        city="Delhi",
        state="Delhi",
        nabl_id="NABL-DEMO-TC-1234",
        accreditation_valid_until="2026-12-31",
        tests_covered=["TEST-001-01", "TEST-001-02", "TEST-001-03"],
        contact_email="demo-lab-a@example.com",
        contact_phone="+91-11-XXXX-XXXX",
        estimated_cost_inr=24000,
        estimated_turnaround_days=15,
        website="https://example-nabl-lab-a.com",
        data_label=DEMO_LABEL,
    ),
    Laboratory(
        id="LAB-002",
        name="NABL Lab B - Appliance Test Centre [DEMO DATA]",
        city="Mumbai",
        state="Maharashtra",
        nabl_id="NABL-DEMO-TC-5678",
        accreditation_valid_until="2027-03-31",
        tests_covered=["TEST-001-01", "TEST-001-04"],
        contact_email="demo-lab-b@example.com",
        contact_phone="+91-22-XXXX-XXXX",
        estimated_cost_inr=20000,
        estimated_turnaround_days=12,
        website="https://example-nabl-lab-b.com",
        data_label=DEMO_LABEL,
    ),
    Laboratory(
        id="LAB-003",
        name="NABL Lab C - Materials & Pressure Testing Centre [DEMO DATA]",
        city="Bangalore",
        state="Karnataka",
        nabl_id="NABL-DEMO-TC-9012",
        accreditation_valid_until="2026-09-30",
        tests_covered=["TEST-001-05"],
        contact_email="demo-lab-c@example.com",
        contact_phone="+91-80-XXXX-XXXX",
        estimated_cost_inr=5000,
        estimated_turnaround_days=5,
        website="https://example-nabl-lab-c.com",
        data_label=DEMO_LABEL,
    ),
]

BOM_PROD_001 = [
    BOMComponent(
        id="BOM-001-01",
        name="Heating Element",
        material="Nichrome alloy / sheathed tubular",
        supplier="Demo Supplier A [DEMO]",
        part_number="HE-3KW-230V",
        quantity=1,
        unit="pcs",
        compliance_status=BOMStatus.POTENTIALLY_APPLICABLE,
        applicable_standard="IS 1258:2018 Clause 9 [DEMO] - Heating element specs",
        remarks="May trigger additional sub-component certification. Verify with BIS. [DEMO]",
        action_required="Obtain heating element compliance declaration from supplier.",
    ),
    BOMComponent(
        id="BOM-001-02",
        name="Thermostat",
        material="Bimetallic / electronic",
        supplier="Demo Supplier B [DEMO]",
        part_number="TS-85C-ADJ",
        quantity=1,
        unit="pcs",
        compliance_status=BOMStatus.CONFIRMED_NO_REQUIREMENT,
        applicable_standard=None,
        remarks="No separate IS standard for thermostat in this context. Covered under product-level test. [DEMO]",
        action_required=None,
    ),
    BOMComponent(
        id="BOM-001-03",
        name="Pressure Relief Valve",
        material="Brass",
        supplier="Demo Supplier C [DEMO]",
        part_number="PRV-8BAR",
        quantity=1,
        unit="pcs",
        compliance_status=BOMStatus.NEEDS_VERIFICATION,
        applicable_standard="Possibly IS 3624 [DEMO] - Pressure relief valves",
        remarks="Needs verification whether IS 3624 applies to this sub-component. [DEMO]",
        action_required="Consult BIS or a compliance expert to confirm IS 3624 applicability.",
    ),
    BOMComponent(
        id="BOM-001-04",
        name="Tank Body",
        material="SS 304 Stainless Steel",
        supplier="Demo Supplier D [DEMO]",
        part_number="TANK-25L-SS304",
        quantity=1,
        unit="pcs",
        compliance_status=BOMStatus.CONFIRMED_NO_REQUIREMENT,
        applicable_standard=None,
        remarks="Raw stainless steel body - no separate certification required. Covered at product level. [DEMO]",
        action_required=None,
    ),
    BOMComponent(
        id="BOM-001-05",
        name="Electrical Cable",
        material="PVC insulated copper conductor",
        supplier="Demo Supplier E [DEMO]",
        part_number="CABLE-3C-1.5SQ",
        quantity=1.5,
        unit="meters",
        compliance_status=BOMStatus.POTENTIALLY_APPLICABLE,
        applicable_standard="IS 694 [DEMO] - PVC insulated cables",
        remarks="Power supply cable may need to comply with IS 694. Check if ISI-marked cable is used. [DEMO]",
        action_required="Confirm power cable is sourced from BIS ISI-licensed manufacturer.",
    ),
    BOMComponent(
        id="BOM-001-06",
        name="Insulation Foam",
        material="Polyurethane foam",
        supplier="Demo Supplier F [DEMO]",
        part_number="PU-FOAM-50MM",
        quantity=2,
        unit="kg",
        compliance_status=BOMStatus.NO_REQUIREMENT_IDENTIFIED,
        applicable_standard=None,
        remarks="No specific IS standard identified for PU insulation foam in this product context. [DEMO]",
        action_required=None,
    ),
]

DOCUMENTS_PROD_001 = [
    Document(
        id="DOC-001-01",
        name="Test Report - Electrical Safety & Leakage Current",
        type="test_report",
        status=DocumentStatus.PARTIAL,
        file_name="test_report_elec_safety_v1.pdf",
        uploaded_at="2026-08-15",
        valid_until="2027-08-15",
        issuing_body="NABL Lab A [DEMO]",
        remarks="Report covers Electrical Safety and Leakage Current. Temperature Rise section is MISSING. [DEMO]",
        gaps=["Temperature Rise Test (Clause 6.3) section absent", "Amendment 1 limits not referenced"],
    ),
    Document(
        id="DOC-001-02",
        name="Product Specification Sheet",
        type="specification",
        status=DocumentStatus.VALID,
        file_name="product_spec_sheet_geyser_25L.pdf",
        uploaded_at="2026-07-01",
        valid_until=None,
        issuing_body="Manufacturer [DEMO]",
        remarks="Complete specification sheet uploaded. [DEMO]",
        gaps=[],
    ),
    Document(
        id="DOC-001-03",
        name="BIS Certification Application",
        type="application",
        status=DocumentStatus.MISSING,
        file_name=None,
        uploaded_at=None,
        valid_until=None,
        issuing_body="BIS [DEMO]",
        remarks="Application not yet filed. Required for ISI Mark licence. [DEMO]",
        gaps=["Complete application not submitted", "Prerequisite test reports incomplete"],
    ),
    Document(
        id="DOC-001-04",
        name="Pressure Test Certificate",
        type="test_report",
        status=DocumentStatus.VALID,
        file_name="pressure_test_cert.pdf",
        uploaded_at="2026-08-20",
        valid_until="2027-08-20",
        issuing_body="NABL Lab C [DEMO]",
        remarks="Hydraulic pressure test passed at 10.5 bar. [DEMO]",
        gaps=[],
    ),
]

EVIDENCE_GAPS_PROD_001 = [
    Evidence(
        requirement_id="REQ-001-03",
        requirement_name="Temperature Rise Test",
        evidence_type="test_report",
        status=RequirementStatus.MISSING,
        document_id=None,
        document_name=None,
        gap_description=(
            "Temperature Rise Test report is missing. The existing test report (DOC-001-01) "
            "does not include this section. IS 1258:2018 Amendment 1 updated the temperature "
            "limits, requiring a fresh test. [DEMO DATA]"
        ),
        action_required="Schedule Temperature Rise Test at NABL Lab A or Lab B. Estimated cost: ₹10,000. Estimated time: 7 days.",
    ),
    Evidence(
        requirement_id="REQ-001-04",
        requirement_name="Energy Efficiency Test",
        evidence_type="test_report",
        status=RequirementStatus.MISSING,
        document_id=None,
        document_name=None,
        gap_description=(
            "Energy Efficiency (Standing Heat Loss) test report has not been uploaded. "
            "This is mandatory under IS 1258:2018 Clause 7.1. [DEMO DATA]"
        ),
        action_required="Schedule Energy Efficiency Test at NABL Lab A or Lab B. Estimated cost: ₹12,000. Estimated time: 10 days.",
    ),
    Evidence(
        requirement_id="REQ-001-07",
        requirement_name="BIS Certification (ISI Mark)",
        evidence_type="certificate",
        status=RequirementStatus.MISSING,
        document_id=None,
        document_name=None,
        gap_description=(
            "BIS ISI Mark licence application has not been submitted. "
            "The product falls under mandatory QCO coverage and cannot be sold without an ISI Mark. [DEMO DATA]"
        ),
        action_required="File BIS ISI Mark application via BIS CMS portal after completing all test reports.",
    ),
]

CHANGE_EVENTS_PROD_001 = [
    ChangeEvent(
        id="CE-001-01",
        event_type=ChangeEventType.AMENDMENT,
        title="[DEMO] IS 1258 Amendment 1 - Updated Temperature Rating Requirements",
        description=(
            "IS 1258:2018 Amendment 1 (2022) revises the temperature rise limits for "
            "accessible surfaces and introduces new test conditions for thermostatic control. "
            "Products tested before this amendment may need re-testing. [DEMO DATA - not a real notice]"
        ),
        standard_affected="IS 1258:2018",
        effective_date="2022-06-01",
        impact_level="HIGH",
        action_required="Re-test product for temperature rise under amended clause 6.3 limits.",
        source_url="https://www.bis.gov.in/",  # Demo URL only
        data_label=DEMO_LABEL,
    ),
    ChangeEvent(
        id="CE-001-02",
        event_type=ChangeEventType.QCO_UPDATE,
        title="[DEMO] QCO Extension - Electric Appliances Coverage Expanded",
        description=(
            "The Electric and Electronic Appliances QCO has been extended to cover "
            "additional product sub-categories including instantaneous water heaters. "
            "Storage water heaters already covered - no new action required. [DEMO DATA]"
        ),
        standard_affected="QCO-001",
        effective_date="2024-01-01",
        impact_level="LOW",
        action_required="No action required. Product was already covered under existing QCO.",
        source_url="https://www.bis.gov.in/",
        data_label=DEMO_LABEL,
    ),
]

PRODUCT_001 = Product(
    id="DEMO-PROD-001",
    name="Electric Storage Water Heater (25L) [DEMO PRODUCT]",
    description=(
        "25-litre electric storage water heater (geyser) rated at 2000W, 230V AC, "
        "with thermostat, pressure relief valve, and SS304 inner tank. "
        "Intended for domestic household use. [DEMO DATA]"
    ),
    category=ProductCategory.ELECTRICAL,
    hs_code="8419.19",
    manufacturer="Demo Manufacturer Pvt. Ltd. [DEMO]",
    model_number="WH-25L-2KW-DEMO",
    attributes=[
        ProductAttribute(name="Capacity", value="25", unit="Litres", confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Rated Power", value="2000", unit="W", confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Rated Voltage", value="230", unit="V AC", confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Working Pressure", value="7", unit="bar", confidence=0.9, source="extracted"),
        ProductAttribute(name="Tank Material", value="SS 304 Stainless Steel", unit=None, confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Thermostat Setting", value="35-75", unit="°C", confidence=0.9, source="extracted"),
        ProductAttribute(name="IP Rating", value="IP25", unit=None, confidence=0.8, source="extracted"),
        ProductAttribute(name="Usage", value="Domestic", unit=None, confidence=1.0, source="user_confirmed"),
    ],
    applicable_standards=STANDARDS_PROD_001,
    applicable_qcos=QCOS_PROD_001,
    requirements=REQUIREMENTS_PROD_001,
    tests=TESTS_PROD_001,
    laboratories=LABS_PROD_001,
    bom_components=BOM_PROD_001,
    documents=DOCUMENTS_PROD_001,
    evidence_gaps=EVIDENCE_GAPS_PROD_001,
    change_events=CHANGE_EVENTS_PROD_001,
    compliance_score=52.0,  # 4 of 8 requirements met, weighted
    overall_status="PARTIAL",
    created_at="2026-07-01T10:00:00",
    updated_at="2026-09-30T00:00:00",
    data_label=DEMO_LABEL,
)


# ===========================================================================
# PRODUCT 2: Plastic Toy (Basic)
# ===========================================================================

STANDARDS_PROD_002 = [
    Standard(
        id="STD-002",
        title="Safety of Toys - Specification [DEMO DATA]",
        number="IS 9873-1:2019",
        year=2019,
        status="ACTIVE",
        scope="Safety requirements for toys intended for use by children under 14 years. [DEMO DATA]",
        amendment=None,
        bis_catalog_url="https://www.bis.gov.in/",
        data_label=DEMO_LABEL,
    ),
    Standard(
        id="STD-002B",
        title="Safety of Toys - Chemical Properties [DEMO DATA]",
        number="IS 9873-3:2017",
        year=2017,
        status="ACTIVE",
        scope="Chemical safety requirements for toys - limits for hazardous elements. [DEMO DATA]",
        amendment=None,
        bis_catalog_url="https://www.bis.gov.in/",
        data_label=DEMO_LABEL,
    ),
]

QCOS_PROD_002 = [
    QCO(
        id="QCO-002",
        title="Toys (Quality Control) Order 2020 [DEMO DATA]",
        notification_number="SO 896(E) [DEMO]",
        effective_date="2021-01-01",
        ministry="Ministry of Commerce & Industry [DEMO]",
        product_categories=["Plastic Toys", "Soft Toys", "Electronic Toys", "Board Games"],
        mandatory_certification=True,
        data_label=DEMO_LABEL,
    )
]

REQUIREMENTS_PROD_002 = [
    Requirement(
        id="REQ-002-01",
        name="Mechanical Safety",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 9873-1:2019 Clause 4 [DEMO]",
        description="No sharp edges, no small parts for children under 3 years, structural integrity. [DEMO DATA]",
        test_required=True,
        test_id="TEST-002-01",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Mechanical safety tests passed. [DEMO]",
    ),
    Requirement(
        id="REQ-002-02",
        name="Chemical Safety - Heavy Metals",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 9873-3:2017 Clause 5 [DEMO]",
        description="Limits for Pb, Cd, Cr(VI), Hg, Ba, Sb, As, Se in accessible materials. [DEMO DATA]",
        test_required=True,
        test_id="TEST-002-02",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Chemical analysis report uploaded. All elements within limits. [DEMO]",
    ),
    Requirement(
        id="REQ-002-03",
        name="Flammability",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 9873-1:2019 Clause 7 [DEMO]",
        description="Materials shall not catch fire or, if they do, burn only slowly. [DEMO DATA]",
        test_required=True,
        test_id="TEST-002-03",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Flammability test passed. Burn rate within acceptable limits. [DEMO]",
    ),
    Requirement(
        id="REQ-002-04",
        name="BIS ISI Mark Certification",
        category="Certification",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 9873-1:2019 + QCO-002 [DEMO]",
        description="Valid BIS ISI Mark licence required under Toys QCO. [DEMO DATA]",
        test_required=False,
        evidence_type="certificate",
        evidence_status="UPLOADED",
        remarks="BIS licence obtained. Valid until 2027-06-30. [DEMO]",
    ),
]

TESTS_PROD_002 = [
    TestRequirement(
        id="TEST-002-01",
        name="Mechanical & Physical Safety Test",
        clause="IS 9873-1:2019 Clause 4 [DEMO]",
        method="Drop test, bite test, small parts cylinder test, torque test",
        parameter="Structural integrity, sharp edges, small parts",
        acceptance_criteria="No sharp edges; no small parts for <3yr toys; no breakage under load",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=15000,
        estimated_days=7,
    ),
    TestRequirement(
        id="TEST-002-02",
        name="Chemical Analysis - Heavy Metals",
        clause="IS 9873-3:2017 Clause 5 [DEMO]",
        method="ICP-OES / XRF analysis for heavy metals in accessible materials",
        parameter="Heavy metal content (mg/kg)",
        acceptance_criteria="Pb ≤ 90 mg/kg, Cd ≤ 75 mg/kg, Hg ≤ 60 mg/kg (as per IS limits)",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=20000,
        estimated_days=10,
    ),
    TestRequirement(
        id="TEST-002-03",
        name="Flammability Test",
        clause="IS 9873-1:2019 Clause 7 [DEMO]",
        method="Flame application test on fabric and soft materials",
        parameter="Burn rate (mm/s)",
        acceptance_criteria="Surface burn rate ≤ 30 mm/s for fabric; materials shall not ignite readily",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=8000,
        estimated_days=5,
    ),
]

LABS_PROD_002 = [
    Laboratory(
        id="LAB-004",
        name="NABL Lab D - Toy Safety Testing Centre [DEMO DATA]",
        city="Chennai",
        state="Tamil Nadu",
        nabl_id="NABL-DEMO-TC-3456",
        accreditation_valid_until="2027-06-30",
        tests_covered=["TEST-002-01", "TEST-002-02", "TEST-002-03"],
        contact_email="demo-lab-d@example.com",
        contact_phone="+91-44-XXXX-XXXX",
        estimated_cost_inr=43000,
        estimated_turnaround_days=15,
        website="https://example-nabl-lab-d.com",
        data_label=DEMO_LABEL,
    ),
]

PRODUCT_002 = Product(
    id="DEMO-PROD-002",
    name="Plastic Toy - Building Blocks Set (Age 3+) [DEMO PRODUCT]",
    description=(
        "Set of 100 ABS plastic building blocks for children aged 3 and above. "
        "No electronic components. No small parts intended for children under 3. [DEMO DATA]"
    ),
    category=ProductCategory.TOY,
    hs_code="9503.00",
    manufacturer="Demo Toy Maker Pvt. Ltd. [DEMO]",
    model_number="TOY-BB-100-DEMO",
    attributes=[
        ProductAttribute(name="Target Age", value="3+", unit="years", confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Material", value="ABS Plastic", unit=None, confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Piece Count", value="100", unit="pcs", confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Electronic Components", value="None", unit=None, confidence=1.0, source="user_confirmed"),
    ],
    applicable_standards=STANDARDS_PROD_002,
    applicable_qcos=QCOS_PROD_002,
    requirements=REQUIREMENTS_PROD_002,
    tests=TESTS_PROD_002,
    laboratories=LABS_PROD_002,
    bom_components=[
        BOMComponent(
            id="BOM-002-01",
            name="ABS Plastic Granules",
            material="Acrylonitrile Butadiene Styrene",
            supplier="Demo Polymer Supplier [DEMO]",
            part_number="ABS-NATURAL-FG",
            quantity=2.5,
            unit="kg",
            compliance_status=BOMStatus.CONFIRMED_NO_REQUIREMENT,
            applicable_standard=None,
            remarks="Food-grade ABS, no separate IS requirement at component level. [DEMO]",
        ),
        BOMComponent(
            id="BOM-002-02",
            name="Packaging Box (Cardboard)",
            material="Recycled cardboard",
            supplier="Demo Packaging Co. [DEMO]",
            part_number="PKG-BOX-STD",
            quantity=1,
            unit="pcs",
            compliance_status=BOMStatus.NO_REQUIREMENT_IDENTIFIED,
            applicable_standard=None,
            remarks="Standard packaging. No IS standard identified. [DEMO]",
        ),
    ],
    documents=[
        Document(
            id="DOC-002-01",
            name="Full Test Report - Toy Safety",
            type="test_report",
            status=DocumentStatus.VALID,
            file_name="toy_safety_test_report_v2.pdf",
            uploaded_at="2026-05-10",
            valid_until="2028-05-10",
            issuing_body="NABL Lab D [DEMO]",
            remarks="Complete test report covering all three test areas. [DEMO]",
            gaps=[],
        ),
        Document(
            id="DOC-002-02",
            name="BIS ISI Mark Licence Certificate",
            type="certificate",
            status=DocumentStatus.VALID,
            file_name="bis_isi_licence_toy_demo.pdf",
            uploaded_at="2026-06-15",
            valid_until="2027-06-30",
            issuing_body="Bureau of Indian Standards [DEMO]",
            remarks="ISI Mark licence valid. [DEMO]",
            gaps=[],
        ),
    ],
    evidence_gaps=[],
    change_events=[
        ChangeEvent(
            id="CE-002-01",
            event_type=ChangeEventType.CLARIFICATION,
            title="[DEMO] Clarification on Toys QCO Self-Certification",
            description=(
                "MoCI issued a clarification on documentation requirements for "
                "ISI Mark licence renewal for toy manufacturers. No change to testing requirements. [DEMO DATA]"
            ),
            standard_affected="QCO-002",
            effective_date="2025-03-01",
            impact_level="LOW",
            action_required="Review renewal documentation checklist before next licence renewal.",
            source_url="https://www.bis.gov.in/",
            data_label=DEMO_LABEL,
        ),
    ],
    compliance_score=95.0,
    overall_status="COMPLIANT",
    created_at="2026-05-01T10:00:00",
    updated_at="2026-09-30T00:00:00",
    data_label=DEMO_LABEL,
)


# ===========================================================================
# PRODUCT 3: Industrial Safety Helmet
# ===========================================================================

STANDARDS_PROD_003 = [
    Standard(
        id="STD-003",
        title="Industrial Safety Helmets - Specification [DEMO DATA]",
        number="IS 2925:1984",
        year=1984,
        status="ACTIVE",
        scope="Specification for industrial safety helmets for protection of head from impact, penetration and electric shock. [DEMO DATA]",
        amendment="Amendment 2 (2005)",
        bis_catalog_url="https://www.bis.gov.in/",
        data_label=DEMO_LABEL,
    )
]

QCOS_PROD_003 = [
    QCO(
        id="QCO-003",
        title="Personal Protective Equipment Quality Control Order [DEMO DATA]",
        notification_number="SO 1748(E) [DEMO]",
        effective_date="2022-07-01",
        ministry="Ministry of Labour & Employment [DEMO]",
        product_categories=["Safety Helmets", "Safety Footwear", "Safety Harnesses", "Gloves"],
        mandatory_certification=True,
        data_label=DEMO_LABEL,
    )
]

REQUIREMENTS_PROD_003 = [
    Requirement(
        id="REQ-003-01",
        name="Impact Resistance",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 2925:1984 Clause 4.3 [DEMO]",
        description="Helmet shall transmit not more than 5 kN peak force during impact test. [DEMO DATA]",
        test_required=True,
        test_id="TEST-003-01",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="Impact resistance test passed. Peak force 3.8 kN. [DEMO]",
    ),
    Requirement(
        id="REQ-003-02",
        name="Penetration Resistance",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MET,
        standard_ref="IS 2925:1984 Clause 4.4 [DEMO]",
        description="A steel striker dropped from 1 m shall not penetrate the helmet shell. [DEMO DATA]",
        test_required=True,
        test_id="TEST-003-02",
        evidence_type="test_report",
        evidence_status="UPLOADED",
        remarks="No penetration observed. Test passed. [DEMO]",
    ),
    Requirement(
        id="REQ-003-03",
        name="Retention System Strength",
        category="Safety",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MISSING,
        standard_ref="IS 2925:1984 Clause 4.6 [DEMO]",
        description="Chin strap and retention system shall withstand 50 N load without failure. [DEMO DATA]",
        test_required=True,
        test_id="TEST-003-03",
        evidence_type="test_report",
        evidence_status="MISSING",
        remarks="Retention system test report not uploaded. CRITICAL GAP. [DEMO]",
    ),
    Requirement(
        id="REQ-003-04",
        name="Electrical Insulation",
        category="Safety",
        type=RequirementType.CONDITIONAL,
        status=RequirementStatus.NOT_APPLICABLE,
        standard_ref="IS 2925:1984 Clause 4.7 [DEMO]",
        description="Class E helmets only: withstand 20 kV AC for 3 minutes. [DEMO DATA]",
        test_required=False,
        evidence_type="declaration",
        evidence_status="UPLOADED",
        remarks="Product is Class G (General). Electrical insulation test not applicable. [DEMO]",
    ),
    Requirement(
        id="REQ-003-05",
        name="BIS ISI Mark Certification",
        category="Certification",
        type=RequirementType.MANDATORY,
        status=RequirementStatus.MISSING,
        standard_ref="IS 2925:1984 + QCO-003 [DEMO]",
        description="Mandatory BIS ISI Mark licence under PPE QCO. [DEMO DATA]",
        test_required=False,
        evidence_type="certificate",
        evidence_status="MISSING",
        remarks="BIS application not submitted. Retention system test must be completed first. [DEMO]",
    ),
]

TESTS_PROD_003 = [
    TestRequirement(
        id="TEST-003-01",
        name="Impact Attenuation Test",
        clause="IS 2925:1984 Clause 4.3 [DEMO]",
        method="Drop 5 kg striker from specified height onto conditioned helmet on headform",
        parameter="Peak force transmitted (kN)",
        acceptance_criteria="Peak force ≤ 5 kN",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=7000,
        estimated_days=4,
    ),
    TestRequirement(
        id="TEST-003-02",
        name="Penetration Resistance Test",
        clause="IS 2925:1984 Clause 4.4 [DEMO]",
        method="Drop steel cone striker from 1 metre onto shell",
        parameter="Penetration depth",
        acceptance_criteria="No penetration through shell",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=5000,
        estimated_days=3,
    ),
    TestRequirement(
        id="TEST-003-03",
        name="Retention System Test",
        clause="IS 2925:1984 Clause 4.6 [DEMO]",
        method="Apply 50 N dynamic load on chin strap for 30 seconds",
        parameter="Strap elongation and failure",
        acceptance_criteria="No failure; elongation ≤ 25 mm",
        lab_required=True,
        nabl_accreditation_required=True,
        estimated_cost_inr=4000,
        estimated_days=2,
    ),
]

LABS_PROD_003 = [
    Laboratory(
        id="LAB-005",
        name="NABL Lab E - PPE & Safety Equipment Testing [DEMO DATA]",
        city="Pune",
        state="Maharashtra",
        nabl_id="NABL-DEMO-TC-7890",
        accreditation_valid_until="2027-12-31",
        tests_covered=["TEST-003-01", "TEST-003-02", "TEST-003-03"],
        contact_email="demo-lab-e@example.com",
        contact_phone="+91-20-XXXX-XXXX",
        estimated_cost_inr=16000,
        estimated_turnaround_days=10,
        website="https://example-nabl-lab-e.com",
        data_label=DEMO_LABEL,
    ),
]

PRODUCT_003 = Product(
    id="DEMO-PROD-003",
    name="Industrial Safety Helmet - Class G [DEMO PRODUCT]",
    description=(
        "Hard hat / industrial safety helmet, Class G (General use), "
        "high-density polyethylene shell with 6-point suspension. "
        "For construction and industrial applications. [DEMO DATA]"
    ),
    category=ProductCategory.SAFETY_EQUIPMENT,
    hs_code="6506.10",
    manufacturer="Demo Safety Gear Pvt. Ltd. [DEMO]",
    model_number="HELM-G-HDPE-DEMO",
    attributes=[
        ProductAttribute(name="Class", value="G (General)", unit=None, confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Shell Material", value="HDPE", unit=None, confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Suspension Points", value="6", unit=None, confidence=1.0, source="extracted"),
        ProductAttribute(name="Weight", value="380", unit="grams", confidence=0.9, source="extracted"),
        ProductAttribute(name="Color", value="Yellow", unit=None, confidence=1.0, source="user_confirmed"),
        ProductAttribute(name="Application", value="Construction / Industrial", unit=None, confidence=1.0, source="user_confirmed"),
    ],
    applicable_standards=STANDARDS_PROD_003,
    applicable_qcos=QCOS_PROD_003,
    requirements=REQUIREMENTS_PROD_003,
    tests=TESTS_PROD_003,
    laboratories=LABS_PROD_003,
    bom_components=[
        BOMComponent(
            id="BOM-003-01",
            name="HDPE Shell",
            material="High-Density Polyethylene",
            supplier="Demo Polymer Co. [DEMO]",
            part_number="HDPE-SHELL-YLW",
            quantity=1,
            unit="pcs",
            compliance_status=BOMStatus.CONFIRMED_NO_REQUIREMENT,
            applicable_standard=None,
            remarks="HDPE material - no separate IS requirement at component level. [DEMO]",
        ),
        BOMComponent(
            id="BOM-003-02",
            name="6-Point Suspension Harness",
            material="Nylon webbing / plastic",
            supplier="Demo Harness Supplier [DEMO]",
            part_number="SUSP-6PT-NYLON",
            quantity=1,
            unit="pcs",
            compliance_status=BOMStatus.POTENTIALLY_APPLICABLE,
            applicable_standard="IS 2925:1984 Clause 4.5 [DEMO] - Harness requirements",
            remarks="Harness is a critical safety component. Ensure it meets dimensional requirements of IS 2925. [DEMO]",
            action_required="Verify harness compliance with IS 2925:1984 Clause 4.5 dimensional specs.",
        ),
        BOMComponent(
            id="BOM-003-03",
            name="Chin Strap",
            material="Nylon",
            supplier="Demo Harness Supplier [DEMO]",
            part_number="STRAP-CHIN-NYLON",
            quantity=1,
            unit="pcs",
            compliance_status=BOMStatus.NEEDS_VERIFICATION,
            applicable_standard="IS 2925:1984 Clause 4.6 [DEMO]",
            remarks="Chin strap is part of the retention system - needs to be validated as part of retention test. [DEMO]",
            action_required="Include chin strap in retention system test (TEST-003-03).",
        ),
    ],
    documents=[
        Document(
            id="DOC-003-01",
            name="Impact & Penetration Test Report",
            type="test_report",
            status=DocumentStatus.VALID,
            file_name="helmet_impact_pen_test.pdf",
            uploaded_at="2026-06-01",
            valid_until="2028-06-01",
            issuing_body="NABL Lab E [DEMO]",
            remarks="Impact and penetration tests passed. [DEMO]",
            gaps=[],
        ),
        Document(
            id="DOC-003-02",
            name="Retention System Test Report",
            type="test_report",
            status=DocumentStatus.MISSING,
            file_name=None,
            uploaded_at=None,
            valid_until=None,
            issuing_body=None,
            remarks="Not yet performed. Required for BIS certification application. [DEMO]",
            gaps=["Retention system test not conducted"],
        ),
    ],
    evidence_gaps=[
        Evidence(
            requirement_id="REQ-003-03",
            requirement_name="Retention System Strength",
            evidence_type="test_report",
            status=RequirementStatus.MISSING,
            document_id=None,
            document_name=None,
            gap_description=(
                "Retention system (chin strap) strength test has not been conducted. "
                "IS 2925:1984 Clause 4.6 mandates this test. [DEMO DATA]"
            ),
            action_required="Schedule Retention System Test at NABL Lab E. Est. cost ₹4,000. Est. time 2 days.",
        ),
        Evidence(
            requirement_id="REQ-003-05",
            requirement_name="BIS ISI Mark Certification",
            evidence_type="certificate",
            status=RequirementStatus.MISSING,
            document_id=None,
            document_name=None,
            gap_description=(
                "BIS ISI Mark licence application cannot be submitted until Retention System Test is completed. [DEMO DATA]"
            ),
            action_required="Complete Retention System Test first, then file BIS ISI Mark application via CMS portal.",
        ),
    ],
    change_events=[
        ChangeEvent(
            id="CE-003-01",
            event_type=ChangeEventType.NEW_STANDARD,
            title="[DEMO] New IS 2925 Revision Under Development",
            description=(
                "BIS is reportedly working on a revision of IS 2925 to align with EN 397:2012+A1:2012 "
                "for improved impact attenuation testing. The revision is in draft stage. "
                "No effective date confirmed. [DEMO DATA - not a real notice]"
            ),
            standard_affected="IS 2925:1984",
            effective_date="TBD",
            impact_level="MEDIUM",
            action_required="Monitor BIS website for revised IS 2925 publication. Plan re-testing when finalized.",
            source_url="https://www.bis.gov.in/",
            data_label=DEMO_LABEL,
        ),
    ],
    compliance_score=55.0,
    overall_status="PARTIAL",
    created_at="2026-06-01T10:00:00",
    updated_at="2026-09-30T00:00:00",
    data_label=DEMO_LABEL,
)


# ===========================================================================
# In-Memory Product Store
# ===========================================================================

PRODUCTS_DB: dict[str, Product] = {
    "DEMO-PROD-001": PRODUCT_001,
    "DEMO-PROD-002": PRODUCT_002,
    "DEMO-PROD-003": PRODUCT_003,
}


# ===========================================================================
# BIS Services (Demo)
# ===========================================================================

BIS_SERVICES = [
    {
        "id": "SVC-001",
        "name": "ISI Mark Certification",
        "description": "Mandatory certification for products covered under QCOs and voluntary for others under IS standards. Grants the right to use the ISI Mark. [DEMO DATA]",
        "url": "https://www.bis.gov.in/",
        "category": "Certification",
        "applicable_to": ["Electrical Appliances", "Toys", "PPE", "Building Materials", "Food Products"],
        "data_label": DEMO_LABEL,
    },
    {
        "id": "SVC-002",
        "name": "BIS CRS (Compulsory Registration Scheme)",
        "description": "Self-declaration based registration for electronics and IT products. Manufacturer tests product at BIS-recognised lab and registers. [DEMO DATA]",
        "url": "https://www.bis.gov.in/",
        "category": "Registration",
        "applicable_to": ["Electronics", "IT Equipment", "Lighting", "Batteries"],
        "data_label": DEMO_LABEL,
    },
    {
        "id": "SVC-003",
        "name": "Hallmarking (Gold & Silver)",
        "description": "BIS hallmarking for gold and silver jewellery ensuring purity. Mandatory for gold jewellery under BIS Hallmarking Order 2000. [DEMO DATA]",
        "url": "https://www.bis.gov.in/",
        "category": "Hallmarking",
        "applicable_to": ["Gold Jewellery", "Silver Jewellery", "Precious Metal Articles"],
        "data_label": DEMO_LABEL,
    },
    {
        "id": "SVC-004",
        "name": "Foreign Manufacturers Certification Scheme (FMCS)",
        "description": "Certification for foreign manufacturers wishing to use the ISI Mark in India. [DEMO DATA]",
        "url": "https://www.bis.gov.in/",
        "category": "Certification",
        "applicable_to": ["Import Products", "Foreign Manufactured Goods"],
        "data_label": DEMO_LABEL,
    },
    {
        "id": "SVC-005",
        "name": "Eco Mark Certification",
        "description": "Voluntary eco-labelling scheme for environmentally friendly products. [DEMO DATA]",
        "url": "https://www.bis.gov.in/",
        "category": "Eco Label",
        "applicable_to": ["Consumer Products", "Industrial Products"],
        "data_label": DEMO_LABEL,
    },
]


# ===========================================================================
# Regulatory Updates (Demo)
# ===========================================================================

REGULATORY_UPDATES = [
    {
        "id": "UPD-001",
        "title": "[DEMO] Toys QCO - Extended to Additional Categories",
        "summary": "Ministry of Commerce & Industry has expanded the Toys QCO to include additional toy sub-categories. Manufacturers of affected products must obtain ISI Mark licence. [DEMO DATA - not a real notification]",
        "ministry": "Ministry of Commerce & Industry [DEMO]",
        "date": "2026-08-15",
        "impact": "HIGH",
        "categories_affected": ["Toys", "Hobby Items", "Craft Sets"],
        "source_url": "https://www.bis.gov.in/",
        "data_label": DEMO_LABEL,
    },
    {
        "id": "UPD-002",
        "title": "[DEMO] IS 1258 Amendment 1 - Temperature Rise Limits Revised",
        "summary": "IS 1258:2018 Amendment 1 revises temperature rise limits for electric storage water heaters. Products tested before amendment must be re-tested. [DEMO DATA]",
        "ministry": "Bureau of Indian Standards [DEMO]",
        "date": "2022-06-01",
        "impact": "HIGH",
        "categories_affected": ["Electric Water Heaters", "Geysers", "Immersion Heaters"],
        "source_url": "https://www.bis.gov.in/",
        "data_label": DEMO_LABEL,
    },
    {
        "id": "UPD-003",
        "title": "[DEMO] PPE QCO - Compliance Deadline Reminder",
        "summary": "The PPE Quality Control Order covering Safety Helmets, Safety Footwear and Harnesses requires all manufacturers to hold BIS ISI Mark licence. Deadline for compliance passed in 2022. Non-compliant products are liable for seizure. [DEMO DATA]",
        "ministry": "Ministry of Labour & Employment [DEMO]",
        "date": "2022-07-01",
        "impact": "HIGH",
        "categories_affected": ["Safety Helmets", "Safety Footwear", "Safety Harnesses"],
        "source_url": "https://www.bis.gov.in/",
        "data_label": DEMO_LABEL,
    },
    {
        "id": "UPD-004",
        "title": "[DEMO] BIS CRS - New Electronic Products Added",
        "summary": "BIS has added new product categories to the Compulsory Registration Scheme for electronics, including certain IoT devices and wearables. [DEMO DATA]",
        "ministry": "Ministry of Electronics & IT [DEMO]",
        "date": "2026-07-01",
        "impact": "MEDIUM",
        "categories_affected": ["IoT Devices", "Wearables", "Smart Appliances"],
        "source_url": "https://www.bis.gov.in/",
        "data_label": DEMO_LABEL,
    },
    {
        "id": "UPD-005",
        "title": "[DEMO] Reduced BIS Licence Fees for MSMEs",
        "summary": "BIS has announced reduced application and surveillance fees for MSME-certified manufacturers across all product categories. [DEMO DATA]",
        "ministry": "Bureau of Indian Standards [DEMO]",
        "date": "2026-06-15",
        "impact": "LOW",
        "categories_affected": ["All Certified Products"],
        "source_url": "https://www.bis.gov.in/",
        "data_label": DEMO_LABEL,
    },
]


# ===========================================================================
# Demo Standards Catalog (for search)
# ===========================================================================

STANDARDS_CATALOG = [
    {"id": "CAT-001", "number": "IS 1258:2018", "title": "Electric Storage Water Heaters - Specification", "year": 2018, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-002", "number": "IS 9873-1:2019", "title": "Safety of Toys - Part 1: Safety Aspects Related to Mechanical and Physical Properties", "year": 2019, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-003", "number": "IS 9873-3:2017", "title": "Safety of Toys - Part 3: Migration of Certain Elements", "year": 2017, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-004", "number": "IS 2925:1984", "title": "Industrial Safety Helmets - Specification", "year": 1984, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-005", "number": "IS 302-2-3:2008", "title": "Safety of Household and Similar Electrical Appliances", "year": 2008, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-006", "number": "IS 694:2010", "title": "PVC Insulated Cables for Working Voltages up to and including 1100 V", "year": 2010, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-007", "number": "IS 3624:1987", "title": "Pressure Gauges and Vacuum Gauges - Specification", "year": 1987, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-008", "number": "IS 616:2017", "title": "Safety Requirements for Mains Operated Electronic and Related Apparatus", "year": 2017, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-009", "number": "IS 13252-1:2010", "title": "Information Technology Equipment - Safety", "year": 2010, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-010", "number": "IS 15885-2-1:2012", "title": "Safety of LED Luminaires", "year": 2012, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-011", "number": "IS 1647:2014", "title": "Code of Practice for Fire Safety of Buildings", "year": 2014, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-012", "number": "IS 4456:2012", "title": "Safety Footwear - Specification", "year": 2012, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-013", "number": "IS 15140:2002", "title": "Personal Protective Equipment - Safety Harnesses", "year": 2002, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-014", "number": "IS 1179:1967", "title": "Equipment for Eye and Face Protection During Welding Operations", "year": 1967, "status": "ACTIVE", "data_label": DEMO_LABEL},
    {"id": "CAT-015", "number": "IS 7328:2013", "title": "High Density Polyethylene Pipes - Specification", "year": 2013, "status": "ACTIVE", "data_label": DEMO_LABEL},
]
