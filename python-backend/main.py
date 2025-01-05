from fastapi import FastAPI

from routes.embeddings_router import embeddings_router

app = FastAPI()

app.include_router(embeddings_router, prefix="/api/v1")