from collections import defaultdict

from app.retrieval.retriever import Retriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.reranker import Reranker


class HybridRetriever:

    def __init__(
        self,
        dense_top_k: int = 10,
        bm25_top_k: int = 10,
        rrf_k: int = 60,
        rerank_top_k: int = 5,
    ):

        self.dense_retriever = Retriever(
            top_k=dense_top_k
        )

        self.bm25_retriever = BM25Retriever()

        self.reranker = Reranker()

        self.bm25_top_k = bm25_top_k
        self.rrf_k = rrf_k
        self.rerank_top_k = rerank_top_k
    def retrieve_candidates(
        self,
        query: str,
    ):

        dense_results = (
            self.dense_retriever.search_parents(
                query
            )
        )

        bm25_results = (
            self.bm25_retriever.retrieve(
                query,
                top_k=self.bm25_top_k,
            )
        )

        rrf_scores = defaultdict(float)
        parent_objects = {}

        # Dense ranking
        for rank, parent in enumerate(
            dense_results,
            start=1,
        ):

            parent_id = parent["parent_id"]

            rrf_scores[parent_id] += (
                1.0 /
                (self.rrf_k + rank)
            )

            parent_objects[parent_id] = parent

        # BM25 ranking
        for rank, result in enumerate(
            bm25_results,
            start=1,
        ):

            parent = result["parent"]

            parent_id = (
                parent["metadata"]["parent_id"]
            )

            rrf_scores[parent_id] += (
                1.0 /
                (self.rrf_k + rank)
            )

            parent_objects[parent_id] = parent

        ranked = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        candidates = []

        for parent_id, score in ranked:

            parent = parent_objects[parent_id]

            candidates.append(
                {
                    "parent_id": parent_id,
                    "text": parent["text"],
                    "metadata": parent["metadata"],
                    "rrf_score": score,
                    "matched_children": parent.get(
                        "matched_children",
                        [],
                    ),
                }
            )

        return candidates
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        candidates = self.retrieve_candidates(
            query
        )

        reranked = self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )

        return reranked
    