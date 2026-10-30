import { useEffect, useState, useRef } from 'react'
import api from '../lib/api.js'
import Sidebar from '../components/Sidebar.jsx'
import ChatMessage from '../components/ChatMessage.jsx'
import { useNavigate } from 'react-router-dom'

export default function ChatPage() {
  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const bottomRef = useRef(null)
  const nav = useNavigate()

  const fetchConvs = async () => {
    try { const res = await api.get('/api/conversations'); setConversations(res.data) } catch(e){ if(e.response?.status===401){ nav('/login') } }
  }
  useEffect(()=>{ fetchConvs() }, [])

  const loadConversation = async (id) => {
    setActiveId(id)
    try { const res = await api.get(`/api/conversations/${id}`); setMessages(res.data.messages || []) } catch(e){ console.error(e) }
  }

  const createNewChat = async () => {
    try { const res = await api.post('/api/conversations', { title: 'New Chat' }); await fetchConvs(); setActiveId(res.data.id); setMessages([]) } catch(e){ console.error(e) }
  }

  const sendMessage = async () => {
    if(!input.trim() || loading) return
    if(!activeId){ 
      const res = await api.post('/api/conversations', { title: input.slice(0,30) || 'New Chat' });
      await fetchConvs(); setActiveId(res.data.id); return;
    }
    const content = input; setInput(''); setLoading(true)
    setMessages(prev => [...prev, { role:'user', content, created_at: new Date().toISOString() }])
    try {
      const res = await api.post(`/api/conversations/${activeId}/messages`, { content })
      setMessages(prev => [...prev, { role: res.data.role, content: res.data.content, created_at: res.data.created_at }])
      fetchConvs()
    } catch(err) {
      const msg = err.response?.data?.detail || 'Failed to generate'
      setMessages(prev => [...prev, { role:'assistant', content: '⚠ ' + msg, created_at: new Date().toISOString() }])
    } finally { setLoading(false); bottomRef.current?.scrollIntoView({ behavior:'smooth' }) }
  }

  const handleRename = async (id) => {
    const newTitle = prompt('Enter new title:')
    if(!newTitle) return
    try { await api.patch(`/api/conversations/${id}`, { title: newTitle }); fetchConvs() } catch(e){ alert('Rename failed') }
  }
  const handleDelete = async (id) => {
    if(!confirm('Delete this conversation?')) return
    try { await api.delete(`/api/conversations/${id}`); if(activeId===id){ setActiveId(null); setMessages([]) } ; fetchConvs() } catch(e){ alert('Delete failed') }
  }
  const logout = async () => { try{ await api.post('/api/auth/logout') }catch{}; localStorage.clear(); nav('/login') }

  useEffect(()=>{ bottomRef.current?.scrollIntoView({ behavior:'smooth' }) }, [messages])

  return (
    <div className="h-screen flex bg-[#0f0f0f]">
      <Sidebar conversations={conversations} activeId={activeId} onSelect={loadConversation} onNewChat={createNewChat} onRename={handleRename} onDelete={handleDelete} open={sidebarOpen} setOpen={setSidebarOpen} />
      <div className="flex-1 flex flex-col min-w-0">
        <div className="h- border-b border-white/10 flex items-center justify-between px-4">
          <button className="md:hidden p-2" onClick={()=>setSidebarOpen(!sidebarOpen)}>☰</button>
          <p className="text-sm font-medium">{conversations.find(c=>c.id===activeId)?.title || 'Maham GPT'}</p>
          <button onClick={logout} className="text-xs bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg">Logout</button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 md:px-0 py-6">
          <div className="max-w-3xl mx-auto w-full">
            {!activeId && messages.length===0 && (
              <div className="text-center mt-24">
                <h1 className="text-3xl font-bold">Maham GPT ✨</h1>
                <p className="text-white/50 text-sm mt-2">Your personal AI assistant</p>
                <button onClick={createNewChat} className="mt-6 bg-white text-black px-5 py-2.5 rounded-full text-sm font-semibold">+ New Chat</button>
              </div>
            )}
            {messages.map((m,i)=><ChatMessage key={i} role={m.role} content={m.content} />)}
            {loading && (
              <div className="flex items-center gap-3 mt-4">
                <div className="w-8 h-8 rounded-full bg-[#1e1e1e] border border-white/10 flex items-center justify-center animate-pulse">
                  <span className="text-sm font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">M</span>
                </div>
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 bg-white/30 rounded-full animate-bounce"></span>
                  <span className="w-1.5 h-1.5 bg-white/30 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                  <span className="w-1.5 h-1.5 bg-white/30 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        </div>
        <div className="border-t border-white/10 p-3 md:p-4 bg-[#0f0f0f]">
          <div className="max-w-3xl mx-auto flex items-end gap-2 bg-[#1e1e1e] border border-white/10 rounded-2xl px-3 py-2">
            <textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMessage() } }} placeholder="Ask Maham GPT..." className="flex-1 bg-transparent resize-none outline-none text-sm max-h- min-h- py-1" rows={1} />
            <button disabled={loading || !input.trim()} onClick={sendMessage} className="bg-white text-black rounded-full w-8 h-8 flex items-center justify-center disabled:opacity-30">↑</button>
          </div>
          <p className="text- text-white/30 text-center mt-2">Maham GPT</p>
        </div>
      </div>
    </div>
  )
}