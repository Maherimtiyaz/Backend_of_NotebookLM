# File defines the Document data structure in the database
# import ORM base

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

# ----------------------------------
# DOCUMENT MODEL
# ----------------------------------


class Document(DeclarativeBase):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    filename = Column(String)
    created_at = Column(String)

    # Relationship to User model
    user = relationship("User", back_populates="documents")
