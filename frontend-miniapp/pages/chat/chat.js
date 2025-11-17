const api = require("../../services/api")
Page({
  data: { input: "", msgs: [] },
  onInput(e) { this.setData({ input: e.detail.value }) },
  send() {
    const v = this.data.input
    if (!v) return
    const msgs = this.data.msgs.concat([{ role: "user", content: v }])
    this.setData({ input: "", msgs })
    api.chatSend({ user_id: 1, family_id: 1, member_role: "父亲", content: v }).then(r => {
      const m = msgs.concat([{ role: "assistant", content: r.answer || JSON.stringify(r) }])
      this.setData({ msgs: m })
    })
  }
})