// BIS SAKSHAM Demo Data
// All data is clearly labeled as DEMO DATA for demonstration purposes
// This does not represent official BIS information or authoritative compliance guidance

export const DEMO_LABEL = "DEMO DATA";
export const AI_ASSISTED_LABEL = "AI-assisted";
export const BIS_SOURCE_LABEL = "BIS Source";
export const NEEDS_VERIFICATION_LABEL = "Needs Verification";

export interface ProductAttribute {
  key: string;
  value: string;
  confidence: "high" | "medium" | "low" | "unknown";
  source: "extracted" | "user-provided" | "inferred";
}

export interface Standard {
  id: string;
  number: string;
  title: string;
  year: number;
  status: "current" | "superseded" | "under-revision";
  category: string;
  type: "IS" | "QCO" | "BIS";
  dataLabel: string;
}

export interface Requirement {
  id: string;
  title: string;
  description: string;
  type: "STANDARD" | "QCO" | "CERTIFICATION" | "TEST" | "DOCUMENT" | "COMPONENT";
  mandatory: boolean;
  status: "SATISFIED" | "MISSING" | "REVIEW" | "NOT_APPLICABLE";
  evidence: EvidenceItem | null;
  sourceStandard: string;
  sourceClause: string;
  dataLabel: string;
}

export interface EvidenceItem {
  id: string;
  source: string;
  document: string;
  page: string;
  section: string;
  date: string;
  available: boolean;
  url?: string;
}

export interface Test {
  id: string;
  name: string;
  purpose: string;
  requirement: string;
  expectedEvidence: string;
  relatedStandard: string;
  status: "COMPLETED" | "PENDING" | "IN_PROGRESS" | "NOT_STARTED";
  dataLabel: string;
}

export interface Laboratory {
  id: string;
  name: string;
  location: string;
  city: string;
  state: string;
  lat: number;
  lng: number;
  accreditation: string;
  testsOffered: string[];
  contact: string;
  dataLabel: string;
}

export interface BOMComponent {
  id: string;
  name: string;
  partNumber?: string;
  material?: string;
  status: "CONFIRMED" | "POTENTIALLY_APPLICABLE" | "NO_REQUIREMENT" | "NEEDS_VERIFICATION";
  potentialRequirement?: string;
  reason?: string;
  evidence?: string;
  action?: string;
  dataLabel: string;
}

export interface ChangeEvent {
  id: string;
  title: string;
  description: string;
  affectedStandard: string;
  affectedProducts: string[];
  publishedDate: string;
  effectiveDate: string;
  impact: "HIGH" | "MEDIUM" | "LOW";
  status: "PUBLISHED" | "REVIEW" | "EFFECTIVE";
  action: string;
  dataLabel: string;
}

export interface ComplianceGap {
  requirementId: string;
  requirementTitle: string;
  expectedEvidence: string;
  uploadedEvidence: string | null;
  status: "MISSING" | "REVIEW" | "SATISFIED";
  action: string;
  reasoning: string;
  dataLabel: string;
}

export interface Product {
  id: string;
  name: string;
  category: string;
  attributes: ProductAttribute[];
  standards: Standard[];
  requirements: Requirement[];
  tests: Test[];
  bom: BOMComponent[];
  gaps: ComplianceGap[];
  changeEvents: ChangeEvent[];
  requirementCoverage: number;
  openGaps: number;
  lastReviewed: string;
  dataLabel: string;
}

// ============================================================
// SEEDED DEMO DATA
// ============================================================

