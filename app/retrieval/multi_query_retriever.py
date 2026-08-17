
from app.retrieval.query_expander import QueryExpander
from app.retrieval.hybrid_retriever import HybridRetriever


class MultiQueryRetriever:

    def __init__(
        self,
        num_queries: int = 3,
        dense_top_k: int = 10,
        bm25_top_k: int = 10,
        rerank_top_k: int = 5,
    ):

        self.query_expander = QueryExpander(
            num_queries=num_queries
        )

        self.hybrid_retriever = HybridRetriever(
            dense_top_k=dense_top_k,
            bm25_top_k=bm25_top_k,
            rerank_top_k=rerank_top_k,
        )
        self.last_trace = {}
    def retrieve(
    self,
    query: str,
    top_k: int = 5,
    ):

        print("\n[MQR] Starting multi-query retrieval")
        print(f"[MQR] Original query: {query}")

        # ==================================================
        # 1. Query Expansion
        # ==================================================

        print("[MQR] Expanding query...")

        queries = self.query_expander.expand(query)

        print(
            f"[MQR] Query expansion completed: "
            f"{len(queries)} queries"
        )

        for index, search_query in enumerate(
            queries,
            start=1,
        ):
            print(f"{index}. {search_query}")

        # ==================================================
        # 2. Hybrid Retrieval
        # ==================================================

        all_candidates = {}

        retrieval_stats = []

        for search_query in queries:

            print(
                f"\n[MQR] Retrieving candidates for: "
                f"{search_query}"
            )

            candidates = (
                self.hybrid_retriever
                .retrieve_candidates(search_query)
            )

            print(
                f"[MQR] Candidates returned: "
                f"{len(candidates)}"
            )

            retrieval_stats.append({
                "query": search_query,
                "candidates": len(candidates),
            })

            for candidate in candidates:

                parent_id = candidate["parent_id"]

                if parent_id not in all_candidates:

                    all_candidates[parent_id] = {
                        **candidate,
                        "query_matches": [],
                    }

                all_candidates[parent_id][
                    "query_matches"
                ].append({
                    "query": search_query,
                    "rrf_score": candidate["rrf_score"],
                })

        # ==================================================
        # 3. Multi-query scoring
        # ==================================================

        candidates = list(
            all_candidates.values()
        )

        for candidate in candidates:

            query_matches = candidate[
                "query_matches"
            ]

            scores = [
                match["rrf_score"]
                for match in query_matches
            ]

            max_score = max(scores)

            query_match_count = len(
                query_matches
            )

            candidate["multi_query_score"] = (
                max_score +
                (0.01 * query_match_count)
            )

            candidate["query_match_count"] = (
                query_match_count
            )

        # ==================================================
        # 4. Sort before reranking
        # ==================================================

        candidates.sort(
            key=lambda x: x["multi_query_score"],
            reverse=True,
        )

        # ==================================================
        # 5. Reranking
        # ==================================================

        print(
            f"\n[MQR] Starting reranking for "
            f"{len(candidates)} candidates..."
        )

        reranked = (
            self.hybrid_retriever
            .reranker
            .rerank(
                query=query,
                documents=candidates,
                top_k=top_k,
            )
        )

        print(
            f"[MQR] Reranking completed. "
            f"Results: {len(reranked)}"
        )

        # ==================================================
        # 6. Store trace for frontend/API
        # ==================================================

        self.last_trace = {
            "original_query": query,
            "expanded_queries": queries,
            "query_count": len(queries),
            "total_candidates": len(candidates),
            "retrieval_stats": retrieval_stats,
            "reranked_results": len(reranked),
            "results": [
                {
                    "parent_id": result["parent_id"],
                    "rerank_score": result.get(
                        "rerank_score",
                        0,
                    ),
                    "rrf_score": result.get(
                        "rrf_score",
                        0,
                    ),
                    "multi_query_score": result.get(
                        "multi_query_score",
                        0,
                    ),
                    "query_match_count": result.get(
                        "query_match_count",
                        0,
                    ),
                }
                for result in reranked
            ],
        }

        return {
    "results": reranked,
    "queries": queries,
    "candidate_count": len(candidates),
}