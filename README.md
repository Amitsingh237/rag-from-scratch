# RAG From Scratch 🚀

A hands-on implementation of **Retrieval-Augmented Generation (RAG)** using Python and Large Language Models (LLMs).

This project explores how RAG works internally by implementing its core components from scratch, without initially depending on frameworks such as LangChain or vector databases.

## 🎯 Project Goals

- Understand the fundamentals of Retrieval-Augmented Generation.
- Learn how documents are loaded and processed.
- Generate vector embeddings using Ollama.
- Understand semantic search and cosine similarity.
- Retrieve relevant document chunks based on user queries.
- Build a foundation for developing AI-powered document assistants.

## 🛠️ Technologies Used

- **Python** – Core programming language
- **Ollama** – Running local embedding models
- **OpenAI Python SDK** – Communicating with Ollama's compatible API
- **NumPy** – Vector operations and cosine similarity
- **python-dotenv** – Environment variable management

## 📂 Project Structure

```text
rag-from-scratch/
│
├── Code_Snippets/
│   ├── doc_search.py
│   ├── chunk_search.py
│   ├── semantic_search_test.py
│   ├── stream_test.py
│   ├── stream_tools_test.py
│   └── test_embedding.py
│
├── knowledge_base/
│   └── sample documents
│
├── simple_ai_assistant.py
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Amitsingh237/rag-from-scratch.git
cd rag-from-scratch
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install openai python-dotenv numpy
```

### 4. Install and run Ollama

Download Ollama from:

https://ollama.com/

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
EMBED_MODEL=nomic-embed-text
KB_FOLDER=knowledge_base
```

Do not upload your actual `.env` file or API keys to GitHub.

### 6. Run the project

Run your Python modules from the project root:

```bash
python -m Code_Snippets.doc_search
```

## 🧠 Concepts Being Explored

| Concept | Purpose |
|---|---|
| Document Loading | Read documents from files |
| Text Chunking | Split documents into smaller pieces |
| Embeddings | Convert text into numerical vectors |
| Cosine Similarity | Measure semantic similarity |
| Semantic Search | Find relevant text using embeddings |
| Retrieval | Select the most relevant chunks |
| LLM Integration | Generate answers using retrieved context |

## 📌 Current Implementation

The project initially implements semantic search manually:

1. Load documents from the knowledge base.
2. Split documents into chunks.
3. Generate embeddings for the chunks.
4. Store embeddings in Python data structures.
5. Convert the user query into an embedding.
6. Calculate cosine similarity.
7. Retrieve the most relevant chunks.

**Note:** A dedicated vector database has not yet been integrated. The initial implementation focuses on understanding vector storage and retrieval internally.

## 🚀 Future Improvements

- Integrate ChromaDB or FAISS.
- Build a complete RAG question-answering pipeline.
- Add PDF and DOCX document support.
- Explore multimodal RAG.
- Integrate Agentic AI and tool calling.
- Build a web interface for the AI assistant.

## 📚 Learning Objective

The main objective is to understand the internal working of modern RAG systems by building each component step by step rather than relying entirely on pre-built frameworks.

---

**Built with Python ❤️ | Learning RAG and Agentic AI**
