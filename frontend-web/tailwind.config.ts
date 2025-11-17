import type { Config } from "tailwindcss"

export default {
  content: [
    "./src/app/**/*.{ts,tsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/hooks/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#3A86FF"
      },
      boxShadow: {
        holo: "0 8px 40px rgba(58,134,255,0.25)"
      }
    }
  },
  plugins: []
} satisfies Config