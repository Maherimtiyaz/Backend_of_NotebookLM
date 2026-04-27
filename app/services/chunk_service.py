import uuid
from typing import List
from app.models.chunk import Chunk
from app.services.document_service import save_chunks_to_db

# -----------------------------
# CREATE CHUNK OBJECTS
# -----------------------------
def create_chunks(document_id: str, chunk_texts: List[str]) -> List[Chunk]:
    chunks = []
    for index, chunk_text in enumerate(chunk_texts):
        chunk = Chunk(
            id=str(uuid.uuid4()),
            document_id=document_id,
            content=chunk_text,
            chunk_index=index
        )
        chunks.append(chunk)
    return chunks

# SAVE CHUNKS TO DB
def save_chunks(chunks: List[Chunk]):
    save_chunks_to_db(chunks)

# DELETE CHUNKS FROM DB
def delete_chunks(document_id: str):
    # This function would contain logic to delete chunks from the database based on document_id
    pass


