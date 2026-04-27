from typing import List
from app.services.storage_service import read_file
from app.services.document_service import (
    get_document_from_db,
    mark_document_as_processed
)
from app.services.chunk_service import create_chunks, save_chunks


# -----------------------------
# PURE FUNCTION
# -----------------------------
def split_into_chunks(text: str, chunk_size: int = 1000) -> List[str]:
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


# -----------------------------
# MAIN ORCHESTRATOR
# -----------------------------
def process_document(document_id: str):

    # 1. Fetch document
    document = get_document_from_db(document_id)
    if not document:
        raise ValueError(f"Document {document_id} not found")

    # 2. Idempotency check
    if document.processed:
        return {
            "status": "already_processed",
            "document_id": document_id
        }

    # 3. Read file from storage
    file_bytes = read_file(document_id)
    if not file_bytes:
        raise ValueError("File could not be read from storage")

    # 4. Convert bytes → text
    try:
        text = file_bytes.decode("utf-8")
    except Exception:
        raise ValueError("File decoding failed")

    # 5. Split into chunks
    chunks_texts = split_into_chunks(text)

    if not chunks_texts:
        return {
            "status": "no_content",
            "document_id": document_id
        }
    
    # 6. Create chunk objects
    chunk_objects = create_chunks(document_id, chunks_texts)
    # 7. Save chunks to DB
    save_chunks(chunk_objects)

    # 8. Mark document as processed
    mark_document_as_processed(document_id)

    # 9. Return result
    return {
        "status": "success",
        "document_id": document_id,
        "chunks_created": len(chunk_objects)
    }