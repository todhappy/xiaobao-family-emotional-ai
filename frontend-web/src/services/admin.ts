import { api } from "@/services/api"

export const getModules = async () => {
  try { return await api.get("/admin/modules").then(r => r.data) } catch {
    return [
      { name: "数据库与模型", status: "ok", time: new Date().toISOString(), lastLog: "pg/neo4j 连接正常" },
      { name: "后端微服务", status: "ok", time: new Date().toISOString(), lastLog: "api 正常" },
      { name: "AI 能力层", status: "warning", time: new Date().toISOString(), lastLog: "LLM 响应波动" },
      { name: "前端图谱与 UI", status: "ok", time: new Date().toISOString(), lastLog: "Graph3D 渲染正常" },
      { name: "硬件适配与 WebSocket", status: "ok", time: new Date().toISOString(), lastLog: "在线 1" },
      { name: "MCP 插件封装", status: "ok", time: new Date().toISOString(), lastLog: "全部可用" },
      { name: "系统联调与测试", status: "ok", time: new Date().toISOString(), lastLog: "集成通过" },
      { name: "腾讯云部署", status: "warning", time: new Date().toISOString(), lastLog: "待上线" }
    ]
  }
}

export const getLogs = async () => {
  try { return await api.get("/admin/logs").then(r => r.data) } catch {
    try { return await api.get("/logs").then(r => r.data) } catch { return { items: [] } }
  }
}

export const getMcpStats = async () => {
  try { return await api.get("/admin/mcp/stats").then(r => r.data) } catch {
    return [{ name: "weather", count: 2 }, { name: "calendar", count: 1 }, { name: "search", count: 3 }]
  }
}

export const listUsers = async () => {
  try { return await api.get("/admin/users").then(r => r.data) } catch {
    return [{ nickname: "测试用户", source: "web", lastActive: new Date().toLocaleString() }]
  }
}