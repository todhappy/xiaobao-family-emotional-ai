import useFetch from "@/hooks/useFetch"
import { listMemory } from "@/services/memory"
import MemoryItem from "@/components/MemoryItem"

export default function Page() {
  const { data } = useFetch(listMemory, [])
  const items = Array.isArray(data) ? data : []
  return (
    <div className="grid gap-4">
      <div className="title">记忆时间轴</div>
      <div className="grid gap-3">
        {items.map((it, i) => <MemoryItem key={i} item={it} />)}
      </div>
    </div>
  )
}