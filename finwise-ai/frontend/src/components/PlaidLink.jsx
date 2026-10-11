import { useEffect, useState } from 'react'
import { usePlaidLink } from 'react-plaid-link'
import { api } from '../api/client'
export default function PlaidLink({ onLinked }) {
  const [token, setToken] = useState(null)
  useEffect(() => { api.linkToken().then((r) => setToken(r.link_token)).catch(() => {}) }, [])
  const { open, ready } = usePlaidLink({ token, onSuccess: async (pt) => { await api.exchange(pt); onLinked?.() } })
  return <button onClick={() => open()} disabled={!ready} className="bg-emerald-600 disabled:opacity-50 text-white px-4 py-2 rounded-lg">+ Link bank account</button>
}
