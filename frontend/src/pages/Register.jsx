
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../lib/api.js'

export default function Register() {
  const [form, setForm] = useState({ name:'', email:'', password:'', confirm_password:'' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const nav = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    if(form.password !== form.confirm_password){ setError('Passwords do not match'); return }
    setError(''); setLoading(true)
    try {
      await api.post('/api/auth/register', form)
      nav('/login')
    } catch(err){ setError(err.response?.data?.detail || 'Registration failed') }
    finally{ setLoading(false) }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f] p-4">
      <div className="w-full max-w-sm bg-[#1a1a1a] rounded-2xl p-8 border border-white/10">
        <h1 className="text-2xl font-bold mb-1">Create account</h1>
        <p className="text-sm text-white/60 mb-6">Start your AI Chatbot journey</p>
        {error && <div className="bg-red-500/20 text-red-300 text-sm p-3 rounded-lg mb-4">{error}</div>}
        <form onSubmit={submit} className="space-y-3">
          <input value={form.name} onChange={e=>setForm({...form,name:e.target.value})} required placeholder="Full Name" className="w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none" />
          <input value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required type="email" placeholder="Email" className="w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none" />
          <input value={form.password} onChange={e=>setForm({...form,password:e.target.value})} required type="password" placeholder="Password (min 8 chars)" className="w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none" />
          <input value={form.confirm_password} onChange={e=>setForm({...form,confirm_password:e.target.value})} required type="password" placeholder="Confirm Password" className="w-full bg-[#2a2a2a] border border-white/10 rounded-lg px-3 py-2.5 text-sm outline-none" />
          <button disabled={loading} className="w-full bg-white text-black rounded-lg py-2.5 text-sm font-semibold mt-2">{loading?'Creating...':'Create Account'}</button>
        </form>
        <p className="text-xs text-center text-white/50 mt-6">Have account? <Link to="/login" className="text-white underline">Login</Link></p>
      </div>
    </div>
  )
}