export const DEMO_LABORATORIES: Laboratory[] = [
  {
    id: "LAB-001",
    name: "Central Power Research Institute (CPRI) - Delhi",
    location: "New Delhi, Delhi",
    city: "New Delhi",
    state: "Delhi",
    lat: 28.6139,
    lng: 77.2090,
    accreditation: "NABL Accredited",
    testsOffered: ["Electrical Safety", "Leakage Current", "Temperature Rise", "Insulation Resistance"],
    contact: "+91-11-XXXX-XXXX [DEMO]",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "LAB-002",
    name: "Electrical Research & Development Association (ERDA) - Vadodara",
    location: "Vadodara, Gujarat",
    city: "Vadodara",
    state: "Gujarat",
    lat: 22.3072,
    lng: 73.1812,
    accreditation: "NABL Accredited",
    testsOffered: ["Electrical Safety", "Energy Efficiency", "Leakage Current", "Temperature Rise"],
    contact: "+91-265-XXXX-XXXX [DEMO]",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "LAB-003",
    name: "Bureau Veritas Testing & Inspections India - Bangalore",
    location: "Bengaluru, Karnataka",
    city: "Bengaluru",
    state: "Karnataka",
    lat: 12.9716,
    lng: 77.5946,
    accreditation: "NABL Accredited",
    testsOffered: ["Pressure Test", "Insulation Resistance", "Energy Efficiency"],
    contact: "+91-80-XXXX-XXXX [DEMO]",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "LAB-004",
    name: "SGS India Pvt. Ltd. - Mumbai",
    location: "Mumbai, Maharashtra",
    city: "Mumbai",
    state: "Maharashtra",
    lat: 19.0760,
    lng: 72.8777,
    accreditation: "NABL Accredited",
    testsOffered: ["Mechanical Safety", "Chemical Safety", "Flammability"],
    contact: "+91-22-XXXX-XXXX [DEMO]",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "LAB-005",
    name: "National Test House (NTH) - Kolkata",
    location: "Kolkata, West Bengal",
    city: "Kolkata",
    state: "West Bengal",
    lat: 22.5726,
    lng: 88.3639,
    accreditation: "NABL Accredited",
    testsOffered: ["Impact Resistance", "Penetration Resistance", "Retention System Test"],
    contact: "+91-33-XXXX-XXXX [DEMO]",
    dataLabel: DEMO_LABEL,
  },
];

export const DEMO_STANDARDS: Standard[] = [
  {
    id: "STD-001",
    number: "IS 1258:2018",
    title: "Electric Storage Type Water Heaters — Specification",
    year: 2018,
    status: "current",
    category: "Electrical Appliances",
    type: "IS",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "STD-002",
    number: "IS 1884:2019",
    title: "Safety of Household and Similar Electrical Appliances",
    year: 2019,
    status: "current",
    category: "Electrical Safety",
    type: "IS",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "STD-003",
    number: "QCO-EEA-2023",
    title: "Quality Control Order — Electric and Electronic Appliances [DEMO]",
    year: 2023,
    status: "current",
    category: "Quality Control",
    type: "QCO",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "STD-004",
    number: "IS 9873 (Part 1):2015",
    title: "Safety of Toys — Mechanical and Physical Properties",
    year: 2015,
    status: "current",
    category: "Consumer Products",
    type: "IS",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "STD-005",
    number: "IS 2925:1984",
    title: "Industrial Safety Helmets — Specification",
    year: 1984,
    status: "current",
    category: "Personal Protective Equipment",
    type: "IS",
    dataLabel: DEMO_LABEL,
  },
];

