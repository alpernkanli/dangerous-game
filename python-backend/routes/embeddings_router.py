from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.embeddings_factory import get_service

embeddings_router = APIRouter()

class EncodingRequest(BaseModel):
    text: str
    model: str = "flan-t5"

class DecodingRequest(BaseModel):
    embedding: list
    model: str = "flan-t5"

@embeddings_router.post("/generate-embedding")
async def generate_embedding(request: EncodingRequest):
    service = get_service(request.model)
    embedding = service.encode(request.text)
    return {"embedding": embedding.tolist()}

@embeddings_router.post("/generate-text")
async def generate_text(request: DecodingRequest):
    service = get_service(request.model)
    text = service.decode(request.embedding)
    return {"text": text}