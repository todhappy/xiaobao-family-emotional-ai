import io from "socket.io-client"
import { useEffect, useRef } from "react"

export default function useSocket() {
  const ref = useRef<any>(null)
  useEffect(() => {
    const url = process.env.NODE_ENV === "production" ? process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:5001" : "/"
    const s = io(url, { transports: ["websocket"], path: process.env.NODE_ENV === "production" ? undefined : "/socket.io" })
    ref.current = s
    return () => { s.close() }
  }, [])
  return ref
}