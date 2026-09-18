import os
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize Chroma client locally
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="chatbot_docs")

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def add_document_to_rag(doc_id, text, metadata=None):
    """Embeds and adds text chunks to the local vector store."""
    embedding = embedding_model.encode(text).tolist()
    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata or {}]
    )

def search_docs(query, n_results=2):
    """Searches your stored information for relevant context."""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents)