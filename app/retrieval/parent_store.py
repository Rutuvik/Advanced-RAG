import json
from pathlib import Path


class ParentStore:

    def __init__(
        self,
        path: str = "data/parent_store.json",
    ):
        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.path.exists():
            with open(
                self.path,
                "r",
                encoding="utf-8",
            ) as f:
                self.parents = json.load(f)

        else:
            self.parents = {}

    def add_parent(
        self,
        parent_id: str,
        text: str,
        metadata: dict,
    ):

        self.parents[parent_id] = {
            "text": text,
            "metadata": metadata,
        }

    def get_parent(
        self,
        parent_id: str,
    ):

        return self.parents.get(
            parent_id
        )

    def save(self):

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.parents,
                f,
                indent=2,
                ensure_ascii=False,
            )

    def count(self):

        return len(self.parents)