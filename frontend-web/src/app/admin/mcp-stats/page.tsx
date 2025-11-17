import useFetch from "@/hooks/useFetch"
import { getMcpStats } from "@/services/admin"
import ChartPie from "@/components/ChartPie"
import GlassCard from "@/components/GlassCard"

export default function Page() {
  const { data } = useFetch(getMcpStats, [])
  const items = Array.isArray(data) ? data : []
  return (
    <div className="grid gap-4">
      <div className="title">MCP 服务调用统计</div>
      <GlassCard>
        <ChartPie data={items.map((x: any) => ({ name: x.name, value: x.count }))} />
      </GlassCard>
    </div>
  )
}