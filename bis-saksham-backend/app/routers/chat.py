"""
BIS SAKSHAM - Chat Router
Contextual AI assistant with canned intelligent responses.
[DEMO DATA] - All responses are clearly labeled as demo data.
"""

from fastapi import APIRouter
from app.models import ChatRequest, ChatResponse
from app.seed_data import DEMO_LABEL, PRODUCTS_DB

router = APIRouter(prefix="/api/chat", tags=["Chat Assistant"])

# ---------------------------------------------------------------------------
# Response library: (keyword_triggers, response_text, suggestions, related_reqs)
# ---------------------------------------------------------------------------

RESPONSE_LIBRARY = [
    # BIS Certification
    (
        ["bis certification", "isi mark", "how to certify", "how do i get certified", "get isi", "apply for isi"],
        (
            "To obtain BIS ISI Mark certification, you need to:\n\n"
            "1. **Identify the applicable IS standard** for your product.\n"
            "2. **Get your product tested** at an NABL-accredited lab recognised by BIS.\n"
            "3. **Apply online** via the BIS Customer Management System (CMS) portal at https://www.bis.gov.in/\n"
            "4. **Submit test reports**, product drawings, manufacturing process details, and fees.\n"
            "5. **BIS inspection** of your manufacturing facility.\n"
            "6. **Grant of licence** and right to use ISI Mark.\n\n"
            "[DEMO DATA - Please verify current procedures on the BIS website]"
        ),
        ["What documents do I need for BIS certification?", "How long does BIS certification take?", "What is the BIS CMS portal?"],
        ["REQ-001-07", "REQ-002-04"],
    ),
    # QCO
    (
        ["qco", "quality control order", "mandatory", "compulsory", "is it mandatory"],
        (
            "A Quality Control Order (QCO) is issued by the Government of India under the Bureau of Indian Standards Act, 2016. "
            "Products covered by a QCO **cannot be manufactured, stored, or sold in India without BIS certification**.\n\n"
            "Key points:\n"
            "- QCOs are issued by different ministries (e.g., MoHI for appliances, MoCI for toys).\n"
            "- Non-compliance can result in product seizure, fines, and criminal liability.\n"
            "- Check the BIS website for the latest list of products under mandatory certification.\n\n"
            "[DEMO DATA]"
        ),
        ["Which products are covered under QCO?", "What are the penalties for QCO non-compliance?", "How do I find if my product has a QCO?"],
        [],
    ),
    # Temperature rise
    (
        ["temperature rise", "temperature test", "thermal test", "clause 6.3"],
        (
            "For the **Temperature Rise Test** under IS 1258:2018 Clause 6.3 [DEMO]:\n\n"
            "- The appliance is operated at rated input until thermal equilibrium is reached.\n"
            "- Surface temperatures of accessible parts are measured.\n"
            "- **Limits**: ≤ 60°C rise on accessible surfaces, ≤ 75°C on handles.\n"
            "- **IS 1258:2018 Amendment 1** revised the temperature limits — re-testing is required if tested under the old standard.\n\n"
            "This test must be conducted at an NABL-accredited lab. NABL Lab A in Delhi covers this test in the demo. [DEMO DATA]"
        ),
        ["Which lab can conduct the temperature rise test?", "How much does the temperature rise test cost?", "What is IS 1258 Amendment 1?"],
        ["REQ-001-03"],
    ),
    # Energy efficiency
    (
        ["energy efficiency", "bee", "star rating", "standing heat loss", "clause 7.1"],
        (
            "**Energy Efficiency (Standing Heat Loss)** requirements for electric water heaters [DEMO]:\n\n"
            "- Governed by IS 1258:2018 Clause 7.1 and Bureau of Energy Efficiency (BEE) standards.\n"
            "- The standing heat loss measures how much energy the heater loses when not actively heating water.\n"
            "- Products must meet minimum BEE star rating thresholds based on rated storage capacity.\n"
            "- Test is conducted per BEE measurement protocol.\n\n"
            "This is a mandatory requirement under the demo product profile. [DEMO DATA]"
        ),
        ["How is standing heat loss measured?", "What is the BEE star rating for water heaters?", "Which lab covers the energy efficiency test?"],
        ["REQ-001-04"],
    ),
    # Toys
    (
        ["toy", "toys", "is 9873", "mechanical safety", "chemical safety toy", "flammability toy"],
        (
            "For toys, the key BIS compliance requirements under IS 9873 series are [DEMO]:\n\n"
            "1. **Mechanical & Physical Safety** (IS 9873-1): No sharp edges, no small parts for <3yr age group, structural integrity.\n"
            "2. **Chemical Safety** (IS 9873-3): Limits for heavy metals (Pb, Cd, Hg, Cr(VI), etc.) in accessible materials.\n"
            "3. **Flammability** (IS 9873-1): Materials must not catch fire readily or burn slowly.\n"
            "4. **BIS ISI Mark** mandatory under the Toys QCO 2020 for all toys sold in India.\n\n"
            "[DEMO DATA]"
        ),
        ["What labs test toys for BIS compliance?", "How do I apply for BIS certification for toys?", "What is the Toys QCO?"],
        ["REQ-002-01", "REQ-002-02", "REQ-002-03"],
    ),
    # Safety helmet
    (
        ["helmet", "safety helmet", "hard hat", "is 2925", "retention system", "impact"],
        (
            "For Industrial Safety Helmets under IS 2925:1984 [DEMO]:\n\n"
            "- **Impact Attenuation**: Peak force transmitted ≤ 5 kN during drop test.\n"
            "- **Penetration Resistance**: No penetration when steel cone dropped from 1 metre.\n"
            "- **Retention System**: Chin strap must withstand 50 N dynamic load without failure.\n"
            "- **Class G** (General) helmets are not required to pass electrical insulation tests.\n"
            "- **Class E** (Electrical) helmets must withstand 20 kV AC.\n\n"
            "For the demo product (DEMO-PROD-003), the Retention System Test is **MISSING** — this is a critical gap. [DEMO DATA]"
        ),
        ["How do I conduct the retention system test?", "Which lab tests safety helmets?", "What is IS 2925?"],
        ["REQ-003-03", "REQ-003-05"],
    ),
    # NABL lab
    (
        ["nabl", "lab", "laboratory", "testing lab", "accredited lab", "where to test"],
        (
            "NABL (National Accreditation Board for Testing and Calibration Laboratories) accreditation is mandatory "
            "for labs that issue test reports accepted by BIS.\n\n"
            "To find a NABL-accredited lab:\n"
            "1. Visit the NABL portal: https://www.nabl-india.org/\n"
            "2. Search by product category or test parameter.\n"
            "3. Verify the lab's scope of accreditation covers your specific IS standard clauses.\n\n"
            "Demo labs in this system are for illustration only and are NOT real NABL labs. [DEMO DATA]"
        ),
        ["How do I verify a lab's NABL accreditation?", "Can I use a non-NABL lab for BIS testing?", "What is the NABL portal URL?"],
        [],
    ),
    # BOM
    (
        ["bom", "bill of materials", "component compliance", "sub-component"],
        (
            "For **Bill of Materials (BOM) compliance** under BIS:\n\n"
            "- Some sub-components may have their own mandatory IS standards (e.g., IS 694 for PVC cables).\n"
            "- Critical components like heating elements, motors, and switches should be sourced from BIS ISI-licensed suppliers.\n"
            "- Upload your BOM file (CSV/XLSX) to get a heuristic compliance assessment in this demo.\n\n"
            "The BOM analysis in this demo is heuristic only — consult a BIS compliance expert for authoritative guidance. [DEMO DATA]"
        ),
        ["How do I check if a component supplier has BIS certification?", "Can I upload my BOM for analysis?", "Which components need separate BIS certification?"],
        [],
    ),
    # Cost / timeline
    (
        ["cost", "how much", "fees", "price", "timeline", "how long", "days"],
        (
            "Estimated BIS compliance costs (demo indicative figures only — actual costs vary) [DEMO DATA]:\n\n"
            "**Testing Costs (per product):**\n"
            "- Electrical Safety tests: ₹6,000 – ₹12,000\n"
            "- Energy Efficiency test: ₹10,000 – ₹15,000\n"
            "- Full toy safety suite: ₹35,000 – ₹50,000\n"
            "- Safety helmet tests: ₹15,000 – ₹20,000\n\n"
            "**BIS Application Fees:**\n"
            "- Application fee: ₹1,000 – ₹5,000 (varies by category)\n"
            "- Grant fee and annual fee: varies by product and licence type\n\n"
            "**Timelines:**\n"
            "- Lab testing: 2 – 15 working days depending on tests\n"
            "- BIS review and inspection: 4 – 12 weeks typically\n\n"
            "[DEMO DATA - Verify current fees on the BIS website]"
        ),
        ["Where can I find official BIS fee schedules?", "How can I reduce compliance costs?", "Can MSMEs get fee concessions?"],
        [],
    ),
    # CMS portal
    (
        ["cms", "portal", "apply online", "online application", "bis portal", "bis cms"],
        (
            "The **BIS Customer Management System (CMS)** is the online portal for all BIS certification applications:\n\n"
            "- URL: https://www.bis.gov.in/ (navigate to 'Customer Portal' or 'CMS')\n"
            "- You can apply for ISI Mark licence, track application status, submit documents, and pay fees online.\n"
            "- For CRS (Compulsory Registration Scheme) products, registration is also done through CMS.\n\n"
            "[DEMO DATA - URLs are indicative; verify the current portal URL on the BIS website]"
        ),
        ["How do I register on the BIS CMS portal?", "What documents are needed for CMS submission?", "Can I track my BIS application status online?"],
        [],
    ),
    # Gaps / missing
    (
        ["gap", "missing", "what is missing", "compliance gap", "what do i need", "what's missing"],
        (
            "Based on the demo product profile, the key compliance gaps are:\n\n"
            "**For Electric Water Heater (DEMO-PROD-001):**\n"
            "1. ❌ Temperature Rise Test Report (IS 1258:2018 Clause 6.3) — MISSING\n"
            "2. ❌ Energy Efficiency Test Report (IS 1258:2018 Clause 7.1) — MISSING\n"
            "3. ❌ BIS ISI Mark Certification — APPLICATION NOT SUBMITTED\n\n"
            "**For Safety Helmet (DEMO-PROD-003):**\n"
            "1. ❌ Retention System Test Report (IS 2925:1984 Clause 4.6) — MISSING\n"
            "2. ❌ BIS ISI Mark Certification — BLOCKED by missing test\n\n"
            "Use the Gaps tab for full details. [DEMO DATA]"
        ),
        ["How do I close the temperature rise test gap?", "Which lab should I use for energy efficiency testing?", "How long will it take to close all gaps?"],
        ["REQ-001-03", "REQ-001-04", "REQ-001-07", "REQ-003-03"],
    ),
]

