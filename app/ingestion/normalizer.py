import hashlib
import re
from pathlib import Path
from langchain_core.documents import Document
def generate_document_id(source: str) -> str:
    """Generate a stable ID from the source path.
    """
    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()[:16]
    
def clean_text(text: str) -> str:
    """
    Clean and reconstruct extracted PDF/DOCX text.

    Handles:
    - excessive whitespace
    - broken single-character PDF extraction
    - excessive blank lines
    - control characters
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove non-printable/control characters
    text = "".join(
        char
        for char in text
        if char == "\n"
        or char == "\t"
        or char.isprintable()
    )

    lines = text.split("\n")

    reconstructed_lines = []
    character_buffer = []

    def flush_character_buffer():
        if character_buffer:
            reconstructed_lines.append(
                "".join(character_buffer)
            )
            character_buffer.clear()

    for line in lines:
        stripped = line.strip()

        # Completely empty line
        if not stripped:
            flush_character_buffer()

            # Preserve a paragraph break
            if (
                not reconstructed_lines
                or reconstructed_lines[-1] != ""
            ):
                reconstructed_lines.append("")

            continue

        # If the extracted line contains exactly one
        # alphanumeric character, it is probably part
        # of a word broken by the PDF extractor.
        if len(stripped) == 1 and stripped.isalnum():
            character_buffer.append(stripped)
            continue

        # Normal line
        flush_character_buffer()
        reconstructed_lines.append(stripped)

    flush_character_buffer()

    # Remove excessive blank lines
    cleaned_lines = []

    previous_blank = False

    for line in reconstructed_lines:

        if not line:
            if not previous_blank:
                cleaned_lines.append("")

            previous_blank = True

        else:
            cleaned_lines.append(line)
            previous_blank = False

    text = "\n".join(cleaned_lines)

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces surrounding newlines
    text = re.sub(r" *\n *", "\n", text)

    # Maximum two consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
    
def normalize_document(document: Document) -> Document:
    """
    Convert a raw LangChain Document into our
    normalized document representation.
    """

    source = document.metadata.get("source", "unknown")

    source_path = Path(source)

    document_id = generate_document_id(str(source_path))

    cleaned_text = clean_text(document.page_content)

    metadata = {
        "document_id": document_id,
        "source": str(source_path),
        "filename": source_path.name,
        "file_type": source_path.suffix.lower().replace(".", ""),
    }

    # Preserve page number when available
    if "page" in document.metadata:
        metadata["page"] = document.metadata["page"]

    # Preserve total page count when available
    if "total_pages" in document.metadata:
        metadata["total_pages"] = document.metadata["total_pages"]

    return Document(
        page_content=cleaned_text,
        metadata=metadata,
    )