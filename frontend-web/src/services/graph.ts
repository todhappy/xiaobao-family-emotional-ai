import { api } from "@/services/api"

export const getGraph = async () => api.get("/graph").then(r => r.data)