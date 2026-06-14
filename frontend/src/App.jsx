import { useState, useRef, useEffect } from 'react'
import './App.css'

const SUGGESTIONS = [
  { icon: '💊', text: 'What are the common side effects of ibuprofen?' },
  { icon: '🩺', text: 'Explain the symptoms of Type 2 Diabetes' },
  { icon: '🫀', text: 'What causes high blood pressure?' },
  { icon: '🧬', text: 'What is anemia and how is it treated?' },
]

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const sendMessage = async (question) => {
    const userQuestion = question || input.trim()
    if (!userQuestion || isLoading) return

    const userMsg = { role: 'user', content: userQuestion }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsLoading(true)

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userQuestion }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || `Server error (${res.status})`)
      }

      const data = await res.json()
      const botMsg = {
        role: 'bot',
        content: data.answer,
        sources: data.sources || [],
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      const errorMsg = {
        role: 'bot',
        content: `Sorry, I couldn't process your question. ${err.message}`,
        isError: true,
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-icon">🏥</div>
        <div className="header-text">
          <h1>MediBot</h1>
          <p>AI-Powered Medical Assistant</p>
        </div>
      </header>

      {/* Chat Area */}
      <main className="chat-area">
        <div className="chat-area-inner">
          {messages.length === 0 && !isLoading ? (
            <Welcome onSuggestionClick={sendMessage} />
          ) : (
            <>
              {messages.map((msg, i) => (
                <Message key={i} message={msg} />
              ))}
              {isLoading && <TypingIndicator />}
            </>
          )}
          <div ref={chatEndRef} />
        </div>
      </main>

      {/* Input */}
      <footer className="input-area">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            className="input-field"
            id="chat-input"
            placeholder="Ask a medical question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={isLoading}
          />
          <button
            className="send-button"
            id="send-button"
            onClick={() => sendMessage()}
            disabled={isLoading || !input.trim()}
            title="Send message"
          >
            ➤
          </button>
        </div>
        <p className="input-hint">
          MediBot uses medical reference material. Always consult a healthcare professional.
        </p>
      </footer>
    </div>
  )
}

/* ── Welcome Component ──────────────────────────────────── */
function Welcome({ onSuggestionClick }) {
  return (
    <div className="welcome">
      <div className="welcome-icon">🩺</div>
      <h2>Welcome to MediBot</h2>
      <p>
        I'm your AI medical assistant powered by medical reference material.
        Ask me about symptoms, conditions, treatments, and more.
      </p>
      <div className="welcome-suggestions">
        {SUGGESTIONS.map((s, i) => (
          <button
            key={i}
            className="suggestion-card"
            id={`suggestion-${i}`}
            onClick={() => onSuggestionClick(s.text)}
          >
            <span>{s.icon}</span>
            {s.text}
          </button>
        ))}
      </div>
    </div>
  )
}

/* ── Message Component ──────────────────────────────────── */
function Message({ message }) {
  const [showSources, setShowSources] = useState(false)
  const isUser = message.role === 'user'

  return (
    <div className={`message ${isUser ? 'user' : 'bot'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className={`message-bubble ${message.isError ? 'error-bubble' : ''}`}>
          {message.content}
        </div>
        {!isUser && message.sources?.length > 0 && (
          <div className="sources">
            <button
              className="sources-toggle"
              onClick={() => setShowSources(!showSources)}
            >
              📄 {showSources ? 'Hide' : 'Show'} Sources ({message.sources.length})
            </button>
            {showSources && (
              <div className="sources-list">
                {message.sources.map((src, i) => (
                  <div key={i} className="source-item">
                    <div className="source-label">
                      Source {i + 1} {src.page != null && `• Page ${src.page + 1}`}
                    </div>
                    {src.content}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

/* ── Typing Indicator ───────────────────────────────────── */
function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <div className="message-avatar">🤖</div>
      <div className="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  )
}

export default App
