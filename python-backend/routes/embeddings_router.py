from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.embeddings_factory import get_service
from services.word_service import WordService  # Updated import

embeddings_router = APIRouter()
word_service = WordService()

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

@embeddings_router.get("/random-word")
async def get_random_word():
    word = word_service.get_random_word()
    if word:
        return {"word": word.word, "definition": word.definition, "word_embedding": word.word_embedding, "definition_embedding": word.definition_embedding}
    return {"error": "No words found"}

@embeddings_router.get("/random-words")
async def get_random_words(n: int):
    words = word_service.get_random_words(n)
    
    return [
        {
            "word": word.word,
            "definition": word.definition,
            "word_embedding": word.word_embedding,
            "definition_embedding": word.definition_embedding,
        }
        for word in words
    ]

@embeddings_router.post("/find-closest-word")
async def find_closest_word(request: DecodingRequest):
    closest_word = word_service.find_closest_word(request.embedding)
    return {"word": closest_word.word, "definition": closest_word.definition}