/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
                'wave-1': 'wave 1s ease-in-out infinite',
                'wave-2': 'wave 1s ease-in-out infinite 0.1s',
                'wave-3': 'wave 1s ease-in-out infinite 0.2s',
            },
            keyframes: {
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                wave: {
                    '0%, 100%': { height: '10px' },
                    '50%': { height: '24px' },
                }
            }
        },
    },
    plugins: [],
}
