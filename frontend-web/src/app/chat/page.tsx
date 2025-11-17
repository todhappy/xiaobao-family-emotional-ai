import useSocket from "@/hooks/useSocket"
import GlassCard from "@/components/GlassCard"
import { useEffect, useState } from "react"

export default function Page() {
  const sref = useSocket()
  const [msgs, setMsgs] = useState<any[]>([])
  const [input, setInput] = useState("")
  useEffect(() => {
    const s = sref.current
    if (!s) return
    const onReply = (d: any) => setMsgs(m => [...m, { role: "assistant", content: d?.answer || JSON.stringify(d) }])
    s.on("chat_reply", onReply)
    return () => { s.off("chat_reply", onReply) }
  }, [sref])
  const send = () => {
    const s = sref.current
    if (!s || !input) return
    setMsgs(m => [...m, { role: "user", content: input }])
    s.emit("chat_message", { user_id: 1, family_id: 1, member_role: "父亲", content: input })
    setInput("")
  }
  return (
    <div className="grid gap-4">
      <div className="title">与孝宝小智聊天</div>
      <GlassCard>
        <div className="grid gap-2 max-h-[420px] overflow-auto">
          {msgs.map((m, i) => <div key={i} className="rounded-xl px-3 py-2 bg-white/5"><div className="subtitle">{m.role}</div><div>{m.content}</div></div>)}
        </div>
        <div className="mt-3 flex gap-2">
          <input value={input} onChange={e => setInput(e.target.value)} className="flex-1 px-3 py-2 rounded-xl bg-white/10" />
          <button className="btn" onClick={send}>发送</button>
        </div>
      </GlassCard>
    </div>
  )
}