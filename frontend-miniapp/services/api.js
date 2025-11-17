const BASE = "http://127.0.0.1:5001/api"
function request(path, method, data) {
  return new Promise((resolve, reject) => {
    wx.request({ url: BASE + path, method, data, success: res => resolve(res.data), fail: reject })
  })
}
module.exports = {
  family: () => request("/family", "GET"),
  memoryList: () => request("/memory", "GET"),
  chatSend: (payload) => request("/chat", "POST", payload),
  graph: () => request("/graph", "GET")
}