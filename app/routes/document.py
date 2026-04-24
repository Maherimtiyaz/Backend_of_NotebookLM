# creating a router for document-related endpoints
from fastapi import APIRouter, Depends, UploadFile, File
from app.services.document_service import DocumentService
from fastapi import Form

# this groups all document-related endpoints under /documents
router = APIRouter(prefix="/documents", tags=["documents"])

# ----------------------------
# CREATE DOCUMENT ENDPOINT
# ----------------------------

# define POST endpoint for cretaeing a document
@router.post("/")
async def create_document(
    user_id: str = Form(...), 
    title: str = Form(...),
    file: UploadFile = File(...)):
    document_id = await DocumentService.create_document(user_id, title, file)
    return {
       "message": "Document created successfully",
       "document_id": document_id
   }

# ---------------------------------
# GET DOCUMENTS ENDPOINT FOR USER
# ---------------------------------

# define GET endpoint for fetching documents of a user
@router.get("/{user_id}")
async def get_documents_by_user(user_id: str):
    documents = await DocumentService.get_documents_by_user(user_id)
    # service return list of documents
    return {"documents": documents}


# ---------------------------------
# DELETE DOCUMENT ENDPOINT
# ---------------------------------

# define DELETE endpoint for deleting a document
@router.delete("/{document_id}")
async def delete_document(document_id: str):
    await DocumentService.delete_document(document_id)
    return {"message": "Document deleted successfully"}

