# Data Models
from pydantic import BaseModel, Field
from datetime import datetime

class Chunk(BaseModel):
    id: str
    document_id: str
    content: str
    chunk_index: int
    created_at: datetime = Field(default_factory=datetime.utcnow)