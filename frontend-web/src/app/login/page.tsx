import QRLogin from "@/components/QRLogin"

export default function Page() {
  return (
    <div className="grid gap-4 max-w-4xl mx-auto">
      <div className="title">登录</div>
      <QRLogin />
    </div>
  )
}