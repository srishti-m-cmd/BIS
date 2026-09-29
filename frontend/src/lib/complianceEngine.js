/**
 * BIS SAKSHAM — Deterministic Compliance Engine
 *
 * ARCHITECTURE PRINCIPLE:
 * "AI can explain compliance. AI cannot invent compliance."
 *
 * This engine computes compliance state deterministically from seeded data.
 * It does NOT use an LLM to determine compliance truth.
 * LLMs are only used to explain and clarify, never to decide.
 */

import { getProductById, LABORATORIES } from './demoData.js';

// ─── REQUIREMENT STATUS COMPUTATION ───────────────────────────────────────────

/**
 * Compute overall compliance status from a list of requirements.
 */
export function computeComplianceStatus(requirements) {
  const counts = { SATISFIED: 0, MISSING: 0, REVIEW: 0, NOT_APPLICABLE: 0 };
  for (const req of requirements) {
    counts[req.status] = (counts[req.status] || 0) + 1;
  }

  const total = requirements.length;
  const evidenceCompletion = total > 0
    ? Math.round((counts.SATISFIED / total) * 100)
    : 0;

  let overallStatus = 'ON_TRACK';
  if (counts.MISSING > 0) overallStatus = 'ACTION_REQUIRED';
  else if (counts.REVIEW > 0) overallStatus = 'REVIEW_NEEDED';

  return {
    total,
    satisfied: counts.SATISFIED,
    missing: counts.MISSING,
    review: counts.REVIEW,
    notApplicable: counts.NOT_APPLICABLE,
    evidenceCompletion,
    overallStatus,
    openGaps: counts.MISSING + counts.REVIEW,
  };
}

// ─── PRODUCT COMPLIANCE PASSPORT ──────────────────────────────────────────────

/**
 * Build the complete Compliance Passport for a product.
 * This is the central data structure for the Compliance Passport page.
 */
export function buildCompliancePassport(productId) {
  const product = getProductById(productId);
  if (!product) return null;

  const status = computeComplianceStatus(product.requirements);
  const missingTests = product.tests.filter(t => t.status === 'MISSING');
  const completedTests = product.tests.filter(t => t.status === 'COMPLETED');
  const labIds = [...new Set(product.tests.flatMap(t => t.labs || []))];
  const labs = labIds.map(id => LABORATORIES[id]).filter(Boolean);

  return {
    productId: product.id,
    productName: product.name,
    productCode: `BIS-PROD-${product.id.split('-')[1]}`,
    category: product.category,
    attributes: product.attributes,
    standards: product.standards,
    qcos: product.qcos,
    requirements: product.requirements,
    tests: product.tests,
    laboratories: labs,
    documents: product.documents,
    changeEvents: product.changeEvents,
    bom: product.bom,
    complianceSummary: {
      ...status,
      missingTests: missingTests.map(t => t.name),
      completedTests: completedTests.map(t => t.name),
    },
    lastReviewed: product.lastReviewed,
    demoLabel: true,
    disclaimer: 'BIS SAKSHAM is an AI-assisted information and workflow tool. It does not issue BIS certification or replace official BIS decisions. Users should verify current requirements against official BIS sources.',
  };
}

// ─── GAP ANALYSIS ─────────────────────────────────────────────────────────────

/**
 * Compute gap analysis comparing requirements against uploaded evidence.
 * Deterministic — based on seeded requirement statuses.
 */
export function computeGapAnalysis(productId) {
  const product = getProductById(productId);
  if (!product) return [];

  return product.requirements.map(req => {
    const gap = {
      requirementId: req.id,
      requirement: req.title,
      type: req.type,
      mandatory: req.mandatory,
      expectedEvidence: getExpectedEvidence(req.type),
      uploadedEvidence: req.evidence?.uploadedDocument || null,
      status: req.status,
      action: getGapAction(req),
      source: req.evidence?.source || 'BIS',
      sourceDocument: req.evidence?.document || req.standard,
    };
    return gap;
  });
}

