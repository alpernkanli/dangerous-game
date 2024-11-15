from fastapi import APIRouter, Query
from models.factory import get_service

embeddings_router = APIRouter()

@embeddings_router.post("/generate-embedding")
async def generate_embedding(text: str, model: str = Query("flan-t5")):
    service = get_service(model)
    embedding = service.encode(text)
    return {"embedding": embedding.tolist()}