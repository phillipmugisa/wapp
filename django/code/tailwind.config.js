/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './TEMPLATES/*html',
    './TEMPLATES/manager/*html',
    './TEMPLATES/payments/*html',
    './TEMPLATES/utils/*html',
    './TEMPLATES/whatsapp/*html',
    './TEMPLATES/account/*html',
    './TEMPLATES/account/socialaccount/*html',
    './venv/lib/python3.9/site-packages/allauth/templates/socialaccount',
  ],
  theme: {
    screens: {
        sm: '480px',
        md: '768px',
        lg: '976px',
        xl: '1440px',
    },
    extend: {
      colors: {
        clifford: '#da373d',
        accent: "hsla(182, 100%, 20%, 0.8)",
        dark: "hsl(0, 1%, 15%)",
        "dark-200": "#1F2937",
        backColor: "#b8ffe8"
      },
      gridTemplateColumns: {
        'dash': '1fr 5fr',
        'whatspp-lg': '1fr 2fr',
        'whatspp-md': '1fr 1fr',
        'whatspp-sm': '1fr',
      }
    }
  },
  plugins: [],
}
