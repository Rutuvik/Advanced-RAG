from sentence_transformers import SentenceTransformer
MODEL_NAME = "BAAI/bge-small-en-v1.5"
class EmbeddingModel:
    def __init__(self, model_name: str = MODEL_NAME):
        print(f"Loading embedding model: {model_name}")
        self.model= SentenceTransformer(model_name)
        print("Embedding model loaded successfully!")
    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        
        embeddings= self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        return embeddings.tolist()
    def embed_query(self, query: str,) -> list[float]:
        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )
        return embedding.tolist()
        