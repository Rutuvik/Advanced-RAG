import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


PARENT_CHUNK_SIZE = 1200
PARENT_CHUNK_OVERLAP = 150

CHILD_CHUNK_SIZE = 350
CHILD_CHUNK_OVERLAP = 50


def generate_id(value: str) -> str:
    """
    Generate a deterministic ID.
    """
    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:16]


def create_parent_chunks(
    document: Document,
) -> list[Document]:
    """
    Split a normalized document into larger parent chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_CHUNK_SIZE,
        chunk_overlap=PARENT_CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    parent_texts = splitter.split_text(
        document.page_content
    )

    parents = []

    # Page is important for making IDs unique.
    # DOCX/TXT documents may not have a page number.
    page = document.metadata.get(
        "page",
        "document",
    )

    for index, text in enumerate(parent_texts):

        parent_id = generate_id(
            f"{document.metadata['document_id']}"
            f":page:{page}"
            f":parent:{index}"
        )

        metadata = document.metadata.copy()

        metadata.update(
            {
                "parent_id": parent_id,
                "parent_index": index,
                "chunk_type": "parent",
            }
        )

        parents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return parents


def create_child_chunks(
    parent: Document,
) -> list[Document]:
    """
    Split a parent chunk into smaller child chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_CHUNK_SIZE,
        chunk_overlap=CHILD_CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            "",
        ],
    )

    child_texts = splitter.split_text(
        parent.page_content
    )

    children = []

    for index, text in enumerate(child_texts):

        child_id = generate_id(
            f"{parent.metadata['parent_id']}"
            f":child:{index}"
        )

        metadata = parent.metadata.copy()

        metadata.update(
            {
                "child_id": child_id,
                "child_index": index,
                "chunk_type": "child",
            }
        )

        children.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return children


def create_parent_child_chunks(
    document: Document,
) -> tuple[list[Document], list[Document]]:
    """
    Create parent and child chunks from a normalized document.
    """

    parents = create_parent_chunks(document)

    children = []

    for parent in parents:

        children.extend(
            create_child_chunks(parent)
        )

    return parents, children