// Product 1: Electric Storage Water Heater
export const WATER_HEATER_REQUIREMENTS: Requirement[] = [
  {
    id: "REQ-001",
    title: "Electrical Safety Test",
    description: "The appliance must comply with general electrical safety requirements including protection against electric shock, resistance to heat and fire.",
    type: "TEST",
    mandatory: true,
    status: "REVIEW",
    evidence: {
      id: "EV-001",
      source: "DEMO DATA",
      document: "IS 1258:2018 — Clause 4.1 [DEMO]",
      page: "12",
      section: "4.1 Safety Requirements",
      date: "2018-01-01",
      available: true,
    },
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 4.1",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-002",
    title: "Leakage Current Test",
    description: "Maximum permissible leakage current under normal operating conditions must not exceed specified limits.",
    type: "TEST",
    mandatory: true,
    status: "MISSING",
    evidence: null,
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 4.3",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-003",
    title: "Temperature Rise Test",
    description: "Temperature rise of accessible surfaces and internal components must be within specified limits during normal operation.",
    type: "TEST",
    mandatory: true,
    status: "MISSING",
    evidence: null,
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 4.4",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-004",
    title: "Energy Efficiency Rating",
    description: "Product must meet minimum energy efficiency requirements as specified under the Bureau of Energy Efficiency guidelines.",
    type: "STANDARD",
    mandatory: true,
    status: "MISSING",
    evidence: null,
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 5.2",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-005",
    title: "Pressure Test",
    description: "The water storage vessel must withstand specified hydraulic pressure without leakage or structural failure.",
    type: "TEST",
    mandatory: true,
    status: "SATISFIED",
    evidence: {
      id: "EV-002",
      source: "DEMO DATA",
      document: "Pressure Test Report — ABC Testing Lab [DEMO]",
      page: "3",
      section: "Test Results — Hydraulic Pressure",
      date: "2024-01-15",
      available: true,
    },
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 4.6",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-006",
    title: "Insulation Resistance",
    description: "Insulation resistance between live parts and accessible conductive parts must meet minimum specified values.",
    type: "TEST",
    mandatory: true,
    status: "SATISFIED",
    evidence: {
      id: "EV-003",
      source: "DEMO DATA",
      document: "Electrical Test Report — DEMO [DEMO]",
      page: "5",
      section: "Insulation Resistance Measurement",
      date: "2024-01-15",
      available: true,
    },
    sourceStandard: "IS 1884:2019",
    sourceClause: "Clause 6.1",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-007",
    title: "BIS Certification (ISI Mark)",
    description: "Product requires BIS Product Certification under IS 1258 to bear the ISI Mark, which is mandatory under the applicable QCO.",
    type: "CERTIFICATION",
    mandatory: true,
    status: "MISSING",
    evidence: null,
    sourceStandard: "QCO-EEA-2023",
    sourceClause: "Schedule I",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "REQ-008",
    title: "Technical Documentation",
    description: "Complete technical file including product specifications, circuit diagrams, and test reports must be maintained.",
    type: "DOCUMENT",
    mandatory: false,
    status: "REVIEW",
    evidence: {
      id: "EV-004",
      source: "DEMO DATA",
      document: "Product Specification Sheet (partial) [DEMO]",
      page: "1-8",
      section: "Technical Specifications",
      date: "2024-02-01",
      available: true,
    },
    sourceStandard: "IS 1258:2018",
    sourceClause: "Clause 8",
    dataLabel: DEMO_LABEL,
  },
];

export const WATER_HEATER_BOM: BOMComponent[] = [
  {
    id: "BOM-001",
    name: "Heating Element (Nichrome)",
    partNumber: "HE-250W-220V",
    material: "Nichrome wire in copper sheath",
    status: "POTENTIALLY_APPLICABLE",
    potentialRequirement: "IS 1258:2018 — Heating Element Requirements",
    reason: "Heating elements in electric water heaters may be subject to additional component-level requirements under IS 1258. The material and rating should be verified against Clause 3 specifications.",
    evidence: "IS 1258:2018 Clause 3 [DEMO DATA — verify against current standard]",
    action: "Verify heating element specifications against IS 1258:2018 Clause 3 requirements",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "BOM-002",
    name: "Thermostat (Bimetallic)",
    partNumber: "TS-85C-16A",
    material: "Bimetallic strip",
    status: "CONFIRMED",
    potentialRequirement: undefined,
    reason: "Standard bimetallic thermostat for this application. No separate BIS requirement identified for this component class beyond the appliance-level standard.",
    evidence: "Analysis based on IS 1258:2018 scope [DEMO DATA]",
    action: "No additional action required for this component",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "BOM-003",
    name: "Pressure Relief Valve",
    partNumber: "PRV-7BAR",
    material: "Brass body, EPDM seal",
    status: "NEEDS_VERIFICATION",
    potentialRequirement: "Component safety requirements — pressure-bearing parts",
    reason: "Pressure relief valves in water heaters are safety-critical components. Applicability of specific component standards requires verification against current BIS notifications.",
    evidence: "Verification required against current official BIS sources [DEMO DATA]",
    action: "Verify PRV compliance requirements against official BIS sources",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "BOM-004",
    name: "Tank Body (Stainless Steel)",
    partNumber: "TANK-SS-25L",
    material: "SS 304 Stainless Steel",
    status: "CONFIRMED",
    potentialRequirement: undefined,
    reason: "No separate BIS standard identified specifically for the stainless steel tank body as a component. Material compliance is covered under the appliance-level standard.",
    evidence: "IS 1258:2018 material requirements [DEMO DATA]",
    action: "Ensure material specifications are documented in the technical file",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "BOM-005",
    name: "Power Supply Cable",
    partNumber: "CABLE-3C-2.5SQ",
    material: "PVC insulated copper",
    status: "POTENTIALLY_APPLICABLE",
    potentialRequirement: "IS 694 — PVC Insulated Cables for Working Voltages up to and including 1100V",
    reason: "Power supply cables used in electrical appliances are often required to conform to IS 694. The appliance standard may specify cable requirements — verify.",
    evidence: "IS 694 reference — verify applicability [DEMO DATA]",
    action: "Confirm cable conformance to IS 694 or applicable standard",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "BOM-006",
    name: "Polyurethane Insulation Foam",
    partNumber: "FOAM-PU-25MM",
    material: "Polyurethane foam",
    status: "NO_REQUIREMENT",
    potentialRequirement: undefined,
    reason: "Insulation foam as used in this application does not appear to trigger a separate BIS product-level requirement based on available information. No requirement identified.",
    evidence: "Analysis based on product category [DEMO DATA]",
    action: "No additional BIS compliance action identified for this component",
    dataLabel: DEMO_LABEL,
  },
];

