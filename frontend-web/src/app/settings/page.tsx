import GlassCard from "@/components/GlassCard"

export default function Page() {
  return (
    <div className="grid gap-4 max-w-2xl">
      <div className="title">偏好设置</div>
      <GlassCard>
        <div className="grid gap-3">
          <div className="grid grid-cols-3 items-center"><div className="subtitle">主题色</div><input type="color" defaultValue="#3A86FF" className="col-span-2" /></div>
          <div className="grid grid-cols-3 items-center"><div className="subtitle">老人模式</div><input type="checkbox" /></div>
        </div>
      </GlassCard>
    </div>
  )
}