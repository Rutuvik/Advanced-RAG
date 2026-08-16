import re

from rank_bm25 import BM25Okapi

from app.retrieval.parent_store import ParentStore


class BM25Retriever:

    def __init__(self):

        self.parent_store = ParentStore()

        self.parents = []
        self.tokenized_corpus = []
        self.bm25 = None

        self._build_index()

    def tokenize(self, text: str) -> list[str]:
        """
        Convert text into lowercase tokens.
        """

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )

    def _build_index(self):

        # ParentStore stores parent records as dictionaries
        self.parents = list(
            self.parent_store.parents.values()
        )

        if not self.parents:
            raise ValueError(
                "No parent documents found in ParentStore."
            )

        self.tokenized_corpus = [
            self.tokenize(
                parent["text"]
            )
            for parent in self.parents
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_corpus
        )

        print(
            f"BM25 index built: "
            f"{len(self.parents)} parents"
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ):

        query_tokens = self.tokenize(
            query
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:top_k]:

            parent = self.parents[index]
            results.append(
                {
                    "parent": {
                        "parent_id": parent[
                            "metadata"
                        ]["parent_id"],
                        "text": parent["text"],
                        "metadata": parent["metadata"],
                        "matched_children": [],
                },
                "score": float(
                scores[index]
            ),
        }
    )

            

        return results