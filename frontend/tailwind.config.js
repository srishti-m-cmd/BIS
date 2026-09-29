/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // BIS SAKSHAM Design System
        navy: {
          50:  '#EEF2F7',
          100: '#D5E0EE',
          200: '#AABFDC',
          300: '#7F9DC9',
          400: '#547CB7',
          500: '#2A5BA4',
          600: '#1A3E72',
          700: '#122D55',
          800: '#0D2040',
          900: '#0B1F3A',  // PRIMARY NAVY
          950: '#071528',
        },
        saffron: {
          50:  '#FFFBEB',
          100: '#FEF3C7',
          200: '#FDE68A',
          300: '#FCD34D',
          400: '#FBBF24',
          500: '#F59E0B',  // PRIMARY SAFFRON
          600: '#D97706',
          700: '#B45309',
          800: '#92400E',
          900: '#78350F',
        },
        gov: {
          green:   '#16834B',
          success: '#16834B',
          warning: '#D97706',
          danger:  '#C0392B',
        },
        ai: {
          DEFAULT: '#4F46E5',  // AI ACCENT
          50:  '#EEEFFE',
          100: '#E0E1FC',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
        },
        // Semantic
        surface: '#F7F8FA',   // Background
        card:    '#FFFFFF',
        border:  '#E2E8F0',
        'text-primary':   '#111827',
        'text-secondary': '#64748B',
        'text-muted':     '#94A3B8',
      },
      fontFamily: {
        sans:      ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        devanagari: ['Noto Sans Devanagari', 'sans-serif'],
      },
      fontSize: {
        'display-xl': ['3.5rem',  { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '700' }],
        'display-lg': ['2.75rem', { lineHeight: '1.15', letterSpacing: '-0.02em', fontWeight: '700' }],
        'display-md': ['2rem',    { lineHeight: '1.2', letterSpacing: '-0.015em', fontWeight: '600' }],
      },
      animation: {
        'pulse-slow':   'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float':        'float 6s ease-in-out infinite',
        'node-pulse':   'nodePulse 2s ease-in-out infinite',
        'flow-dash':    'flowDash 2s linear infinite',
        'fade-in-up':   'fadeInUp 0.5s ease-out forwards',
        'slide-right':  'slideRight 0.4s ease-out forwards',
        'shimmer':      'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-8px)' },
        },
        nodePulse: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(79, 70, 229, 0.3)' },
          '50%':      { boxShadow: '0 0 0 8px rgba(79, 70, 229, 0)' },
        },
        flowDash: {
          '0%':   { strokeDashoffset: '100' },
          '100%': { strokeDashoffset: '0' },
        },
        fadeInUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideRight: {
          '0%':   { opacity: '0', transform: 'translateX(-16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      boxShadow: {
        'card':      '0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.06)',
        'card-md':   '0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.07)',
        'card-lg':   '0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.08)',
        'navy':      '0 4px 24px -4px rgba(11,31,58,0.25)',
        'ai':        '0 4px 24px -4px rgba(79,70,229,0.2)',
        'saffron':   '0 4px 24px -4px rgba(245,158,11,0.25)',
      },
      borderRadius: {
        'xl2': '1rem',
        'xl3': '1.5rem',
      },
    },
  },
  plugins: [],
}
