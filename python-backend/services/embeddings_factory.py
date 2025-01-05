from functools import lru_cache

from services.embeddings_service import EmbeddingsService
from models.distilbart_embeddings_service import DistilBARTEmbeddingsService
from models.flant5_embeddings_service import FLANT5EmbeddingsService

embeddings_services = {
    "flan-t5": FLANT5EmbeddingsService,
    "distilbart": DistilBARTEmbeddingsService,
}

service_cache = {}

@lru_cache(maxsize=2)
def get_service(model_name: str) -> EmbeddingsService:
    if model_name in service_cache:
        print(f"Using cached service for model: {model_name}")
        return service_cache[model_name]
    
    if model_name in embeddings_services:
        print(f"Instantiating service for model: {model_name}")
        service = embeddings_services[model_name]()
        service_cache[model_name] = service
        return service
    
    raise ValueError(f"Unknown model: {model_name}")
