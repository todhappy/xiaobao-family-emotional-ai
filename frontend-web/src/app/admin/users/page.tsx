import useFetch from "@/hooks/useFetch"
import { listUsers } from "@/services/admin"
import GlassCard from "@/components/GlassCard"

export default function Page() {
  const { data } = useFetch(listUsers, [])
  const items = Array.isArray(data) ? data : []
  return (
    <div className="grid gap-4">
      <div className="title">用户列表</div>
      <GlassCard>
        <table className="w-full text-sm">
          <thead><tr><th className="text-left">昵称</th><th className="text-left">来源</th><th className="text-left">最近活跃</th></tr></thead>
          <tbody>
            {items.map((u: any, i: number) => (
              <tr key={i} className="border-b border-white/10"><td>{u.nickname}</td><td>{u.source}</td><td>{u.lastActive}</td></tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  )
}