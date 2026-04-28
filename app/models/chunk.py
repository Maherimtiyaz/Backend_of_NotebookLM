# Data Models
from tokenize import String


from sqlalchemy import Column, String, Integer, ForeignKey
from pydantic import BaseModel, Field
from datetime import datetime
from app.db.database import Base

class Chunk(Base):
    __tablename__ = "chunks"
    __allow_unmapped__ = True

    id = Column(String, primary_key=True)
    document_id = Column(Integer, index=True)
    content = Column(String)
    chunk_index = Column(Integer)
    created_at = Column(String, default=datetime.utcnow)