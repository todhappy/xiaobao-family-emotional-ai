const api = require("../../services/api")
Page({
  data: { items: [] },
  onShow() {
    api.memoryList().then(r => { this.setData({ items: Array.isArray(r) ? r : [] }) })
  }
})