function getExpectedEvidence(type) {
  const map = {
    STANDARD: 'Accredited laboratory test report per applicable IS standard',
    QCO: 'ISI Mark licence from BIS / QCO compliance certificate',
    CERTIFICATION: 'BIS licence certificate / BEE Star Rating certificate',
    TEST: 'Test report from NABL-accredited laboratory',
    DOCUMENT: 'Technical declaration / product datasheet',
    COMPONENT: 'Component compliance certificate / supplier declaration',
  };
  return map[type] || 'Supporting evidence as per applicable requirement';
}

function getGapAction(req) {
  if (req.status === 'SATISFIED') return 'No action required — requirement satisfied';
  if (req.status === 'MISSING') {
    if (req.tests?.length > 0) return `Arrange ${req.tests.join(', ')} test at an accredited laboratory`;
    return 'Submit required documentation to fulfill this requirement';
  }
  if (req.status === 'REVIEW') return 'Review uploaded evidence — additional documentation may be required';
  return 'Verify applicability against current official BIS requirements';
}

// ─── TEST-TO-LAB OPTIMIZER ────────────────────────────────────────────────────

/**
 * Find optimal laboratory coverage for a set of outstanding tests.
 * Sorts by coverage (descending), not by distance.
 */
export function optimizeTestToLab(productId) {
  const product = getProductById(productId);
  if (!product) return { outstandingTests: [], labOptions: [] };

  const outstandingTests = product.tests.filter(
    t => t.status === 'MISSING' || t.status === 'IN_PROGRESS'
  );

  const outstandingCodes = outstandingTests.map(t => t.code);
  const relevantLabIds = [...new Set(outstandingTests.flatMap(t => t.labs || []))];

  const labOptions = relevantLabIds
    .map(labId => {
      const lab = LABORATORIES[labId];
      if (!lab) return null;
      const coveredTests = outstandingTests.filter(t => t.labs?.includes(labId));
      return {
        ...lab,
        coveredTests,
        coverageCount: coveredTests.length,
        coveragePercent: outstandingTests.length > 0
          ? Math.round((coveredTests.length / outstandingTests.length) * 100)
          : 0,
        isOptimal: coveredTests.length === outstandingTests.length,
      };
    })
    .filter(Boolean)
    .sort((a, b) => b.coverageCount - a.coverageCount);

  // Build suggested route (greedy coverage algorithm)
  const route = [];
  const coveredCodes = new Set();

  for (const lab of labOptions) {
    const newCodes = lab.coveredTests
      .map(t => t.code)
      .filter(code => !coveredCodes.has(code));
    if (newCodes.length > 0) {
      route.push({ ...lab, testsAtThisLab: lab.coveredTests.filter(t => newCodes.includes(t.code)) });
      newCodes.forEach(code => coveredCodes.add(code));
    }
    if (coveredCodes.size === outstandingCodes.length) break;
  }

  return {
    outstandingTests,
    labOptions,
    suggestedRoute: route,
    allCovered: coveredCodes.size === outstandingCodes.length,
  };
}

// ─── BOM ANALYSIS ─────────────────────────────────────────────────────────────

/**
 * Analyze BOM items and return compliance dependency analysis.
 */
export function analyzeBOM(productId) {
  const product = getProductById(productId);
  if (!product) return [];
  return product.bom;
}

/**
 * Parse a demo CSV/text BOM and map to known components.
 * For demo purposes, maps uploaded content to seeded BOM data.
 */
export function parseDemoBOM(productId) {
  // Returns seeded BOM regardless of uploaded file content (demo mode)
  return analyzeBOM(productId);
}

// ─── CHANGE IMPACT ────────────────────────────────────────────────────────────

/**
 * Get change events affecting a product, with impact analysis.
 */
