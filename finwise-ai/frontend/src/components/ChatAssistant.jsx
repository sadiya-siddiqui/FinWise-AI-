import { useState } from 'react'
import { api } from '../api/client'
export default function ChatAssistant() {
  const [msgs, setMsgs] = useState([{ role: 'ai', text: 'Ask me anything about your spending, e.g. "How much did I spend on dining last month?"' }])
  const [input, setInput] = useState(''), [busy, setBusy] = useState(false)
  const send = async (e) => {
    e.preventDefault(); if (!input.trim()) return
    const q = input; setInput(''); setBusy(true); setMsgs((m) => [...m, { role: 'user', text: q }])
    try { const r = await api.chat(q); setMsgs((m) => [...m, { role: 'ai', text: r.reply }]) }
    catch (err) { setMsgs((m) => [...m, { role: 'ai', text: 'Error: ' + err.message }]) }
    setBusy(false)
  }
  return (
    <div className="bg-white rounded-xl shadow-sm flex flex-col h-96">
      <h3 className="font-semibold p-4 pb-2">Chat with your finances</h3>
      <div className="flex-1 overflow-auto px-4 space-y-2">
        {msgs.map((m, i) => <div key={i} className={`text-sm p-2 rounded-lg max-w-[85%] whitespace-pre-wrap ${m.role === 'user' ? 'bg-emerald-600 text-white ml-auto' : 'bg-slate-100'}`}>{m.text}</div>)}
        {busy && <div className="text-sm text-slate-400">Thinking…</div>}
      </div>
      <form onSubmit={send} className="p-3 flex gap-2">
        <input className="flex-1 border rounded-lg p-2 text-sm" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask a question…" />
        <button className="bg-emerald-600 text-white px-4 rounded-lg text-sm">Send</button>
      </form>
    </div>
  )
}
