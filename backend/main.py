import os
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ── Load environment ──────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
    raise RuntimeError(
        "Please set your Groq API key in backend/.env\n"
        "   GROQ_API_KEY=gsk_..."
    )

DB_FAISS_PATH = os.path.join(os.path.dirname(__file__), "..", "vectorstore", "db_faiss")

# ── Load FAISS vector store ───────────────────────────────────────
print("Loading embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Loading FAISS vector store...")
if not os.path.exists(DB_FAISS_PATH):
    raise RuntimeError(
        f"FAISS vector store not found at {DB_FAISS_PATH}\n"
        "   Run create_memory_for_llm.py first to build it."
    )

db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 4})
print("FAISS vector store loaded successfully!")

# ── Medical prompt template ───────────────────────────────────────
MEDICAL_PROMPT = ChatPromptTemplate.from_template(
    """You are MediBot, a knowledgeable medical assistant. Use the following pieces of medical reference material to answer the user's question accurately and helpfully.

If the context contains relevant information, provide a thorough answer based on it. If the context doesn't contain enough information to fully answer the question, say so honestly and provide what information you can from the context.

Always remind users to consult a healthcare professional for personal medical advice.

Context from medical references:
{context}

Patient's Question: {question}

MediBot's Response:"""
)

# ── Build RAG chain ───────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=GROQ_API_KEY,
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | MEDICAL_PROMPT
    | llm
    | StrOutputParser()
)

# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(title="MediBot RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class SourceDoc(BaseModel):
    content: str
    page: int | None = None
    source: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceDoc]


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "MediBot is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Retrieve source documents
        source_docs = retriever.invoke(request.question)

        # Get answer from RAG chain
        answer = rag_chain.invoke(request.question)

        # Format sources
        sources = []
        for doc in source_docs:
            sources.append(
                SourceDoc(
                    content=doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                    page=doc.metadata.get("page"),
                    source=doc.metadata.get("source"),
                )
            )

        return ChatResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("Starting MediBot API server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
