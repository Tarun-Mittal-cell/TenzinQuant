/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Custom color palette inspired by Elon Musk's design aesthetics
        quantum: {
          primary: '#1DB954',    // Vibrant green for primary actions
          secondary: '#1E1E1E',  // Dark gray for secondary elements
          accent: '#FF4B4B',     // Red for alerts and important info
          dark: {
            100: '#2A2A2A',
            200: '#1E1E1E',
            300: '#171717',
            400: '#121212',
            500: '#0A0A0A',
          },
          light: {
            100: '#FFFFFF',
            200: '#F5F5F5',
            300: '#E5E5E5',
            400: '#D4D4D4',
            500: '#A3A3A3',
          }
        }
      },
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgb(29, 185, 84, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgb(29, 185, 84, 0.9)' }
        }
      }
    },
  },
  plugins: [],
}