DEFAULT_RESPONSE = (
    "I'm BIS SAKSHAM, your BIS compliance assistant. I can help you with:\n\n"
    "- Understanding IS standards and QCOs\n"
    "- Identifying compliance gaps for your product\n"
    "- Finding NABL-accredited labs for testing\n"
    "- Navigating the BIS certification process\n"
    "- Analyzing BOM components for compliance\n\n"
    "Please ask me a specific question about your product or BIS compliance. [DEMO DATA]"
)


def _find_response(message: str, product_id: Optional[str] = None):
    """Find the best matching canned response for the message."""
    msg_lower = message.lower()

    for keywords, response_text, suggestions, related_reqs in RESPONSE_LIBRARY:
        if any(kw in msg_lower for kw in keywords):
            return response_text, suggestions, related_reqs

    return DEFAULT_RESPONSE, [
        "What IS standards apply to my product?",
        "How do I get BIS ISI Mark certification?",
        "What are the compliance gaps for my product?",
        "Which labs can test my product?",
    ], []


# ---------------------------------------------------------------------------
# POST /api/chat
# ---------------------------------------------------------------------------

@router.post("", response_model=ChatResponse, summary="Chat with BIS compliance assistant")
async def chat(request: ChatRequest):
    """
    Contextual AI compliance assistant. Returns intelligent canned responses
    based on the message content and optional product context.
    [DEMO DATA - Not connected to a real AI model]
    """
    from typing import Optional

    response_text, suggestions, related_reqs = _find_response(request.message, request.product_id)

    # If a product is in context, personalise slightly
    if request.product_id and request.product_id in PRODUCTS_DB:
        product = PRODUCTS_DB[request.product_id]
        gap_count = len(product.evidence_gaps)
        context_note = (
            f"\n\n---\n📋 **Current product context**: {product.name} "
            f"(Score: {product.compliance_score:.0f}%, {gap_count} gap(s) identified) [DEMO DATA]"
        )
        response_text += context_note

    return ChatResponse(
        message=response_text,
        suggestions=suggestions if suggestions else None,
        related_requirements=related_reqs if related_reqs else None,
        data_label=DEMO_LABEL,
    )
