/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./main/templates/main/*.html'],
  theme: {
    extend: {
      colors :{
        'index-color' : {
          'purple' : '#C51E8C',
          'hover' : '#1F0739',
          'p' : '#FE2FD7'
        },
      },
    },
  },
  plugins: [],
}