export function getChangeImpact(productId) {
  const product = getProductById(productId);
  if (!product) return [];
  return product.changeEvents.map(event => ({
    ...event,
    affectedRequirementsDetails: product.requirements.filter(r =>
      event.affectedRequirements?.includes(r.id)
    ),
  }));
}

// ─── COMPLIANCE GRAPH DATA ────────────────────────────────────────────────────

/**
 * Build React Flow nodes and edges for the compliance graph.
 */
export function buildComplianceGraph(productId) {
  const product = getProductById(productId);
  if (!product) return { nodes: [], edges: [] };

  const nodes = [];
  const edges = [];

  // Product node
  nodes.push({
    id: 'product',
    type: 'productNode',
    position: { x: 300, y: 20 },
    data: { label: product.name, type: 'PRODUCT', detail: product },
  });

  // Standard nodes
  product.standards.forEach((std, i) => {
    const nodeId = `std-${std.id}`;
    nodes.push({
      id: nodeId,
      type: 'standardNode',
      position: { x: 100 + i * 280, y: 140 },
      data: { label: std.number, title: std.title, type: 'STANDARD', detail: std },
    });
    edges.push({ id: `e-product-${nodeId}`, source: 'product', target: nodeId, type: 'smoothstep', animated: true });
  });

  // QCO nodes
  product.qcos.forEach((qco, i) => {
    const nodeId = `qco-${qco.id}`;
    nodes.push({
      id: nodeId,
      type: 'qcoNode',
      position: { x: 100 + (product.standards.length + i) * 280, y: 140 },
      data: { label: 'QCO', title: qco.title, type: 'QCO', detail: qco },
    });
    edges.push({ id: `e-product-${nodeId}`, source: 'product', target: nodeId, type: 'smoothstep', animated: true });
  });

  // Requirement nodes
  const reqX = [50, 200, 350, 500, 650, 800];
  product.requirements.slice(0, 6).forEach((req, i) => {
    const nodeId = `req-${req.id}`;
    nodes.push({
      id: nodeId,
      type: 'requirementNode',
      position: { x: reqX[i] || i * 150, y: 280 },
      data: { label: req.title, type: 'REQUIREMENT', status: req.status, mandatory: req.mandatory, detail: req },
    });
    // Connect to relevant standard
    const stdId = product.standards[0]?.id;
    if (stdId) {
      edges.push({ id: `e-std-${nodeId}`, source: `std-${stdId}`, target: nodeId, type: 'smoothstep' });
    }
  });

  // Test nodes
  product.tests.slice(0, 5).forEach((test, i) => {
    const nodeId = `test-${test.id}`;
    nodes.push({
      id: nodeId,
      type: 'testNode',
      position: { x: 50 + i * 180, y: 420 },
      data: { label: test.name, type: 'TEST', status: test.status, detail: test },
    });
    // Connect test to requirement
    const reqId = test.requirementIds?.[0];
    if (reqId) {
      edges.push({ id: `e-req-${nodeId}`, source: `req-${reqId}`, target: nodeId, type: 'smoothstep' });
    }
  });

  // Lab nodes
  const labIds = [...new Set(product.tests.flatMap(t => t.labs || []))].slice(0, 3);
  labIds.forEach((labId, i) => {
    const lab = LABORATORIES[labId];
    if (!lab) return;
    const nodeId = `lab-${labId}`;
    nodes.push({
      id: nodeId,
      type: 'labNode',
      position: { x: 100 + i * 250, y: 560 },
      data: { label: lab.shortName, location: lab.location, type: 'LAB', detail: lab },
    });
    // Connect to tests that use this lab
    product.tests.filter(t => t.labs?.includes(labId)).slice(0, 2).forEach(test => {
      edges.push({ id: `e-${nodeId}-${test.id}`, source: `test-${test.id}`, target: nodeId, type: 'smoothstep' });
    });
  });

  return { nodes, edges };
}
