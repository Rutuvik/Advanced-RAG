from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.vector_store import VectorStore
from app.retrieval.parent_store import ParentStore


class Retriever:

    def __init__(
        self,
        top_k: int = 10,
    ):

        self.top_k = top_k

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        self.parent_store = ParentStore()


    def search_children(
        self,
        query: str,
    ):

        query_embedding = (
            self.embedding_model.embed_query(
                query
            )
        )

        results = (
            self.vector_store.client.query_points(
                collection_name=(
                    self.vector_store.collection_name
                ),
                query=query_embedding,
                limit=self.top_k,
                with_payload=True,
            )
        )

        return results.points

    def search_parents(
        self,
        query: str,
    ):
        """
        Dense retrieval followed by parent expansion.

        This method intentionally does NOT rerank.
        It is used by hybrid retrieval.
        """

        child_results = self.search_children(
            query
        )

        parents = {}

        for result in child_results:

            parent_id = result.payload.get(
                "parent_id"
            )

            if not parent_id:
                continue

            parent = self.parent_store.get_parent(
                parent_id
            )

            if not parent:
                continue

            if parent_id not in parents:

                parents[parent_id] = {
                    "parent_id": parent_id,
                    "text": parent["text"],
                    "metadata": parent["metadata"],
                    "best_child_score": result.score,
                    "matched_children": [],
                }

            parents[parent_id][
                "matched_children"
            ].append(
                {
                    "child_id": result.payload.get(
                        "child_id"
                    ),
                    "score": result.score,
                    "text": result.payload.get(
                        "text",
                        "",
                    ),
                }
            )

            parents[parent_id][
                "best_child_score"
            ] = max(
                parents[parent_id][
                    "best_child_score"
                ],
                result.score,
            )

        ranked_parents = sorted(
            parents.values(),
            key=lambda x: x[
                "best_child_score"
            ],
            reverse=True,
        )

        return ranked_parents
