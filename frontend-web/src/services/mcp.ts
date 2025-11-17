import { api } from "@/services/api"

export const callMcp = async (payload: any) => api.post("/mcp/call", payload).then(r => r.data)