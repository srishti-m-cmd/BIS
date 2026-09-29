import React, { useCallback, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Package, BookOpen, Shield, ClipboardList, FlaskConical,
  Building2, FileText, ChevronRight, X, AlertCircle,
  CheckCircle2, Clock, Info
} from 'lucide-react';
import { buildComplianceGraph } from '../../lib/complianceEngine.js';

// ─── Custom Node Types ─────────────────────────────────────────────────────────

const STATUS_COLORS = {
  SATISFIED:   { bg: '#DCFCE7', border: '#16A34A', text: '#166534', dot: '#16A34A' },
  MISSING:     { bg: '#FEF2F2', border: '#DC2626', text: '#991B1B', dot: '#DC2626' },
  REVIEW:      { bg: '#FEF9C3', border: '#EAB308', text: '#854D0E', dot: '#EAB308' },
  COMPLETED:   { bg: '#DCFCE7', border: '#16A34A', text: '#166534', dot: '#16A34A' },
  IN_PROGRESS: { bg: '#FEF9C3', border: '#EAB308', text: '#854D0E', dot: '#EAB308' },
  DEFAULT:     { bg: '#F8FAFC', border: '#CBD5E1', text: '#475569', dot: '#94A3B8' },
};

function getStatusColors(status) {
  return STATUS_COLORS[status] || STATUS_COLORS.DEFAULT;
}

// Product Node
function ProductNode({ data, selected }) {
  return (
    <div
      className={`px-4 py-3 rounded-xl border-2 cursor-pointer transition-all ${
        selected ? 'border-navy-900 shadow-lg' : 'border-navy-700'
      }`}
      style={{ background: '#0B1F3A', minWidth: 180 }}
    >
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-saffron-500 flex items-center justify-center flex-shrink-0">
          <Package size={16} color="#111827" />
        </div>
        <div>
          <div className="text-xs font-semibold text-saffron-500 uppercase tracking-wider">Product</div>
          <div className="text-sm font-bold text-white leading-tight">{data.label}</div>
        </div>
      </div>
    </div>
  );
}

// Standard Node
function StandardNode({ data, selected }) {
  return (
    <div
      className={`px-3 py-2.5 rounded-lg border-2 cursor-pointer transition-all ${
        selected ? 'border-ai-600 shadow-md' : 'border-blue-300'
      }`}
      style={{ background: '#EFF6FF', minWidth: 160 }}
    >
      <div className="flex items-center gap-2">
        <BookOpen size={14} className="text-blue-700 flex-shrink-0" />
        <div>
          <div className="text-xs font-bold text-blue-700 font-mono">{data.label}</div>
          <div className="text-xs text-blue-600 leading-tight mt-0.5" style={{ maxWidth: 140 }}>
            {data.title?.split('—')[0]?.trim()}
          </div>
        </div>
      </div>
    </div>
  );
}

// QCO Node
function QCONode({ data, selected }) {
  return (
    <div
      className={`px-3 py-2.5 rounded-lg border-2 cursor-pointer transition-all ${
        selected ? 'border-saffron-600 shadow-md' : 'border-saffron-400'
      }`}
      style={{ background: '#FFFBEB', minWidth: 160 }}
    >
      <div className="flex items-center gap-2">
        <Shield size={14} className="text-saffron-700 flex-shrink-0" />
        <div>
          <div className="text-xs font-bold text-saffron-700">QCO</div>
          <div className="text-xs text-saffron-600 leading-tight mt-0.5" style={{ maxWidth: 140 }}>
            {data.title?.split('(')[0]?.trim()}
          </div>
        </div>
      </div>
    </div>
  );
}

// Requirement Node
function RequirementNode({ data, selected }) {
  const colors = getStatusColors(data.status);
  return (
    <div
      className={`px-3 py-2.5 rounded-lg border-2 cursor-pointer transition-all ${selected ? 'shadow-md' : ''}`}
      style={{ background: colors.bg, borderColor: colors.border, minWidth: 150 }}
    >
      <div className="flex items-start gap-2">
        <ClipboardList size={12} style={{ color: colors.text, flexShrink: 0, marginTop: 2 }} />
        <div>
          <div className="text-xs font-semibold leading-tight" style={{ color: colors.text, maxWidth: 130 }}>
            {data.label}
          </div>
          {data.mandatory && (
            <span className="text-xs mt-0.5" style={{ color: colors.text, opacity: 0.7 }}>Mandatory</span>
          )}
        </div>
        <div className="w-2 h-2 rounded-full flex-shrink-0 mt-1" style={{ background: colors.dot }} />
      </div>
    </div>
  );
}

