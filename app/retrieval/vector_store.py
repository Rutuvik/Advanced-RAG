from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME="advanced_rag"
VECTOR_SIZE=384

class VectorStore:
    def __init__(self, collection_name: str = COLLECTION_NAME,):
        self.collection_name=collection_name
        self.client=QdrantClient(path="data/qdrant")
        self._create_collection()
    def _create_collection(self):

        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_collections:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

            print(
                f"Created collection: "
                f"{self.collection_name}"
            )

        else:

            print(
                f"Collection already exists: "
                f"{self.collection_name}"
            )

    def collection_info(self):

        return self.client.get_collection(
            self.collection_name
        )
        