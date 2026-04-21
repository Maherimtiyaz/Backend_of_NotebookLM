# User routes user will hits API this file receives it

from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.services.user_service import create_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    return create_user(user)

# route to get user details by user_id
@router.get("/users/{user_id}")
def get_user(user_id: int):
    # logic to fetch user details from database using user_id
    return {"message": f"User details for user_id: {user_id}"}