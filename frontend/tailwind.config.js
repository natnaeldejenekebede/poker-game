// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}', // Includes page.tsx, layout.tsx, components
    './src/components/**/*.{js,ts,jsx,tsx,mdx}', // In case you add components outside app/
  ],
  theme: {
    extend: {
      colors: {
        'gray-900': '#1a202c',
        'gray-100': '#e2e8f0',
        'green-900': '#1a202c',
        'green-700': '#2d3748',
        'yellow-300': '#f6e05e',
      },
    },
  },
  plugins: [],
};