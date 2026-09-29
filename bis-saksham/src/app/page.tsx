"use client";

import { useMemo, useState } from "react";
import {
  Activity, ArrowDownRight, ArrowRight, ArrowUpRight, Award, Bell, BookOpen,
  Check, ChevronDown, ChevronRight, CircleHelp, ClipboardCheck,
  Clock3, FileCheck2, FileText, FlaskConical, Grid2X2, LifeBuoy, Menu,
  MoreHorizontal, Package, Plus, Search, Settings2, ShieldCheck, Sparkles,
  TrendingUp, X,
} from "lucide-react";
import {
  BIS_SERVICES, DEMO_LABEL, DEMO_LABORATORIES, DEMO_PRODUCTS, DEMO_STANDARDS,
  DEMO_UPDATES,
} from "@/lib/demo-data";
import { formatDate, getStatusLabel } from "@/lib/utils";

type Section = "Overview" | "Products" | "Standards" | "Laboratories" | "Updates" | "BIS services";
const navigation: { label: Section; icon: typeof Grid2X2 }[] = [
  { label: "Overview", icon: Grid2X2 }, { label: "Products", icon: Package },
  { label: "Standards", icon: BookOpen }, { label: "Laboratories", icon: FlaskConical },
  { label: "Updates", icon: Bell }, { label: "BIS services", icon: Award },
];

const statusClass = (status: string) => {
  if (status === "SATISFIED" || status === "COMPLETED" || status === "current") return "status status-green";
  if (status === "MISSING" || status === "NOT_STARTED") return "status status-red";
  if (status === "REVIEW" || status === "IN_PROGRESS" || status === "under-revision") return "status status-amber";
  return "status status-gray";
};

function DemoTag({ children = DEMO_LABEL }: { children?: string }) {
  return <span className="demo-tag"><span className="demo-dot" />{children}</span>;
}

function Header({ section, query, setQuery, onMenu }: { section: Section; query: string; setQuery: (value: string) => void; onMenu: () => void }) {
  return <header className="topbar">
    <button className="mobile-menu icon-button" onClick={onMenu} aria-label="Open navigation"><Menu size={19} /></button>
    <div className="breadcrumbs"><span>Workspace</span><ChevronRight size={14} /><strong>{section}</strong></div>
    <div className="topbar-actions">
      <label className="searchbox"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search workspace..." /><kbd>⌘ K</kbd></label>
      <button className="icon-button notification" aria-label="Notifications"><Bell size={18} /><i /></button>
      <span className="top-divider" />
      <button className="profile"><span className="avatar">A</span><span className="profile-copy"><b>Acme Industries</b><small>Workspace admin</small></span><ChevronDown size={15} /></button>
    </div>
  </header>;
}

function Sidebar({ section, setSection, open, close }: { section: Section; setSection: (s: Section) => void; open: boolean; close: () => void }) {
  return <>
    {open && <button className="mobile-scrim" onClick={close} aria-label="Close navigation" />}
    <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
      <div className="brand"><span className="brand-mark"><ShieldCheck size={20} strokeWidth={2.2} /></span><span><b>SAKSHAM</b><small>by BIS</small></span><button className="close-menu icon-button" onClick={close} aria-label="Close navigation"><X size={18} /></button></div>
      <div className="workspace-switch"><div className="workspace-emblem">A</div><span><small>WORKSPACE</small><b>Acme Industries</b></span><ChevronDown size={15} /></div>
      <div className="nav-caption">WORKSPACE</div>
      <nav>{navigation.map(({ label, icon: Icon }) => <button key={label} className={`nav-item ${section === label ? "nav-active" : ""}`} onClick={() => { setSection(label); close(); }}><Icon size={18} /><span>{label}</span>{label === "Updates" && <i className="nav-count">3</i>}</button>)}</nav>
      <div className="nav-caption tools-caption">TOOLS</div>
      <button className="nav-item" onClick={() => { setSection("Products"); close(); }}><ClipboardCheck size={18} /><span>Compliance checklist</span></button>
      <div className="sidebar-spacer" />
      <div className="sidebar-help"><div className="help-icon"><LifeBuoy size={17} /></div><b>Need a hand?</b><p>Explore the BIS services and find the right support for your product.</p><button onClick={() => { setSection("BIS services"); close(); }}>Explore services <ArrowRight size={14} /></button></div>
      <button className="nav-item settings-item" onClick={() => {}}><Settings2 size={18} /><span>Settings</span></button>
      <div className="sidebar-footer"><span className="online-dot" /> Demo workspace <span className="footer-version">v0.1</span></div>
    </aside>
  </>;
}

