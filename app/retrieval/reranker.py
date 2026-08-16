from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):

        print(
            f"Loading reranker model: {model_name}"
        )

        self.model = CrossEncoder(
            model_name
        )

        print(
            "Reranker loaded successfully!"
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ):

        if not documents:
            return []

        pairs = [
            (
                query,
                document["text"],
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = []

        for document, score in zip(
            documents,
            scores,
        ):

            result = document.copy()

            result["rerank_score"] = float(
                score
            )

            reranked.append(result)

        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        return reranked[:top_k]