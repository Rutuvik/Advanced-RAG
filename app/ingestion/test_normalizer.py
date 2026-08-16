from pathlib import Path

from app.ingestion.loader import load_document
from app.ingestion.normalizer import normalize_document


raw_dir = Path("data/raw")

files = [
    file
    for file in raw_dir.iterdir()
    if file.suffix.lower() in {".pdf", ".txt", ".docx"}
]


for file_path in files:

    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    documents = load_document(str(file_path))

    for i, document in enumerate(documents[:3]):

        normalized = normalize_document(document)

        print(f"\n--- Normalized Document {i + 1} ---")

        print("\nMetadata:")
        print(normalized.metadata)

        print("\nContent:")
        print(normalized.page_content[:700])