Page({
  data:{ member:{} },
  onLoad(){
    wx.request({ url:'http://127.0.0.1:5001/api/v1/family/member/1', success: (res)=>{ this.setData({ member: res.data }); }});
  }
})