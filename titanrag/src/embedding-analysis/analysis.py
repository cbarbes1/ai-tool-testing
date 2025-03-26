from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import requests
from typing import List
# # 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")





def extract_text_from_pdf(path: str = "/home/cbarbes/constitution.pdf") -> str:
    reader = PdfReader(path)
    lines = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            # Clean and split into lines
            page_lines = [line.strip() for line in text.splitlines() if line.strip()]
            lines.extend(page_lines)

    return " ".join(lines)

def extract_chunks_from_pdf(path: str = "/home/cbarbes/constitution.pdf", chunk_size=500, overlap=50):
    full_text = extract_text_from_pdf(path)
    # Split into chunks
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        if len(full_text[start:end]) > 1:
            chunks.append(full_text[start:end])
            start = end - overlap  # keep some overlap
    return chunks

def get_relevant(docs: List[str], query: str) -> str:
    embeddings = model.encode(docs)
    query_embedding = model.encode([query])
    # Step 3: Create a FAISS index and add embeddings
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    # Step 5: Retrieve relevant documents
    _, indices = index.search(query_embedding, k=2)
    relevant = "\n".join([chunks[i] for i in indices[0]])
    
    
    return relevant
    
    

chunks = extract_chunks_from_pdf()
print(chunks[:10])

# Step 4: Ask a question
user_question = input("Ask a question: ")

relevant = get_relevant(chunks[:10], user_question)


# Step 6: Generate answer using Ollama
prompt = f"""Answer the question using the context below.

Context:
{relevant}

Question:
{user_question}
"""

res = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "deepseek-r1", "prompt": prompt, "stream": False}
)

print("\n🔍 Answer:")
print(res.json()["response"])