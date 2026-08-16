from pathlib import Path
from langchain_community.document_loaders import(
    PyMuPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)
SUPPORTED_EXTENSIONS={
    ".pdf",
    ".docx",
    ".txt",
}
def load_document(file_path:str):
    path=Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found:{file_path}")
    extension=path.suffix.lower()
    if extension==".pdf":
        loader=PyMuPDFLoader(str(path))
        
    elif extension==".txt":
        loader=TextLoader(
            str(path),
            encoding="utf-8",)
    elif extension == ".docx":
        loader=UnstructuredWordDocumentLoader(str(path))
        
    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )
    return loader.load()