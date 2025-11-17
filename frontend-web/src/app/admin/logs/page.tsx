import useFetch from "@/hooks/useFetch"
import { getLogs } from "@/services/admin"
import GlassCard from "@/components/GlassCard"

export default function Page() {
  const { data } = useFetch(getLogs, [])
  const items = Array.isArray(data?.items) ? data?.items : []
  return (
    <div className="grid gap-4">
      <div className="title">系统日志</div>
      <div className="grid gap-2">
        {items.map((it: any, i: number) => (
          <GlassCard key={i}><div className="flex justify-between"><div>{it.message}</div><div className="subtitle">{it.module}</div></div></GlassCard>
        ))}
      </div>
    </div>
  )
}