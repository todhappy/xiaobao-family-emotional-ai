import { useEffect, useState } from "react"

export default function useFetch<T>(fn: () => Promise<T>, deps: any[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    let mounted = true
    setLoading(true)
    fn().then(d => { if (mounted) { setData(d); setError(null) } }).catch(e => { if (mounted) setError(String(e)) }).finally(() => { if (mounted) setLoading(false) })
    return () => { mounted = false }
  }, deps)
  return { data, loading, error }
}