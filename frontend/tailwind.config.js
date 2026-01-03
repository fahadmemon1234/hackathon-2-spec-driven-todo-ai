/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        zinc: {
          950: '#0a0a0a',
        },
        slate: {
          50: '#f8fafc',
        },
        indigo: {
          500: '#6366f1',
        },
        brandDark: '#252525',
        brandRed: '#d90429',
        brandGold: '#f6d72d',
        surface: '#F8F9FA',
        corporate: {
          background: '#FFFFFF',
          surface: '#FFFFFF',
          border: 'rgba(37, 37, 37, 0.1)',
          accent: {
            crimson: '#d90429',       // Action Crimson
            gold: '#f6d72d',          // Accent Gold
          },
          text: {
            primary: '#252525',       // Dark Charcoal
            secondary: '#71717A',     // Zinc
          },
          status: {
            completed: '#10B981',     // Emerald for done
            pending: '#F59E0B',       // Amber for pending
          }
        }
      },
      fontFamily: {
        sans: ['Inter', 'Geist Sans', 'sans-serif'],
      },
      boxShadow: {
        'professional': '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.3)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.1)',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        }
      },
      animation: {
        shimmer: 'shimmer 2s infinite',
      }
    },
  },
  plugins: [],
}