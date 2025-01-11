from typing import List, Optional
from pydantic import BaseModel
import torch
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, SampleQuery, Sample
import random

from models.flant5_embeddings_service import FLANT5EmbeddingsService

class Word(BaseModel):
    word: str
    definition: str
    word_embedding: Optional[List[float]] = None
    definiton_embedding: Optional[List[float]] = None
    similarity_score: Optional[float] = None

class WordService:
    def __init__(self, collection_name: str = "theembeddings"):
        self.qdrant = QdrantClient(path="./data/words_and_their_mappings")
        self.collection_name = collection_name
        
        self.embedding_service = FLANT5EmbeddingsService()
        #self._init_collection()

    def _init_collection(self):
        self.qdrant.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE)
        )

    def add_word(self, word: str, definition: str):
        word_embedding = self.embedding_service.encode(word)
        definition_embedding = self.embedding_service.encode(definition)

        pooled = definition_embedding.squeeze(0).mean(dim=0)
        
        self.qdrant.upsert(
            collection_name=self.collection_name,
             points=[
                PointStruct(
                    id=hash(word),
                    vector=pooled.tolist(),
                    payload={
                        "word": word,
                        "definition": definition,
                        "word_embedding": word_embedding.tolist(),
                        "definition_embedding": definition_embedding.tolist()
                    }
                )
            ]
        )

    def batch_add_words(self, words: list[str], definitions: list[str]):
        definition_embeddings = self.embedding_service.encode_batch(definitions)
        
        word_embeddings = self.embedding_service.encode_batch(words)

        points = []
        for i, (w, d) in enumerate(zip(words, definitions)):
            pooled = definition_embeddings[i].mean(dim=0)  # or however you pool
            points.append(
                PointStruct(
                    id=hash(w),
                    vector=pooled.tolist(),
                    payload={
                        "word": w,
                        "definition": d,
                        "word_embedding": word_embeddings[i].tolist(),
                        "definition_embedding": definition_embeddings[i].tolist()
                    }
                )
            )

        self.qdrant.upsert(collection_name=self.collection_name, points=points)

    def get_word(self, word: str) -> Optional[Word]:
        results = self.qdrant.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[FieldCondition(key="word", match=MatchValue(value=word))]
            ),
            limit=1
        )[0]
        
        if not results:
            return None
            
        point = results[0]
        return Word(
            word=point.payload["word"],
            definition=point.payload["definition"],
            word_embedding=point.payload["word_embedding"],
            definition_embedding=point.payload["definition_embedding"]
        )

    def get_random_word(self) -> Optional[Word]:
        sampled = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=SampleQuery(sample=Sample.RANDOM)
        )
        
        if not sampled:
            return None
        print(sampled)
        random_point = sampled
        return Word(
            word=random_point.payload["word"],
            definition=random_point.payload["definition"],
            word_embedding=random_point.payload["word_embedding"],
            definition_embedding=random_point.payload["definition_embedding"]
        )
    
    def get_random_words(self, n: int) -> List[Word]:
        # Query n random points directly
        sampled = self.qdrant.scroll(
            collection_name=self.collection_name,
            limit=n,
            with_payload=True,
            offset=random.randint(0, self.qdrant.get_collection(self.collection_name).points_count - n)
        )[0]
        
        if not sampled:
            return []
        
        return [
            Word(
                word=point.payload["word"],
                definition=point.payload["definition"],
                word_embedding=point.payload["word_embedding"],
                definition_embedding=point.payload["definition_embedding"]
            )
            for point in sampled
        ]

    def search_similar_definitions(self, query: str, limit: int = 5) -> List[Word]:
        query_embedding = self.embedding_service.encode(query)

        search_results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.flatten().tolist(),
            limit=limit
        )

        return [
            Word(
                word=result.payload["word"],
                definition=result.payload["definition"],
                word_embedding=result.payload["word_embedding"],
                definition_embedding=result.payload["definition_embedding"],
                similarity_score=result.score
            )
            for result in search_results
        ]