/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      filter: ['responsive', 'hover'],
      colors: {
        primary: {
          "50":"#f5f3ff",
          "100":"#ede9fe",
          "200":"#ddd6fe",
          "300":"#c4b5fd",
          "400":"#a78bfa",
          "500":"#8b5cf6",
          "600":"#7c3aed",
          "700":"#6d28d9",
          "800":"#5b21b6",
          "900":"#4c1d95",
          "950":"#2e1065"
        },
        background: "#ffffff",
      }
    },
    fontFamily: {
      'body': [
        'Inter',
        'ui-sans-serif',
        'system-ui',
        '-apple-system',
        'system-ui',
        'Segoe UI',
        'Roboto',
        'Helvetica Neue',
        'Arial',
        'Noto Sans',
        'sans-serif',
        'Apple Color Emoji',
        'Segoe UI Emoji',
        'Segoe UI Symbol',
        'Noto Color Emoji'
      ],
      'sans': [
        'Inter',
        'ui-sans-serif',
        'system-ui',
        '-apple-system',
        'system-ui',
        'Segoe UI',
        'Roboto',
        'Helvetica Neue',
        'Arial',
        'Noto Sans',
        'sans-serif',
        'Apple Color Emoji',
        'Segoe UI Emoji',
        'Segoe UI Symbol',
        'Noto Color Emoji'
      ]
    }
  },
  plugins: [
    require('flowbite/plugin')({
      charts: true,
    })
  ],
}

