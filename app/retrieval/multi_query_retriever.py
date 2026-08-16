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

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        # ==================================================
        # 1. Generate multiple search queries
        # ==================================================

        queries = self.query_expander.expand(
            query
        )

        print("\nGenerated search queries:")

        for index, search_query in enumerate(
            queries,
            start=1,
        ):
            print(
                f"{index}. {search_query}"
            )

        # ==================================================
        # 2. Retrieve candidates for every query
        # ==================================================

        all_candidates = {}

        for search_query in queries:

            candidates = (
                self.hybrid_retriever
                .retrieve_candidates(
                    search_query
                )
            )

            for candidate in candidates:

                parent_id = candidate[
                    "parent_id"
                ]

                # ------------------------------------------
                # First time seeing this parent
                # ------------------------------------------

                if parent_id not in all_candidates:

                    all_candidates[parent_id] = {
                        **candidate,
                        "query_matches": [],
                    }

                # ------------------------------------------
                # Store how this parent matched
                # ------------------------------------------

                all_candidates[
                    parent_id
                ]["query_matches"].append(
                    {
                        "query": search_query,
                        "rrf_score": candidate[
                            "rrf_score"
                        ],
                    }
                )

        # ==================================================
        # 3. Calculate multi-query score
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

            # Highest score means the document
            # strongly matched at least one query.
            max_score = max(scores)

            # Number of different generated queries
            # that retrieved this document.
            query_match_count = len(
                query_matches
            )

            # ------------------------------------------------
            # Multi-query score
            #
            # max_score:
            #   rewards strong relevance
            #
            # match_count:
            #   rewards consistency across queries
            # ------------------------------------------------

            candidate[
                "multi_query_score"
            ] = (
                max_score
                + (
                    0.01
                    * query_match_count
                )
            )

            candidate[
                "query_match_count"
            ] = query_match_count

        # ==================================================
        # 4. Sort candidates before reranking
        # ==================================================

        candidates.sort(
            key=lambda x: x[
                "multi_query_score"
            ],
            reverse=True,
        )

        # ==================================================
        # 5. Rerank using original query
        # ==================================================

        reranked = (
            self.hybrid_retriever
            .reranker
            .rerank(
                query=query,
                documents=candidates,
                top_k=top_k,
            )
        )

        # ==================================================
        # 6. Return final results
        # ==================================================

        return reranked