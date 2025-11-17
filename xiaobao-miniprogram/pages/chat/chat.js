Page({
  data:{ messages:[], input:"" },
  onInput(e){ this.setData({ input: e.detail.value }); },
  async send(){
    const content = this.data.input;
    this.setData({ messages: this.data.messages.concat([{ role:"me", text: content }]), input:"" });
    try{
      const r = await wx.request({
        url: 'http://127.0.0.1:5001/api/v1/chat/send',
        method: 'POST',
        data: { user_id:1, family_id:1, member_role:'父亲', content },
        header: { 'content-type':'application/json' }
      });
    }catch(err){}
  }
})