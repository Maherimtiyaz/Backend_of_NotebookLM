# Create app and connects routes
from fastapi import FastAPI
from app.routes import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)