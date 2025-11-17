import GlassCard from "@/components/GlassCard"

export default function MemoryItem({ item }: { item: any }) {
  return (
    <GlassCard>
      <div className="flex items-center justify-between">
        <div>
          <div className="font-semibold">{item.title}</div>
          <div className="subtitle">{item.category}</div>
        </div>
        <div className="text-xs opacity-70">{new Date(item.time || Date.now()).toLocaleString()}</div>
      </div>
      <div className="mt-2 opacity-90">{item.content}</div>
    </GlassCard>
  )
}