export const WATER_HEATER_TESTS: Test[] = [
  {
    id: "TEST-001",
    name: "Electrical Safety Test",
    purpose: "Verify protection against electric shock, fire risk, and unsafe temperatures under normal and fault conditions",
    requirement: "REQ-001",
    expectedEvidence: "Accredited laboratory test report conforming to IS 1258:2018 / IS 1884:2019",
    relatedStandard: "IS 1258:2018, IS 1884:2019",
    status: "IN_PROGRESS",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "TEST-002",
    name: "Leakage Current Test",
    purpose: "Measure leakage current under normal and single-fault conditions to verify within permissible limits",
    requirement: "REQ-002",
    expectedEvidence: "Accredited laboratory test report with leakage current measurements",
    relatedStandard: "IS 1258:2018 Clause 4.3",
    status: "NOT_STARTED",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "TEST-003",
    name: "Temperature Rise Test",
    purpose: "Verify that accessible surfaces and internal components do not exceed permissible temperature limits during operation",
    requirement: "REQ-003",
    expectedEvidence: "Accredited laboratory test report with temperature measurements at all monitoring points",
    relatedStandard: "IS 1258:2018 Clause 4.4",
    status: "NOT_STARTED",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "TEST-004",
    name: "Energy Efficiency Test",
    purpose: "Measure standing heat loss and energy factor to verify compliance with energy efficiency requirements",
    requirement: "REQ-004",
    expectedEvidence: "BEE-recognized laboratory test report with energy efficiency measurements",
    relatedStandard: "IS 1258:2018 Clause 5.2",
    status: "NOT_STARTED",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "TEST-005",
    name: "Hydraulic Pressure Test",
    purpose: "Verify structural integrity of the water storage vessel under specified hydraulic pressure",
    requirement: "REQ-005",
    expectedEvidence: "Test report confirming vessel withstands 1.5x working pressure without leakage",
    relatedStandard: "IS 1258:2018 Clause 4.6",
    status: "COMPLETED",
    dataLabel: DEMO_LABEL,
  },
];

