import { api } from "@/services/api"

export const sendChat = async (payload: any) => api.post("/chat", payload).then(r => r.data)