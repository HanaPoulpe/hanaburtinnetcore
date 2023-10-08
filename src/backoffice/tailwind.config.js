/** @type {import('tailwindcss').Config} */

module.exports = {
  purge: [
      './static/*.htnl',
      '.static/**/*.js',
  ],
  darkMode: false,
  content: [
    './pages/**/*.{html,js}',
    './components/**/*.{html,js}',
  ],
  theme: {
    colors: {}
  },
  plugins: [],
};
