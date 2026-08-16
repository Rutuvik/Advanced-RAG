from app.retrieval.vector_store import VectorStore


vector_store = VectorStore()

info = vector_store.collection_info()

print("\nQdrant collection information")
print("--------------------------------")

print("Collection:", vector_store.collection_name)

print("Vectors:", info.points_count)

print("Vector size:", info.config.params.vectors.size)

print("Distance:", info.config.params.vectors.distance)