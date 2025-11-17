import { ReactNode } from "react"

export default function GlassCard({ children, className }: { children: ReactNode, className?: string }) {
  return <div className={["glass rounded-2xl p-4", className || ""].join(" ")}>{children}</div>
}