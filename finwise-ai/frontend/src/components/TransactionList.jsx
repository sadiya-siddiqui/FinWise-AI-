export default function TransactionList({ items = [] }) {
  return (
    <div className="bg-white rounded-xl shadow-sm divide-y max-h-96 overflow-auto">
      {items.length === 0 && <p className="p-4 text-slate-500 text-sm">No transactions yet. Link an account to get started.</p>}
      {items.map((t) => (
        <div key={t.id} className="flex justify-between p-3 text-sm">
          <div><p className="font-medium">{t.merchant || t.name}</p><p className="text-slate-500">{t.date} · {t.category}{t.pending && ' · pending'}</p></div>
          <p className={t.amount < 0 ? 'text-emerald-600 font-medium' : 'font-medium'}>{t.amount < 0 ? '+' : '-'}${Math.abs(t.amount).toFixed(2)}</p>
        </div>
      ))}
    </div>
  )
}
