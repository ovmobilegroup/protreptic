/** @type {import('tailwindcss').Config} */
// 所有核心颜色经由 CSS 变量（style.css 的 :root / [data-theme="light"] 定义），
// 因此切换 data-theme 即可整体换肤（深墨 ↔ 浅色）。
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // 墨 — 基底（页底 / 面板 / 输入）
        ink: {
          950: 'rgb(var(--pt-ink-950) / <alpha-value>)',
          900: 'rgb(var(--pt-ink-900) / <alpha-value>)',
          850: 'rgb(var(--pt-ink-850) / <alpha-value>)',
          800: 'rgb(var(--pt-ink-800) / <alpha-value>)',
          700: 'rgb(var(--pt-ink-700) / <alpha-value>)',
          600: 'rgb(var(--pt-ink-600) / <alpha-value>)',
        },
        // 金 — 主强调（典藏 / 智慧）
        gold: {
          200: 'rgb(var(--pt-gold-200) / <alpha-value>)',
          300: 'rgb(var(--pt-gold-300) / <alpha-value>)',
          400: 'rgb(var(--pt-gold-400) / <alpha-value>)',
          500: 'rgb(var(--pt-gold-500) / <alpha-value>)',
          600: 'rgb(var(--pt-gold-600) / <alpha-value>)',
          700: 'rgb(var(--pt-gold-700) / <alpha-value>)',
        },
        // 玉 — 次强调
        jade: {
          300: 'rgb(var(--pt-jade-300) / <alpha-value>)',
          400: 'rgb(var(--pt-jade-400) / <alpha-value>)',
          500: 'rgb(var(--pt-jade-500) / <alpha-value>)',
          600: 'rgb(var(--pt-jade-600) / <alpha-value>)',
        },
        // 正文前景
        parchment: 'rgb(var(--pt-parchment) / <alpha-value>)',
        // 叠加层：深色主题=白（提亮），浅色主题=黑（压暗）。组件里统一用 white/10 这类写法。
        white: 'rgb(var(--pt-overlay) / <alpha-value>)',
        black: 'rgb(var(--pt-shadow) / <alpha-value>)',
        // 金底上的固定深色字（按钮/徽记），不随主题翻转
        obsidian: '#0a0c11',
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
