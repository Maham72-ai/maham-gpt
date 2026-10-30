
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../lib/api.js'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const nav = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError(''); setLoading(true)
    try {
      const res = await api.post('/api/auth/login', { email, password })
      localStorage.setItem('token', res.data.access_token)
      localStorage.setItem('user', JSON.stringify(res.data.user))
      nav('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f] p-4">
      <div className="w-full max-w-sm bg-[#1a1a1a] rounded-2xl p-8 border border-white/10">
        <h1 className="text-2xl font-bold mb-1">Welcome back</h1>
        <p className="text-sm text-white/60 mb-6">Login to your AI Chatbot</p>
        {error && <div className="bg-red-500/20 text-red-300 text-sm p-3 rounded-lg mb-4">{error}</div>}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="text-xs text-white/70">Email</label>
            <input value={email} onChange={e=>setEmail(e.target.value)} required type="email" className="mt-1 w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none focus:border-white/30" placeholder="you@example.com" />
          </div>
          <div>
            <label className="text-xs text-white/70">Password</label>
            <input value={password} onChange={e=>setPassword(e.target.value)} required type="password" className="mt-1 w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none" placeholder="••••••••" />
          </div>
          <button disabled={loading} className="w-full bg-white text-black rounded-lg py-2.5 text-sm font-semibold hover:bg-white/90 disabled:opacity-50">
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="text-xs text-center text-white/50 mt-6">No account? <Link to="/register" className="text-white underline">Register</Link></p>
      </div>
    </div>
  )
}
