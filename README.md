# 🏥 MediBot - AI Medical Assistant

A RAG (Retrieval-Augmented Generation) based medical Q&A chatbot 
that answers medical questions using a curated knowledge base, 
powered by LangChain, FAISS, and Groq LLM.

![MediBot Demo](frontend/src/assets/hero.png)

---

## 🧠 What is RAG?

Traditional LLMs answer from their training data which can be 
outdated or hallucinated. RAG solves this by:

1. Storing your own documents as vector embeddings
2. When a question is asked, retrieving the most relevant chunks
3. Feeding those chunks as context to the LLM
4. LLM generates answer grounded in your actual documents

This means MediBot answers only from verified medical reference 
material — not from random internet data.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite |
| Backend | FastAPI + Uvicorn |
| LLM | Groq API (Llama 3.1 8B) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| RAG Framework | LangChain |
| Environment | Python 3.13 |

MediBot/

├── backend/

│   └── main.py              # FastAPI server + RAG chain

├── data/

│   └── medical_knowledge.txt # Medical reference knowledge base

├── frontend/

│   ├── src/

│   │   ├── App.jsx          # Main React component

│   │   ├── App.css          # Styling

│   │   └── main.jsx         # Entry point

│   ├── package.json

│   └── vite.config.js

├── create_memory_for_llm.py  # Script to build FAISS vectorstore

├── Pipfile                   # Python dependencies

└── README.md

---

## 🔄 How It Works - Pipeline Flow
User Question

│

▼

Frontend (React)

│  HTTP POST /chat

▼

FastAPI Backend

│

▼

HuggingFace Embeddings

(converts question to vector)

│

▼

FAISS Vector Store

(finds top 4 similar chunks

from medical_knowledge.txt)

│

▼

LangChain RAG Chain

(formats retrieved chunks

question into prompt)

│

▼

Groq LLM - Llama 3.1 8B

(generates answer from context)

│

▼

FastAPI Response

(answer + source documents)

│

▼

Frontend displays answer

with source snippets


---

## 📚 Knowledge Base

The chatbot answers questions on these medical topics:

- Diabetes (Type 1, Type 2, Gestational)
- Hypertension (High Blood Pressure)
- Anemia and its types
- Asthma
- Arthritis (Osteoarthritis, Rheumatoid)
- Common Cold & Influenza
- Allergies & Anaphylaxis
- Migraine
- Pneumonia
- Depression
- UTI (Urinary Tract Infection)
- Cholesterol
- GERD
- Thyroid Disorders
- Osteoporosis
- Stroke
- Ibuprofen usage & warnings

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key (free at console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/Ankush-S803/Medical-RAG-Chatbot.git
cd Medical-RAG-Chatbot
```

### 2. Set up Python environment
```bash
pip install pipenv
pipenv install
pipenv shell
```

Or using pip directly:
```bash
pip install fastapi uvicorn langchain langchain-community 
langchain-huggingface langchain-groq faiss-cpu 
sentence-transformers python-dotenv
```

### 3. Set up environment variables
Create a `.env` file inside the `backend/` folder:
GROQ_API_KEY=your_groq_api_key_here
Get your free API key at: https://console.groq.com

### 4. Build the FAISS vectorstore
```bash
python create_memory_for_llm.py
```
This will:
- Load medical_knowledge.txt from data/ folder
- Split into chunks (500 chars, 50 overlap)
- Generate HuggingFace embeddings
- Save FAISS index to vectorstore/db_faiss/

### 5. Start the backend server
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Backend runs at: http://localhost:8000

Verify it's working:
http://localhost:8000/health
Should return: `{"status": "ok", "message": "MediBot is running"}`

### 6. Start the frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

### 7. Open the app
Go to http://localhost:5173 in your browser and start asking 
medical questions!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /chat | Ask a medical question |

### POST /chat
**Request:**
```json
{
  "question": "What causes high blood pressure?"
}
```

**Response:**
```json
{
  "answer": "High blood pressure (hypertension) is caused by...",
  "sources": [
    {
      "content": "Hypertension, or high blood pressure...",
      "source": "data/medical_knowledge.txt"
    }
  ]
}
```

---

## 💡 Example Questions to Ask

- "What are the symptoms of Type 2 diabetes?"
- "What causes high blood pressure?"
- "How is anemia treated?"
- "What are asthma triggers?"
- "What medications are used for depression?"
- "What are the warning signs of a stroke?"

---

## ⚠️ Disclaimer

MediBot is for **educational purposes only**. It is not a substitute 
for professional medical advice, diagnosis, or treatment. Always 
consult a qualified healthcare professional for medical decisions.

---
 


---

## 🗂️ Project Structure