export const WATER_HEATER_GAPS: ComplianceGap[] = [
  {
    requirementId: "REQ-002",
    requirementTitle: "Leakage Current Test",
    expectedEvidence: "Accredited laboratory test report with leakage current measurements within permissible limits as per IS 1258:2018",
    uploadedEvidence: null,
    status: "MISSING",
    action: "Arrange Leakage Current Test at an accredited laboratory",
    reasoning: "No test report for leakage current measurement has been uploaded or identified in the document set. This test is mandatory under IS 1258:2018 Clause 4.3.",
    dataLabel: DEMO_LABEL,
  },
  {
    requirementId: "REQ-003",
    requirementTitle: "Temperature Rise Test",
    expectedEvidence: "Complete temperature rise test report from accredited laboratory",
    uploadedEvidence: "Partial test report uploaded — Temperature Rise section is incomplete [DEMO]",
    status: "REVIEW",
    action: "Complete the temperature rise test and obtain full accredited report",
    reasoning: "An uploaded test report was found, but the temperature rise section appears incomplete. Full measurements at all monitoring points are required.",
    dataLabel: DEMO_LABEL,
  },
  {
    requirementId: "REQ-004",
    requirementTitle: "Energy Efficiency Rating",
    expectedEvidence: "Energy efficiency test report from BEE-recognized laboratory",
    uploadedEvidence: null,
    status: "MISSING",
    action: "Arrange Energy Efficiency Test at a recognized laboratory",
    reasoning: "No energy efficiency documentation has been found. This is a mandatory requirement under IS 1258:2018.",
    dataLabel: DEMO_LABEL,
  },
  {
    requirementId: "REQ-007",
    requirementTitle: "BIS Certification (ISI Mark)",
    expectedEvidence: "Valid BIS Product Certification License under IS 1258",
    uploadedEvidence: null,
    status: "MISSING",
    action: "Submit BIS Product Certification application after completing required tests",
    reasoning: "BIS Product Certification is mandatory for this product under the applicable QCO. No certification application or license has been identified.",
    dataLabel: DEMO_LABEL,
  },
];

export const WATER_HEATER_CHANGE_EVENT: ChangeEvent = {
  id: "CHG-001",
  title: "[DEMO] IS 1258 — Updated Temperature Performance Requirements",
  description: "A demonstration change event. In this scenario, IS 1258 has been amended to update temperature performance rating requirements for electric storage water heaters above 15L capacity. Products with ongoing certification should review impact on existing test reports.",
  affectedStandard: "IS 1258:2018",
  affectedProducts: ["DEMO-PROD-001"],
  publishedDate: "2025-03-01",
  effectiveDate: "2025-09-01",
  impact: "MEDIUM",
  status: "EFFECTIVE",
  action: "Review existing Temperature Rise test reports against updated requirements. Retesting may be required.",
  dataLabel: DEMO_LABEL,
};

