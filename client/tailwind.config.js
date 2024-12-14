/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#90caf9',
        secondary: '#f48fb1',
        background: {
          DEFAULT: '#121212',
          paper: '#1d1d1d',
        },
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true,
  }
}

