from typing import List
from app.services.storage_service import read_file
from app.services.document_service import (
    get_document_from_db,
    save_chunks_to_db,
    mark_document_as_processed
)
from app.models.chunk import Chunk
import uuid


# -----------------------------
# PURE FUNCTION (NO SIDE EFFECTS)
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
    file_bytes = read_file(document.filename)
    if not file_bytes:
        raise ValueError("File could not be read from storage")

    # 4. Convert bytes → text
    try:
        text = file_bytes.decode("utf-8")
    except Exception:
        raise ValueError("File decoding failed")

    # 5. Split into chunks
    chunks = split_into_chunks(text)

    if not chunks:
        return {
            "status": "no_content",
            "document_id": document_id
        }

    # 6. Convert to Chunk objects
    chunk_objects = []
    for index, content in enumerate(chunks):
        chunk = Chunk(
            id=str(uuid.uuid4()),
            document_id=document.id,
            content=content,
            chunk_index=index
        )
        chunk_objects.append(chunk)

    # 7. Save chunks
    save_chunks_to_db(chunk_objects)

    # 8. Mark document as processed
    mark_document_as_processed(document_id)

    # 9. Return result
    return {
        "status": "success",
        "document_id": document_id,
        "chunks_created": len(chunk_objects)
    }