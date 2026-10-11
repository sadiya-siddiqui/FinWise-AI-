import useApi from '../hooks/useApi'
import { api, setToken } from '../api/client'
import PlaidLink from './PlaidLink'
import SpendingChart from './SpendingChart'
import TransactionList from './TransactionList'
import ChatAssistant from './ChatAssistant'
import BudgetAlerts from './BudgetAlerts'

const Stat = ({ label, value }) => <div className="bg-white rounded-xl p-4 shadow-sm"><p className="text-sm text-slate-500">{label}</p><p className="text-2xl font-bold">{value}</p></div>
const usd = (n) => `$${Number(n || 0).toLocaleString(undefined, { maximumFractionDigits: 0 })}`

export default function Dashboard() {
  const accounts = useApi(api.accounts, []), summary = useApi(() => api.summary(30)), txns = useApi(api.transactions, [])
  const forecast = useApi(api.forecast, []), subs = useApi(api.subscriptions, []), alerts = useApi(api.alerts, [])
  const reloadAll = () => [accounts, summary, txns, forecast, subs, alerts].forEach((x) => x.reload())
  const net = (accounts.data || []).reduce((s, a) => s + a.balance, 0)
  return (
    <div className="max-w-6xl mx-auto p-4 space-y-4">
      <header className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-emerald-600">FinWise AI</h1>
        <div className="flex gap-2 items-center">
          <button className="text-sm underline" onClick={() => api.sync().then(reloadAll)}>Sync now</button>
          <PlaidLink onLinked={reloadAll} />
          <button className="text-sm text-slate-500" onClick={() => { setToken(null); location.reload() }}>Log out</button>
        </div>
      </header>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Stat label="Total balance" value={usd(net)} /><Stat label="Spent (30d)" value={usd(summary.data?.total_spent)} />
        <Stat label="Income (30d)" value={usd(summary.data?.income)} /><Stat label="Linked accounts" value={accounts.data?.length || 0} />
      </div>
      <SpendingChart summary={summary.data} forecast={forecast.data} />
      <div className="grid md:grid-cols-2 gap-4">
        <ChatAssistant />
        <div className="space-y-4">
          <BudgetAlerts alerts={alerts.data} onChange={alerts.reload} />
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <h3 className="font-semibold mb-2">Detected subscriptions</h3>
            {(subs.data || []).length === 0 && <p className="text-sm text-slate-500">None detected yet.</p>}
            {(subs.data || []).map((s) => <div key={s.merchant} className="flex justify-between text-sm py-1"><span>{s.merchant}</span><span>${s.amount}/mo · ${s.annual_cost}/yr</span></div>)}
          </div>
        </div>
      </div>
      <h3 className="font-semibold">Recent transactions</h3>
      <TransactionList items={txns.data} />
    </div>
  )
}
