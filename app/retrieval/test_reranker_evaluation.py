from app.retrieval.multi_query_retriever import (
    MultiQueryRetriever
)

from app.evaluation_dataset import (
    EVALUATION_DATASET
)


retriever = MultiQueryRetriever(
    num_queries=3,
    dense_top_k=10,
    bm25_top_k=10,
)


def evaluate_reranker():

    print("\n" + "=" * 80)
    print("RERANKER EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1,
    ):

        question = item["question"]

        expected_pages = item.get(
            "expected_pages",
            [],
        )

        # Skip unanswerable query
        if not expected_pages:
            continue

        print("\n" + "-" * 80)
        print(
            f"[{index}] {question}"
        )
        print(
            f"Expected pages: {expected_pages}"
        )

        # --------------------------------------------------
        # Generate queries
        # --------------------------------------------------

        queries = (
            retriever.query_expander.expand(
                question
            )
        )

        # --------------------------------------------------
        # Collect candidates BEFORE reranking
        # --------------------------------------------------

        all_candidates = {}

        for search_query in queries:

            candidates = (
                retriever.hybrid_retriever
                .retrieve_candidates(
                    search_query
                )
            )

            for candidate in candidates:

                parent_id = candidate[
                    "parent_id"
                ]

                if parent_id not in all_candidates:

                    all_candidates[
                        parent_id
                    ] = {
                        **candidate,
                        "query_matches": [],
                    }

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

        candidates = list(
            all_candidates.values()
        )

        # --------------------------------------------------
        # Candidate ranking before reranking
        # --------------------------------------------------

        candidates.sort(
            key=lambda x: max(
                match["rrf_score"]
                for match in x[
                    "query_matches"
                ]
            ),
            reverse=True,
        )

        candidate_pool = candidates[:20]

        print("\nBEFORE RERANKING")

        for rank, candidate in enumerate(
            candidate_pool,
            start=1,
        ):

            page = candidate[
                "metadata"
            ].get("page")

            score = candidate[
                "rrf_score"
            ]

            marker = (
                " <-- EXPECTED"
                if page in expected_pages
                else ""
            )

            print(
                f"{rank}. "
                f"Page {page} | "
                f"RRF={score:.6f}"
                f"{marker}"
            )

        # --------------------------------------------------
        # Reranking
        # --------------------------------------------------

        reranked = (
            retriever.hybrid_retriever
            .reranker
            .rerank(
                query=question,
                documents=candidate_pool,
                top_k=10,
            )
        )

        print("\nAFTER RERANKING")

        for rank, result in enumerate(
            reranked,
            start=1,
        ):

            page = result[
                "metadata"
            ].get("page")

            score = result.get(
                "rerank_score"
            )

            marker = (
                " <-- EXPECTED"
                if page in expected_pages
                else ""
            )

            print(
                f"{rank}. "
                f"Page {page} | "
                f"Rerank={score:.6f}"
                f"{marker}"
            )


if __name__ == "__main__":
    evaluate_reranker()