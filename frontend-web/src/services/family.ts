import { api } from "@/services/api"

export const getFamily = async () => api.get("/family").then(r => r.data)