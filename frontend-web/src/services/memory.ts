import { api } from "@/services/api"

export const listMemory = async () => api.get("/memory").then(r => r.data)
export const createMemory = async (payload: any) => api.post("/memory", payload).then(r => r.data)