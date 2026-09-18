/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 墨 — 基底
        ink: {
          950: '#04060c',
          900: '#080c16',
          850: '#0c1220',
          800: '#111a2b',
          700: '#182338',
          600: '#22304a',
        },
        // 金 — 主强调（典藏 / 智慧）
        gold: {
          200: '#f7e6c0',
          300: '#f0d79f',
          400: '#e4bd74',
          500: '#d4a24c',
          600: '#b8843a',
          700: '#8f6529',
        },
        // 玉 — 次强调
        jade: {
          300: '#8ff0dd',
          400: '#5eead4',
          500: '#2fd4b8',
          600: '#14b8a6',
        },
        parchment: '#f3ece0',
      },
      fontFamily: {
        display: ['"Noto Serif SC"', '"Source Han Serif SC"', '"Songti SC"', 'STSong', 'SimSun', 'Georgia', 'serif'],
        sans: ['system-ui', '-apple-system', '"PingFang SC"', '"Hiragino Sans GB"', '"Microsoft YaHei"', '"Noto Sans SC"', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace'],
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(212,162,76,.25), 0 12px 40px -12px rgba(212,162,76,.35)',
        'glow-jade': '0 0 0 1px rgba(94,234,212,.25), 0 12px 40px -12px rgba(94,234,212,.3)',
        card: '0 1px 0 0 rgba(255,255,255,.04) inset, 0 20px 40px -24px rgba(0,0,0,.9)',
      },
      backgroundImage: {
        'radial-gold': 'radial-gradient(circle at 50% 0%, rgba(212,162,76,.18), transparent 60%)',
        'radial-jade': 'radial-gradient(circle at 80% 20%, rgba(94,234,212,.12), transparent 55%)',
        'gold-line': 'linear-gradient(90deg, transparent, rgba(212,162,76,.6), transparent)',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        'glow-pulse': {
          '0%,100%': { opacity: '.5' },
          '50%': { opacity: '1' },
        },
        float: {
          '0%,100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
      },
      animation: {
        'fade-up': 'fade-up .5s cubic-bezier(.2,.7,.3,1) both',
        shimmer: 'shimmer 1.6s linear infinite',
        'glow-pulse': 'glow-pulse 3.5s ease-in-out infinite',
        float: 'float 6s ease-in-out infinite',
      },
      transitionTimingFunction: {
        silk: 'cubic-bezier(.2,.7,.3,1)',
      },
    },
  },
  plugins: [],
}
