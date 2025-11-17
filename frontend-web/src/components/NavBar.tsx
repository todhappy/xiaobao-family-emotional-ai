import Link from "next/link"
import clsx from "clsx"

export default function NavBar() {
  const link = (href: string, text: string) => (
    <Link href={href} className={clsx("px-3 py-2 rounded-lg", "hover:bg-white/10")}>{text}</Link>
  )
  return (
    <div className="glass flex items-center justify-between px-4 py-3">
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-full bg-primary/60" />
        <div className="font-semibold">孝宝·小智</div>
      </div>
      <div className="flex items-center gap-1">
        {link("/login", "登录")}
        {link("/dashboard", "首页")}
        {link("/family-map", "图谱")}
        {link("/memory-timeline", "时间轴")}
        {link("/chat", "聊天")}
        {link("/settings", "设置")}
        {link("/admin", "管理员")}
      </div>
    </div>
  )
}