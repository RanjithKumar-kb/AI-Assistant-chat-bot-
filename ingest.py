import os
import glob
import uuid
from pypdf import PdfReader
from docx import Document
from rag import add_document_to_rag

def run_ingestion():
    ai_folder = "AI"
    if not os.path.exists(ai_folder):
        print(f"Error: The '{ai_folder}' folder does not exist.")
        return

    # Find all supported files (.txt, .pdf, .docx) inside the AI folder
    files = []
    files.extend(glob.glob(os.path.join(ai_folder, "*.txt")))
    files.extend(glob.glob(os.path.join(ai_folder, "*.pdf")))
    files.extend(glob.glob(os.path.join(ai_folder, "*.docx")))
    
    if not files:
        print(f"No .txt, .pdf, or .docx files found in the '{ai_folder}' folder.")
        return

    print(f"Found {len(files)} file(s). Starting ingestion...")
    total_chunks = 0

    for file_path in files:
        print(f"Processing: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()
        content = ""

        try:
            # 1. Read Text Files
            if ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

            # 2. Read PDF Files
            elif ext == ".pdf":
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"

            # 3. Read Word (.docx) Files
            elif ext == ".docx":
                doc = Document(file_path)
                for para in doc.paragraphs:
                    if para.text:
                        content += para.text + "\n"

        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            continue

        # Split content into individual line chunks for precise search matching
        chunks = [chunk.strip() for chunk in content.split("\n") if chunk.strip()]

        for chunk in chunks:
            doc_id = str(uuid.uuid4())
            add_document_to_rag(doc_id, chunk, metadata={"source": os.path.basename(file_path)})
            total_chunks += 1

    print(f"Successfully loaded a total of {total_chunks} chunks from {len(files)} file(s) into your RAG database!")

if __name__ == "__main__":
    run_ingestion()