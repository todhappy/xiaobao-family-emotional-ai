Page({
  data:{ content:"", tag:"" },
  onInput(e){ this.setData({ content: e.detail.value }); },
  onTag(e){ this.setData({ tag: e.detail.value }); },
  add(){
    const tags = this.data.tag? [this.data.tag] : [];
    wx.request({
      url:'http://127.0.0.1:5001/api/v1/memory/add',
      method:'POST',
      data:{ family_id:1, member_id:1, content:this.data.content, tags },
      header:{ 'content-type':'application/json' },
      success:()=>{ this.setData({ content:"", tag:"" }); }
    });
  }
})