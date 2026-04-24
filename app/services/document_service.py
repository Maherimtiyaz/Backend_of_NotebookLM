# Core bussiness logic for documents
# Validation (basic level)
# Coordination between models
# Functions: create_document(user_id, title, content). get_documents(user_id), delete_document(document_id, user_id)
# Flow: Check user exists -> create document record -> store content -> return document

from app.models import Document, User
import app.services as storage_service
import uuid



class DocumentService:
    @staticmethod
    async def create_document(user_id, title, file):
          # check if user exists
        user = await User.get(id=user_id)
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