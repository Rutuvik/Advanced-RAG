class RetrievalConfidence:

    def __init__(
        self,
        strong_threshold: float = 0.5,
        weak_threshold: float = 0.01,
    ):

        self.strong_threshold = strong_threshold
        self.weak_threshold = weak_threshold

    def evaluate(
        self,
        results: list[dict],
    ):

        if not results:

            return {
                "level": "none",
                "score": 0.0,
                "should_answer": False,
            }

        scores = [
            result.get(
                "rerank_score",
                0.0,
            )
            for result in results
        ]

        best_score = max(scores)

        if best_score >= self.strong_threshold:

            return {
                "level": "high",
                "score": best_score,
                "should_answer": True,
            }

        if best_score >= self.weak_threshold:

            return {
                "level": "medium",
                "score": best_score,
                "should_answer": True,
            }

        return {
            "level": "low",
            "score": best_score,
            "should_answer": False,
        }