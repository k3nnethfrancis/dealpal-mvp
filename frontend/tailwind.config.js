module.exports = {
  content: ['./frontend/**/*.{js,jsx,ts,tsx}', './public/index.html', './pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'primary': '#1B9AAA', // Lilac
        'secondary': '#DDDBCB', // Tropical Indigo
        'background': '#40434E', // Space Gray
        'neutral': {
          '200': '#2d3748', // Darker Gray
          '300': '#DDDBCB', // Medium Gray
          '900': '#F5F1E3', // Light Gray
        },  
      },
      fontFamily: {
        'retro': ['"Orbitron"', 'sans-serif'],
      },
      boxShadow: {
        'neon-pink': '0 0 10px #FF4081, 0 0 20px #FF4081, 0 0 30px #FF4081',
        'neon-blue': '0 0 10px #1E90FF, 0 0 20px #1E90FF, 0 0 30px #1E90FF',
      },
    },
  },
  plugins: [],
};