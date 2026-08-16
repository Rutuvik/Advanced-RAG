from pathlib import Path

from app.ingestion.loader import load_document
from app.ingestion.normalizer import normalize_document
from app.ingestion.chunker import create_parent_child_chunks


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

    # Test only the first few source documents/pages
    for document in documents[:3]:

        normalized = normalize_document(document)

        parents, children = create_parent_child_chunks(
            normalized
        )

        print(
            f"\nPage: "
            f"{normalized.metadata.get('page', 'N/A')}"
        )

        print(
            f"Parents created: {len(parents)}"
        )

        print(
            f"Children created: {len(children)}"
        )

        for parent in parents:

            print("\n--- PARENT ---")
            print(
                "Parent ID:",
                parent.metadata["parent_id"]
            )

            print(
                "Length:",
                len(parent.page_content)
            )

            print(
                parent.page_content[:500]
            )

            for child in children:

                if (
                    child.metadata["parent_id"]
                    == parent.metadata["parent_id"]
                ):
                    
                    print("\n  --- CHILD ---")

                    print("Child ID:", child.metadata["child_id"])
                    print("Parent ID:", child.metadata["parent_id"])
                    print("Document ID:", child.metadata["document_id"])
                    print("Source:", child.metadata["source"])
                    print("Page:", child.metadata.get("page", "N/A"))
                    print("Length:", len(child.page_content))

                    print("\nContent:")
                    print(child.page_content[:300])
                