export const DEMO_PRODUCTS: Product[] = [
  {
    id: "DEMO-PROD-001",
    name: "Electric Storage Water Heater",
    category: "Electrical Appliances",
    attributes: [
      { key: "Capacity", value: "25 Litres", confidence: "high", source: "extracted" },
      { key: "Voltage", value: "220–240V AC, 50Hz", confidence: "high", source: "extracted" },
      { key: "Power Rating", value: "2000W", confidence: "medium", source: "inferred" },
      { key: "Intended Use", value: "Domestic", confidence: "high", source: "extracted" },
      { key: "Mounting", value: "Wall-mounted", confidence: "medium", source: "inferred" },
      { key: "Tank Material", value: "Stainless Steel (SS 304)", confidence: "medium", source: "extracted" },
      { key: "IP Rating", value: "IPX4 (minimum)", confidence: "low", source: "inferred" },
    ],
    standards: [DEMO_STANDARDS[0], DEMO_STANDARDS[1], DEMO_STANDARDS[2]],
    requirements: WATER_HEATER_REQUIREMENTS,
    tests: WATER_HEATER_TESTS,
    bom: WATER_HEATER_BOM,
    gaps: WATER_HEATER_GAPS,
    changeEvents: [WATER_HEATER_CHANGE_EVENT],
    requirementCoverage: 37,
    openGaps: 4,
    lastReviewed: "2025-09-29",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "DEMO-PROD-002",
    name: "Plastic Toy (Age 3+)",
    category: "Consumer Products — Toys",
    attributes: [
      { key: "Target Age", value: "3 years and above", confidence: "high", source: "extracted" },
      { key: "Material", value: "ABS Plastic", confidence: "high", source: "extracted" },
      { key: "Category", value: "Non-electronic toy", confidence: "high", source: "extracted" },
      { key: "Market", value: "Domestic (India)", confidence: "high", source: "user-provided" },
    ],
    standards: [DEMO_STANDARDS[3]],
    requirements: [
      {
        id: "REQ-TOY-001",
        title: "Mechanical & Physical Safety",
        description: "Toy must not have sharp edges, points, or pose mechanical hazards to children.",
        type: "STANDARD",
        mandatory: true,
        status: "SATISFIED",
        evidence: {
          id: "EV-TOY-001",
          source: "DEMO DATA",
          document: "IS 9873 Part 1:2015 [DEMO]",
          page: "8",
          section: "Clause 4 — Mechanical Properties",
          date: "2015-01-01",
          available: true,
        },
        sourceStandard: "IS 9873 (Part 1):2015",
        sourceClause: "Clause 4",
        dataLabel: DEMO_LABEL,
      },
      {
        id: "REQ-TOY-002",
        title: "Chemical Safety",
        description: "Migration of hazardous elements from surface coatings must be within permissible limits.",
        type: "TEST",
        mandatory: true,
        status: "SATISFIED",
        evidence: {
          id: "EV-TOY-002",
          source: "DEMO DATA",
          document: "Chemical Test Report [DEMO]",
          page: "2",
          section: "Heavy Metal Migration",
          date: "2024-06-01",
          available: true,
        },
        sourceStandard: "IS 9873 (Part 2):2017",
        sourceClause: "Clause 3",
        dataLabel: DEMO_LABEL,
      },
      {
        id: "REQ-TOY-003",
        title: "BIS Certification",
        description: "Toys for children up to 14 years require BIS certification under applicable QCO.",
        type: "CERTIFICATION",
        mandatory: true,
        status: "REVIEW",
        evidence: {
          id: "EV-TOY-003",
          source: "DEMO DATA",
          document: "BIS Certification Application (under review) [DEMO]",
          page: "1",
          section: "Application Reference",
          date: "2024-09-01",
          available: true,
        },
        sourceStandard: "QCO-TOYS",
        sourceClause: "Schedule I",
        dataLabel: DEMO_LABEL,
      },
    ],
    tests: [],
    bom: [],
    gaps: [
      {
        requirementId: "REQ-TOY-003",
        requirementTitle: "BIS Certification",
        expectedEvidence: "Valid BIS Product Certification License",
        uploadedEvidence: "Application submitted — pending approval [DEMO]",
        status: "REVIEW",
        action: "Monitor BIS certification application status",
        reasoning: "Certification application submitted but approval is pending. Monitor BIS portal for status updates.",
        dataLabel: DEMO_LABEL,
      },
    ],
    changeEvents: [],
    requirementCoverage: 78,
    openGaps: 1,
    lastReviewed: "2025-09-15",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "DEMO-PROD-003",
    name: "Industrial Safety Helmet",
    category: "Personal Protective Equipment",
    attributes: [
      { key: "Type", value: "Type I — General Industrial Use", confidence: "high", source: "extracted" },
      { key: "Material", value: "HDPE Shell", confidence: "high", source: "extracted" },
      { key: "Target Market", value: "Construction, Manufacturing", confidence: "high", source: "user-provided" },
      { key: "Colour", value: "White/Yellow (varies)", confidence: "medium", source: "extracted" },
    ],
    standards: [DEMO_STANDARDS[4]],
    requirements: [
      {
        id: "REQ-HELM-001",
        title: "Impact Resistance Test",
        description: "Helmet shell must absorb specified impact energy without fracture or excessive transmission to headform.",
        type: "TEST",
        mandatory: true,
        status: "SATISFIED",
        evidence: {
          id: "EV-HELM-001",
          source: "DEMO DATA",
          document: "Impact Test Report [DEMO]",
          page: "4",
          section: "Impact Absorption Results",
          date: "2024-03-01",
          available: true,
        },
        sourceStandard: "IS 2925:1984",
        sourceClause: "Clause 4.2",
        dataLabel: DEMO_LABEL,
      },
      {
        id: "REQ-HELM-002",
        title: "Penetration Resistance Test",
        description: "Helmet must resist penetration by a specified steel striker under defined test conditions.",
        type: "TEST",
        mandatory: true,
        status: "MISSING",
        evidence: null,
        sourceStandard: "IS 2925:1984",
        sourceClause: "Clause 4.3",
        dataLabel: DEMO_LABEL,
      },
      {
        id: "REQ-HELM-003",
        title: "Retention System Strength",
        description: "The chin strap and harness must withstand specified tensile loads.",
        type: "TEST",
        mandatory: true,
        status: "SATISFIED",
        evidence: {
          id: "EV-HELM-003",
          source: "DEMO DATA",
          document: "Retention System Test Report [DEMO]",
          page: "6",
          section: "Strap Retention Load Test",
          date: "2024-03-01",
          available: true,
        },
        sourceStandard: "IS 2925:1984",
        sourceClause: "Clause 4.4",
        dataLabel: DEMO_LABEL,
      },
    ],
    tests: [],
    bom: [],
    gaps: [
      {
        requirementId: "REQ-HELM-002",
        requirementTitle: "Penetration Resistance Test",
        expectedEvidence: "Accredited laboratory test report for penetration resistance",
        uploadedEvidence: null,
        status: "MISSING",
        action: "Arrange penetration resistance test at accredited laboratory",
        reasoning: "No test report for penetration resistance found. This is mandatory under IS 2925.",
        dataLabel: DEMO_LABEL,
      },
    ],
    changeEvents: [],
    requirementCoverage: 65,
    openGaps: 1,
    lastReviewed: "2025-08-20",
    dataLabel: DEMO_LABEL,
  },
];