// Test Node
function TestNode({ data, selected }) {
  const colors = getStatusColors(data.status);
  return (
    <div
      className={`px-3 py-2 rounded-lg border-2 cursor-pointer transition-all ${selected ? 'shadow-md' : ''}`}
      style={{ background: colors.bg, borderColor: colors.border, minWidth: 140 }}
    >
      <div className="flex items-center gap-2">
        <FlaskConical size={12} style={{ color: colors.text, flexShrink: 0 }} />
        <div className="text-xs font-semibold" style={{ color: colors.text, maxWidth: 120 }}>
          {data.label}
        </div>
      </div>
    </div>
  );
}

// Lab Node
function LabNode({ data, selected }) {
  return (
    <div
      className={`px-3 py-2 rounded-lg border-2 cursor-pointer transition-all ${
        selected ? 'border-gov-green shadow-md' : 'border-green-300'
      }`}
      style={{ background: '#F0FDF4', minWidth: 140 }}
    >
      <div className="flex items-center gap-2">
        <Building2 size={12} className="text-green-700 flex-shrink-0" />
        <div>
          <div className="text-xs font-bold text-green-800">{data.label}</div>
          <div className="text-xs text-green-600">{data.location?.split(',')[0]}</div>
        </div>
      </div>
    </div>
  );
}

const nodeTypes = {
  productNode:     ProductNode,
  standardNode:    StandardNode,
  qcoNode:         QCONode,
  requirementNode: RequirementNode,
  testNode:        TestNode,
  labNode:         LabNode,
};

// ─── Detail Drawer ─────────────────────────────────────────────────────────────

function NodeDetailDrawer({ node, onClose }) {
  if (!node) return null;
  const { data } = node;
  const detail = data.detail || {};

  return (
    <AnimatePresence>
      <motion.div
        className="drawer-overlay"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      />
      <motion.div
        className="drawer-panel"
        initial={{ x: 420 }}
        animate={{ x: 0 }}
        exit={{ x: 420 }}
        transition={{ type: 'spring', damping: 30, stiffness: 300 }}
      >
        {/* Header */}
        <div className="p-4 border-b border-border flex items-start justify-between">
          <div>
            <span className={`badge ${
              data.type === 'PRODUCT' ? 'badge-standard' :
              data.type === 'STANDARD' ? 'badge-standard' :
              data.type === 'QCO' ? 'badge-qco' :
              data.type === 'REQUIREMENT' ? 'badge-document' :
              data.type === 'TEST' ? 'badge-test' :
              'badge-satisfied'
            } mb-2`}>
              {data.type}
            </span>
            <h3 className="heading-lg text-base">{data.label || data.title}</h3>
          </div>
          <button onClick={onClose} className="btn-ghost p-1.5 -mt-1">
            <X size={18} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Status */}
          {data.status && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-text-secondary font-medium">Status:</span>
              <span className={`badge badge-${data.status?.toLowerCase()}`}>{data.status}</span>
            </div>
          )}

          {/* Type-specific details */}
          {data.type === 'STANDARD' && detail.number && (
            <div className="space-y-2">
              <InfoRow label="Standard Number" value={detail.number} mono />
              <InfoRow label="Title" value={detail.title} />
              <InfoRow label="Status" value={detail.status} />
              <InfoRow label="Published" value={detail.publishedDate} />
              <InfoRow label="Applicability" value={detail.applicability} />
            </div>
          )}

          {data.type === 'REQUIREMENT' && detail.description && (
            <div className="space-y-2">
              <p className="text-sm text-text-secondary">{detail.description}</p>
              <InfoRow label="Standard" value={detail.standard} mono />
              <InfoRow label="Clause" value={detail.clause} />
              {detail.mandatory && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-text-secondary">Mandatory:</span>
                  <span className="badge badge-mandatory">Yes</span>
                </div>
              )}
            </div>
          )}

          {data.type === 'TEST' && (
            <div className="space-y-2">
              {detail.purpose && <p className="text-sm text-text-secondary">{detail.purpose}</p>}
              <InfoRow label="Standard" value={detail.standard} mono />
            </div>
          )}

          {data.type === 'LAB' && detail.accreditation && (
            <div className="space-y-2">
              <InfoRow label="Accreditation" value={`${detail.accreditation} — ${detail.accreditationNumber}`} />
              <InfoRow label="Location" value={detail.location} />
              <InfoRow label="Turnaround" value={`~${detail.turnaroundDays} days`} />
              <InfoRow label="Contact" value={detail.contact} />
            </div>
          )}

          {/* Evidence */}
          {detail.evidence && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div className="flex items-center gap-1.5 mb-2">
                <Info size={13} className="text-blue-600" />
                <span className="text-xs font-semibold text-blue-700 uppercase tracking-wider">Source Evidence</span>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-blue-800">
                  <span className="font-medium">Source:</span> {detail.evidence.source}
                </div>
                <div className="text-xs text-blue-800">
                  <span className="font-medium">Document:</span> {detail.evidence.document || detail.standard}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Demo Footer */}
        <div className="p-3 border-t border-border">
          <span className="trust-label demo">DEMO DATA</span>
          <p className="text-xs text-text-muted mt-1">
            Verify all requirements against current official BIS sources.
          </p>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

