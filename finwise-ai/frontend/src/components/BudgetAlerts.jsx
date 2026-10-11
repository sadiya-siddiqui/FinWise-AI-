import { useState } from 'react'
import { api } from '../api/client'
const color = { ok: 'bg-emerald-500', warning: 'bg-amber-500', over: 'bg-red-500' }
export default function BudgetAlerts({ alerts = [], onChange }) {
  const [cat, setCat] = useState(''), [limit, setLimit] = useState('')
  const add = async (e) => { e.preventDefault(); await api.setBudget(cat, parseFloat(limit)); setCat(''); setLimit(''); onChange?.() }
  return (
    <div className="bg-white rounded-xl p-4 shadow-sm space-y-3">
      <h3 className="font-semibold">Budgets</h3>
      {alerts.map((a) => (
        <div key={a.category}>
          <div className="flex justify-between text-sm"><span>{a.category}{a.level !== 'ok' && ` ⚠ ${a.level === 'over' ? 'over budget' : 'near limit'}`}</span><span>${a.spent} / ${a.limit}</span></div>
          <div className="h-2 bg-slate-100 rounded"><div className={`h-2 rounded ${color[a.level]}`} style={{ width: `${Math.min(a.percent, 100)}%` }} /></div>
        </div>
      ))}
      <form onSubmit={add} className="flex gap-2">
        <input className="border rounded p-1 text-sm flex-1" placeholder="Category" value={cat} onChange={(e) => setCat(e.target.value)} required />
        <input className="border rounded p-1 text-sm w-20" type="number" placeholder="$" value={limit} onChange={(e) => setLimit(e.target.value)} required />
        <button className="bg-slate-800 text-white px-3 rounded text-sm">Set</button>
      </form>
    </div>
  )
}
