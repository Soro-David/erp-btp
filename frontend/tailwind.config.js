/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          sidebar: '#0f294a',       // Bleu profond BTP pour la Sidebar
          'sidebar-hover': '#163b66',
          'sidebar-active': '#1d4ed8', // Bleu royal surbrillance active
          nav: '#047857',           // Vert professionnel pour la Navbar
          'nav-hover': '#065f46',
          primary: '#1d4ed8',       // Bleu boutons principaux
          'primary-hover': '#1e40af',
          secondary: '#64748b',     // Gris boutons secondaires
          'secondary-hover': '#475569',
          'secondary-light': '#f1f5f9',
          bg: '#f8fafc',            // Fond blanc / gris très clair
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
