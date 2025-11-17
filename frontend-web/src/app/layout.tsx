import "./globals.css"
import { ReactNode } from "react"
import NavBar from "@/components/NavBar"

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <NavBar />
        <main className="p-6">{children}</main>
      </body>
    </html>
  )
}