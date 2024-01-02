/** @type {import('tailwindcss').Config} */

const { createThemes } = require('tw-colors');

module.exports = {
  content: [
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    createThemes({
      hanaburtin: {
        'primary': '#b27eca',
        'secondary': '#a9eae5',
        'brand': '#7b3499',
      },
      strict: true,
      produceThemeClass: (themeName) => `theme-${themeName}`,
    })
  ],
};
