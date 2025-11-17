import Link from "next/link"
import GlassCard from "@/components/GlassCard"

export default function Page() {
  return (
    <div className="grid gap-4">
      <div className="title">管理员后台</div>
      <div className="grid-cards">
        <GlassCard><Link href="/admin/modules-check" className="btn">核心模块状态</Link></GlassCard>
        <GlassCard><Link href="/admin/logs" className="btn">系统日志</Link></GlassCard>
        <GlassCard><Link href="/admin/mcp-stats" className="btn">MCP 调用统计</Link></GlassCard>
        <GlassCard><Link href="/admin/users" className="btn">用户列表</Link></GlassCard>
      </div>
    </div>
  )
}