function MetricCard({ label, value, change, positive, icon: Icon, tone }: { label: string; value: string; change: string; positive: boolean; icon: typeof Grid2X2; tone: string }) {
  return <div className="metric-card"><div className={`metric-icon ${tone}`}><Icon size={19} /></div><div className="metric-head"><span>{label}</span><button aria-label={`${label} options`}><MoreHorizontal size={18} /></button></div><div className="metric-value">{value}</div><div className="metric-foot"><span className={positive ? "trend-up" : "trend-down"}>{positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}{change}</span><span>vs. last month</span></div></div>;
}

function Overview({ setSection, setProductId, query }: { setSection: (s: Section) => void; setProductId: (id: string) => void; query: string }) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const focusProduct = DEMO_PRODUCTS[0];
  const matchingProducts = DEMO_PRODUCTS.filter((item) => !query || `${item.name} ${item.category}`.toLowerCase().includes(query.toLowerCase()));
  const outstanding = focusProduct.requirements.filter((r) => r.status === "MISSING" || r.status === "REVIEW");
  return <>
    <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line" /> COMPLIANCE OVERVIEW</div><h1>Good morning, Acme <span className="wave">✳</span></h1><p>Here&apos;s your compliance snapshot for today.</p></div><button className="button button-primary" onClick={() => setSection("Products")}><Plus size={16} /> Add a product</button></div>
    <div className="demo-banner"><div className="demo-banner-icon"><Sparkles size={17} /></div><div><strong>You&apos;re exploring a demo workspace</strong><span>All standards, requirements, laboratories and activity below are illustrative sample data.</span></div><DemoTag /></div>
    <section className="metrics-grid">
      <MetricCard label="Tracked products" value="03" change="1 new" positive icon={Package} tone="metric-blue" />
      <MetricCard label="Avg. requirement coverage" value="60%" change="8.2%" positive icon={Activity} tone="metric-violet" />
      <MetricCard label="Open compliance gaps" value="06" change="2 this month" positive={false} icon={FileCheck2} tone="metric-orange" />
      <MetricCard label="Standards to review" value="02" change="1 updated" positive={false} icon={BookOpen} tone="metric-green" />
    </section>
    <div className="content-grid">
      <section className="panel focus-panel"><div className="panel-heading"><div><div className="panel-kicker">YOUR FOCUS</div><h2>Products at a glance</h2></div><button className="text-action" onClick={() => setSection("Products")}>View all <ArrowRight size={15} /></button></div>
        <div className="table-wrap"><table><thead><tr><th>PRODUCT</th><th>STANDARDS</th><th>COVERAGE</th><th>OPEN GAPS</th><th /></tr></thead><tbody>{matchingProducts.map((product) => { const index = DEMO_PRODUCTS.findIndex((item) => item.id === product.id); return <tr key={product.id} className="product-row" onClick={() => { setProductId(product.id); setSection("Products"); }}><td><div className="product-cell"><span className={`product-glyph glyph-${index}`}><Package size={17} /></span><span><b>{product.name}</b><small>{product.category}</small></span></div></td><td><span className="standard-count">{product.standards.length} standards</span></td><td><div className="coverage-cell"><div className="progress-track"><span style={{ width: `${product.requirementCoverage}%` }} /></div><b>{product.requirementCoverage}%</b></div></td><td><span className={`gap-count ${product.openGaps ? "gap-warning" : ""}`}>{String(product.openGaps).padStart(2, "0")}</span></td><td><ChevronRight size={16} className="row-arrow" /></td></tr>; })}</tbody></table>{matchingProducts.length === 0 && <div className="search-hint">No products match “{query}”.</div>}</div>
        <div className="panel-foot"><DemoTag /><span>Last synced just now</span></div>
      </section>
      <section className="panel actions-panel"><div className="panel-heading"><div><div className="panel-kicker">NEEDS YOUR ATTENTION</div><h2>Priority actions <span className="attention-count">{outstanding.length}</span></h2></div><button className="icon-button subtle" aria-label="More actions"><MoreHorizontal size={19} /></button></div>
        <div className="attention-list">{outstanding.slice(0, 4).map((req) => <button className="attention-item" key={req.id} onClick={() => setExpanded(expanded === req.id ? null : req.id)}><span className={`attention-symbol ${req.status === "MISSING" ? "symbol-red" : "symbol-amber"}`}>{req.status === "MISSING" ? <FileText size={16} /> : <Clock3 size={16} />}</span><span className="attention-copy"><b>{req.title}</b><small>{focusProduct.name} <i>·</i> {req.sourceStandard}</small>{expanded === req.id && <em>{req.description}</em>}</span><ChevronRight size={15} className="attention-arrow" /></button>)}</div>
        <button className="all-actions" onClick={() => { setProductId(focusProduct.id); setSection("Products"); }}>Review all requirements <ArrowRight size={14} /></button>
      </section>
    </div>
    <div className="content-grid lower-grid">
      <section className="panel"><div className="panel-heading"><div><div className="panel-kicker">LATEST ACTIVITY</div><h2>Standards &amp; updates</h2></div><button className="text-action" onClick={() => setSection("Updates")}>All updates <ArrowRight size={15} /></button></div><div className="activity-list">{DEMO_UPDATES.slice(0, 3).map((update, i) => <button className="activity-item" key={update.id} onClick={() => setSection("Updates")}><span className={`activity-marker marker-${i}`}><TrendingUp size={15} /></span><span className="activity-copy"><b>{update.title.replace(/^\[DEMO\]\s*/, "")}</b><small>{update.category} <i>·</i> Published {formatDate(update.publishedDate)}</small></span><span className={`status status-${update.impact === "HIGH" ? "red" : update.impact === "MEDIUM" ? "amber" : "green"}`}>{update.impact.toLowerCase()} impact</span></button>)}</div></section>
      <section className="panel lab-preview"><div className="panel-heading"><div><div className="panel-kicker">TESTING NETWORK</div><h2>Nearby laboratories</h2></div><button className="text-action" onClick={() => setSection("Laboratories")}>Explore <ArrowRight size={15} /></button></div><div className="lab-list">{DEMO_LABORATORIES.slice(0, 3).map((lab) => <div className="lab-item" key={lab.id}><span className="lab-icon"><FlaskConical size={17} /></span><span><b>{lab.name.split(" - ")[0]}</b><small>{lab.city}, {lab.state}</small></span><span className="lab-verified"><Check size={12} /> NABL</span></div>)}</div><div className="lab-note">Sample directory for demonstration only</div></section>
    </div>
  </>;
}

function Products({ productId, setProductId, query }: { productId: string; setProductId: (id: string) => void; query: string }) {
  const [filter, setFilter] = useState("All requirements");
  const [openReq, setOpenReq] = useState<string | null>(null);
  const product = DEMO_PRODUCTS.find((item) => item.id === productId) ?? DEMO_PRODUCTS[0];
  const matchingProducts = DEMO_PRODUCTS.filter((item) => !query || `${item.name} ${item.category}`.toLowerCase().includes(query.toLowerCase()));
  const requirements = product.requirements.filter((req) => filter === "All requirements" || (filter === "Open only" ? req.status !== "SATISFIED" && req.status !== "NOT_APPLICABLE" : req.status === filter.toUpperCase()));
  return <>
    <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line" /> PRODUCT COMPLIANCE</div><h1>Your products</h1><p>Track standards, requirements and evidence in one place.</p></div><button className="button button-primary"><Plus size={16} /> Add a product</button></div>
    <div className="demo-banner"><div className="demo-banner-icon"><Sparkles size={17} /></div><div><strong>Illustrative compliance data</strong><span>Check current requirements with official BIS sources before making decisions.</span></div><DemoTag /></div>
    <div className="product-detail-grid"><aside className="panel product-picker"><div className="panel-heading"><div><div className="panel-kicker">PRODUCT PORTFOLIO</div><h2>{matchingProducts.length} products</h2></div><button className="icon-button subtle" aria-label="Add product"><Plus size={18} /></button></div>{matchingProducts.map((item) => { const index = DEMO_PRODUCTS.findIndex((entry) => entry.id === item.id); return <button className={`picker-item ${product.id === item.id ? "picker-selected" : ""}`} onClick={() => { setProductId(item.id); setOpenReq(null); }} key={item.id}><span className={`product-glyph glyph-${index}`}><Package size={17} /></span><span><b>{item.name}</b><small>{item.category}</small><span className="picker-progress"><span style={{ width: `${item.requirementCoverage}%` }} /></span></span><ChevronRight size={15} /></button>; })}{matchingProducts.length === 0 && <div className="search-hint">No matching products.</div>}</aside>
      <section className="panel requirements-panel"><div className="product-summary"><div className="summary-top"><span className="product-glyph glyph-0"><Package size={20} /></span><span className="summary-title"><h2>{product.name}</h2><small>{product.category} <i>·</i> Reviewed {formatDate(product.lastReviewed)}</small></span><button className="button button-secondary compact"><MoreHorizontal size={17} /> Actions</button></div><div className="summary-stats"><div><strong>{product.requirementCoverage}%</strong><small>Coverage</small><span className="summary-track"><i style={{ width: `${product.requirementCoverage}%` }} /></span></div><div><strong>{product.standards.length}</strong><small>Applicable standards</small></div><div><strong>{product.openGaps}</strong><small>Open gaps</small></div></div></div>
        <div className="requirements-head"><div><h3>Requirements <span>{product.requirements.length}</span></h3><p>Review each item and the supporting evidence.</p></div><select value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="Filter requirements"><option>All requirements</option><option>Open only</option><option>Missing</option><option>Review</option><option>Satisfied</option></select></div>
        <div className="requirements-list">{requirements.map((req) => <div className={`requirement-item ${openReq === req.id ? "requirement-open" : ""}`} key={req.id}><button className="requirement-main" onClick={() => setOpenReq(openReq === req.id ? null : req.id)}><span className={`req-check req-${req.status.toLowerCase()}`}>{req.status === "SATISFIED" ? <Check size={14} /> : req.status === "REVIEW" ? <Clock3 size={14} /> : <X size={14} />}</span><span className="req-info"><b>{req.title}</b><small>{req.sourceStandard} <i>·</i> {req.sourceClause}</small></span><span className={statusClass(req.status)}>{getStatusLabel(req.status)}</span><ChevronDown size={16} className="req-chevron" /></button>{openReq === req.id && <div className="requirement-detail"><p>{req.description}</p>{req.evidence ? <div className="evidence-row"><FileCheck2 size={15} /><span><b>{req.evidence.document}</b><small>{req.evidence.section} · {formatDate(req.evidence.date)}</small></span><DemoTag /></div> : <div className="missing-evidence"><FileText size={15} /><span>No evidence attached yet.</span><button onClick={() => {}}>Add evidence</button></div>}</div>}</div>)}</div>
        <div className="standards-chips"><b>Linked standards</b>{product.standards.map((standard) => <span key={standard.id}><BookOpen size={13} /> {standard.number}</span>)}</div>
      </section>
    </div>
  </>;
}

