
export default function ChatMessage({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${isUser ? 'bg-white text-black rounded-br-sm' : 'bg-[#1e1e1e] text-white border border-white/10 rounded-bl-sm'}`}>
        {content}
      </div>
    </div>
  )
}
