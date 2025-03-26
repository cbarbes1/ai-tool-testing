
# Custom RAG System Design Summary

## Goal
Build a modular Retrieval-Augmented Generation (RAG) system with functionality similar to LangChain. The goal is to:

- Keep components separate and swappable
- Support file ingestion from various formats
- Enable chunking, embedding, and vector retrieval
- Chain components together in a configurable flow
- Support interaction with local LLMs (like Ollama)
- Optionally include chat history, streaming, and parallel execution

---

## Core RAG Pipeline Components

### 1. **Ingestion / Loader Tool**
- Extracts raw text from multiple file types (PDF, DOCX, TXT, etc.)
- Cleans text and attaches metadata (filename, page number, etc.)
- Output: List of `Document` objects with `content` and `metadata`

### 2. **Chunker**
- Splits large texts into smaller chunks
- Configurable by size, overlap, or semantic boundaries
- Retains reference to original metadata

### 3. **Embedder**
- Converts chunks to vector embeddings
- Uses local embedding models (e.g., `sentence-transformers`) or APIs
- Output includes vector and associated metadata

### 4. **Vector Store / Retriever**
- Stores and indexes embedded vectors
- Supports fast similarity search (FAISS, Chroma, etc.)
- Interface to retrieve top-k similar documents

### 5. **Prompt Builder / Context Assembler**
- Builds prompt by merging retrieved documents and user query
- Includes options for formatting, compression, or history inclusion

### 6. **LLM Interface**
- Sends prompt to local or API-based LLM (e.g., Ollama, OpenAI)
- Handles retries, streaming, and output formatting

### 7. **Chaining System**
- Connects components like ingestion → embedding → retrieval → LLM
- Should support:
  - Sequential chaining
  - Parallel execution
  - Optional branching (if/else logic)

---

## Conversation History Support
- Maintain a list of `{role, content}` message objects per session
- Support retrieving recent turns or summarizing long history
- Integrate with prompt assembly to maintain conversation flow

---

## Multithreading & Parallel Execution
- Use multithreading/multiprocessing where applicable:
  - Parallel embedding generation
  - Concurrent file ingestion
  - Async vector store retrieval
- Use `ThreadPoolExecutor` or `asyncio.gather` depending on task type

---

## Suggested Folder Structure

```
titanrag/
├── ingest/
│   ├── loader.py           # load text from PDF, DOCX, etc.
│   ├── chunker.py          # split into chunks
├── embed/
│   ├── embedder.py         # create embeddings
│   └── vector_store.py     # FAISS/Chroma wrapper
├── retrieve/
│   └── retriever.py        # search vector store
├── llm/
│   ├── client.py           # main LLMClient
│   ├── backends/           # ollama.py, openai.py, etc.
├── chains/
│   └── rag_chain.py        # orchestrates full RAG flow
├── utils/
│   └── text_cleaning.py
├── main.py                 # CLI / entry point
└── requirements.txt
```

---

## LLMClient Abstraction
- Accepts provider (e.g., Ollama, OpenAI) and model name
- Unified `.generate()` interface
- Abstracts backend-specific logic
- Can later support `.stream()`, `.chat()`, etc.
- Keeps LLM integration clean and swappable

---

## Next Steps
- Build the file loader and chunker tool
- Implement `LLMClient` for local Ollama support
- Set up basic chain execution structure
- Add retrieval + prompt assembly
- Optionally: add conversation history + multithreading

---

_This summary captures the high-level design goals and architecture discussed for building a modular, extensible RAG engine._

