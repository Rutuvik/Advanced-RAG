from app.config import settings
print("Advanced RAG configuration loaded!")
print("LLM:", settings.groq_model)
print("Embedding model:", settings.embedding_model)
print("Top K:", settings.top_k)
print("Rerank Top K:", settings.rerank_top_k)