function Directory({ section, query }: { section: Exclude<Section, "Overview" | "Products">; query: string }) {
  const q = query.trim().toLowerCase();
  const standards = useMemo(() => DEMO_STANDARDS.filter((item) => !q || `${item.number} ${item.title} ${item.category}`.toLowerCase().includes(q)), [q]);
  const labs = useMemo(() => DEMO_LABORATORIES.filter((item) => !q || `${item.name} ${item.city} ${item.state} ${item.testsOffered.join(" ")}`.toLowerCase().includes(q)), [q]);
  const updates = useMemo(() => DEMO_UPDATES.filter((item) => !q || `${item.title} ${item.category} ${item.summary}`.toLowerCase().includes(q)), [q]);
  const services = useMemo(() => BIS_SERVICES.filter((item) => !q || `${item.title} ${item.description} ${item.who}`.toLowerCase().includes(q)), [q]);
  const config = {
    Standards: { eyebrow: "STANDARDS LIBRARY", title: "Standards to know", subtitle: "Browse the standards linked to your product portfolio.", count: standards.length, noun: "standards" },
    Laboratories: { eyebrow: "TESTING NETWORK", title: "Find a laboratory", subtitle: "Explore sample testing locations and capabilities.", count: labs.length, noun: "laboratories" },
    Updates: { eyebrow: "REGULATORY WATCH", title: "Standards & updates", subtitle: "Keep an eye on sample changes that may affect your products.", count: updates.length, noun: "updates" },
    "BIS services": { eyebrow: "BIS DIRECTORY", title: "Services & support", subtitle: "A starting point for finding BIS service information.", count: services.length, noun: "services" },
  }[section];
  return <><div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line" /> {config.eyebrow}</div><h1>{config.title}</h1><p>{config.subtitle}</p></div></div><div className="demo-banner"><div className="demo-banner-icon"><Sparkles size={17} /></div><div><strong>Sample directory content</strong><span>Details are illustrative. Confirm current information through official BIS and accreditation sources.</span></div><DemoTag /></div>
    <div className="directory-toolbar"><div className="directory-count">{config.count} {config.noun} <span>·</span> Demo workspace</div><button className="button button-secondary compact"><Settings2 size={15} /> Filter <ChevronDown size={14} /></button></div>
    {section === "Standards" && <div className="directory-grid">{standards.map((s) => <article className="panel directory-card" key={s.id}><div className="directory-card-head"><span className="directory-icon standards-icon"><BookOpen size={18} /></span><span className={statusClass(s.status)}>{s.status.replace("-", " ")}</span></div><div className="standard-id">{s.number}</div><h2>{s.title}</h2><p>{s.category} <i>·</i> {s.type}</p><div className="directory-card-foot"><DemoTag /><button className="icon-button subtle" aria-label={`More about ${s.number}`}><ArrowRight size={16} /></button></div></article>)}</div>}
    {section === "Laboratories" && <div className="directory-grid">{labs.map((lab) => <article className="panel directory-card" key={lab.id}><div className="directory-card-head"><span className="directory-icon lab-directory-icon"><FlaskConical size={18} /></span><span className="lab-verified"><Check size={12} /> {lab.accreditation}</span></div><h2>{lab.name}</h2><p>{lab.location}</p><div className="test-tags">{lab.testsOffered.slice(0, 3).map((test) => <span key={test}>{test}</span>)}{lab.testsOffered.length > 3 && <span>+{lab.testsOffered.length - 3}</span>}</div><div className="directory-card-foot"><DemoTag /><span className="lab-contact">{lab.contact}</span></div></article>)}</div>}
    {section === "Updates" && <div className="updates-list">{updates.map((update) => <article className="panel update-card" key={update.id}><span className="update-date"><small>{new Date(`${update.publishedDate}T00:00:00`).toLocaleDateString("en-IN", { month: "short" })}</small><b>{new Date(`${update.publishedDate}T00:00:00`).getDate()}</b></span><div className="update-body"><div className="update-meta"><span>{update.category}</span><span>Published {formatDate(update.publishedDate)}</span><span className={`status status-${update.impact === "HIGH" ? "red" : update.impact === "MEDIUM" ? "amber" : "green"}`}>{update.impact} impact</span></div><h2>{update.title}</h2><p>{update.summary}</p><div className="update-affected"><b>Affected:</b> {update.affectedProducts.join(", ")} <i>·</i> Effective {formatDate(update.effectiveDate)}</div><DemoTag /></div></article>)}</div>}
    {section === "BIS services" && <div className="directory-grid services-grid">{services.map((service) => <article className="panel directory-card service-card" key={service.id}><span className="directory-icon standards-icon"><Award size={18} /></span><h2>{service.title}</h2><p>{service.description}</p><div className="service-detail"><b>Who it helps</b><span>{service.who}</span></div><div className="service-detail"><b>How to get started</b><span>{service.how}</span></div><div className="directory-card-foot"><DemoTag /><a href={service.link} target="_blank" rel="noreferrer">Visit BIS <ArrowUpRight size={14} /></a></div></article>)}</div>}
    {config.count === 0 && <div className="empty-state"><Search size={25} /><h2>No matches found</h2><p>Try another search term.</p></div>}
  </>;
}

