import GlassCard from "@/components/GlassCard"
import useFetch from "@/hooks/useFetch"
import { getFamily } from "@/services/family"
import ChartLine from "@/components/ChartLine"

export default function Page() {
  const { data } = useFetch(getFamily, [])
  return (
    <div className="grid gap-4">
      <div className="title">家庭记忆库</div>
      <div className="grid-cards">
        <GlassCard>
          <div className="subtitle">今日建议</div>
          <div className="mt-2">保持沟通与陪伴</div>
        </GlassCard>
        <GlassCard>
          <div className="subtitle">家庭成员</div>
          <div className="mt-2">{Array.isArray(data?.members) ? data?.members.length : 0}</div>
        </GlassCard>
        <GlassCard>
          <div className="subtitle">活跃度</div>
          <ChartLine series={[5,8,12,9,7,10,13,12,11,9]} />
        </GlassCard>
      </div>
    </div>
  )
}