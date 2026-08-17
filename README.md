# Advanced RAG System

A production-style Retrieval-Augmented Generation (RAG) system that delivers accurate, grounded answers from a technical knowledge base using hybrid retrieval, reranking, and confidence-aware generation.

## Overview

Advanced RAG combines hybrid retrieval, multi-query expansion, parent-child document retrieval, cross-encoder reranking, and confidence evaluation into a single pipeline — going well beyond a basic vector-search chatbot. It ships with a FastAPI backend and a React frontend for interactive question answering.

## Features

- **Multi-Query Expansion** – Generates multiple search queries from the original question to improve retrieval recall.
- **Hybrid Retrieval** – Combines dense vector search (Qdrant) with BM25 keyword search.
- **RRF Fusion** – Merges results from multiple retrieval strategies using Reciprocal Rank Fusion.
- **Parent-Child Retrieval** – Retrieves precise child chunks while expanding to parent documents for richer context.
- **Multi-Query Scoring** – Boosts documents that are consistently retrieved across multiple generated queries.
- **Cross-Encoder Reranking** – Reorders candidates using `BAAI/bge-reranker-base` for higher relevance.
- **Confidence Evaluation** – Scores retrieval quality and rejects/falls back when evidence is insufficient, reducing hallucinations.
- **Context Builder** – Assembles a focused, relevant context window for the LLM.
- **Grounded Generation** – Generates answers using Groq, strictly from retrieved context.
- **Performance Metrics** – Tracks per-stage and total pipeline latency.
- **Source Attribution** – Returns the documents used to generate each answer.
- **FastAPI Backend** – REST API with `/`, `/health`, and `/query` endpoints.
- **React Frontend** – Interactive UI for asking questions and viewing answers, sources, confidence, and metrics.

## Architecture

```
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI API
 │
 ▼
RAG Pipeline
 │
 ├── Multi-Query Expansion
 │
 ├── Hybrid Retrieval
 │    ├── Dense Search → Qdrant
 │    └── BM25 Search
 │
 ├── RRF Fusion
 │
 ├── Parent Document Expansion
 │
 ├── Multi-Query Scoring
 │
 ├── Cross-Encoder Reranking
 │
 ├── Confidence Evaluation
 │
 ├── Context Construction
 │
 └── LLM Generation → Groq
 │
 ▼
Answer + Sources + Confidence + Metrics
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic, Uvicorn |
| Retrieval | Qdrant, BM25, Sentence Transformers, RRF |
| Embedding Model | `BAAI/bge-small-en-v1.5` |
| Reranker | `BAAI/bge-reranker-base` |
| LLM | Groq API |
| Frontend | React, Vite, JavaScript, CSS |
| Tooling | Git, GitHub |

## Project Structure

```
advanced-rag/
├── app/
│   ├── api/
│   │   └── server.py
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── parent_store.py
│   │   ├── indexer.py
│   │   ├── retriever.py
│   │   ├── bm25_retriever.py
│   │   ├── hybrid_retriever.py
│   │   ├── multi_query_retriever.py
│   │   ├── query_expander.py
│   │   ├── reranker.py
│   │   └── confidence.py
│   ├── generation/
│   │   └── groq_generator.py
│   ├── context_builder.py
│   └── rag_pipeline.py
├── data/
│   └── parent_store.json
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   └── package.json
├── requirements.txt
├── .python-version
├── .gitignore
└── README.md
```

## Run Locally

### Prerequisites

- Python 3.11
- Node.js & npm
- Qdrant account / API credentials
- Groq API key

### Backend

```bash
git clone https://github.com/Rutuvik/Advanced-RAG.git
cd Advanced-RAG

python3.11 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

Start the API:

```bash
python -m uvicorn app.api.server:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- Frontend: `http://localhost:5173`

## Why This Approach?

A basic vector-search RAG system can fail when query terminology doesn't match the documents, exact keywords matter, top vector results aren't the most relevant, or weak evidence still gets an answer. This architecture addresses each of these with a dedicated stage:

| Problem | Solution |
|---|---|
| Query vocabulary mismatch | Multi-query expansion |
| Missing exact terminology | BM25 keyword search |
| Combining retrieval methods | RRF fusion |
| Insufficient chunk context | Parent-child retrieval |
| Irrelevant retrieved documents | Cross-encoder reranking |
| Inconsistent retrieval | Multi-query scoring |
| Weak evidence | Confidence evaluation |
| Unfocused context | Context builder |
| Unknown latency bottlenecks | Pipeline metrics |

## Current Limitations

This project targets local development, experimentation, and portfolio demonstration. Not yet implemented: authentication, rate limiting, distributed tracing, streaming responses, conversation persistence, and CI/CD deployment.

## Future Improvements

- RAG evaluation on benchmark datasets (retrieval precision/recall, faithfulness)
- Streaming LLM responses
- Authentication, authorization, and rate limiting
- Redis caching and async retrieval/generation
- Document upload interface and conversation history
- Docker-based deployment and CI/CD pipeline

## Goal

Demonstrate how a basic RAG chatbot can be extended into a reliable, explainable, and measurable retrieval system — through hybrid search, reranking, confidence-based decisions, source attribution, and performance monitoring.

## Author

**Rutvik Chavhan**
GitHub: [github.com/Rutuvik](https://github.com/Rutuvik)

## License

This project is intended for educational, research, and portfolio purposes.
