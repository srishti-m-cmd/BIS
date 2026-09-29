import React, { createContext, useContext, useState, useCallback } from 'react';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  // ─── User Mode ───────────────────────────────────────────────────────────────
  const [userMode, setUserMode] = useState('industry'); // 'industry' | 'consumer'

  // ─── Active Product ───────────────────────────────────────────────────────────
  const [activeProduct, setActiveProduct] = useState(null);

  // ─── Language ─────────────────────────────────────────────────────────────────
  const [language, setLanguage] = useState('en'); // 'en' | 'hi'

  // ─── Toast System ─────────────────────────────────────────────────────────────
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback(({ message, type = 'info', duration = 4000 }) => {
    const id = Date.now() + Math.random();
    setToasts(prev => [...prev, { id, message, type, duration }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, duration);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  // ─── Command Palette ──────────────────────────────────────────────────────────
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // ─── Saved Products ───────────────────────────────────────────────────────────
  const [savedProducts, setSavedProducts] = useState([
    { id: 'PROD-001', name: 'Electric Storage Water Heater', evidenceCompletion: 50, openGaps: 3, lastReviewed: '2024-03-15' },
  ]);

  const saveProduct = useCallback((product) => {
    setSavedProducts(prev => {
      const exists = prev.find(p => p.id === product.id);
      if (exists) return prev;
      return [...prev, {
        id: product.id,
        name: product.name,
        evidenceCompletion: product.complianceSummary?.evidenceCompletion || 0,
        openGaps: product.complianceSummary?.openGaps || 0,
        lastReviewed: product.lastReviewed || new Date().toISOString().split('T')[0],
      }];
    });
  }, []);

  // ─── Ask SAKSHAM Panel ────────────────────────────────────────────────────────
  const [isAskSakshamOpen, setIsAskSakshamOpen] = useState(false);

  const value = {
    // Mode
    userMode, setUserMode,
    // Product
    activeProduct, setActiveProduct,
    // Language
    language, setLanguage,
    // Toasts
    toasts, addToast, removeToast,
    // Command Palette
    isCommandPaletteOpen, setIsCommandPaletteOpen,
    // Saved Products
    savedProducts, saveProduct,
    // AI Panel
    isAskSakshamOpen, setIsAskSakshamOpen,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
