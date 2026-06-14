# 🏥 MediBot - AI Medical Assistant

A RAG-based medical Q&A chatbot that answers medical questions 
from a curated knowledge base using LangChain, FAISS, and Groq LLM.

---

## 🔄 Pipeline Flow

User Question → React Frontend → FastAPI Backend → 
HuggingFace Embeddings → FAISS Vector Search → 
LangChain RAG Chain → Groq LLM → Answer with Sources

---

## ⚙️ Tech Stack

- **Frontend:** React + Vite
- **Backend:** FastAPI + Uvicorn
- **LLM:** Groq API (Llama 3.1 8B) — free
- **Embeddings:** HuggingFace all-MiniLM-L6-v2 — local, free
- **Vector Store:** FAISS
- **RAG Framework:** LangChain

---

## 🚀 Setup Instructions

**1. Clone the repo**
```bash
git clone https://github.com/Ankush-S803/Medical-RAG-Chatbot.git
cd Medical-RAG-Chatbot
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn langchain langchain-community
pip install langchain-huggingface langchain-groq faiss-cpu
pip install sentence-transformers python-dotenv
```

**3. Add your API key**

Create `backend/.env` file:
Get free key at: https://console.groq.com

**4. Build vector store**
```bash
python create_memory_for_llm.py
```

**5. Start backend**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**6. Start frontend**
```bash
cd frontend
npm install
npm run dev
```

**7. Open browser**

---

## 💡 Sample Questions

- What causes high blood pressure?
- What are symptoms of Type 2 diabetes?
- How is anemia treated?
- What are warning signs of a stroke?

---

## ⚠️ Disclaimer

For educational purposes only. Always consult a 
healthcare professional for medical advice.

---
