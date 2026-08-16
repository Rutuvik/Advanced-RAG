from pathlib import Path
from uuid import uuid4

from qdrant_client.models import PointStruct

from app.retrieval.parent_store import ParentStore
from app.ingestion.loader import load_document
from app.ingestion.normalizer import normalize_document
from app.ingestion.chunker import create_parent_child_chunks
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.vector_store import VectorStore


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def get_source_files():

    raw_dir = Path("data/raw")

    return [
        file
        for file in raw_dir.iterdir()
        if file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def index_documents():

    print("\nInitializing embedding model...")

    embedding_model = EmbeddingModel()

    print("\nInitializing vector store...")

    vector_store = VectorStore()

    print("\nInitializing parent store...")

    parent_store = ParentStore()

    source_files = get_source_files()

    total_children = 0

    for file_path in source_files:

        print("\n" + "=" * 70)
        print(f"Processing: {file_path.name}")
        print("=" * 70)

        documents = load_document(
            str(file_path)
        )

        print(
            f"Loaded {len(documents)} documents/pages"
        )

        for document in documents:

            normalized = normalize_document(
                document
            )

            parents, children = (
                create_parent_child_chunks(
                    normalized
                )
            )

            # Store parent chunks
            for parent in parents:

                parent_store.add_parent(
                    parent_id=parent.metadata["parent_id"],
                    text=parent.page_content,
                    metadata=parent.metadata,
                )

            if not children:
                continue

            print(
                f"Page: "
                f"{normalized.metadata.get('page', 'N/A')} "
                f"| Parents: {len(parents)} "
                f"| Children: {len(children)}"
            )

            # Extract child text
            texts = [
                child.page_content
                for child in children
            ]

            # Generate embeddings
            embeddings = (
                embedding_model.embed_documents(
                    texts
                )
            )

            points = []

            for child, embedding in zip(
                children,
                embeddings,
            ):

                payload = {
                    "text": child.page_content,
                    **child.metadata,
                }

                point = PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload=payload,
                )

                points.append(point)

            # Store child vectors in Qdrant
            vector_store.client.upsert(
                collection_name=(
                    vector_store.collection_name
                ),
                points=points,
            )

            total_children += len(children)

    # Save all parents once after indexing completes
    parent_store.save()

    print(
        f"\nTotal parents stored: "
        f"{parent_store.count()}"
    )

    print("\n" + "=" * 70)
    print("INDEXING COMPLETE")
    print("=" * 70)

    print(
        f"Total child chunks indexed: "
        f"{total_children}"
    )


if __name__ == "__main__":
    index_documents()