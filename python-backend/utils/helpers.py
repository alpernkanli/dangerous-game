from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

service_cache = LRUCache(capacity=2)

def get_service(model_name: str) -> EmbeddingsService:
    # Check the cache first
    cached_service = service_cache.get(model_name)
    if cached_service:
        print(f"Using cached service for model: {model_name}")
        return cached_service

    # Lazily instantiate and add to the cache
    if model_name in embeddings_services:
        print(f"Instantiating service for model: {model_name}")
        service = embeddings_services[model_name]()
        service_cache.put(model_name, service)
        return service

    raise ValueError(f"Unknown model: {model_name}")
