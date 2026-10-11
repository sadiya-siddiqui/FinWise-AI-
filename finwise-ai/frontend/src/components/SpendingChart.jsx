import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid } from 'recharts'
const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#64748b']
export default function SpendingChart({ summary, forecast }) {
  const daily = [...(summary?.daily || []).map((d) => ({ date: d.date.slice(5), actual: d.amount })),
                 ...(forecast || []).map((d) => ({ date: d.date.slice(5), predicted: d.predicted }))]
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-white rounded-xl p-4 shadow-sm h-72">
        <h3 className="font-semibold mb-2">By category</h3>
        <ResponsiveContainer><PieChart>
          <Pie data={summary?.by_category || []} dataKey="amount" nameKey="category" outerRadius={90} label>
            {(summary?.by_category || []).map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Pie><Tooltip formatter={(v) => `$${v}`} /></PieChart></ResponsiveContainer>
      </div>
      <div className="bg-white rounded-xl p-4 shadow-sm h-72">
        <h3 className="font-semibold mb-2">Daily spend &amp; 30-day forecast</h3>
        <ResponsiveContainer><AreaChart data={daily}>
          <CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" fontSize={11} /><YAxis fontSize={11} /><Tooltip />
          <Area dataKey="actual" stroke="#10b981" fill="#d1fae5" />
          <Area dataKey="predicted" stroke="#6366f1" strokeDasharray="4 4" fill="#e0e7ff" />
        </AreaChart></ResponsiveContainer>
      </div>
    </div>
  )
}
