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


def reciprocal_rank(
    retrieved_pages,
    expected_pages,
):
    """
    Calculate Reciprocal Rank.

    Returns:
        1 / rank of first relevant result
        0 if no relevant result is found
    """

    for rank, page in enumerate(
        retrieved_pages,
        start=1,
    ):

        if page in expected_pages:
            return 1 / rank

    return 0.0


def evaluate():

    total = len(
        EVALUATION_DATASET
    )

    answerable_queries = 0
    unanswerable_queries = 0

    answerable_hits = 0
    unanswerable_correct = 0

    recall_scores = []
    precision_scores = []
    reciprocal_ranks = []

    print("\n" + "=" * 80)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 80)

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1,
    ):

        question = item[
            "question"
        ]

        expected_pages = item.get(
            "expected_pages",
            [],
        )

        expected_sources = item.get(
            "expected_sources",
            [],
        )

        # ==========================================
        # Retrieve
        # ==========================================

        results = retriever.retrieve(
            query=question,
            top_k=5,
        )

        retrieved_pages = []

        retrieved_sources = []

        for result in results:

            metadata = result[
                "metadata"
            ]

            page = metadata.get(
                "page"
            )

            source = metadata.get(
                "source",
                "",
            )

            filename = source.split(
                "/"
            )[-1]

            if page is not None:
                retrieved_pages.append(
                    page
                )

            retrieved_sources.append(
                filename
            )

        # ==========================================
        # Determine query type
        # ==========================================

        is_unanswerable = (
            not expected_pages
            and not expected_sources
        )

        # ==========================================
        # PAGE-BASED ANSWERABLE QUERY
        # ==========================================

        if expected_pages:

            answerable_queries += 1

            relevant_pages = [
                page
                for page in retrieved_pages
                if page in expected_pages
            ]

            hit = bool(
                relevant_pages
            )

            if hit:
                answerable_hits += 1

            # ------------------------------
            # Recall@5
            # ------------------------------

            recall = (
                len(
                    set(relevant_pages)
                )
                /
                len(
                    set(expected_pages)
                )
            )

            recall = min(
                recall,
                1.0,
            )

            recall_scores.append(
                recall
            )

            # ------------------------------
            # Precision@5
            # ------------------------------

            precision = (
                len(
                    set(relevant_pages)
                )
                /
                len(
                    retrieved_pages
                )
                if retrieved_pages
                else 0.0
            )

            precision_scores.append(
                precision
            )

            # ------------------------------
            # MRR@5
            # ------------------------------

            mrr = reciprocal_rank(
                retrieved_pages,
                expected_pages,
            )

            reciprocal_ranks.append(
                mrr
            )

            status = (
                "PASS"
                if hit
                else "FAIL"
            )

            print(
                f"\n[{index}/{total}] "
                f"{status}"
            )

            print(
                "Query type: ANSWERABLE"
            )

            print(
                "Question:",
                question,
            )

            print(
                "Expected pages:",
                expected_pages,
            )

            print(
                "Retrieved pages:",
                retrieved_pages,
            )

            print(
                f"Recall@5: "
                f"{recall:.2%}"
            )

            print(
                f"Precision@5: "
                f"{precision:.2%}"
            )

            print(
                f"MRR@5: "
                f"{mrr:.4f}"
            )

        # ==========================================
        # SOURCE-BASED ANSWERABLE QUERY
        # ==========================================

        elif expected_sources:

            answerable_queries += 1

            matched_sources = [
                source
                for source in retrieved_sources
                if source in expected_sources
            ]

            hit = bool(
                matched_sources
            )

            if hit:
                answerable_hits += 1

            # Source-based retrieval doesn't have
            # meaningful page recall here, so we
            # evaluate source hit separately.

            print(
                f"\n[{index}/{total}] "
                f"{'PASS' if hit else 'FAIL'}"
            )

            print(
                "Query type: ANSWERABLE"
            )

            print(
                "Question:",
                question,
            )

            print(
                "Expected sources:",
                expected_sources,
            )

            print(
                "Retrieved sources:",
                retrieved_sources,
            )

        # ==========================================
        # UNANSWERABLE QUERY
        # ==========================================

        elif is_unanswerable:

            unanswerable_queries += 1

            # Retrieval itself can still return
            # weak candidates. That's okay.
            #
            # The confidence layer should eventually
            # reject this query.

            from app.retrieval.confidence import (
                RetrievalConfidence
            )

            confidence = (
                RetrievalConfidence()
            )

            confidence_result = (
                confidence.evaluate(
                    results
                )
            )

            correctly_rejected = not (
                confidence_result[
                    "should_answer"
                ]
            )

            if correctly_rejected:
                unanswerable_correct += 1

            print(
                f"\n[{index}/{total}] "
                f"{'PASS' if correctly_rejected else 'FAIL'}"
            )

            print(
                "Query type: UNANSWERABLE"
            )

            print(
                "Question:",
                question,
            )

            print(
                "Confidence level:",
                confidence_result[
                    "level"
                ],
            )

            print(
                "Confidence score:",
                confidence_result[
                    "score"
                ],
            )

            print(
                "Should answer:",
                confidence_result[
                    "should_answer"
                ],
            )

    # ==============================================
    # Final metrics
    # ==============================================

    answerable_recall = (
        answerable_hits
        /
        answerable_queries
        if answerable_queries
        else 0.0
    )

    unanswerable_accuracy = (
        unanswerable_correct
        /
        unanswerable_queries
        if unanswerable_queries
        else 0.0
    )

    average_recall = (
        sum(recall_scores)
        /
        len(recall_scores)
        if recall_scores
        else 0.0
    )

    average_precision = (
        sum(precision_scores)
        /
        len(precision_scores)
        if precision_scores
        else 0.0
    )

    average_mrr = (
        sum(reciprocal_ranks)
        /
        len(reciprocal_ranks)
        if reciprocal_ranks
        else 0.0
    )

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(
        f"Total Queries: "
        f"{total}"
    )

    print(
        f"Answerable Queries: "
        f"{answerable_queries}"
    )

    print(
        f"Unanswerable Queries: "
        f"{unanswerable_queries}"
    )

    print(
        f"Answerable Hit Rate: "
        f"{answerable_recall:.2%}"
    )

    print(
        f"Average Recall@5: "
        f"{average_recall:.2%}"
    )

    print(
        f"Average Precision@5: "
        f"{average_precision:.2%}"
    )

    print(
        f"MRR@5: "
        f"{average_mrr:.4f}"
    )

    print(
        f"Unanswerable Detection: "
        f"{unanswerable_accuracy:.2%}"
    )


if __name__ == "__main__":
    evaluate()