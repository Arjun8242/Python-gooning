import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from uuid import uuid4
# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
from rag_app.ingestion import add_doc

app = FastAPI()
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

UPLOAD_DIR = "./uploaded_pdfs"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_MIME_TYPES = {"application/pdf"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


def build_vectorstore(pdf_path: str, doc_id: str):
    return add_doc(doc_id, pdf_path, embedding_function=embeddings)

@app.post("/documents")
async def upload_documents(file: UploadFile = File(...)):
    # 1. Validate MIME type reported by client
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # 2. Read file content and enforce size limit
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum allowed size is 20 MB.")

    # 3. Validate PDF magic bytes (prevents disguised non-PDF uploads)
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Invalid PDF file: missing PDF signature.")

    doc_id = str(uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    with open(save_path, "wb") as f:
        f.write(content)

    try:
        vectorstore = build_vectorstore(save_path, doc_id)
    except Exception as e:
        os.remove(save_path)  # Clean up orphaned file on failure
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {str(e)}")

    return {"message": "Document uploaded successfully", "doc_id": doc_id}
