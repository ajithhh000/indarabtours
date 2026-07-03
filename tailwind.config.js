/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        primary:       '#01506E',
        'primary-dark':'#013C54',
        secondary:     '#5FA8C7',
        accent:        '#D4AF37',
        background:    '#FFFFFF',
        surface:       '#F4F8FA',
        'text-primary':  '#1F2A33',
        'text-secondary':'#5A6B73',
        success:       '#2F9E63',
        warning:       '#D69E2E',
        error:         '#E5484D'
      },
      fontFamily: {
        body:     ['"Source Sans Pro"', 'sans-serif'],
        heading:  ['"Playfair Display"', 'serif'],
        cta:      ['Montserrat', 'sans-serif']
      }
    }
  },
  plugins: []
};