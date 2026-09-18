import uuid
from rag import add_document_to_rag

# Add all your personal information and documents here
my_personal_info = [
    "My name is [Your Name] and I live in [Your City].",
    "I am building a Flask chatbot project named Lumina using Ollama[cite: 1, 3] and local LLMs.",
    "Here are some notes about my project architecture: It uses Flask for the backend, database.py[cite: 3] for session storage, and ChromaDB for RAG.",
    # Add as many custom facts or text lines as you need!
]

def run_ingestion():
    print("Ingesting your information into the RAG model...")
    for text in my_personal_info:
        doc_id = str(uuid.uuid4())
        add_document_to_rag(doc_id, text, metadata={"source": "user_input"})
    print(f"Successfully loaded {len(my_personal_info)} pieces of information into your RAG database!")

if __name__ == "__main__":
    run_ingestion()