export default function Home() {
  const [section, setSection] = useState<Section>("Overview");
  const [productId, setProductId] = useState(DEMO_PRODUCTS[0].id);
  const [query, setQuery] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const isDirectory = section !== "Overview" && section !== "Products";
  const filteredProductCount = DEMO_PRODUCTS.filter((product) => !query || `${product.name} ${product.category}`.toLowerCase().includes(query.toLowerCase())).length;
  return <div className="app-shell"><Sidebar section={section} setSection={setSection} open={menuOpen} close={() => setMenuOpen(false)} /><main className="main-area"><Header section={section} query={query} setQuery={setQuery} onMenu={() => setMenuOpen(true)} /><div className="page-content">{section === "Overview" && <Overview setSection={setSection} setProductId={setProductId} query={query} />}{section === "Products" && <Products productId={productId} setProductId={setProductId} query={query} />}{isDirectory && <Directory section={section as Exclude<Section, "Overview" | "Products">} query={query} />}{query && section === "Products" && filteredProductCount === 0 && <div className="search-hint">No products match “{query}”.</div>}</div><footer className="app-footer"><span>SAKSHAM <i>·</i> BIS compliance workspace</span><span><CircleHelp size={14} /> Help centre <i>·</i> All data is illustrative demo content</span></footer></main></div>;
}
