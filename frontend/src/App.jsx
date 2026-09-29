import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AppProvider } from './context/AppContext.jsx';

// Layout
import Navbar from './components/layout/Navbar.jsx';
import Footer from './components/layout/Footer.jsx';
import ToastSystem from './components/layout/ToastSystem.jsx';
import CommandPalette from './components/layout/CommandPalette.jsx';
import AskSaksham from './components/ai/AskSaksham.jsx';

// Pages
import LandingPage from './pages/LandingPage.jsx';
import ProductAnalysisPage from './pages/ProductAnalysisPage.jsx';
import CompliancePassportPage from './pages/CompliancePassportPage.jsx';
import BOMAnalyzerPage from './pages/BOMAnalyzerPage.jsx';
import DocumentIntelligencePage from './pages/DocumentIntelligencePage.jsx';
import TestLabOptimizerPage from './pages/TestLabOptimizerPage.jsx';
import ChangeImpactPage from './pages/ChangeImpactPage.jsx';
import StandardsExplorerPage from './pages/StandardsExplorerPage.jsx';
import BISServicesPage from './pages/BISServicesPage.jsx';
import UpdatesDashboardPage from './pages/UpdatesDashboardPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';

// Scroll to top on navigation
function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return null;
}

function AppShell() {
  return (
    <div className="min-h-screen bg-surface flex flex-col">
      <ScrollToTop />
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/analyze" element={<ProductAnalysisPage />} />
          <Route path="/compliance/:productId" element={<CompliancePassportPage />} />
          <Route path="/compliance" element={<CompliancePassportPage />} />
          <Route path="/bom" element={<BOMAnalyzerPage />} />
          <Route path="/documents" element={<DocumentIntelligencePage />} />
          <Route path="/labs" element={<TestLabOptimizerPage />} />
          <Route path="/changes" element={<ChangeImpactPage />} />
          <Route path="/standards" element={<StandardsExplorerPage />} />
          <Route path="/services" element={<BISServicesPage />} />
          <Route path="/updates" element={<UpdatesDashboardPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
      <Footer />
      {/* Global Overlays */}
      <ToastSystem />
      <CommandPalette />
      <AskSaksham />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <AppShell />
      </AppProvider>
    </BrowserRouter>
  );
}
