# user schema for validation and data transfer
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str