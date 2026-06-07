/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        ink: '#090b10',
        panel: '#11141b',
        line: '#252a35',
        mist: '#939baa',
        signal: '#b7f36b',
        violet: '#a78bfa',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        phone: '0 30px 90px rgba(0,0,0,.55)',
      },
    },
  },
  plugins: [],
}
