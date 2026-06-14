import warnings
import logging
import sys

# Suppress noisy warnings
warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Step 1: Load text files from data directory
DATA_PATH = "data/"

def load_text_files(data):
    loader = DirectoryLoader(data, glob='*.txt', loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    documents = loader.load()
    return documents

print("[1/4] Loading text files...")
documents = load_text_files(data=DATA_PATH)
print("Number of documents loaded: ", len(documents))


# Step 2: Filter out empty pages and create chunks
documents = [doc for doc in documents if doc.page_content and doc.page_content.strip()]
print("Documents with actual content: ", len(documents))

if len(documents) == 0:
    print("ERROR: No documents with text content were found in data/ folder.")
    print("Please add .txt files with medical content to the data/ folder.")
    sys.exit(1)

def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = create_chunks(extracted_data=documents)
text_chunks = [chunk for chunk in text_chunks if chunk.page_content and chunk.page_content.strip()]
print("[2/4] Text Chunks created: ", len(text_chunks))

if len(text_chunks) == 0:
    print("ERROR: No text chunks were created. Check your text files.")
    sys.exit(1)


# Step 3: Create Vector Embeddings
print("[3/4] Loading embedding model (first run downloads the model)...")
def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model = get_embedding_model()


# Step 4: Store embeddings in FAISS
print("[4/4] Building FAISS vector store...")
DB_FAISS_PATH = "vectorstore/db_faiss"
db = FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)
print("DONE! FAISS vector store saved at:", DB_FAISS_PATH)
print(f"Total chunks indexed: {len(text_chunks)}")