// Compliance Graph Data
export const getComplianceGraphData = (productId: string) => {
  if (productId !== "DEMO-PROD-001") {
    return { nodes: [], edges: [] };
  }
  return {
    nodes: [
      { id: "product", type: "product", data: { label: "Electric Storage Water Heater", type: "PRODUCT" }, position: { x: 400, y: 50 } },
      { id: "std-001", type: "standard", data: { label: "IS 1258:2018", type: "STANDARD" }, position: { x: 150, y: 200 } },
      { id: "std-002", type: "standard", data: { label: "IS 1884:2019", type: "STANDARD" }, position: { x: 400, y: 200 } },
      { id: "qco-001", type: "qco", data: { label: "QCO EEA 2023", type: "QCO" }, position: { x: 650, y: 200 } },
      { id: "req-001", type: "requirement", data: { label: "Electrical Safety", type: "REQUIREMENT", status: "REVIEW" }, position: { x: 100, y: 380 } },
      { id: "req-002", type: "requirement", data: { label: "Leakage Current", type: "REQUIREMENT", status: "MISSING" }, position: { x: 300, y: 380 } },
      { id: "req-003", type: "requirement", data: { label: "Temperature Rise", type: "REQUIREMENT", status: "MISSING" }, position: { x: 500, y: 380 } },
      { id: "req-007", type: "requirement", data: { label: "BIS Certification", type: "REQUIREMENT", status: "MISSING" }, position: { x: 700, y: 380 } },
      { id: "test-001", type: "test", data: { label: "Electrical Safety Test", type: "TEST" }, position: { x: 100, y: 540 } },
      { id: "test-002", type: "test", data: { label: "Leakage Current Test", type: "TEST" }, position: { x: 300, y: 540 } },
      { id: "test-003", type: "test", data: { label: "Temperature Rise Test", type: "TEST" }, position: { x: 500, y: 540 } },
      { id: "lab-001", type: "lab", data: { label: "CPRI Delhi", type: "LABORATORY" }, position: { x: 200, y: 700 } },
      { id: "lab-002", type: "lab", data: { label: "ERDA Vadodara", type: "LABORATORY" }, position: { x: 500, y: 700 } },
    ],
    edges: [
      { id: "e1", source: "product", target: "std-001" },
      { id: "e2", source: "product", target: "std-002" },
      { id: "e3", source: "product", target: "qco-001" },
      { id: "e4", source: "std-001", target: "req-001" },
      { id: "e5", source: "std-001", target: "req-002" },
      { id: "e6", source: "std-001", target: "req-003" },
      { id: "e7", source: "qco-001", target: "req-007" },
      { id: "e8", source: "req-001", target: "test-001" },
      { id: "e9", source: "req-002", target: "test-002" },
      { id: "e10", source: "req-003", target: "test-003" },
      { id: "e11", source: "test-001", target: "lab-001" },
      { id: "e12", source: "test-002", target: "lab-001" },
      { id: "e13", source: "test-003", target: "lab-001" },
      { id: "e14", source: "test-001", target: "lab-002" },
    ],
  };
};

