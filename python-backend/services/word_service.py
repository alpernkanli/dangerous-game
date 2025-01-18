from typing import List, Optional
from pydantic import BaseModel
import torch
import chromadb
from chromadb.config import Settings
import random

from models.flant5_embeddings_service import FLANT5EmbeddingsService

class Word(BaseModel):
    word: str
    definition: str
    word_embedding: Optional[List[List[float]]] = None
    definition_embedding: Optional[List[List[float]]] = None
    similarity_score: Optional[float] = None

class WordService:
    def __init__(self, collection_name: str = "the-embeddings"):
        self.client = chromadb.PersistentClient(path="./utils/data/words_and_their_mappings_chromadb")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.collection_name = collection_name
        self.embedding_service = FLANT5EmbeddingsService()

    def add_word(self, word: str, definition: str):
        word_embedding = self.embedding_service.encode(word)
        definition_embedding = self.embedding_service.encode(definition)
        
        pooled = definition_embedding.squeeze(0).mean(dim=0)
        
        self.collection.add(
            ids=[str(hash(word))],
            embeddings=[pooled.tolist()],
            metadatas=[{
                "word": word,
                "definition": definition,
                "word_embedding": word_embedding.tolist(),
                "definition_embedding": definition_embedding.tolist()
            }]
        )

    def batch_add_words(self, words: list[str], definitions: list[str]):
        definition_embeddings = self.embedding_service.encode_batch(definitions)
        word_embeddings = self.embedding_service.encode_batch(words)

        ids = [str(hash(w)) for w in words]
        embeddings = [emb.mean(dim=0).tolist() for emb in definition_embeddings]
        metadatas = [
            {
                "word": w,
                "definition": d,
                "word_embedding": str(we.tolist()),
                "definition_embedding": str(de.tolist())
            }
            for w, d, we, de in zip(words, definitions, word_embeddings, definition_embeddings)
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def get_word(self, word: str) -> Optional[Word]:
        results = self.collection.get(
            where={"word": word},
            limit=1
        )
        
        if not results['metadatas']:
            return None
            
        metadata = results['metadatas'][0]
        return Word(
            word=metadata["word"],
            definition=metadata["definition"],
            word_embedding=metadata["word_embedding"],
            definition_embedding=metadata["definition_embedding"]
        )

    def get_random_word(self) -> Optional[Word]:
        total_count = self.collection.count()
        if total_count == 0:
            return None
            
        random_index = random.randint(0, total_count - 1)
        result = self.collection.get(limit=1, offset=random_index)
        
        if not result['metadatas']:
            return None
            
        metadata = result['metadatas'][0]
        return Word(
            word=metadata["word"],
            definition=metadata["definition"],
            word_embedding=eval(metadata["word_embedding"]),
            definition_embedding=eval(metadata["definition_embedding"])
        )
    
    def get_random_words(self, n: int) -> List[Word]:
        total_count = self.collection.count()
        if total_count == 0:
            return []
            
        # Generate n random unique indices
        indices = random.sample(range(total_count), min(n, total_count))
        
        # Get words one by one using their indices
        words = []
        for idx in indices:
            result = self.collection.get(limit=1, offset=idx)
            if result['metadatas']:
                metadata = result['metadatas'][0]
                words.append(Word(
                    word=metadata["word"],
                    definition=metadata["definition"],
                    word_embedding=eval(metadata["word_embedding"]),
                    definition_embedding=eval(metadata["definition_embedding"])
                ))
        
        return words

    def search_similar_definitions(self, query: str, limit: int = 5) -> List[Word]:
        query_embedding = self.embedding_service.encode(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.flatten().tolist()],
            n_results=limit
        )
        
        if not results['metadatas']:
            return []

        return [
            Word(
                word=metadata["word"],
                definition=metadata["definition"],
                word_embedding=metadata["word_embedding"],
                definition_embedding=metadata["definition_embedding"],
                similarity_score=distance
            )
            for metadata, distance in zip(results['metadatas'][0], results['distances'][0])
        ]
    
    def find_closest_word(self, embedding: List[float]) -> Optional[Word]:
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )
    
        if not result['metadatas'] or not result['metadatas'][0]:
            return None
        
        metadata = result['metadatas'][0][0]  # Get first result's metadata
        return Word(
            word=metadata["word"],
            definition=metadata["definition"],
            word_embedding=eval(metadata["word_embedding"]),
            definition_embedding=eval(metadata["definition_embedding"])
        )