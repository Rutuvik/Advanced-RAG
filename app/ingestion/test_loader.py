from pathlib import Path
from app.ingestion.loader import load_document
raw_dir = Path("data/raw")
files=[file 
       for file in raw_dir.iterdir()
       if file.suffix.lower() in {".pdf",".txt",".docx"}]
if not files:
    raise FileNotFoundError("No supported documents found in data/raw/")
for file_path in files:
    print(f"\nLoading:{file_path}")
    documents=load_document(str(file_path))
    print(f"Loaded {len(documents)} document objects")
    for i, document in enumerate(documents[:3]):
        print("\n---Document", i+1,"---")
        print("Content:")
        print(document.page_content[:500])
        print("\nMetadata:")
        print(document.metadata)