import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from filelock import FileLock
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

REGISTRY_PATH = "./doc_registry.json"
REGISTRY_LOCK = "./doc_registry.lock"


def load_registry() -> Dict[str, Dict]:
    """Load the document registry from disk.
    
    Returns an empty dict if the file doesn't exist yet.
    Uses a file lock to prevent concurrent read/write conflicts.
    """
    with FileLock(REGISTRY_LOCK):
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, 'r') as f:
                return json.load(f)
    return {}


def save_registry(data: Dict):
    """Persist the full registry dict back to disk.
    
    Uses a file lock to prevent concurrent write conflicts.
    """
    with FileLock(REGISTRY_LOCK):
        with open(REGISTRY_PATH, 'w') as f:
            json.dump(data, f, indent=2)


def add_doc(doc_id: str, pdf_path: str, embedding_function, metadata: dict = None):
    """Ingest a PDF into ChromaDB and record it in the registry.

    Steps:
      1. Load the PDF pages
      2. Split into overlapping chunks
      3. Store the chunks in a Chroma collection named after doc_id
      4. Record the doc_id, path, chunk count, and timestamp in the registry
    
    Returns the Chroma vectorstore for the new collection.
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    ).split_documents(docs)

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_function,
        collection_name=doc_id
    )
    
    vectorstore.add_documents(chunks)

    registry = load_registry()
    registry[doc_id] = {
        "pdf_path": pdf_path,
        "chunk_count": len(chunks),
        "ingested_at": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    save_registry(registry)

    return vectorstore


def get_doc_by_id(doc_id: str) -> Optional[Dict]:
    """Look up a document's registry entry by its ID.

    Returns the metadata dict if found, or None if the doc_id
    hasn't been ingested.
    """
    registry = load_registry()
    return registry.get(doc_id, None)


def get_all_doc_ids() -> List[str]:
    """Return a list of every ingested document ID."""
    registry = load_registry()
    return list(registry.keys())


def delete_doc_by_id(doc_id: str):
    """Remove a document from both ChromaDB and the registry.

    Steps:
      1. Connect to the Chroma collection for this doc_id (no embedding function needed for deletion)
      2. Delete the entire collection
      3. Remove the entry from the JSON registry
    """
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        collection_name=doc_id
    )
    vectorstore.delete_collection()

    registry = load_registry()
    if doc_id in registry:
        del registry[doc_id]
        save_registry(registry)