from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import settings


COLLECTION_NAME = "advanced_rag"
VECTOR_SIZE = 384


class VectorStore:

    def __init__(
        self,
        collection_name: str = COLLECTION_NAME,
    ):
        self.collection_name = collection_name

        # Use Qdrant Cloud when credentials are configured.
        if settings.qdrant_url and settings.qdrant_api_key:
            print("Using Qdrant Cloud...")
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )

        # Otherwise use local Qdrant.
        else:
            print("Using local Qdrant...")
            self.client = QdrantClient(
                path="data/qdrant"
            )

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