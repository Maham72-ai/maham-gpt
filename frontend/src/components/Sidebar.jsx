
import { useMemo } from 'react'

function groupConversations(convs) {
  const now = new Date()
  const todayStr = now.toDateString()
  const yesterday = new Date(now); yesterday.setDate(now.getDate()-1)
  const yestStr = yesterday.toDateString()
  const sevenDaysAgo = new Date(now); sevenDaysAgo.setDate(now.getDate()-7)

  const groups = { Today: [], Yesterday: [], 'Previous 7 Days': [], Older: [] }
  convs.forEach(c => {
    const d = new Date(c.last_message_at)
    const ds = d.toDateString()
    if (ds === todayStr) groups.Today.push(c)
    else if (ds === yestStr) groups.Yesterday.push(c)
    else if (d > sevenDaysAgo) groups['Previous 7 Days'].push(c)
    else groups.Older.push(c)
  })
  return groups
}

export default function Sidebar({ conversations, activeId, onSelect, onNewChat, onRename, onDelete, open, setOpen }) {
  const grouped = useMemo(()=> groupConversations(conversations), [conversations])

  return (
    <>
      <div className={`fixed md:static inset-y-0 left-0 z-40 w-[280px] bg-[#171717] border-r border-white/10 flex flex-col transition-transform ${open ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="p-3">
          <button onClick={onNewChat} className="w-full bg-white text-black rounded-lg py-2.5 text-sm font-semibold flex items-center justify-center gap-2">+ New Chat</button>
        </div>
        <div className="flex-1 overflow-y-auto px-2 pb-4 scrollbar-thin">
          {Object.entries(grouped).map(([label, items]) => items.length > 0 && (
            <div key={label} className="mb-4">
              <p className="text-[11px] uppercase tracking-wider text-white/40 px-2 py-2">{label}</p>
              <div className="space-y-1">
                {items.map(c => (
                  <div key={c.id} className={`group flex items-center justify-between rounded-lg px-2 py-2 text-sm cursor-pointer ${activeId===c.id ? 'bg-white/10 text-white' : 'text-white/70 hover:bg-white/5'}`}>
                    <span onClick={()=>{onSelect(c.id); setOpen(false)}} className="truncate flex-1">{c.title}</span>
                    <div className="hidden group-hover:flex gap-1 ml-2">
                      <button onClick={()=>onRename(c.id)} className="text-xs p-1 hover:bg-white/10 rounded">✎</button>
                      <button onClick={()=>onDelete(c.id)} className="text-xs p-1 hover:bg-red-500/20 rounded">🗑</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
          {conversations.length===0 && <p className="text-xs text-white/30 text-center mt-10">No chats yet</p>}
        </div>
        <div className="p-3 border-t border-white/10 text-xs text-white/40">AI Chatbot Final • Gemini</div>
      </div>
      {open && <div className="fixed inset-0 bg-black/50 z-30 md:hidden" onClick={()=>setOpen(false)} />}
    </>
  )
}
