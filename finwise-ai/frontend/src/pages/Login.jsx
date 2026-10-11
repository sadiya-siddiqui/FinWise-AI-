import { useState } from 'react'
import { api, setToken } from '../api/client'
export default function Login({ onAuth }) {
  const [mode, setMode] = useState('login'), [email, setEmail] = useState(''), [pw, setPw] = useState(''), [err, setErr] = useState('')
  const submit = async (e) => {
    e.preventDefault(); setErr('')
    try { const r = await (mode === 'login' ? api.login : api.register)(email, pw); setToken(r.access_token); onAuth() }
    catch (e) { setErr(e.message) }
  }
  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={submit} className="bg-white p-8 rounded-2xl shadow w-96 space-y-4">
        <h1 className="text-2xl font-bold text-emerald-600">FinWise AI</h1>
        <p className="text-sm text-slate-500">All your accounts. One smart view.</p>
        <input className="w-full border rounded-lg p-2" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input className="w-full border rounded-lg p-2" type="password" placeholder="Password (8+ chars)" value={pw} onChange={(e) => setPw(e.target.value)} required />
        {err && <p className="text-sm text-red-600">{err}</p>}
        <button className="w-full bg-emerald-600 text-white rounded-lg p-2 font-medium">{mode === 'login' ? 'Sign in' : 'Create account'}</button>
        <button type="button" className="text-sm text-slate-500 underline" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
          {mode === 'login' ? 'Need an account? Register' : 'Have an account? Sign in'}
        </button>
      </form>
    </div>
  )
}