function InfoRow({ label, value, mono }) {
  if (!value) return null;
  return (
    <div className="flex gap-2">
      <span className="text-xs text-text-secondary font-medium flex-shrink-0">{label}:</span>
      <span className={`text-xs text-text-primary ${mono ? 'font-mono text-navy-900 font-semibold' : ''}`}>{value}</span>
    </div>
  );
}

// ─── Legend ────────────────────────────────────────────────────────────────────

function GraphLegend() {
  const items = [
    { color: '#0B1F3A', label: 'Product' },
    { color: '#3B82F6', label: 'Standard' },
    { color: '#D97706', label: 'QCO' },
    { color: '#16A34A', label: 'Satisfied' },
    { color: '#DC2626', label: 'Missing' },
    { color: '#EAB308', label: 'Review / In Progress' },
    { color: '#166534', label: 'Laboratory' },
  ];

  return (
    <div className="card-base p-3 text-xs space-y-1.5">
      <div className="font-semibold text-text-secondary uppercase tracking-wider text-xs mb-2">Legend</div>
      {items.map(({ color, label }) => (
        <div key={label} className="flex items-center gap-2">
          <div className="w-3 h-3 rounded flex-shrink-0" style={{ background: color }} />
          <span className="text-text-secondary">{label}</span>
        </div>
      ))}
    </div>
  );
}

// ─── Main Component ────────────────────────────────────────────────────────────

export default function ComplianceGraph({ productId }) {
  const graphData = buildComplianceGraph(productId || 'PROD-001');
  const [nodes, setNodes, onNodesChange] = useNodesState(graphData.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(graphData.edges);
  const [selectedNode, setSelectedNode] = useState(null);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((_, node) => {
    setSelectedNode(node);
  }, []);

  return (
    <div className="relative" style={{ height: 640 }}>
      {/* Legend */}
      <div className="absolute top-3 left-3 z-10">
        <GraphLegend />
      </div>

      {/* Info banner */}
      <div className="absolute top-3 right-3 z-10">
        <div className="card-base px-3 py-2 text-xs flex items-center gap-1.5 text-text-secondary">
          <Info size={12} />
          Click any node to view details
        </div>
      </div>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        defaultEdgeOptions={{
          style: { stroke: '#CBD5E1', strokeWidth: 1.5 },
        }}
        proOptions={{ hideAttribution: true }}
      >
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            const typeColors = {
              productNode:     '#0B1F3A',
              standardNode:    '#3B82F6',
              qcoNode:         '#F59E0B',
              requirementNode: '#6366F1',
              testNode:        '#10B981',
              labNode:         '#16A34A',
            };
            return typeColors[node.type] || '#94A3B8';
          }}
          style={{ background: '#F8FAFC', border: '1px solid #E2E8F0' }}
        />
        <Background color="#E2E8F0" gap={20} />
      </ReactFlow>

      {/* Detail Drawer */}
      <NodeDetailDrawer node={selectedNode} onClose={() => setSelectedNode(null)} />
    </div>
  );
}
