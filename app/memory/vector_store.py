import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

VECTOR_STORE_PATH = "memory_index"

def get_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

def save_memory(text: str):
    try:
        embeddings = get_embeddings()
        docs = [Document(page_content=text)]
        if os.path.exists(VECTOR_STORE_PATH):
            store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
            store.add_documents(docs)
        else:
            store = FAISS.from_documents(docs, embeddings)
        store.save_local(VECTOR_STORE_PATH)
    except Exception as e:
        print(f"Memory save failed: {e}")

def get_memory(query: str) -> str:
    try:
        embeddings = get_embeddings()
        if not os.path.exists(VECTOR_STORE_PATH):
            return ""
        store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        docs = store.similarity_search(query, k=2)
        return "\n\n".join([d.page_content for d in docs])
    except Exception as e:
        return ""