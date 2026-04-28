from fastapi import APIRouter

router = APIRouter()

@router.post("/process")
def process():
    # logic to process the document
    return {"message": "Document processed successfully"}