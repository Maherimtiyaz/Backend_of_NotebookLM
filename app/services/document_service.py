# Core bussiness logic for documents
# Validation (basic level)
# Coordination between models
# Functions: create_document(user_id, title, content). get_documents(user_id), delete_document(document_id, user_id)
# Flow: Check user exists -> create document record -> store content -> return document

from app import db
from app.models.document import Document
from app.models.user import User
import app.services as storage_service
from app.db.database import SessionLocal
from app.models.user import User
import uuid
import os
from fastapi import UploadFile

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.document import Document

db = SessionLocal()

class DocumentService:
    @staticmethod
    async def create_document(user_id, title, file):
          # check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Validate file (basic validation)
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            raise ValueError("Unsupported file type")
        
        # Store the file using StorageService
        document_id = str(uuid.uuid4())  # Generate a unique ID for the document
        await storage_service.store_file(document_id, file)
        document = Document(
            id=document_id,
            user_id=user_id,
            filename=file.filename
        )
        success = await storage_service.store_file(document_id, file)
        if not success:
            raise ValueError("Failed to store the file")

        # Create a document record in the database
        document = Document(id=document_id, user_id=user_id, title=title, filename=file.filename)
        await document.save()
        
        return document_id

    @staticmethod
    async def validate_file(file: UploadFile):
        """Basic validation for uploaded files: type and size."""
        if not hasattr(file, "content_type"):
            raise ValueError("Invalid file")

        if file.content_type not in ALLOWED_TYPES:
            raise ValueError("Unsupported file type")

        # Read up to MAX_FILE_SIZE + 1 bytes to check size without loading entire file
        contents = await file.read(MAX_FILE_SIZE + 1)
        size = len(contents)

        # Reset file pointer for further use
        try:
            await file.seek(0)
        except Exception:
            # UploadFile may not support async seek; try sync
            try:
                file.file.seek(0)
            except Exception:
                pass

        if size > MAX_FILE_SIZE:
            raise ValueError("File too large")

        return True
    async def get_documents_by_user(user_id):
        # Fetch documents for the user from the database
        documents = await Document.filter(user_id=user_id).all()
    
        # raise ValueError("No documents found for this user")
        if not documents:
            raise ValueError("No documents found for this user")
        return [{"id": doc.id, "filename": doc.filename, "title": doc.title} for doc in documents]
        

    @staticmethod
    async def delete_document(document_id, user_id, filename):
        # Delete the document record from the database
        document = await Document.get(id=document_id)
        if not document:
            raise ValueError("Document not found")
        
        if document.user_id != user_id:
            raise ValueError("Unauthorized to delete this document")

        await document.delete()
        
        # Delete the file from storage
        await storage_service.delete_file(document_id, filename)

# Validation and coordination for uploading documents

ALLOWED_TYPES = [
    "application/pdf",
    "text/plain"
]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

async def validate_file(file: UploadFile):

    contents = await file.read()

    # validate size
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    # validate type
    if file.content_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported file type")
    
    await file.seek(0)


# Service function to handle file upload

UPLOAD_DIR = "uploads/"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_document_service(file: UploadFile):

    await validate_file(file)

    filepath = os.path.join(UPLOAD_DIR, file.filename)

    # save physical file
    with open(filepath, "wb") as f:
        f.writes(await file.read())

    # save DB record
    db: Session = SessionLocal()

    document = Document(
        filename=file.filename,
        filepath=filepath
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename,
        "filepath": document.filepath
    }