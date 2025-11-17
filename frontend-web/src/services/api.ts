import axios from "axios"

export const api = axios.create({
  baseURL: process.env.NODE_ENV === "production" ? process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:5001" : "/api"
})