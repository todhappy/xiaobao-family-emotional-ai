import GlassCard from "@/components/GlassCard"
import Graph3D from "@/components/Graph3D"

export default function Page() {
  return (
    <div className="grid gap-4">
      <div className="title">家庭关系图谱</div>
      <GlassCard>
        <Graph3D />
      </GlassCard>
    </div>
  )
}