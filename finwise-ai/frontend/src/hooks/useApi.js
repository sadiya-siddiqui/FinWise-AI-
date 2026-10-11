import { useEffect, useState, useCallback } from 'react'
export default function useApi(fn, fallback = null) {
  const [data, setData] = useState(fallback)
  const [loading, setLoading] = useState(true)
  const load = useCallback(() => { setLoading(true); return fn().then(setData).catch(() => {}).finally(() => setLoading(false)) }, [])
  useEffect(() => { load() }, [load])
  return { data, loading, reload: load }
}