export const BIS_SERVICES = [
  {
    id: "SVC-001",
    title: "Standards",
    description: "Access Indian Standards (IS) documents, technical specifications, and standard development information.",
    icon: "BookOpen",
    who: "Manufacturers, engineers, researchers, regulatory agencies",
    how: "Available through BIS webstore (bis.gov.in) and BIS e-Library",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-002",
    title: "Product Certification (ISI Mark)",
    description: "BIS Product Certification scheme that allows manufacturers to use the ISI mark on conforming products.",
    icon: "Award",
    who: "Manufacturers whose products fall under mandatory or voluntary certification schemes",
    how: "Apply through BIS portal, grant of license after factory inspection and type testing",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-003",
    title: "Hallmarking",
    description: "BIS Hallmarking scheme for gold and silver jewellery to assure purity.",
    icon: "Gem",
    who: "Jewellery manufacturers and retailers",
    how: "Registration on BIS portal, assaying and hallmarking at BIS-recognised centres",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-004",
    title: "Testing Laboratories",
    description: "BIS-recognised and NABL-accredited testing facilities for product conformity assessment.",
    icon: "FlaskConical",
    who: "Manufacturers requiring product testing for certification",
    how: "Engage recognised labs for testing against applicable Indian Standards",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-005",
    title: "Foreign Manufacturer Certification",
    description: "Certification scheme for foreign manufacturers exporting products to India requiring BIS certification.",
    icon: "Globe",
    who: "Foreign manufacturers exporting to Indian market",
    how: "Apply through BIS portal, conformity assessment as per applicable scheme",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-006",
    title: "Training & Education",
    description: "BIS training programs on standards, quality, and conformity assessment for industry professionals.",
    icon: "GraduationCap",
    who: "Industry professionals, students, SMEs",
    how: "Register for training programs through BIS portal",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-007",
    title: "Consumer Services",
    description: "Consumer grievance redressal, awareness programs, and guidance on BIS-certified products.",
    icon: "Users",
    who: "Consumers, general public",
    how: "Contact BIS regional offices or use online grievance portal",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "SVC-008",
    title: "Standards Clubs",
    description: "BIS Standards Clubs in educational institutions to promote standards education among youth.",
    icon: "School",
    who: "Educational institutions, students",
    how: "Register institution with BIS to form a Standards Club",
    link: "https://www.bis.gov.in",
    dataLabel: DEMO_LABEL,
  },
];

export const DEMO_UPDATES = [
  {
    id: "UPD-001",
    title: "[DEMO] IS 1258 — Amendment to Temperature Performance Requirements",
    category: "Standards",
    publishedDate: "2025-03-01",
    effectiveDate: "2025-09-01",
    affectedProducts: ["Electric Storage Water Heater"],
    impact: "MEDIUM",
    summary: "Demonstration update event. Temperature performance rating requirements updated for electric storage water heaters above 15L capacity.",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "UPD-002",
    title: "[DEMO] New QCO — Extended Product Coverage Notification",
    category: "QCO",
    publishedDate: "2025-01-15",
    effectiveDate: "2025-07-15",
    affectedProducts: ["Multiple categories"],
    impact: "HIGH",
    summary: "Demonstration QCO update. New products added to mandatory certification scope.",
    dataLabel: DEMO_LABEL,
  },
  {
    id: "UPD-003",
    title: "[DEMO] BIS Hallmarking — Expanded Coverage",
    category: "Certification",
    publishedDate: "2025-02-10",
    effectiveDate: "2025-08-10",
    affectedProducts: ["Gold Jewellery", "Silver Jewellery"],
    impact: "LOW",
    summary: "Demonstration hallmarking update. Coverage expanded to additional article categories.",
    dataLabel: DEMO_LABEL,
  },
];
