import { useEffect, useState } from "react"
import { api } from "@/services/api"
import GlassCard from "@/components/GlassCard"

export default function QRLogin() {
  const [img, setImg] = useState<string>("")
  const [scene, setScene] = useState<string>("")
  const [status, setStatus] = useState<string>("pending")
  useEffect(() => {
    api.get("/auth/qrcode").then(r => { setImg(r.data.qr); setScene(r.data.scene) }).catch(() => { setImg(""); setScene("") })
  }, [])
  useEffect(() => {
    if (!scene) return
    const t = setInterval(() => {
      api.get(`/auth/status/${scene}`).then(r => { setStatus(r.data.status); if (r.data.status === "confirmed") { clearInterval(t); location.href = "/dashboard" } }).catch(() => {})
    }, 2000)
    return () => clearInterval(t)
  }, [scene])
  return (
    <GlassCard className="max-w-sm mx-auto text-center">
      <div className="title mb-2">微信扫码登录</div>
      {img ? <img src={img} alt="qr" className="mx-auto w-48 h-48 rounded-xl" /> : <div className="h-48" />}
      <div className="mt-2 subtitle">状态 {status}</div>
    </GlassCard>
  )
}