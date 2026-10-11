import { useState } from 'react'
import { getToken } from './api/client'
import Login from './pages/Login'
import Dashboard from './components/Dashboard'
export default function App() {
  const [authed, setAuthed] = useState(!!getToken())
  return authed ? <Dashboard /> : <Login onAuth={() => setAuthed(true)} />
}
