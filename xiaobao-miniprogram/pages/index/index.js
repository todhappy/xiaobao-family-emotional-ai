const app = getApp();

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
  },

  onLoad() {
    // 检查本地缓存中是否有用户信息
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({
        userInfo: userInfo,
        hasUserInfo: true,
      });
    }
  },

  login() {
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        });
        wx.setStorageSync('userInfo', res.userInfo);

        // 在这里，你可以将 res.userInfo 发送到你的后端服务器
        // wx.login({
        //   success: loginRes => {
        //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
        //     // api.post('/v1/auth/wx_login', { code: loginRes.code, userInfo: res.userInfo })
        //   }
        // })
      }
    });
  },
});