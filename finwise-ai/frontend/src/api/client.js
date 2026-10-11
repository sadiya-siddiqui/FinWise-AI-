const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const getToken = () => localStorage.getItem('fw_token')
export const setToken = (t) => (t ? localStorage.setItem('fw_token', t) : localStorage.removeItem('fw_token'))

async function req(path, opts = {}) {
  const res = await fetch(BASE + path, {
    ...opts,
    headers: { ...(opts.json ? { 'Content-Type': 'application/json' } : {}), ...(getToken() ? { Authorization: `Bearer ${getToken()}` } : {}), ...opts.headers },
    body: opts.json ? JSON.stringify(opts.json) : opts.body,
  })
  if (res.status === 401) { setToken(null); window.location.reload() }
  if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || 'Request failed')
  return res.json()
}
export const api = {
  register: (email, password) => req('/api/auth/register', { method: 'POST', json: { email, password } }),
  login: (email, password) => req('/api/auth/login', { method: 'POST', body: new URLSearchParams({ username: email, password }) }),
  linkToken: () => req('/api/plaid/link-token', { method: 'POST' }),
  exchange: (public_token) => req('/api/plaid/exchange', { method: 'POST', json: { public_token } }),
  sync: () => req('/api/plaid/sync', { method: 'POST' }),
  accounts: () => req('/api/plaid/accounts'),
  transactions: () => req('/api/transactions?limit=100'),
  summary: (days = 30) => req(`/api/transactions/summary?days=${days}`),
  forecast: () => req('/api/insights/forecast'),
  subscriptions: () => req('/api/insights/subscriptions'),
  alerts: () => req('/api/insights/alerts'),
  setBudget: (category, limit) => req('/api/insights/budgets', { method: 'POST', json: { category, limit } }),
  chat: (message) => req('/api/chat', { method: 'POST', json: { message } }),
}
