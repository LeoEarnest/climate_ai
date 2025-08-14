/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/app/**/*.{ts,tsx,js,jsx}',
    './src/pages/**/*.{ts,tsx,js,jsx}',
    './src/components/**/*.{ts,tsx,js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary:    'rgb(138, 240, 244)',
        surface:    'rgb(37, 38, 40)',
        'surface-2':'rgb(246, 191, 199)',
        glass:      'rgba(255,255,255,0.075)',
        temp: {
          low:     '#a7d7d9',
          medium:  '#c2ccc6',
          high:    '#d9c5c8',
          extreme: '#f6bfc7',
        },
      },
      fontFamily: {
        display: ['"Droid Sans Mono"', 'monospace'],
        sans:    ['"Space Grotesk"', 'sans-serif'],
        alt:     ['"IBM Plex Mono"', 'monospace'],
      },
      fontSize: {
        display: ['7rem', { lineHeight: '1.2' }],
      },
      dropShadow: {
        glow: '0 0 10px rgba(121,129,130,0.6)',
      },
      // 如果需要自訂 borderWidth 或 borderColor，可在這裡 extend：
      // borderWidth: { DEFAULT: '1px', '3': '3px' },
      // borderColor: { DEFAULT: 'currentColor', primary: 'rgb(138,240,244)' },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
