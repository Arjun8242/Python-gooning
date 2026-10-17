from langchain_chroma import Chroma
from rag_app.ingestion import get_doc_by_id

def get_retriever(doc_id:str, embedding_function, k: int = 10):

    if get_doc_by_id(doc_id) is None:
        raise ValueError(f"Document with ID {doc_id} not found.")
        
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_function,
        collection_name=doc_id,
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})