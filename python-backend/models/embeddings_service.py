from abc import ABC, abstractmethod

class EmbeddingsService(ABC):
    @abstractmethod
    def encode(self, text: str):
        """Encodes a text into an embedding."""
        pass

    @abstractmethod
    def decode(self, embedding_or_text: str):
        """Decodes an embedding or text into a description."""
        pass
