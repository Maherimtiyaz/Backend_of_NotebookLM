# Create app and connects routes
from fastapi import FastAPI
from app.routes import user, document, processing
from app.routes.document import router as document_router
from app.routes.processing import router as processing_router


app = FastAPI()

app.include_router(user.router)
app.include_router(document.router)
app.include_router(processing.router)
