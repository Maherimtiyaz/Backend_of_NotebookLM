# creating a router for document-related endpoints
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from app.services.document_service import DocumentService, upload_document_service

from fastapi import Form

# this groups all document-related endpoints under /documents
router = APIRouter(prefix="/documents", tags=["documents"])


# ----------------------------
# HEALTH CHECK
# ----------------------------
@router.get("/health")
def health():
    return {"status": "ok"}

# ----------------------------
# CREATE DOCUMENT ENDPOINT
# ----------------------------

@router.post("/upload")
async def create_document(
    user_id: str = Form(...), 
    title: str = Form(...),
    file: UploadFile = File(...)):
    document_id = await DocumentService.create_document(user_id, title, file)
    return {
       "message": "Document uploaded successfully",
       "document_id": document_id
   }

# ---------------------------------
# GET DOCUMENTS ENDPOINT FOR USER
# ---------------------------------

@router.get("/users/{user_id}")
async def get_documents_by_user(user_id: str):
    documents = await DocumentService.get_documents_by_user(user_id)
    # service return list of documents
    return {"documents": documents}


# ---------------------------------
# DELETE DOCUMENT ENDPOINT
# ---------------------------------

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    await DocumentService.delete_document(document_id)
    return {"message": "Document deleted successfully"}

# ----------------------------
# GET CHUNKS
# ----------------------------
@router.get("/{document_id}/chunks")
async def get_document_chunks(document_id: str):
    chunks = await DocumentService.get_chunks_by_document(document_id)

    return [
        {
            "id": chunk.id,
            "content": chunk.content,
            "chunk_index": chunk.chunk_index
        }
        for chunk in chunks
    ]

# ----------------------------
# POST UPLOAD DOCUMENTS
# ----------------------------

@router.post("/upload")
async def upload_document(
    user_id: int = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...)
):

    try:
        result = await upload_document_service(
            user_id=user_id,
            title=title,
            file=file
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
