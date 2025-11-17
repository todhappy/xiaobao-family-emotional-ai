import useFetch from "@/hooks/useFetch"
import { getModules } from "@/services/admin"
import GlassCard from "@/components/GlassCard"

export default function Page() {
  const { data } = useFetch(getModules, [])
  const items = Array.isArray(data) ? data : []
  return (
    <div className="grid gap-4">
      <div className="title">八大核心模块状态</div>
      <GlassCard>
        <table className="w-full text-sm">
          <thead><tr><th className="text-left">模块</th><th className="text-left">状态</th><th className="text-left">最近时间</th><th className="text-left">日志</th></tr></thead>
          <tbody>
            {items.map((it: any, i: number) => (
              <tr key={i} className="border-b border-white/10"><td>{it.name}</td><td>{it.status}</td><td>{it.time}</td><td>{it.lastLog}</td></tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  )
}